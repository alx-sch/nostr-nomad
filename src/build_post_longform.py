# standard imports
from datetime import datetime

# external imports
from html_to_markdown import convert_to_markdown

# local imports
from models import Posts


def convert_published_time(time: str):
	"""Converts the post date (substack format) to correct nostr format."""
	dt = datetime.fromisoformat(time.replace("Z", "+00:00")) # Parse into datetime object
	unix_seconds = int(dt.timestamp()) # Get Unix timestamp (seconds since epoch)
	return(str(unix_seconds)) # Stringify


def	get_tags(post: Posts):
	"""Initializes a list of tags, stores the post's metadata (to be used for nostr event), and
	returns the list."""
	tags = []
	if post.title is not None:
		tags.append(["title", post.title])
	if post.subtitle is not None:
		tags.append(["summary", post.subtitle])
	tags.append(["published_at", convert_published_time(post.post_date)])
	tags.append(["d", post.d_tag])
	return (tags)


def build_longform(post: Posts, html_content: str):
	"""Adds the correct content format, event kind and tags for a longform event."""
	post.content = convert_to_markdown(str(html_content))
	post.kind = 30023
	post.tags = get_tags(post)
	