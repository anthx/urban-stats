import os, datetime, requests


def check_file_is_young(filename: str) -> bool:
    """
    Returns true if filename is < 1 month old, false otherwise or not exist
    :param filename: str of the filename
    :return: bool
    """
    try:
        path_age = os.path.getmtime(filename)
        month_ago = datetime.datetime.now() - datetime.timedelta(days=30)

        if path_age > month_ago.timestamp() and os.path.getsize(filename) > 0:
            return True
        else:
            return False
    except OSError:
        return False


def get_from_api(defined_word: str):
    try:
        r = requests.get(
            f"http://api.urbandictionary.com/v0/define?term={defined_word}")
        definitions = r.json()
        return definitions
    except requests.ConnectionError:
        raise requests.ConnectionError