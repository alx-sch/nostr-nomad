# standard imports
import re
from dataclasses import dataclass
from typing import List

# external imports
import confini

# local imports
import keys


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

    private_key = config.get('USER_PRIVATE_KEY')
    relays_str = config.get('NOSTR_RELAYS')
    
    # Convert relay string to list
    # Split by any combination of commas and whitespace (incl. newlines), and remove extra spaces
    relays = [relays_str.strip() for relays_str in re.split(r'[,\s]+', relays_str) if relays_str.strip()]
    
    if private_key == 'x':
        priv_key, pub_key = keys.generate_keys()
    else:
        priv_key, pub_key = keys.get_keys(private_key)
        
    if priv_key is None:
        raise ValueError(f"Invalid private key. Please provide in .ini file here: '{path_to_config}'.")
        
    return NostrConfig(priv_key, pub_key, keys.encode_npub(pub_key), relays)
