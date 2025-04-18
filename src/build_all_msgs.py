# standard imports
import os


def build_all_msgs(path_to_html_files: str, builder):
    """ Process all HTML files into plaintext and 
    return a dictionary of post IDs and their corresponding messages."""
    messages = {}
    
    for f in os.listdir(path_to_html_files):
        file_path = os.path.join(path_to_html_files, f)
        if os.path.isfile(file_path) and file_path.endswith('.html'):
            messages.update(builder.build_message(file_path))
    
    return messages

## ADD 'build_all_markdown_msgs' FUNCTION ##
