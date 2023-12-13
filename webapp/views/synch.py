import logging

import requests
import streamlit as st

from .utils import validate_url

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SynchHome:
    class Model:
        pageTitle = "Sync Scraping"

    def view(self, model):
        st.title(model.pageTitle)

        st.write("Scraping a page in synchronous mode.")

        logger.info("Rendering page...")

        # Initialize chat history
        if "synch_messages" not in st.session_state:
            st.session_state.synch_messages = []

        # Display chat messages from history on app rerun
        for message in st.session_state.synch_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        prompt = st.chat_input("Enter a URL to scrape")
        if prompt:
            if not validate_url(prompt):
                st.error(
                    "Invalid URL, example of a valid URL: https://infinite-magicraid.en.aptoide.com/"
                )
                return

            # Display user message in chat message container
            st.chat_message("user").markdown(prompt)
            # Add user message to chat history
            st.session_state.synch_messages.append({"role": "user", "content": prompt})

            with st.spinner("Wait for it..."):
                r = requests.get(
                    "http://api:5000/v1/scrape", params={"target_url": prompt}
                )

            if r.status_code != 200:
                st.error(f"Unable to scrape the URL, status code: {r.status_code}")
                return

            if r.status_code == 200:
                data = r.json()
                result = data["result"]

                response = f"""
                    Name: {result['app_name']} \n
                    Version: {result['app_version']} \n
                    No of downloads: {result['no_downloads']} \n
                    Release date: {result['app_release_date']} \n
                    URL: {result['app_url']} \n
                    Description: {result['app_description']}
                """
                # Display assistant response in chat message container
                with st.chat_message("assistant"):
                    st.markdown(response)

                # Add assistant response to chat history
                st.session_state.synch_messages.append(
                    {"role": "assistant", "content": response}
                )
