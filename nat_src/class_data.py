from dataclasses import dataclass, field
from bs4 import BeautifulSoup

@dataclass # Declaring a dataclass, to store different information.
class	Data:

	# Used for storing file paths for substack export.
	input_std_dir: str = "user_entries/export" # The path of the directory in which to place the substack export.
	input_usr_dir: str = "" # The path of the directory or zip file the user added.
	input_posts_dir: str = "/posts" # The path of the posts directory that is part of the substack export.
	html_files: list[str] = field(default_factory=list) # A list of the .html-files paths.
	post_id: list[str] = field(default_factory=list)
	post_name: list[str] = field(default_factory=list)
	csv_files: list[str] = field(default_factory=list) # A list of the .csv-files paths.
	error_code: int = 0 # Stores a number indicating the error.

	# Used for storing html_files content.
	html_files_content: list[BeautifulSoup] = field(default_factory=list) # A list of each html-file's content in Beautifulsoup format.
	image_urls: list[str] = field(default_factory=list) # A list of all image URLs in all the html-files.
	post_in_markdown: list[str] = field(default_factory=list) # Stores a string in markdown format of each html-file.
