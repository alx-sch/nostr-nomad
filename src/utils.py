# standard imports
import json
import os
from sys import stderr
from datetime import date

# local imports
from models import Posts


def print_green(message: str):
    """ Prints a message in green."""
    bold_green = '\033[1m\033[32m'
    reset = '\033[0m'
    print(f"{bold_green}{message}{reset}")
    
    
def print_red(message: str):
    """ Prints a message in red."""
    bold_red = '\033[1m\033[31m'
    reset = '\033[0m'
    stderr.write(f"{bold_red}{message}{reset}")
    

def print_yellow(message: str):
    """ Prints a message in yellow."""
    yellow = '\033[1m\033[33m'
    reset = '\033[0m'
    print(f"{yellow}{message}{reset}")


def load_cache(path: str):
    """ Load cache from a JSON file."""
    if os.path.exists(path):
        with open(path, 'r', encoding = 'utf-8') as f:
            return json.load(f)
    return {} # If cache doesn't exist, return empty dict


def save_cache(path: str, data: dict):
    """ Save cache to a JSON file."""
    with open(path, 'w', encoding = 'utf-8') as f:
        json.dump(data, f)


def store_assets(post: Posts):
    """Stores a list of the URLs of the images published to nostr in .caches/assets (if 
    not already stored)."""
    file_path = f".caches/assets/" + str(date.today()) # Stores the file path
    os.makedirs(".caches/assets", exist_ok=True) # Makes an assets directory if it doesnt exist.

    existing_urls = set() # Creates an empty collection of unique elements.
    if os.path.isfile(file_path): # Checks if file exists
        with open(file_path, "r") as f: # Opens file in read mode
            existing_urls = set(line.strip() for line in f) # Extracts all URLs listed in the file.

    with open(file_path, "a") as f: # Opens file in append mode.
        for url in post.image_urls: # Iterates through the user input URLs.
            if url not in existing_urls: # If URL is not already in caches-file.
                f.write(url + "\n") # Adds the URL to the caches-file.


def	user_prompt_post_type():
	"""Prompts the user to choose between short or long form content, and returns the type."""
	while (1):
		post_type = input("Would you like to post your content as blog posts or regular posts?\nEnter 1 for blog post (long form, kind 30023)\nEnter 2 for regular post (short form, kind 1)\n: ")
		if (post_type == "1" or post_type == "2"):
			break
	return post_type
