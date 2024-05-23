import asyncio

import streamlit as st
from streamlit_option_menu import option_menu
from views.asynch import AsynchHome
from views.asynch_sse import AsynchSSEHome
from views.synch import SynchHome

st.set_page_config(page_title="Scrape App", page_icon="favicon.ico", layout="wide")


# class Model:
#     menuTitle = "Scrape App"
#     option1 = "Sync Scraping"
#     option2 = "Async Scraping"
#     option3 = "Async Scraping (SSE)"

#     menuIcon = "menu-up"
#     icon1 = "activity"
#     icon2 = "graph-up-arrow"
#     icon3 = "motherboard"


async def view() -> None:
    menuTitle = "Scrape App"
    option1 = "Sync Scraping"
    option2 = "Async Scraping"
    option3 = "Async Scraping (SSE)"

    menuIcon = "menu-up"
    icon1 = "activity"
    icon2 = "graph-up-arrow"
    icon3 = "motherboard"

    with st.sidebar:
        menuItem = option_menu(
            menu_title=menuTitle,
            options=[option1, option2, option3],
            icons=[icon1, icon2, icon3],
            menu_icon=menuIcon,
            default_index=0,
        )

    if menuItem == option1:
        SynchHome().view(SynchHome.Model())

    if menuItem == option2:
        AsynchHome().view(AsynchHome.Model())

    if menuItem == option3:
        AsynchSSEHome().view(AsynchSSEHome.Model())


async def main() -> None:
    await view()


if __name__ == "__main__":
    asyncio.run(main())
