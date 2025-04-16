# standard imports
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
        