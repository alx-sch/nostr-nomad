import sys
import os
from json import load, dump
from dataclasses import dataclass

def print_error(message: str):
    """ Prints an error message in red to stderr."""
    bold_red = '\033[1m\033[31m'
    reset = '\033[0m'
    print(f"{bold_red}{message}{reset}", file=sys.stderr)
    
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
    yellow = '\033[33m'
    reset = '\033[0m'
    print(f"{yellow}{message}{reset}")

def check_export_folder(folder_path: str) -> str:
    """ Checks if the substack export data exists and is valid."""
    # List subfolders in 'folder_path'
    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

    # Check if there is exactly one folder
    if len(subfolders) != 1:
        raise ValueError(f"Expected one substack export folder in '{folder_path}<substack_export>/' (unzipped); found {len(subfolders)}.")
    
    # Get the path to the subfolder
    export_folder = os.path.join(folder_path, subfolders[0])

    # Check if the 'posts' folder exists inside the subfolder
    posts_folder = os.path.join(export_folder, "posts")
    if not os.path.isdir(posts_folder):
        raise FileNotFoundError(f"'posts' folder not found inside the substack export.")


    # Check if the 'posts.csv' file exists inside the 'posts' folder
    posts_csv = os.path.join(export_folder, "posts.csv")
    if not os.path.isfile(posts_csv):
        raise FileNotFoundError(f"'posts.csv' file not found inside the substack export.")

    return export_folder 

def define_paths(base_dir :str="./user_input/"):
    """ Define paths for config, export folder, CSV file, HTML files, and cache file."""
    path_to_config = os.path.join(base_dir, "config.toml")
    path_to_export = check_export_folder(os.path.join(base_dir, "export/"))
    if not path_to_export:
        return None, None, None, None, None
    path_to_csv = os.path.join(path_to_export, "posts.csv")
    path_to_html_files = os.path.join(path_to_export, "posts/")
    cache_file = os.path.join(base_dir, "cache.json")
    return path_to_config, path_to_export, path_to_csv, path_to_html_files, cache_file

def load_cache(path: str):
    """ Load cache from a JSON file."""
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return load(f)
    return {}

def save_cache(path: str, data: dict):
    """ Save cache to a JSON file."""
    with open(path, "w", encoding="utf-8") as f:
        dump(data, f, indent=2)