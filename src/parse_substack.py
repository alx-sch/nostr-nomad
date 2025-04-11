import os
import csv
#import zipfile
from bs4 import BeautifulSoup

"""
def extract_zips(folder_path: str):
    ''' Extracts a single ZIP file in the given folder into 'unzipped' subfolder.'''
    # Get all .zip files in the folder
    zip_files = [f for f in os.listdir(folder_path) if f.endswith(".zip")]
    
    # Check if there is exactly one zip file
    if len(zip_files) != 1:
        print_error(f"Error: Expected exactly one export zip file, found {len(zip_files)}.")
        return False
    
    # Build the path to the zip file and the output directory
    zip_path = os.path.join(folder_path, zip_files[0])
    output_dir = os.path.join(folder_path, "unzipped")
    os.makedirs(output_dir, exist_ok=True)

    # Extract the zip file
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)
    except zipfile.BadZipFile:
        print_error(f"Error: The file {zip_path} is not a valid zip file.")
        return False
    return True
"""

def load_post_titles(csv_file: str):
    """ Load post titles and subtitles from a CSV file.
    Returns a dictionary with post IDs as keys and a dictionary of titles and subtitles as values.
    """
    post_titles = {}
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            post_id = row['post_id']
            # Extract the numeric part of the post_id (before the first dot)
            numeric_post_id = post_id.split('.')[0]
            title = row['title']
            subtitle = row['subtitle']
            post_titles[numeric_post_id] = {'title': title, 'subtitle': subtitle}
    return post_titles

def parse_html_to_simple_text(file_path: str):
    """ Converts HTML file content into a simplified text format."""
    # Open the HTML file and read its content
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
        
    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    result = []

    # Loop through all elements in the document, keeping the order intact
    for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'img']):
        # Check for image elements and add the image URL to the result
        if element.name == 'img':
            image_url = element.get('src')
            if image_url:
                result.append(f"{image_url}")
        # Skip paragraphs containing an 'a' tag with class 'button'
        elif element.name == 'p' and element.find('a', class_='button'):
            continue     
        # Check if the element is a header tag
        elif element.name.startswith('h'):
            result.append(f"{element.get_text(strip=True)}")
        elif element.name == 'p':
            result.append(f"{element.get_text(strip=True)}")

    # Join everything with two newlines to format the final output
    return "\n\n".join(result)

def add_titles_to_simple_text(message:str, title: str, subtitle: str):
    """ Add title and subtitle to a simple text message."""
    if subtitle:
        message = f"{subtitle}\n\n{message}"
    if title:
        message = f"[{title}]\n{message}" # Add title in brackets
    return message

def process_html_files(path_to_html_files: str, post_titles: dict):
    """ Process all HTML files and return a dictionary of post IDs and their corresponding messages."""
    messages = {}
    
    # List all files in the directory
    for filename in os.listdir(path_to_html_files):
        file_path = os.path.join(path_to_html_files, filename)
        # Skip directories, only process files ending with '.html'
        if os.path.isfile(file_path) and file_path.endswith('.html'):
            # Extract ID from the filename (before the first dot)
            post_id = filename.split('.')[0]
            # Check if post_id exists in the titles dictionary
            if post_id in post_titles:
                title = post_titles[post_id]['title']
                subtitle = post_titles[post_id]['subtitle']
            else:
                title = ""
                subtitle = ""
            # Parse HTML and store the message using the post_id as key
            message = parse_html_to_simple_text(file_path)
            # Add title and subtitle to the message
            message = add_titles_to_simple_text(message, title, subtitle)
            messages[post_id] = message
    
    return messages
    