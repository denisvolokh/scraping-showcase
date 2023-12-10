def convert_to_base_url(url: str) -> str:
    """Converts a url to its base url (e.g. https://infinite-magicraid.en.aptoide.com/ -> https://infinite-magicraid.en.aptoide.com)

    Args:
        url (str): The url to be converted

    Returns:
        str: The base url
    """

    base_url_parts = url.split("/")[:3]
    base_url = "/".join(base_url_parts)

    return base_url
