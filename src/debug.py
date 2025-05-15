# local imports
from models import Posts, Paths, Usr
import utils


def	debug_print(paths: Paths, user: Usr, posts: list[Posts]):
	"""Prints out all stored values after parsing and storing."""
	print("\nHtml-files:\n", paths.html_files, "\n") # Prints out the html-files' paths.
	print("CSV-files:\n", paths.csv_files, "\n") # Prints out the csv-files' paths.
	print("posts.csv-file:\n", paths.posts_csv, "\n")
	print("Image URLs:\n", paths.image_urls, "\n")
	utils.print_green("##### ALL POSTS #####\n")
	for post in posts:
		print("Title: ", post.title)
		print("Subtitle: ", post.subtitle)
		print(post.content)
	print("User private key:\n", user.priv_key, "\n")
	print("User relays:\n", user.relays, "\n")
