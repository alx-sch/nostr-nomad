""" build_post_longform.py

Handles the construction of long-form Nostr events from Substack-style posts.

This module:
- Converts post dates to Unix timestamps (Nostr-compatible).
- Extracts metadata such as title, subtitle, and tags.
- Converts HTML content to Markdown.
- Assembles the final Post object fields: `content`, `kind`, and `tags`.
"""

# standard imports
from datetime import datetime

# external imports
from html_to_markdown import convert_to_markdown

# local imports
from models import Post


def convert_published_time(time: str):
	"""Converts an ISO 8601 timestamp (from Substack-style format) into a Unix timestamp string,
    which is the format required by Nostr."""
	dt = datetime.fromisoformat(time.replace("Z", "+00:00")) # Parse into datetime object
	unix_seconds = int(dt.timestamp()) # Get Unix timestamp (seconds since epoch)
	return(str(unix_seconds)) # Stringify


def	get_tags(post: Post):
	"""Builds a list of Nostr tags from post metadata.
    Includes title, subtitle (if present), publication time, and a unique identifier tag "d"."""
	tags = []
	if post.title is not None:
		tags.append(["title", post.title])
	if post.subtitle is not None:
		tags.append(["summary", post.subtitle])
	tags.append(["published_at", convert_published_time(post.post_date)])
	tags.append(["d", post.d_tag])
	return (tags)


def build_longform(post: Post, html_content: str):
	"""Prepares the post for a Nostr long-form event (kind 30023).
    Converts HTML content to Markdown, sets the event kind, and attaches tags."""
	post.content = convert_to_markdown(str(html_content))
	post.kind = 30023
	post.tags = get_tags(post)
	