from coincurve import PrivateKey
from bech32 import convertbits, bech32_decode, bech32_encode

def process_private_key(priv_key: str):
    """ Process private key in either hex or nsec format.
    Parameters:
        priv_key (str): The private key in hex or nsec format.
    Returns:
        tuple: A tuple containing the PrivateKey object and the public key in hex format.
    """
    # Handle hex format private key
    if len(priv_key) == 64 and all(c in '0123456789abcdefABCDEF' for c in priv_key):
        priv_key_bytes = bytes.fromhex(priv_key) 
        
    # Handle nsec format private key
    elif priv_key.startswith('nsec') and len(priv_key) == 63 and priv_key[4:].isalnum():
        _, data = bech32_decode(priv_key)
        priv_key_bytes = bytes(convertbits(data, 5, 8, False))

    else:
        return None, None
    
    # Create private key object and generate the corresponding public key
    priv_key_object = PrivateKey(priv_key_bytes)
    pub_key_hex = priv_key_object.public_key_xonly.format().hex()
    return priv_key_object, pub_key_hex
    
def generate_random_private_key():
    """ Generate a random private key.
    Returns:
        tuple: A tuple containing the PrivateKey object and the public key in hex format.
    """
    priv_key_object = PrivateKey()
    pub_key_hex = priv_key_object.public_key_xonly.format().hex()
    return priv_key_object, pub_key_hex

def encode_npub(pubkey_hex: str):
    """ Encodes a public key in hex format into npub format."""
    pubkey_bytes = bytes.fromhex(pubkey_hex)
    data = convertbits(list(pubkey_bytes), 8, 5)
    return bech32_encode("npub", data)