import streamlit as st


class AsynchSSEHome:
    class Model:
        pageTitle = "Async Scraping (SSE)"

    def view(self, model):
        st.title(model.pageTitle)

        st.write(
            "Scraping a webpage in asynchronous mode and returning data via Server-Sent Events (SSE)."
        )
