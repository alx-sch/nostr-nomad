# standard imports
from sys import exit

# local imports
from paths import get_paths
from config import parse_config
from parse_substack import load_post_titles, process_html_files
from publish_event import publish_posts

def main():
    paths = get_paths()
    config = parse_config(paths.config_dir)

        
    # Get post titles from CSV
    titles = load_post_titles(paths.csv)
    
    # Get HTML content and add titles
    posts = process_html_files(paths.html_dir, titles)
    
    # Publish posts and manage cache
    publish_posts(posts, config.relays, config.private_key, config.public_key, paths.cache)
    
if __name__ == "__main__":
    main()