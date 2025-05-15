# standard imports
from dataclasses import dataclass, field
from typing import Optional

# external imports
from bs4 import BeautifulSoup


### THIS FILE IS DECLARING ALL USED DATACLASSES ###


@dataclass # Declaring a dataclass, to store different information.
class   Usr: 

	# Storing credentials about the user
    priv_key: str = "" # Stores the private key of the user
    pub_key: str = "" # Stores the generated public key of the user
    npub_key: str = "" # Stores the generated public key of the user in npub format.
    relays: list[str] = field(default_factory=list) # Stores a list of relays user wants to post to.
    caches_posts: str = ".caches/posts/caches.json" # Stores the path of caches file (the caches keep track of what's already been published).


@dataclass # Declaring a dataclass, to store path information.
class	Paths:

	# Used for storing file paths for substack export.
	input_std_dir: str = "user_entries/export" # The path of the directory in which to place the substack export.
	input_usr_dir: str = "" # The path of the directory or zip file the user added.
	input_posts_dir: str = "/posts" # The path of the posts directory that is part of the substack export.
	html_files: list[str] = field(default_factory=list) # A list of the .html-files paths.
	posts_csv: str = "" # The path to the "posts.csv"-file.
	csv_files: list[str] = field(default_factory=list) # A list of all the .csv-files paths.
	image_urls: list[str] = field(default_factory=list) # A list of all image URLs in all the html-files (regardless of publishing or not).


@dataclass # Declaring a dataclass, to store different information.
class	Posts: 
	
	# Metadata and content of a post
	post_id: str = "" # Stores the <post_ID_nbr>.<post_name> (e.g. 12345678.hello-world).
	d_tag: str = "" # Stores a d-tag to be passed with the nostr event - to make it an editable event. A unique identifier in this format "123456.nostr-nomad".
	post_date: str = "" # Stores the time the post was originally published.
	is_published: bool = False # If true the post was published on substack (and should also be published on nostr).
	title: str = "" # Stores the title of the post.
	subtitle: str = "" # Stores the summary of the post.
	image_urls: list[str] = field(default_factory=list) # Stores all the image URLs from the post.
	content: str = "" # Stores the post content. If short form --> plaintext format. If long form --> markdown format.
	html_content: Optional[BeautifulSoup] = None # Stores the post content in BeautifulSoup (HTML) format.
	tags: list[str] = field(default_factory=list) # Stores a list of tags (to use for nostr event).
	kind: int = 0 # Stores the nostr event kind (1 for short form, 30023 for long form).

