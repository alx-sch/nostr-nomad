import sys
import os

# Add the 'SRC' directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'SRC'))

import parse

if __name__ == "__main__":
    path = "export"  # Change this if needed
    parse.extract_zips(path)
    print("Main script done.")
    