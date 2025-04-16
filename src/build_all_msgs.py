# standard imports
import csv
import os

# local imports
from build_plaintext import PlaintextBuilder


def load_titles(csv_file: str):
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


def build_all_plaintext_msgs(path_to_html_files: str, csv_file: str):
    """ Process all HTML files into plaintext and 
    return a dictionary of post IDs and their corresponding messages."""
    messages = {}
    titles = load_titles(csv_file)
    builder = PlaintextBuilder(title_map = titles)
    
    for f in os.listdir(path_to_html_files):
        file_path = os.path.join(path_to_html_files, f)
        if os.path.isfile(file_path) and file_path.endswith('.html'):
            messages.update(builder.build_message(file_path))
    
    return messages

## ADD 'build_all_markdown_msgs' FUNCTION ##
