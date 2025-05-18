""" utils.py

Utility functions for printing colored messages and debug info, caching JSON data, and file hashing.

Includes:
- Colored console output helpers (green, red, yellow, error to stderr)
- JSON cache load/save with directory creation
- SHA256 file hashing
"""

# standard imports
import json
import os
import hashlib
from sys import stderr
from datetime import date

# local imports
from models import Post, Paths, User


BOLD_GREEN = '\033[1m\033[32m'
BOLD_RED = '\033[1m\033[31m'
BOLD_YELLOW = '\033[1m\033[33m'
BOLD = '\033[1m'
ITALIC = '\033[3m' 
RESET = '\033[0m'


def print_green(message: str):
    """ Prints a message in green."""
    print(f"{BOLD_GREEN}{message}{RESET}")
    
    
def print_red(message: str):
    """ Prints a message in red."""
    print(f"{BOLD_RED}{message}{RESET}")
    
    
def print_yellow(message: str):
    """ Prints a message in yellow."""
    print(f"{BOLD_YELLOW}{message}{RESET}")
    
    
def print_error(message: str):
    """ Prints an error message in red to stderr (including a newline)."""
    stderr.write(f"{BOLD_RED}{message}{RESET}\n")
    
    
def	debug_print(paths: Paths, user: User, posts: list[Post]):
	"""Prints out all stored values after parsing and storing."""
	print_yellow("##### DEBUG #####\n")
	print("Html-files:\n", paths.html_files, "\n") # Prints out the html-files' paths.
	print("CSV-files:\n", paths.csv_files, "\n") # Prints out the csv-files' paths.
	print("posts.csv-file:\n", paths.posts_csv, "\n")
	print("Image URLs:\n", paths.image_urls, "\n")
	print_yellow("##### ALL POSTS #####\n")
	for post in posts:
		print("Title: ", post.title)
		print("Subtitle: ", post.subtitle)
		print(post.content)
	print("User private key:\n", user.priv_key, "\n")
	print("User relays:\n", user.relays, "\n")


def load_cache(path: str):
    """ Load cache from a JSON file."""
    if os.path.exists(path):
        with open(path, 'r', encoding = 'utf-8') as f:
            return json.load(f)
    return {} # If cache doesn't exist, return empty dict


def save_cache(path: str, data: dict):
    """ Save cache to a JSON file, creating parent directories if needed."""
    dir_path = os.path.dirname(path)
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f)


def sha256_hash(path):
    """Computes the SHA256 hash of a file."""
    hash_sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(8192)  # read in chunks to handle large files
            if not chunk:
                break
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()
