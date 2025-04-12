import os
from zipfile import ZipFile
from class_data import Data


def count_dirs(data: Data):
	"""Makes sure there is only one directory or zip file in input folder."""
	count = 0 
	for path in os.listdir(data.input_std_dir): # Iterates through input directory.
		data.input_usr_dir = os.path.join(data.input_std_dir, path) # Sets the path of directory/zip-file the user has added.
		if (os.path.isdir(data.input_usr_dir) or path.endswith('.zip')): # Only accepts ONE directory or zip-file.
			count += 1
		else: # If anything else is found, it throws an error.
			return 4
	if count != 1:
		return 4
	return 0


def extract_and_store_zip(data: Data):
	"""Extracts zip file, creates an "extracted" directory for all contents, and stores all the paths of the files of substack export directory."""

	csv_found = False # Needs to be at least one csv-file.
	html_found = False # Needs to be at least one html-file.

	extract_path = os.path.join(data.input_std_dir, "extracted") # Sets path to extract-dir.
	os.makedirs(extract_path, exist_ok=True) # Creates the extract directory, and make sure it exists.

	with ZipFile(data.input_usr_dir) as zfile: # Opens zipfile and stores it contents in zfile as a list.
		zfile.extractall(extract_path) # Extracts the contents of the zip file to "extract_path"
	
		for item in zfile.namelist(): # Iterates through zipfile contents.
		
			if (item.endswith('.csv')): # Stores the csv-file.
				csv_found = True
				data.csv_files.append(os.path.join(extract_path, item))
			
			elif (item.startswith('posts/')): # Stores the .html-files.
				if (item.endswith('.html')):
					html_found = True
					data.html_files.append(os.path.join(extract_path, item))
				elif (item.endswith('.csv')): # Stores the csv-file.
					csv_found = True
					data.csv_files.append(os.path.join(extract_path, item))
				else:
					return 5
		
			else:
				return 5

	if (csv_found == False or html_found == False): # If not only ONE csv-file and a posts-folder with html-file(s), return error.
		return 5
	return 0


def store_dir(data: Data):
	"""Stores all the paths of the files of substack export directory."""

	csv_found = False # Used to ensure there's at least one csv-file.
	posts_found = False # Needs to be one "posts"-folder present.
	html_found = False # Needs to be at least one html-file.

	for item in os.listdir(data.input_usr_dir): # Iterating through the user's directory
		full_path = os.path.join(data.input_usr_dir, item) # Creates a path of user's directory and the current file/dir.

		# If a csv-file is found
		if (item.endswith('.csv')):
			csv_found = True
			data.csv_files = full_path
		
		# If "posts"-directory is found
		elif (item == "posts"):
			if (posts_found == True): # If posts was already found (meaning there's two with same name).
				return 2
			if os.path.isdir(full_path): # Checks that "posts" is actually a directory.
				posts_found = True
				for file in os.listdir(full_path): # Iterates through "posts"-directory, making sure there are only .html-files.
					if (file.endswith('.html')):
						html_found = True
						data.html_files.append(os.path.join(full_path, file)) # Adds the .html-files to the list of files.
					elif (file.endswith('.csv')):
						csv_found = True
						data.csv_files.append(full_path)
					else:
						return 6
			else:
				return 6

		# If something else than "posts" or .csv-file was found.
		else:
			return 6
		
	if (csv_found == False or posts_found == False or html_found == False): # If not only ONE csv-file and a posts-folder with html-file(s), return error.
		return 6
	return 0
