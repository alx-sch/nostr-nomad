"""
Key management utilities for handling Nostr keys.

Provides functions to:
- Parse private keys in hex or Bech32 nsec format.
- Generate new random private keys.
- Encode public keys from hex to Bech32 npub format.

Uses `coincurve` for secp256k1 operations and `bech32` for encoding/decoding.
"""

# standard imports
import re

# external imports
from coincurve import PrivateKey
from bech32 import convertbits, bech32_decode, bech32_encode


def get_keys(priv_key: str):
    """Process private key in either hex or nsec format.

    Parameters:
        priv_key (str): The private key in hex or nsec format.

    Returns:
        tuple: (PrivateKey object, public key hex string), or (None, None) if invalid.
    """

    # Handle hex format private key
    if re.fullmatch(r"[0-9a-fA-F]{64}", priv_key):
        priv_key_bytes = bytes.fromhex(priv_key)

    # Handle nsec format private key
    elif priv_key.startswith("nsec") and len(priv_key) == 63 and priv_key[4:].isalnum():
        decoded = bech32_decode(priv_key)
        if decoded is None:
            return None, None
        _, data = decoded
        priv_key_bytes = bytes(convertbits(data, 5, 8, False))
        if priv_key_bytes is None:
            return None, None

    else:
        return None, None

    # Build keypair
    priv_key_obj = PrivateKey(priv_key_bytes)
    pub_key_hex = priv_key_obj.public_key_xonly.format().hex()
    return priv_key_obj, pub_key_hex


def generate_keys():
    """Generate a random private key.

    Returns:
        tuple: (PrivateKey object, public key hex string).
    """
    priv_key_obj = PrivateKey()
    pub_key_hex = priv_key_obj.public_key_xonly.format().hex()
    return priv_key_obj, pub_key_hex


def encode_npub(pub_key_hex: str):
    """Encode a public key hex string into npub Bech32 format.

    Parameters:
        pub_key_hex (str): Public key as hex string.

    Returns:
        str: npub-encoded public key string.
    """
    pub_key_bytes = bytes.fromhex(pub_key_hex)
    data = convertbits(list(pub_key_bytes), 8, 5)
    return bech32_encode("npub", data)
