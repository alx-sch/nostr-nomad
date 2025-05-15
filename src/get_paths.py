# standard imports
import os
from zipfile import ZipFile

# local imports
from models import Paths
from errors import error_and_exit


def count_dirs(paths: Paths):
	"""Makes sure there is only one directory or zip file in input folder."""
	count = 0 
	for path in os.listdir(paths.input_std_dir): # Iterates through input directory.
		paths.input_usr_dir = os.path.join(paths.input_std_dir, path) # Sets the path of directory/zip-file the user has added.
		if (os.path.isdir(paths.input_usr_dir) or path.endswith('.zip')): # Only accepts ONE directory or zip-file.
			count += 1
		else: # If anything else is found, it throws an error.
			error_and_exit(4)
	if count != 1:
		error_and_exit(4)


def extract_and_store_zip(paths: Paths):
	"""Extracts zip file, creates an "extracted" directory for all contents, and stores all the paths of the files of substack export directory."""

	csv_found = False # Needs to be at least one csv-file.
	html_found = False # Needs to be at least one html-file.

	extract_path = os.path.join(paths.input_std_dir, "extracted") # Sets path to extract-dir.
	os.makedirs(extract_path, exist_ok=True) # Creates the extract directory, and make sure it exists.

	with ZipFile(paths.input_usr_dir) as zfile: # Opens zipfile and stores it contents in zfile as a list.
		zfile.extractall(extract_path) # Extracts the contents of the zip file to "extract_path"
	
		for item in zfile.namelist(): # Iterates through zipfile contents.
		
			if (item.endswith('.csv')): # Stores the csv-file.
				if (item == "posts.csv"):
					csv_found = True
					paths.posts_csv = os.path.join(extract_path, item)
				paths.csv_files.append(os.path.join(extract_path, item))
			
			elif (item.startswith('posts/')): # Stores the .html-files.
				if (item.endswith('.html')):
					html_found = True
					paths.html_files.append(os.path.join(extract_path, item))
				elif (item.endswith('.csv')): # Stores the csv-file.
					csv_found = True
					paths.csv_files.append(os.path.join(extract_path, item))
				else:
					error_and_exit(5)
		
			else:
				error_and_exit(5)

	if (csv_found == False or html_found == False): # If not only ONE csv-file and a posts-folder with html-file(s), return error.
		error_and_exit(5)


def store_dir(paths: Paths):
	"""Stores all the paths of the files of substack export directory."""

	csv_found = False # Used to ensure there's at least one csv-file.
	posts_found = False # Needs to be one "posts"-folder present.
	html_found = False # Needs to be at least one html-file.

	for item in os.listdir(paths.input_usr_dir): # Iterating through the user's directory
		full_path = os.path.join(paths.input_usr_dir, item) # Creates a path of user's directory and the current file/dir.

		# If a csv-file is found
		if (item.endswith('.csv')):
			if (item == "posts.csv"): # Needs to be a "posts.csv"-file.
				csv_found = True
				paths.posts_csv = full_path
			paths.csv_files.append(full_path) # Adds the .csv-file to the list of .csv-files.
		
		# If "posts"-directory is found
		elif (item == "posts"):
			if (posts_found == True): # If posts was already found (meaning there's two with same name).
				error_and_exit(5)
			if os.path.isdir(full_path): # Checks that "posts" is actually a directory.
				posts_found = True
				for file in os.listdir(full_path): # Iterates through "posts"-directory, making sure there are only .html-files.
					if (file.endswith('.html')):
						html_found = True
						paths.html_files.append(os.path.join(full_path, file)) # Adds the .html-files to the list of files.
					elif (file.endswith('.csv')):
						csv_found = True
						paths.csv_files.append(full_path)
					else:
						error_and_exit(5)
			else:
				error_and_exit(5)

		# If something else than "posts" or .csv-file was found.
		else:
			error_and_exit(5)
		
	if (csv_found == False or posts_found == False or html_found == False): # If not only ONE csv-file and a posts-folder with html-file(s), return error.
		error_and_exit(5)


def	parse_and_get_paths():
	"""Makes sure the substack export is as expected, and stores all contents in 'paths' dataclass."""
	paths = Paths()

	# Counts how many directories/zip files in 'input-dir', and stores the name of directory or zip file.
	count_dirs(paths)

	# Stores the paths of the .html-files and .csv-file.
	if (paths.input_usr_dir.endswith('.zip')): # If zip-file, extracts and stores the content of the file in "extracted"-directory.
		extract_and_store_zip(paths)
	else: # If directory, stores the content of the directory.
		store_dir(paths)

	return paths
