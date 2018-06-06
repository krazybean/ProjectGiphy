from projectgiphy import app
from projectgiphy.utilities.giphy import Giphy

giphy = Giphy()

def search(search_string, offset=0):
    """ Giphy abstraction for searching

    Args:
        search_string (str): Searchable field to query
        offset (int:optional): if future offsets are passed to be searched
    Returns:
        dict: Dictonary representation of the Giphy API response
    """
    return giphy.search(search_string, offset)