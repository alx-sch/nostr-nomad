# standard imports
import csv

# external imports
from bs4 import BeautifulSoup

# local imports
from errors import error_and_exit
from models import Posts, Paths
from build_post_shortform import build_shortform
from build_post_longform import build_longform


def	extract_image_urls(paths: Paths, post: Posts):
	"""Stores the URLs of all images in the html files."""
	img = post.html_content.find_all("img")
	for item in img:
		post.image_urls.append(item.get("src"))
		paths.image_urls.append(item.get("src"))


def	remove_img_duplicate(soup: BeautifulSoup) -> BeautifulSoup:
	"""Since the substack export has several URL's for each image (different representations of the same image), 
	this function makes sure that there is only one URL per image (to avoid duplicated images)."""
	for a in soup.find_all('a'): # Finds all <a> elements.
		href = a.get('href') # For each <a>, get its href. 
		# If the <a> contains an <img>, or the href ends with an image extension.
		if a.find('img') or (href and href.endswith(('.jpg', '.jpeg', '.png', '.webp', '.avif'))):
			a.unwrap()  # Removes the <a> tag but keeps the content (like <img>)
	return (soup)


def	get_html_content(paths: Paths, post_id: str) -> BeautifulSoup:
	"""Extracts the content from the html files, also removing duplicated image
	URLs. 
	
	Throws an error and exits if:
	- Any of the .html-files are empty.
	- There is a mismatch between 'posts.csv'-file and .html-files.
	"""
	for item in paths.html_files:
		if (post_id in item):
			with open(item, "r", encoding="utf-8") as file:
				content = file.read()
				if not content:
					error_and_exit(6) # Exits with error if html file is empty.
				soup = remove_img_duplicate(BeautifulSoup(content, "html.parser"))
				return (soup)

	error_and_exit(7) # If html files don't match with the posts.csv-file, throws an error and exits.


def	build_posts(paths: Paths, post_type: str):
	"""Reads through the 'posts.csv' file, extracts metadata and stores this in a list
	of Posts objects. Builds the objects based on whether it's short or long form."""
	posts: list[Posts] = []

	with open(paths.posts_csv, "r", encoding="utf-8") as file:
		reader = csv.reader(file) # Uses csv.reader to parse through the 'posts.csv'-file.
		next(reader, None) # Skips the first line because this is just the template.
		for line in reader:

			tmp_html_content = get_html_content(paths, line[0]) # Finds the corresponding html-file, and converts it to Beautifulsoup format.

			post = Posts(
            post_id=line[0],
			d_tag = line[0].split('.')[0] + ".nostr-nomad",
            post_date=line[1],
            is_published=(line[2].lower() == "true"),
            title=line[7],
            subtitle=line[8],
			html_content=tmp_html_content
        )

			if (post.is_published == True):
				if (post_type == "1"):
					build_longform(post, str(tmp_html_content))
				elif (post_type == "2"):
					build_shortform(post, tmp_html_content)

				posts.append(post) # Adds the post to the list of posts to be published.

			extract_image_urls(paths, post) # To later store in .caches/assets.
		
		return (posts)
