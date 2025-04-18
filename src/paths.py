# standard imports
import os
from dataclasses import dataclass
from sys import exit

# local imports
from utils import print_red


def get_export_folder(folder_path: str):
    """ Returns the path to a valid Substack export folder."""
    export_folder = os.path.join(folder_path, "export")
    subfolders = [f for f in os.listdir(export_folder) if os.path.isdir(os.path.join(export_folder, f))]

    if len(subfolders) != 1:
        print_red(f"Error: Expected one substack export folder here: '{export_folder}/<substack_export>' (unzipped); found {len(subfolders)}.")
        exit(1)
    
    substack_folder = os.path.join(export_folder, subfolders[0])

    # Check if the expected files and folders exist (will throw error if not)
    os.stat(os.path.join(substack_folder, "posts"))
    os.stat(os.path.join(substack_folder, "posts.csv"))

    return substack_folder


@dataclass
class ProjectPaths:
    config_dir: str
    export: str
    csv: str
    html_dir: str
    cache: str


def get_paths(base_dir: str = "user_input"):
    """ Retrieves the file paths for the project's configuration, export folder, 
    CSV file, HTML files, and cache."""
    substack_export = get_export_folder(base_dir)
    paths = ProjectPaths(
        config_dir = base_dir,
        export = substack_export,
        csv = os.path.join(substack_export, "posts.csv"),
        html_dir = os.path.join(substack_export, "posts"),
        cache = os.path.join(base_dir, "cache.json")
    )
    return paths
