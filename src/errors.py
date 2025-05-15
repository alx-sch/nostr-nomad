# standard imports
import sys

# local imports
from utils import print_red


def error_and_exit(error_code: int):
    """Prints a error message to stderr and exits with corresponding exit code."""
    if (error_code == 1):
        print_red("Error: Missing 'private_key'. Please provide in 'user_entries/config.ini'.\n")
    elif (error_code == 2):
        print_red("Error: Missing 'relays'. Please provide in 'user_entries/config.ini'.\n")
    elif (error_code == 3):
        print_red("Error: Invalid private key. Please provide in 'user_entries/config.ini'.\n")
    elif (error_code == 4):
        print_red("Error: Please include ONE dir or ONE zip file in 'export'-directory.\n")
    elif (error_code == 5):
        print_red("Error: Please only substack export data. This should include a 'posts.csv'-file and a 'posts'-folder containing .html-files/.csv-files.\n")
    elif (error_code == 6):
        print_red("Error: .html-files can't be empty.\n")
    elif (error_code == 7):
        print_red("Error: 'posts.csv'-file and .html-files don't match. Please only use original substack export data.\n")
    sys.exit(error_code)
