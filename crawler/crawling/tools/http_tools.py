import requests


def get_html(url):
    """
    Return html source from the url, If there is an error, raise the error.
    """
    res = requests.get(url)
    return res.text
