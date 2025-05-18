""" errors.py

Defines error codes and a unified error handling function for the application.
Provides clear error messages and exits the program with the appropriate code.
"""

# local imports
from utils import print_error

# Error codes
MISSING_PRIVATE_KEY =       1
MISSING_RELAYS =            2
INVALID_PRIVATE_KEY =       3
INVALID_EXPORT_STRUCTURE =  4
MISSING_SUBSTACK_DATA =     5
EMPTY_HTML_FILES =          6
MISMATCHED_POST_DATA =      7
MISSING_IMG_HOST =          8
MISSING_WALA_URL =          10
MISSING_IMGUR_CLIENT_ID =   11
MISSING_EVENT_TYPE =        12
MISSMATCHED_HASH =          13


def error_and_exit(error_code: int):
    """Prints a error message to stderr and exits with corresponding exit code."""
    
    if (error_code == MISSING_PRIVATE_KEY):
        print_error("Error: Missing 'private_key'. Please provide in 'user_entries/config.ini'.")
    elif (error_code == MISSING_RELAYS):
        print_error("Error: Missing 'relays'. Please provide in 'user_entries/config.ini'.")
    elif (error_code == INVALID_PRIVATE_KEY):
        print_error("Error: Invalid private key. Please provide in 'user_entries/config.ini'.")
    elif (error_code == INVALID_EXPORT_STRUCTURE):
        print_error("Error: Please include ONE folder or ONE zip file in 'user_entries/export/' (substack export data).")
    elif (error_code == MISSING_SUBSTACK_DATA):
        print_error("Error: Please provide substack export data. This should include a 'posts.csv'-file and a 'posts'-folder.")
    elif (error_code == EMPTY_HTML_FILES):
        print_error("Error: .html-files can't be empty.")
    elif (error_code == MISMATCHED_POST_DATA):
        print_error("Error: 'posts.csv'-file and .html-files don't match. Please only use original substack export data.")
    elif (error_code == MISSING_IMG_HOST):
        print_error("Error: Missing or invalid'image_host'. Please provide in 'user_entries/config.ini'.")
    elif (error_code == MISSING_WALA_URL):
        print_error("Error: Missing 'wala_url'. Please provide in 'user_entries/config.ini'.")
    elif (error_code == MISSING_IMGUR_CLIENT_ID):
        print_error("Error: Missing 'imgur_client_id'. Please provide in 'user_entries/config.ini'.")
    elif (error_code == MISSING_EVENT_TYPE):
        print_error("Error: Missing or invalid 'event_type'. Please provide in 'user_entries/config.ini'.")
    elif (error_code == MISSMATCHED_HASH):
        print_error("Error: Hash mismatch. Make sure the server uses SHA-256 for hashing.")
    else:
        print_error(f"Error: {error_code}")
        raise SystemExit(1)

    raise SystemExit(error_code)
