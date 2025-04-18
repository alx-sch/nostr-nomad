# standard imports
import re
from dataclasses import dataclass
from sys import exit
from typing import List

# external imports
import confini

# local imports
import keys
from utils import print_red


@dataclass
class NostrConfig:
    private_key: str
    public_key: str
    npub_key: str  
    relays: List[str]


def parse_config(path_to_config: str):
    """ Parse the configuration file to extract the private key and relay URLs."""
    config = confini.Config(path_to_config)
    config.process()
    
    try:
        private_key = config.get('USER_PRIVATE_KEY')
    except KeyError:
        print_red(f"Error: Missing 'private_key'. Please provide in '{path_to_config}/config.ini'.")
        exit(1)
    
    try:
        relays_str = config.get('NOSTR_RELAYS')
    except KeyError:
        print_red(f"Error: Missing 'relays'. Please provide in '{path_to_config}/config.ini'.")
        exit(1)
    
    # Convert relay string to list
    # Split by any combination of commas and whitespace (incl. newlines), and remove extra spaces
    relays = [relays_str.strip() for relays_str in re.split(r'[,\s]+', relays_str) if relays_str.strip()]
    
    if private_key == 'x':
        priv_key, pub_key = keys.generate_keys()
    else:
        priv_key, pub_key = keys.get_keys(private_key)
        
    if priv_key is None:
        print_red(f"Error: Invalid private key. Please provide in '{path_to_config}/config.ini'.")
        exit(1)
        
    return NostrConfig(priv_key, pub_key, keys.encode_npub(pub_key), relays)
