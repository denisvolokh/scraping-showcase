import json
import logging

import requests
import streamlit as st
from sseclient import SSEClient

from .utils import validate_url


class AsynchSSEHome:
    class Model:
        pageTitle = "Async Scraping (SSE)"

    def view(self, model):
        st.title(model.pageTitle)

        st.write(
            "Scraping a webpage in asynchronous mode and returning data via Server-Sent Events (SSE)."
        )

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
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
            st.session_state.messages.append({"role": "user", "content": prompt})

            logging.info("Sending request to API")

            r = requests.get("http://api:5000/v2/scrape", params={"target_url": prompt})

            if r.status_code != 200:
                st.error(f"Unable to scrape the URL, status code: {r.status_code}")
                return

            data = r.json()
            task_id = data["task_id"]

            st.session_state["updates"] = SSEClient(
                f"http://api:5000/v2/scrape/updates/{task_id}"
            )

            for msg in st.session_state["updates"]:
                if not msg.data:
                    st.session_state["updates"].resp.close()
                    return

                result = json.loads(msg.data)
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
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
