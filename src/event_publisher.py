"""event_publisher.py

Handles publishing signed Nostr events to relays.

Includes:
- WebSocket-based publishing to relays
- Duplicate avoidance via cache files
- Delayed publishing support
"""

# standard imports
import json
from time import sleep

# external imports
import websocket

# local imports
from models import Post, User, Paths
from event_builder import build_signed_event
from utils import print_red, print_green, print_yellow, load_cache, save_cache


def publish_event(event_json: str, relay: str, padding: int = 0):
    """
    Publish an event to a Nostr relay.

    Parameters:
        event_json (str): The event in JSON format to be sent.
        relay (str): The URL of the Nostr relay to which the event will be sent.
        padding (int): Amount of padding for formatting output.

    Returns:
        bool: True if the event was successfully sent, False otherwise.
    """
    print(f"    - to {relay.ljust(padding)} ... ", end="")

    try:
        ws = websocket.create_connection(relay)
    except Exception as e:
        print_red(f"Connection Error: {e}")
        return False

    try:
        ws.send(event_json)
    except Exception as e:
        print_red(f"WebSocket send error: {e}")
        ws.close()
        return False

    try:
        response = ws.recv()
    except Exception as e:
        print_red(f"WebSocket receive error: {e}")
        ws.close()
        return False

    try:
        response_data = json.loads(response)
    except Exception as e:
        print_red(f"Error decoding JSON response: {e}")
        ws.close()
        return False

    try:
        if response_data[0] == "OK":
            print_green("Sent")
            return True
        else:
            print_red(response_data[0])
            return False
    except Exception as e:
        print_red(f"Response structure error: {e}")
        return False
    finally:
        ws.close()


def publish_posts(posts: list[Post], usr: User, paths: Paths, delay: int = 1):
    """
    Publish a list of posts to the user's configured relays, skipping duplicates.

    Parameters:
        posts (list[Post]): List of posts to publish.
        usr (User): User object containing keys and relays.
        paths (Paths): Paths object holding cache file paths.
        delay (int, optional): Delay between publishing posts (in seconds).
    """
    padding = len(max(usr.relays, key=len)) if usr.relays else 0
    print(f"📝 Publishing as:\n   {usr.npub_key}\n")

    # Load cache from file (or create an empty cache if it doesn't exist)
    published = load_cache(paths.cache_posts)

    # Iterate through posts and publish them
    print("🚀 Sending posts...\n")
    for post in posts:
        relays_published = published.get(
            post.d_tag, []
        )  # Get list of relays post is already published to
        event = build_signed_event(
            post.content, usr.priv_key, usr.pub_key, post.tags, post.kind
        )

        print(f"  → '{post.post_id}'")

        # Publish to relays
        for relay in usr.relays:
            if relay in relays_published:
                print(f"    - to {relay.ljust(padding)} ... ", end="")
                print_yellow("Already published. Skipping this relay.")
                continue

            if publish_event(event, relay, padding):
                relays_published.append(
                    relay
                )  # Add relay to the list of relays post is published to

        print("")
        published[post.d_tag] = relays_published  # Update cache
        save_cache(paths.cache_posts, published)  # Save the updated cache
        sleep(delay)  # Add delay between publishing posts
