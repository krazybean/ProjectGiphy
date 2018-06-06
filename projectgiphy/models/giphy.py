from projectgiphy import app
from projectgiphy.utilities.giphy import Giphy

giphy = Giphy()

def search(search_string, offset=0):
    return giphy.search(search_string, offset)