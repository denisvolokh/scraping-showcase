import time

import requests
import streamlit as st

from .utils import validate_url


class AsynchHome:
    class Model:
        pageTitle = "Async Scraping"

    def view(self, model):
        st.title(model.pageTitle)

        st.write(
            "Scraping a page in asynchronous mode and returning data upon request to the task status endpoint."
        )

        # Initialize chat history
        if "async_messages" not in st.session_state:
            st.session_state.async_messages = []

        # Display chat messages from history on app rerun
        for message in st.session_state.async_messages:
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
            st.session_state.async_messages.append({"role": "user", "content": prompt})

            r = requests.get("http://api:5000/v2/scrape", params={"target_url": prompt})

            if r.status_code != 200:
                st.error(f"Unable to scrape the URL, status code: {r.status_code}")
                return

            task_id = r.json()["task_id"]

            with st.status(
                f"Async scraping in progress... Task status: {r.json()['status']}"
            ) as status:
                while True:
                    r = requests.get(f"http://api:5000/v2/scrape/result/{task_id}")

                    if r.status_code != 200:
                        st.error(
                            f"Unable to check the task status, status code: {r.status_code}"
                        )
                        return

                    if r.json()["status"] == "SUCCESS":
                        status.update(
                            label="Task completed!", state="complete", expanded=False
                        )
                        break
                    else:
                        status.text(
                            f"Async scraping in progress... Task status: {r.json()['status']}"
                        )

                    time.sleep(1)

            result = r.json()["result"]

            response = f"""
                Name: {result['app_name']} \n
                Version: {result['app_version']} \n
                No of downloads: {result['no_downloads']} \n
                Release date: {result['app_release_date']} \n
                URL: {result['app_url']} \n
                Description: {result['app_description']}
            """

            with st.chat_message("assistant"):
                st.markdown(response)

            # Add assistant response to chat history
            st.session_state.async_messages.append(
                {"role": "assistant", "content": response}
            )
