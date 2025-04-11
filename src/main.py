from utils import define_paths
from parse_config import parse_config
from parse_substack import load_post_titles, process_html_files
from publish_event import publish_posts
from sys import exit

def main():
    # Get paths
    path_to_config, path_to_export, path_to_csv, path_to_html_files, cache_file = define_paths()
    if not path_to_export:
        exit(1)

    # Parse config file
    private_key, public_key, relays = parse_config(path_to_config)
    if private_key is None or not relays:
        exit(1)   
        
    # Get post titles from CSV
    titles = load_post_titles(path_to_csv)
    
    # Get HTML content and add titles
    posts = process_html_files(path_to_html_files, titles)
    
    # Publish posts and manage cache
    publish_posts(posts, relays, private_key, public_key, cache_file)
    
if __name__ == "__main__":
    main()