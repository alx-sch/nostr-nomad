from class_data import Data
from class_nostr_format import Usr


def	debug_print(data: Data, user: Usr):
	"""Prints out all stored values after parsing and storing."""
	print("\nHtml-files:\n", data.html_files, "\n") # Prints out the html-files' paths.
	print("CSV-files:\n", data.csv_files, "\n") # Prints out the csv-files' paths.
	print("Html-files content:\n")
	for item in data.html_files_content: # Prints out the content of the html-files.
		print(item.prettify(), "\n")
	print("Post_ids:\n", data.post_id, "\n")
	print("Post_names:\n", data.post_name, "\n")
	print("Image URLs:\n", data.image_urls, "\n")
	print("HTML-files in Markdown-format:\n", data.post_in_markdown, "\n")
	print("User private key:\n", user.priv_key, "\n")
	print("User public key:\n", user.pub_key, "\n")
	print("User relays:\n", user.relays, "\n")
