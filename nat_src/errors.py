import sys


def error_and_exit(error_code: int):
    """Prints a error message to stderr and exits with corresponding exit code."""
    if (error_code == 1):
        sys.stderr.write("Error: Private key missing. Add private key in user_entries/credentials/ADD_PRIVATE_KEY_HERE.txt\n")
    elif (error_code == 2):
        sys.stderr.write("Error: Public key missing. Add public key in user_entries/credentials/ADD_PUBLIC_KEY_HERE.txt\n")
    elif (error_code == 3):
        sys.stderr.write("Error: Relays missing. Add relays in user_entries/credentials/ADD_RELAYS_HERE.txt\n")
    elif (error_code == 4):
        sys.stderr.write("Error: Please only include one dir or zip file in 'export'-directory.\n")
    elif (error_code == 5):
        sys.stderr.write("Error: Please only substack export data. This should include .csv files and a 'posts'-folder containing .html-files/.csv-files.\n")
    elif (error_code == 6):
        sys.stderr.write("Error: .html-files can't be empty.\n")
    sys.exit(error_code)
