import urllib.parse

import requests
import streamlit as st


class SynchHome:
    class Model:
        pageTitle = "Sync Scraping"

    def validate_url(self, url: str) -> bool:
        """Validate the URL

        Args:
            url (str): The URL to validate

        Returns:
            bool: True if the URL is valid, False otherwise
        """

        parsed_url = urllib.parse.urlparse(url)
        domain = parsed_url.netloc

        return domain.endswith("aptoide.com")

    def view(self, model):
        st.title(model.pageTitle)

        st.write("Scraping a page in synchronous mode.")

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        prompt = st.chat_input("Enter a URL to scrape")
        if prompt:
            if not self.validate_url(prompt):
                st.error(
                    "Invalid URL, example of a valid URL: https://infinite-magicraid.en.aptoide.com/"
                )
                return

            # Display user message in chat message container
            st.chat_message("user").markdown(prompt)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

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
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )