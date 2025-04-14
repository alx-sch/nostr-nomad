from utils import print_green, print_red, print_yellow, load_cache, save_cache
from build_event import build_event
from json import loads
from keys import encode_npub
from time import sleep
import websocket

def publish_event(event_json: str, post_id: str, relay_url: str):
    """ Publish an event to a Nostr relay.
    Parameters:
        event_json (str): The event in JSON format to be sent.
        post_id (str): The ID of the post being published.
        relay_url (str): The URL of the Nostr relay to which the event will be sent.
    Returns:
        bool: 'True' if the event was successfully sent, 'False' otherwise.
    """
    print(f"Sending post '{post_id}' to '{relay_url}': ", end="") 
    
    try:
        ws = websocket.create_connection(relay_url) # Create a WebSocket connection
        ws.send(event_json) # Send the event JSON to the relay
        response = ws.recv() # Wait for a response from the relay
        response_data = loads(response) # Parse the response data
        
        if response_data[0] == "OK": 
            print_green(response_data[0])
            ws.close()
            return True
        else:
            print_red(response_data[0])
            ws.close()
            return False
        
    except Exception as e:
        print_red(f"{e}")
        return False
    
def publish_posts(posts, relays, private_key, public_key, cache_file, delay: int=1):
    """ Publish posts to the given relays, checking for duplicates in the cache.
    Parameters:
        posts (dict): Dictionary of posts to be published.
        relays (list): List of relay URLs to publish to.
        private_key (PrivateKey obj): Private key for signing the events.
        public_key (str): Public key (hex format).
        cache_file (str): Path to the cache file for storing published posts.
        delay (int): Delay between publishing each post (default is 1 second).
    """
    # Print the npub key
    npub_key = encode_npub(public_key)
    print(f"Publishing as '{npub_key}'")
    
    # Load cache from file (or create an empty cache if it doesn't exist)
    published = load_cache(cache_file)
    
    # Iterate through posts and publish them
    for post_id, content in posts.items():
        relays_published = published.get(post_id, [])  # Get list of relays post is already published to
        event = build_event(content, private_key, public_key)
        
        # Publish to relays
        for relay in relays:
            if relay in relays_published:
                print_yellow(f"Post '{post_id}' already published to '{relay}'.")
                continue
            if publish_event(event, post_id, relay):
                relays_published.append(relay)  # Add relay to the list of relays post is published to
        
        published[post_id] = relays_published  # Update cache
        
        # Add delay between publishing posts
        sleep(delay)

    # Save the updated cache
    save_cache(cache_file, published)