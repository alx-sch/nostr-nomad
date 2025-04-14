import configparser
from utils import print_error
from process_keys import process_private_key, generate_random_private_key

def parse_config(path_to_config: str):
    """ Parse the configuration file to extract the private key and relay URLs."""
    # Check if the config file exists
    if not exists(path_to_config):
        print_error(f"Error: The config file '{path_to_config}' does not exist.")
        return None, None, None
    
    # Open and parse file
    with open(path_to_config, "rb") as f:
        config = load(f)
        
    # Use .get() to avoid KeyError if the field does not exist
    private_key = config.get("user", {}).get("private_key", None)  # Default to None if not found
    relays = config.get("nostr", {}).get("relays", [])  # Default to empty list if not found
        
    if private_key is None:
        print_error("Error: Private key is missing in the config file.")
        return None, None, None
    if not relays:
        print_error("Error: No relays found in the config file.")
        return None, None, None
    
    if private_key:
        priv_key, pub_key = process_private_key(private_key)
    else:
        priv_key, pub_key = generate_random_private_key()
        
    if priv_key is None:
        print_error(f"Error: Invalid private key. Please provide in '{path_to_config}'.")
        return None, None, None
        
    return priv_key, pub_key, relays


