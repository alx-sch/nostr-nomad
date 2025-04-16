# local imports
from build_all_msgs import build_all_plaintext_msgs
from nostr_config import parse_config
from paths import get_paths
from publish_event import publish_posts

def main():
    paths = get_paths()
    nostr = parse_config(paths.config_dir)
    msgs = build_all_plaintext_msgs(paths.html_dir, paths.csv)
    publish_posts(msgs, nostr, paths.cache)
    
if __name__ == "__main__":
    main()