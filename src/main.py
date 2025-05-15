# local imports
import utils
import usr_config
import build_posts
import get_paths
from event_publish import publish_posts
from debug import debug_print

def main():
	""" Entry point of nostr-nomad.

	Parameters:
		post_type (str): Long form (1) or short form (2) content.
		user (Usr): Usr object containing private and public keys, relays, etc.
		paths (Paths): Paths object containing paths to substack export.
		posts (Posts): List of Posts-objects containing all data about each post.

	Additional info:
		See src/models.py for more info about the pathsclasses.
	"""
	post_type = utils.user_prompt_post_type() # Prompts user for '1' (long form) or '2' (short form).
	user = usr_config.parse_config("user_entries") # Parses and stores contents of 'user_entries/config.ini' (private key and relays).
	paths = get_paths.parse_and_get_paths() # Validates substack export and stores paths to files.
	posts = build_posts.build_posts(paths, post_type) # Stores all necessary post data in a list of posts.
	publish_posts(posts, user) # Creates nostr events, and publishes all posts to the specified relays. 
	# debug_print(paths, user, posts)

if __name__ == "__main__":
    main()
