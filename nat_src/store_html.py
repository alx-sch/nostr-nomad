from bs4 import BeautifulSoup
from html_to_markdown import convert_to_markdown
from class_data import Data


def	store_post_id_and_name(html_file: str, data: Data):
	"""Extracts the post_id (numeral) and post name for each html-file."""

	# The html_file is typically stored like this: "export/extracted/posts/159934842.how-to-use-the-substack-editor.html"
	last_slash_index = html_file.rfind('/') # In order to only look at the .html-file (without path), the index of the last occurence of '/' is stored.
	only_filename = html_file[last_slash_index + 1:] # Everything after the last occurence of '/' is stored in only_filename (159934842.how-to-use-the-substack-editor.html)
	digits = "".join(filter(str.isdigit, only_filename))  # Extracts the digits (159934842)
	data.post_id.append(digits[:9])  # Takes the right amount of digits and stores them in post_id.

	# We now have only_filename containing "159934842.how-to-use-the-substack-editor.html"
	first_dot_index = only_filename.find('.') # We locate the first '.'.
	last_dot_index = only_filename.rfind('.') # We locate the last '.'
	data.post_name.append(only_filename[first_dot_index + 1:last_dot_index]) # We store the post name (which is in between the two '.')


def store_html_files_content(data: Data):
	"""Reads and parses HTML files into BeautifulSoup objects, storing them in data.html_files_content."""

	for item in data.html_files: # Iterating through each html-file and storing their content in a list of BeautifulSoup objects.
		file = open(item, "r", encoding="utf-8") # Opens the .html-file.
		content = file.read() # Reads through the file, and stores everything in content.
		if not content: # If file is empty, returns an error.
			return 3
		data.html_files_content.append(BeautifulSoup(content, "html.parser")) # BeautifulSoup translates the document into an object with attributes, and it's added to the list.
		file.close() # Closes the .html-file.
		store_post_id_and_name(item, data) # Stores the post id and name for the current html file.
	return 0


def	extract_image_urls(data: Data):
	"""Stores the URLs of all images in the html files."""
	for item in data.html_files_content: # Iterates through each html file.
		img = item.find_all("img") # Searches for all instances of "img", indicating there is an image.
		for item in img: # Iterates through all instances of "img".
			data.image_urls.append(item.get("src")) # Gets the "src" part of "img", which is the image URL. Stores this in a list of URLs.


def html_to_markdown(data: Data):
	"""Converts each html file to markdown format."""
	for item in data.html_files_content: # Iterates through every html file.
		data.post_in_markdown.append(convert_to_markdown(item)) # Converts current file to markdown.
