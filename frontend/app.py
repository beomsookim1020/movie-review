import streamlit as st

from api import (
    check_backend_health,
    create_movie,
    create_review,
    delete_movie,
    delete_review,
    get_movie_rating,
    get_movie_reviews,
    get_movies,
    get_reviews,
)

st.set_page_config(page_title="Movie Review Sentiment", layout="wide")


try:
    health = check_backend_health()
except Exception as exc:
    st.error("Backend is not connected.")
    st.caption(str(exc))
    st.stop()


def rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()


def format_datetime(value: str) -> str:
    return value.replace("T", " ")[:19]


def format_movie(movie: dict) -> str:
    return f"{movie['id']} - {movie['title']}"


def is_url(value: str) -> bool:
    return isinstance(value, str) and value.startswith(("http://", "https://"))


def render_poster(poster_url: str):
    if is_url(poster_url):
        st.image(poster_url, width=110)
    else:
        st.caption("No poster")


st.title("Movie Review Sentiment")
st.caption(f"Backend status: {health['status']}")

movies = get_movies()

movies_tab, reviews_tab = st.tabs(["Movies", "Reviews"])

with movies_tab:
    form_col, list_col = st.columns([1, 2])

    with form_col:
        st.subheader("Add Movie")

        with st.form("create_movie_form", clear_on_submit=True):
            title = st.text_input("Title")
            release_date = st.date_input("Release date")
            director = st.text_input("Director")
            genre = st.text_input("Genre")
            poster_url = st.text_input("Poster URL")
            submitted = st.form_submit_button("Add")

        if submitted:
            if not is_url(poster_url):
                st.error("Poster URL must start with http:// or https://")
            else:
                try:
                    create_movie(title, release_date, director, genre, poster_url)
                    st.success("Movie added.")
                    rerun()
                except Exception as exc:
                    st.error("Failed to add movie.")
                    st.caption(str(exc))

    with list_col:
        st.subheader("Movie List")

        if not movies:
            st.info("No movies yet.")

        for movie in movies:
            rating = get_movie_rating(movie["id"])
            poster_col, detail_col, action_col = st.columns([1, 4, 1])

            with poster_col:
                render_poster(movie["poster_url"])

            with detail_col:
                st.markdown(f"**{movie['title']}**")
                st.write(f"Release: {movie['release_date']}")
                st.write(f"Director: {movie['director']}")
                st.write(f"Genre: {movie['genre']}")
                st.write(
                    f"Rating: {rating['average_score']:.2f} "
                    f"({rating['review_count']} reviews)"
                )

            with action_col:
                if st.button("Delete", key=f"delete_movie_{movie['id']}"):
                    try:
                        delete_movie(movie["id"])
                        st.success("Movie deleted.")
                        rerun()
                    except Exception as exc:
                        st.error("Failed to delete movie.")
                        st.caption(str(exc))

            st.divider()

with reviews_tab:
    if not movies:
        st.info("Add a movie before writing reviews.")
    else:
        selected_movie = st.selectbox(
            "Movie",
            movies,
            format_func=format_movie,
        )

        form_col, recent_col = st.columns([1, 2])

        with form_col:
            st.subheader("Add Review")

            with st.form("create_review_form", clear_on_submit=True):
                author = st.text_input("Author")
                content = st.text_area("Review", height=160)
                submitted = st.form_submit_button("Add")

            if submitted:
                try:
                    with st.spinner("Analyzing sentiment..."):
                        review = create_review(selected_movie["id"], author, content)
                    st.session_state["last_review"] = review
                    st.success("Review added.")
                    rerun()
                except Exception as exc:
                    st.error("Failed to add review.")
                    st.caption(str(exc))

            if "last_review" in st.session_state:
                last_review = st.session_state["last_review"]
                st.metric(
                    "Latest sentiment",
                    last_review["sentiment_label"],
                    f"{last_review['sentiment_score']:.2f}",
                )

        with recent_col:
            st.subheader("Recent Reviews")
            recent_reviews = get_reviews(limit=10)

            if not recent_reviews:
                st.info("No reviews yet.")

            for review in recent_reviews:
                row_col, delete_col = st.columns([5, 1])

                with row_col:
                    st.markdown(f"**Movie ID {review['movie_id']}**")
                    st.caption(format_datetime(review["created_at"]))
                    st.write(review["content"])
                    st.write(
                        f"{review['sentiment_label']} "
                        f"({review['sentiment_score']:.2f})"
                    )

                with delete_col:
                    if st.button("Delete", key=f"delete_review_{review['id']}"):
                        try:
                            delete_review(review["id"])
                            st.success("Review deleted.")
                            rerun()
                        except Exception as exc:
                            st.error("Failed to delete review.")
                            st.caption(str(exc))

                st.divider()

        st.subheader("Selected Movie Reviews")
        movie_reviews = get_movie_reviews(selected_movie["id"])

        if not movie_reviews:
            st.info("No reviews for this movie yet.")

        for review in movie_reviews:
            st.markdown(f"**{review['author']}**")
            st.caption(format_datetime(review["created_at"]))
            st.write(review["content"])
            st.write(
                f"{review['sentiment_label']} "
                f"({review['sentiment_score']:.2f})"
            )
            st.divider()
