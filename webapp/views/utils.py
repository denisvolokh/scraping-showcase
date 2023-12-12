import urllib.parse


def validate_url(url: str) -> bool:
    """Validate the URL

    Args:
        url (str): The URL to validate

    Returns:
        bool: True if the URL is valid, False otherwise
    """

    parsed_url = urllib.parse.urlparse(url)
    domain = parsed_url.netloc

    return domain.endswith("aptoide.com")
