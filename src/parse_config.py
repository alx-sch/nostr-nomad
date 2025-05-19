"""usr_config.py

Configuration parser for nostr-nomad.

This module reads a configuration file using the `confini` library,
extracts required settings (e.g., private key, relays, event type, image hosting),
validates them, and returns a populated `User` object.

Expected config fields:
- [USER] PRIVATE_KEY
- [NOSTR] EVENT_TYPE (must be "note" or "blog")
- [NOSTR] RELAYS (comma- or space-separated)
- [IMAGE_HOSTING] IMAGE_HOST (must be "substack", "wala", or "imgur")

If WALA is selected:
- [WALA] WALA_URL

If Imgur is selected:
- [IMGUR] IMGUR_CLIENT_ID

Raises:
- Exits the program with a message from `errors` if required fields are missing or invalid.
"""

# standard imports
import re

# external imports
import confini

# local imports
import keys
from models import User
from errors import (
    MISSING_PRIVATE_KEY,
    MISSING_RELAYS,
    INVALID_PRIVATE_KEY,
    MISSING_IMG_HOST,
    MISSING_WALA_URL,
    MISSING_IMGUR_CLIENT_ID,
    MISSING_EVENT_TYPE,
    error_and_exit,
)


def parse_relays(relays_str: str):
    """Parse relay string into a clean list of relay URLs, skipping comments and duplicates."""
    relay_candidates = re.split(r"[,\s]+", relays_str)

    relays = []
    seen = set()
    for entry in relay_candidates:
        entry = entry.strip()
        if not entry or entry.startswith("#") or entry.startswith(";"):
            continue
        if entry not in seen:
            relays.append(entry)
            seen.add(entry)
    return relays


def parse_config(path_to_config: str):
    """Parse a configuration file and return a User object with keys, relays, event type, and image hosting info."""
    config = confini.Config(path_to_config)
    config.process()

    # Retrieve the private key
    try:
        private_key = config.get("USER_PRIVATE_KEY")
    except KeyError:
        error_and_exit(MISSING_PRIVATE_KEY)

    # Retrieve the event type
    try:
        event_type = config.get("NOSTR_EVENT_TYPE")
    except KeyError:
        error_and_exit(MISSING_EVENT_TYPE)
    if event_type not in ["note", "blog"]:
        error_and_exit(MISSING_EVENT_TYPE)

    # Retrieve the relay URLs
    try:
        relays_str = config.get("NOSTR_RELAYS")
    except KeyError:
        error_and_exit(MISSING_RELAYS)

    # Retrieve the image hosting settings
    try:
        image_host = config.get("IMAGE_HOSTING_IMAGE_HOST")
    except KeyError:
        error_and_exit(MISSING_IMG_HOST)
    if image_host not in ["substack", "wala", "imgur"]:
        error_and_exit(MISSING_IMG_HOST)

    # Retrieve the WALA or Imgur settings, if applicable
    wala_url = ""
    imgur_client_id = ""
    if image_host == "wala":
        try:
            wala_url = config.get("WALA_WALA_URL")
        except KeyError:
            error_and_exit(MISSING_WALA_URL)
        if wala_url is None or wala_url == "":
            error_and_exit(MISSING_WALA_URL)
    elif image_host == "imgur":
        try:
            imgur_client_id = config.get("IMGUR_IMGUR_CLIENT_ID")
        except KeyError:
            error_and_exit(MISSING_IMGUR_CLIENT_ID)
        if imgur_client_id is None or imgur_client_id == "":
            error_and_exit(MISSING_IMGUR_CLIENT_ID)

    # Convert relay string to list
    relays = parse_relays(relays_str)
    if not relays:
        error_and_exit(MISSING_RELAYS)

    if private_key == "x":
        priv_key, pub_key = keys.generate_keys()
    else:
        priv_key, pub_key = keys.get_keys(private_key)

    if priv_key is None:
        error_and_exit(INVALID_PRIVATE_KEY)

    # Construct and return the User object with config values
    return User(
        priv_key,
        pub_key,
        keys.encode_npub(pub_key),
        relays,
        event_type,
        image_host,
        wala_url,
        imgur_client_id,
    )
