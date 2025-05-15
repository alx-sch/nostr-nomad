# standard imports
import json
from time import sleep

# external imports
import websocket

# local imports
import utils
from models import Posts, Usr
from event_build import build_signed_event


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
    print(f"  - to {relay.ljust(padding)} ... ", end="")
        
    try:
        ws = websocket.create_connection(relay)
    except Exception as e: 
        utils.print_red(f"Connection Error: {e}")
        return False
        
    try:
        ws.send(event_json)
    except Exception as e:
        utils.print_red(f"WebSocket send error: {e}")
        ws.close()
        return False
        
    try:
        response = ws.recv()
    except Exception as e:
        utils.print_red(f"WebSocket receive error: {e}")
        ws.close()
        return False
        
    try:
        response_data = json.loads(response)
    except Exception as e:
        utils.print_red(f"Error decoding JSON response: {e}")
        ws.close()
        return False
        
    try:
        if response_data[0] == "OK":
            utils.print_green(response_data[0])
            return True
        else:
            utils.print_red(response_data[0])
            return False
    except Exception as e:
        utils.print_red(f"Response structure error: {e}")
        return False
    finally:
        ws.close()
    
    
def publish_posts(posts: list[Posts], usr: Usr, delay: int=1):
    """ Publish posts to the given relays, checking for duplicates in the cache.
    
    Parameters:
        posts (dict): Dictionary where keys are post IDs and values are post content.
        nostr (NostrConfig): Configuration object containing relays and key information.
        cache_file (str): Path to the file used to cache already-published posts.
        delay (int, optional): Delay in seconds between publishing each post. Defaults to 1.
    """
    bold = '\033[1m'
    reset = '\033[0m'
    padding = len(max(usr.relays, key = len))
    print(f"\nPublishing as '{bold}{usr.npub_key}{reset}'\n")
    
    # Load cache from file (or create an empty cache if it doesn't exist)
    published = utils.load_cache(usr.caches_posts)
    
    # Iterate through posts and publish them
    for post in posts:
        relays_published = published.get(post.d_tag, [])  # Get list of relays post is already published to
        event = build_signed_event(post.content, usr.priv_key, usr.pub_key, post.tags, post.kind)
        
        print(f"Sending post '{post.d_tag}'...")
        
        # Publish to relays
        for relay in usr.relays:
            if relay in relays_published:
                print(f"  - to {relay.ljust(padding)} ... ", end="")
                utils.print_yellow(f"Already published. Skipping this relay.")
                continue
            
            if publish_event(event, relay, padding):
                relays_published.append(relay)  # Add relay to the list of relays post is published to
                utils.store_assets(post)
                
        print('')
        published[post.d_tag] = relays_published  # Update cache
        utils.save_cache(usr.caches_posts, published)   # Save the updated cache
        sleep(delay)  # Add delay between publishing posts
