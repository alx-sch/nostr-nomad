# standard imports
import json
from build_event import build_signed_event
from time import sleep

# external imports
import websocket

# local imports
import utils
from nostr_config import NostrConfig


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


def publish_posts(posts, nostr: NostrConfig, cache_file, delay: int=1):
    """ Publish posts to the given relays, checking for duplicates in the cache.
    
    Parameters:
        posts (dict): Dictionary where keys are post IDs and values are post content.
        nostr (NostrConfig): Configuration object containing relays and key information.
        cache_file (str): Path to the file used to cache already-published posts.
        delay (int, optional): Delay in seconds between publishing each post. Defaults to 1.
    """
    bold = '\033[1m'
    reset = '\033[0m'
    padding = len(max(nostr.relays, key = len))
    print(f"\nPublishing as '{bold}{nostr.npub_key}{reset}'\n")
    
    # Load cache from file (or create an empty cache if it doesn't exist)
    published = utils.load_cache(cache_file)
    
    # Iterate through posts and publish them
    for post_id, content in posts.items():
        relays_published = published.get(post_id, [])  # Get list of relays post is already published to
        event = build_signed_event(content, nostr)
        
        print(f"Sending post '{post_id}'...")
        
        # Publish to relays
        for relay in nostr.relays:
            if relay in relays_published:
                print(f"  - to {relay.ljust(padding)} ... ", end="")
                utils.print_yellow(f"Already published. Skipping this relay.")
                continue
            
            if publish_event(event, relay, padding):
                relays_published.append(relay)  # Add relay to the list of relays post is published to
                
        print('')
        published[post_id] = relays_published  # Update cache
        utils.save_cache(cache_file, published)   # Save the updated cache
        sleep(delay)  # Add delay between publishing posts
    