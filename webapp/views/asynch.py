import streamlit as st


class AsynchHome:
    class Model:
        pageTitle = "Async Scraping"

    def view(self, model):
        st.title(model.pageTitle)

        st.write(
            "Scraping a page in asynchronous mode and returning data upon request to the task status endpoint."
        )
