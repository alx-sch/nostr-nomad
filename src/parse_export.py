"""parse_export.py

Substack export validator and extractor for nostr-nomad.

This module:
- Validates that exactly one zip file or directory exists in the input folder.
- Extracts and verifies the structure of a Substack export.
- Stores paths to key files (posts.csv, HTML files) in a `Paths` dataclass.

Expected export structure:
- Either a .zip file or a single directory.
- A top-level `posts.csv` and a `posts/` folder with .html files.
"""

# standard imports
import os
from zipfile import ZipFile

# local imports
from models import Paths
from errors import INVALID_EXPORT_STRUCTURE, MISSING_SUBSTACK_DATA, error_and_exit


def count_dirs(paths: Paths):
    """Makes sure there is only one directory or zip file in the input folder."""
    count = 0
    for path in os.listdir(paths.input_std_dir):
        full_path = os.path.join(paths.input_std_dir, path)
        if os.path.isdir(full_path) or path.endswith(
            ".zip"
        ):  # Only accepts ONE directory or zip-file.
            count += 1
            paths.input_usr_dir = full_path
        else:
            error_and_exit(INVALID_EXPORT_STRUCTURE)

    if count != 1:
        error_and_exit(INVALID_EXPORT_STRUCTURE)


def extract_and_store_zip(paths: Paths):
    """Extract a zip file and store paths to CSV and HTML files from the Substack export."""
    csv_found = False
    html_found = False

    extract_path = os.path.join(paths.input_std_dir, "extracted")
    os.makedirs(extract_path, exist_ok=True)

    with ZipFile(paths.input_usr_dir) as zfile:
        zfile.extractall(extract_path)

        for item in zfile.namelist():
            if item.endswith(".csv"):
                if item == "posts.csv":
                    csv_found = True
                    paths.posts_csv = os.path.join(extract_path, item)
                paths.csv_files.append(os.path.join(extract_path, item))

            elif item.startswith("posts/"):
                if item.endswith(".html"):
                    html_found = True
                    paths.html_files.append(os.path.join(extract_path, item))
                elif item.endswith(".csv"):
                    csv_found = True
                    paths.csv_files.append(os.path.join(extract_path, item))
                else:
                    error_and_exit(MISSING_SUBSTACK_DATA)

            else:
                error_and_exit(MISSING_SUBSTACK_DATA)

    if not csv_found or not html_found:
        error_and_exit(MISSING_SUBSTACK_DATA)


def store_dir(paths: Paths):
    """Stores all the paths of the files of Substack export directory."""
    csv_found = False
    posts_found = False
    html_found = False

    for item in os.listdir(paths.input_usr_dir):
        full_path = os.path.join(paths.input_usr_dir, item)

        if item.endswith(".csv"):
            if item == "posts.csv":
                csv_found = True
                paths.posts_csv = full_path
            paths.csv_files.append(full_path)

        elif item == "posts":
            if posts_found:
                error_and_exit(MISSING_SUBSTACK_DATA)
            if not os.path.isdir(full_path):
                error_and_exit(MISSING_SUBSTACK_DATA)

            posts_found = True
            for file in os.listdir(
                full_path
            ):  # Iterates through "posts"-directory, making sure there are only .html-files.
                if file.endswith(".html"):
                    html_found = True
                    paths.html_files.append(
                        os.path.join(full_path, file)
                    )  # Adds the .html-files to the list of files.
                elif file.endswith(".csv"):
                    csv_found = True
                    paths.csv_files.append(full_path)
                else:
                    error_and_exit(MISSING_SUBSTACK_DATA)

        else:
            error_and_exit(MISSING_SUBSTACK_DATA)

    if not (
        csv_found and posts_found and html_found
    ):  # If not only ONE csv-file and a posts-folder with html-file(s), return error.
        error_and_exit(MISSING_SUBSTACK_DATA)


def validate_export_paths():
    """Makes sure the substack export is as expected, and stores all contents in 'paths' dataclass."""
    paths = Paths()
    count_dirs(paths)

    if paths.input_usr_dir.endswith(".zip"):
        extract_and_store_zip(paths)
    else:
        store_dir(paths)

    return paths
