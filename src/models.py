""" models.py

This module defines all datasclasses used throughout the nostr-nomad tool:
- User: stores user credentials and relay configuration found in the config file.
- Paths: stores directory and file paths for input/output/cache.
- Post: stores metadata and content of each Substack post.

These structures are shared across modules for consistent data handling.
"""

# standard imports
from dataclasses import dataclass, field
from typing import Optional

# external imports
from bs4 import BeautifulSoup


@dataclass
class   User: 
	""" Confinguration info provided by the user in the config file.

	Attributes:
		priv_key (str):			The user's private key.
		pub_key (str):			The derived public key.
		npub_key (str):			The public key in NIP-19 'npub' format.
		relays (list[str]):		List of Nostr relay URLs.
		event_type (str):		Type of event to be sent (e.g. 'text', 'article').
		image_host (str):		Preferred image hosting service ('substack', 'wala', 'imgur').
		wala_url (str):			URL for the WALA image hosting service.
		imgur_client_id (str):	Client ID for the Imgur image hosting service.
	"""
	priv_key: str = ""
	pub_key: str = ""
	npub_key: str = ""
	relays: list[str] = field(default_factory=list)
	event_type: str = ""
	image_host: str = ""
	wala_url: str = ""	
	imgur_client_id: str = ""


@dataclass 
class	Paths:
	""" All relevant filesystem paths used by nostr-nomad.

	Attributes:
		input_std_dir (str):	Default path to the standard Substack export.
		input_usr_dir (str):	Path to a user-supplied Substack export directory or zip.
		input_posts_dir (str):	Subdirectory containing the individual post HTML files.
		html_files (list[str]):	List of paths to post HTML files.
		posts_csv (str):		Path to the main posts.csv metadata file.
		csv_files (list[str]):	List of all CSV file paths found in the export.
		image_urls (list[str]):	All image URLs extracted from HTML files.
		cache_root (str):		Root directory for storing cache data.
		cache_posts (str):		Path to JSON file tracking published posts.
		cache_imgs (str): 		Path to JSON file tracking uploaded images.
	"""
	input_std_dir: str = "user_entries/export"
	input_usr_dir: str = ""
	input_posts_dir: str = ""	
	html_files: list[str] = field(default_factory=list)
	posts_csv: str = ""
	csv_files: list[str] = field(default_factory=list)
	image_urls: list[str] = field(default_factory=list)
	cache_root: str = "cache"
	cache_posts: str = cache_root + "/posts.json"
	cache_imgs: str = cache_root + "/images.json"
 
 
@dataclass
class	Post:
	""" Represents a single Substack post to be published to Nostr.

	Attributes:
		post_id (str):				Unique Nostr identifier used to make the event editable (e.g. 123456.nostr-nomad).
		post_date (str):			Original publication date of the post.
		is_published (bool):		True if the post was marked as published on Substack.
		title (str):				Title of the post.
		subtitle (str):				Short summary or subtitle of the post.
		image_urls (list[str]):		List of original image URLs found in the HTML.
		content (str):				Post text content; Markdown for long-form or plain text for short-form.
		html_content (BeautifulSoup):	Parsed original HTML content using BeautifulSoup.
		tags (list[str]):			List of tags or categories to be included in the Nostr event.
		kind (int):					Nostr event kind (1 for short-form, 30023 for long-form).
		image_hashes (list[str]):	SHA256 hashes of downloaded/uploaded images.
		new_image_urls (list[str]):	URLs of images after being rehosted.
	"""
	post_id: str = ""
	d_tag: str = ""
	post_date: str = ""		
	is_published: bool = False
	title: str = ""
	subtitle: str = ""
	image_urls: list[str] = field(default_factory=list)
	content: str = ""
	html_content: Optional[BeautifulSoup] = None
	tags: list[str] = field(default_factory=list)
	kind: int = 0
	image_hashes: list[str] = field(default_factory=list)
	new_image_urls: list[str] = field(default_factory=list)
 