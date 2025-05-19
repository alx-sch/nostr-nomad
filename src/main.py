# local imports
from parse_config import parse_config
from parse_export import validate_export_paths
from build_posts import build_posts
from event_publisher import publish_posts

# from utils import debug_print


def main():
    """Entry point of nostr-nomad.

    This function:
    - Parses the config to get user input (keys, relays, etc.)
    - Checks for Substack export and extracts paths
    - Builds posts from the export data
    - Publishes the posts to Nostr relays

    Note:
            See src/models.py for more info about the 'User', 'Paths', and 'Post' classes (function returns).
    """
    user = parse_config("user_entries")
    paths = validate_export_paths()
    posts = build_posts(paths, user)
    publish_posts(posts, user, paths)
    print("✅ Done.")
    # debug_print(paths, user, posts)


if __name__ == "__main__":
    main()
