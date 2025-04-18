# standard imports
import csv
import json
import os
    
    
def print_green(message: str):
    """ Prints a message in green."""
    bold_green = '\033[1m\033[32m'
    reset = '\033[0m'
    print(f"{bold_green}{message}{reset}")
    
    
def print_red(message: str):
    """ Prints a message in red."""
    bold_red = '\033[1m\033[31m'
    reset = '\033[0m'
    print(f"{bold_red}{message}{reset}")
    
    
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
        

def get_titles(csv_file: str):
    """ Load post titles and subtitles from a CSV file.
    Returns a dictionary with post IDs as keys and a dictionary of titles and subtitles as values.
    """
    post_titles = {}
    with open(csv_file, mode = 'r', encoding = 'utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            post_id = row['post_id']
            # Extract the numeric part of the post_id (before the first dot)
            numeric_post_id = post_id.split('.')[0]
            title = row['title']
            subtitle = row['subtitle']
            post_titles[numeric_post_id] = {'title': title, 'subtitle': subtitle}
    return post_titles

        