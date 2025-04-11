from time import time
from json import dumps
from hashlib import sha256

def build_message(content: str, pub_key: str, kind: int, tags):
    """ Build a Nostr message with the given content, public key, kind, and tags.
    Parameters:
        content (str): The content of the message to be sent.
        pub_key (str): The public key of the sender (hex format).
        kind (int): The kind of event.
        tags (list): List of tags for the event.
    Returns:
        list: The message data in a list format.
    """
    if tags is None:
        tags = []
    t = int(time())
    msg = [
        0,          
        pub_key,    # Public key
        t,          # Timestamp
        kind,       # Event kind
        tags,       # Tags 
        content,    # Content of the message
    ]
    return msg

def build_event(message: str, priv_key, pub_key: str, kind: int=1, tags=None):
    """ Builds and signs an event message for publishing to Nostr relays.
    Parameters:
        message (str): The content of the message to be sent.
        priv_key (PrivateKey obj): Private key object file.
        priv_key (str): Public key (in hex format).
        kind (int): The kind of event (default is 1 for text note).
        tags (list): Optional list of tags for the event.
    Returns:
        str: The event in JSON format ready for publishing.
    """
    # Create the unsigned message data
    msg = build_message(message, pub_key, kind, tags)
    msg_json = dumps(msg, ensure_ascii=False, separators=(',', ':'))
    
    # Calculate the signature over the digest of the unsigned message
    hash = sha256()
    hash.update(msg_json.encode("utf-8"))
    msg_hash = hash.digest()
    sig = priv_key.sign_schnorr(msg_hash)
    
    # Assemble and output the message to be published, adding the digest and the signature
    payload = {
        "id": msg_hash.hex(),
        "pubkey": msg[1],
        "created_at": msg[2],
        "kind": msg[3],
        "tags": msg[4],
        "content": msg[5],
        "sig": sig.hex(),
    }
    event = [
        "EVENT",  
        payload,  
    ]
    return dumps(event, ensure_ascii=False)
