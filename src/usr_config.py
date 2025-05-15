# standard imports
import re

# external imports
import confini

# local imports
import keys
from models import Usr
from errors import error_and_exit


def parse_config(path_to_config: str):
    """ Parse the configuration file to extract the private key and relay URLs."""
    config = confini.Config(path_to_config)
    config.process()
    
    try:
        private_key = config.get('USER_PRIVATE_KEY')
    except KeyError:
        error_and_exit(1)
    
    try:
        relays_str = config.get('NOSTR_RELAYS')
    except KeyError:
        error_and_exit(2)
    
    # Convert relay string to list
    # Split by any combination of commas and whitespace (incl. newlines), and remove extra spaces
    relays = [relays_str.strip() for relays_str in re.split(r'[,\s]+', relays_str) if relays_str.strip()]
    
    if private_key == 'x':
        priv_key, pub_key = keys.generate_keys()
    else:
        priv_key, pub_key = keys.get_keys(private_key)
        
    if priv_key is None:
        error_and_exit(3)

    return Usr(priv_key, pub_key, keys.encode_npub(pub_key), relays, ".caches/posts/caches.json")
