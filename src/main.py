# local imports
from build_all_msgs import build_all_msgs
from build_msg import PlaintextBuilder
from nostr_config import parse_config
from paths import get_paths
from publish_event import publish_posts
from utils import get_titles

def main():
    paths = get_paths()
    nostr = parse_config(paths.config_dir)
    builder = PlaintextBuilder(title_map = get_titles(paths.csv))  ## OR CHOOSE MARKDOWN BUILDER ##
    msgs = build_all_msgs(paths.html_dir, builder)
    publish_posts(msgs, nostr, paths.cache)
    
if __name__ == "__main__":
    main()
    