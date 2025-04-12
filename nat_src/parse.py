from class_data import Data
from class_nostr_format import Usr
import store_user_data
import store_html
import store_paths
import debug

def parse_and_store(data: Data, user: Usr):
	"""Parsing an storing input files (paths and contents) from Substack export"""

	# Gets private key, public key and relays from user.
	error_code = store_user_data.get_data_from_user(user)
	if (error_code != 0):
		return error_code

	# Counts how many directories/zip files in 'input-dir', and stores the name of directory or zip file.
	error_code = store_paths.count_dirs(data)
	if (error_code != 0): # Returns with error code if not only 1 zip/dir.
		return error_code

	# Stores the paths of the .html-files and .csv-file.
	if (data.input_usr_dir.endswith('.zip')): # If zip-file, extracts and stores the content of the file in "extracted"-directory.
		error_code = store_paths.extract_and_store_zip(data)
	else: # If directory, stores the content of the directory.
		error_code = store_paths.store_dir(data)
	if (error_code != 0): # Returns with error code if .html files, posts-folder and .csv files are missing, or if other files are present.
		return error_code

	# Store the content of each .html-file, post ID and post name.
	error_code = store_html.store_html_files_content(data)
	if (error_code != 0): # Returns with error code if at least one .html-file is empty.
		return error_code

	# Extracts the image urls from each html-file, and stores them in a list.
	store_html.extract_image_urls(data)

	# Converts each html file to markdown format, and stores this in a markdown-list.
	store_html.html_to_markdown(data)

	# A module for printing values, for debugging.
	debug.debug_print(data, user)

	return 0
