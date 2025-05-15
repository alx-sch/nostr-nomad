# standard imports
from hashlib import sha256
from json import dumps
from time import time


def build_unsigned_event(content: str, pub_key: str, tags: list[str], kind):
    """ Creates an unsigned Nostr event as a list, ready for hashing/signing.

    Parameters:
        content (str): The event content.
        pub_key (str): Hex-encoded public key of the author.
        kind (int): Nostr event kind (e.g., 1 for text notes or 30023 for blog posts).
        tags (List, optional): List of tags associated with the event.

    Returns:
        List: The event in unsigned list format [0, pubkey, created_at, kind, tags, content].
    """
    t = int(time())
    
    event = [
        0,          
        pub_key,    # Public key
        t,          # Timestamp
        kind,       # Event kind
        tags,       # Tags 
        content,    # Content of the messages
    ]
    return event


def build_signed_event(message: str, priv_key: str, pub_key: str, tags: list[str], kind: int):
    """ Creates and signs a Nostr event using Schnorr signature.

    Parameters:
        content (str): The message content.
        nostr (NostrConfig): Nostr configuration object containing private and public keys.
        kind (int): Nostr event kind (default is 1 for text notes).
        tags (List, optional): Tags list.

    Returns:
        str: JSON-encoded signed Nostr event.
    """
    # Create the unsigned event data
    event = build_unsigned_event(message, pub_key, tags, kind)
    event_json = dumps(event, ensure_ascii = False, separators = (',', ':'))
    
    # Calculate the signature over the digest of the unsigned message
    hash = sha256()
    hash.update(event_json.encode("utf-8"))
    event_hash = hash.digest()
    sig = priv_key.sign_schnorr(event_hash)
    
    # Assemble and output the message to be published, adding the digest and the signature
    event_signed = {
        "id": event_hash.hex(),  # SHA-256 hash of the serialized event content 
        "pubkey": event[1],
        "created_at": event[2],
        "kind": event[3],
        "tags": event[4],
        "content": event[5],
        "sig": sig.hex(),  # Schnorr signature of the event hash
    }
    # Relay expects the event to be in a list format
    event_packet = [
        "EVENT",  
        event_signed,  
    ]
    
    return dumps(event_packet, ensure_ascii = False)
