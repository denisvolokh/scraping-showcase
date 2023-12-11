import streamlit as st


def load_css():
    with open("webapp/tools/style.css") as f:
        st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)
