from dataclasses import dataclass, field

@dataclass # Declaring a dataclass, to store different information.
class	NIP_23: # (Long Form Content)

    kind: int = 30023 # The code for long form content.
    created_at: int = 0 # How many seconds since Jan 1st 1970 kinda format.
    content: str = "" # The string in markdown.
    tags: list[tuple[str, str]] = field(default_factory=list) # A list of key-value pairs for the tags
    pubkey: str = "" # 32-bytes lowercase hex-encoded public key of the event creator
    id: str = "" # for instance: nostr.substack.<substack_post_id>

@dataclass # Declaring a dataclass, to store different information.
class   Usr: # Storing credentials about the user

    priv_key_path: str = "user_entries/credentials/ADD_PRIVATE_KEY_HERE.txt"
    pub_key_path: str = "user_entries/credentials/ADD_PUBLIC_KEY_HERE.txt"
    relays_path: str = "user_entries/credentials/ADD_RELAYS_HERE.txt"
    priv_key: str = "" # Stores the private key of the user
    pub_key: str = "" # Stores the public key of the user
    relays: list[str] = field(default_factory=list) # Stores a list of relays user wants to post to

# class   NIP_94: # (File metadata)
#     kind: int = 1063
#     created_at: int = 0
#     content: str = "" # Description of the file
#     tags: list[tuple[str, str]] = field(default_factory=list) # A list of key-value pairs for the tags. tags MUST contain the following:
#     # "url" (the url to download the file)
#     # "m" (a string indicating the data type of the file. The MIME types format must be used, and they should be lowercase.)
#     # "x" (containing the SHA-256 hexencoded string of the file.)
#     pubkey: str = "" # 32-bytes lowercase hex-encoded public key of the event creator
#     id: str = ""  # for instance: nostr.substack.<substack_post_id>
#     sig: str = "" # 64-bytes hex of the signature of the sha256 hash of the serialized event data, which is the same as the "id" field.
