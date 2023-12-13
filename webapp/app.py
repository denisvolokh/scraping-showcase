import asyncio
from typing import Any

import streamlit as st
from streamlit_option_menu import option_menu
from views.asynch import AsynchHome
from views.asynch_sse import AsynchSSEHome
from views.synch import SynchHome

st.set_page_config(page_title="Scrape App", page_icon="favicon.ico", layout="wide")


class Model:
    menuTitle = "Scrape App"
    option1 = "Sync Scraping"
    option2 = "Async Scraping"
    option3 = "Async Scraping (SSE)"

    menuIcon = "menu-up"
    icon1 = "activity"
    icon2 = "graph-up-arrow"
    icon3 = "motherboard"


async def view(model: Any) -> None:
    with st.sidebar:
        menuItem = option_menu(
            menu_title=model.menuTitle,
            options=[model.option1, model.option2, model.option3],
            icons=[model.icon1, model.icon2, model.icon3],
            menu_icon=model.menuIcon,
            default_index=0,
        )

    if menuItem == model.option1:
        SynchHome().view(SynchHome.Model())

    if menuItem == model.option2:
        AsynchHome().view(AsynchHome.Model())

    if menuItem == model.option3:
        AsynchSSEHome().view(AsynchSSEHome.Model())


async def main() -> None:
    await view(Model())


if __name__ == "__main__":
    asyncio.run(main())
