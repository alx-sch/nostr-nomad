""" imgs_uploader.py

Handles image uploading logic for different hosting backends such as WALA or Imgur.

Currently supports:
- Uploading images to a WALA server using SHA-256 content-addressing.
- Future support for Imgur and other platforms can be added here.

This module is used by `handle_imgs()` to upload images after downloading and caching them.
"""

# standard imports
from urllib.request import Request, urlopen
from urllib.parse import urljoin

# external imports
import requests

# local imports
from models import User
from utils import print_yellow, print_red, ITALIC, RESET
from errors import MISSMATCHED_HASH, error_and_exit


def upload_to_wala(file_path: str, wala_url: str, local_hash: str):
    """
    Uploads an image file to a WALA server using HTTP PUT and verifies the returned hash.

    Parameters:
        file_path (str): Path to the image file to be uploaded.
        wala_url (str): Base URL of the WALA server.
        local_hash (str): SHA256 hash of the local file (used for verification).

    Returns:
        tuple:
            - str: Full URL of the uploaded image on the WALA server.
            - None: Placeholder for delete token (not used here).
    """
    # Opens the image file in binary format.
    with open(file_path, 'rb') as f:
        data = f.read() # Reads the file.

    req = Request(
        url=wala_url,
        data=data,
        method='PUT', # PUT, because Wala expects uploads via HTTP PUT.
        headers={"Content-Type": "image/jpg"} # Header: sets Content-Type to application/octet-stream so the server knows it’s dealing with arbitrary binary data.
    )


    with urlopen(req) as response: # Send the request with urlopen(req):
        # Wala server receives the data, computes its SHA256, stores it, and returns that hash in the HTTP response body.
        uploaded_hash = response.read().decode() # Read and decode the response body (a UTF-8 string containing the hash).
        if local_hash != uploaded_hash:
                error_and_exit(MISSMATCHED_HASH)
        new_url = urljoin(wala_url.rstrip('/') + '/', local_hash)
        print(f"{ITALIC}{new_url}{RESET}.")
        
        return new_url, None
    

def upload_to_imgur(file_path: str, client_id: str):
	"""
	Uploads an image to Imgur anonymously using the provided Client ID.

	Parameters:
		file_path (str): Path to the image file to upload.
		client_id (str): Imgur API client ID.

	Returns:
		tuple:
            - str: Full URL of the uploaded image on the WALA server.
            - str: delete hash for the uploaded image.
	"""
	with open(file_path, 'rb') as f:
		image_data = f.read() 

	headers = {"Authorization": f"Client-ID {client_id}"}

	response = requests.post("https://api.imgur.com/3/image", headers=headers, files={"image": image_data})

	if response.status_code != 200: # Print warning and (eventually) fallback to original image URL.
		print_yellow(f"\nWarning: [Imgur Upload Failed] {response.status_code}: {response.text.strip()}")
		return None, None

	data = response.json()["data"]
	new_url = data["link"]
	delete_token = data["deletehash"]
	print(f"{ITALIC}{new_url}{RESET}.")
 
	return new_url, delete_token


def upload_image(file_path: str, user: User, img_hash: str):
    """Uploads an image to the specified hosting service (WALA or Imgur) and returns the URL.
    Returns a tuple of the URL and the delete token (if applicable)."""
    print("...and uploading it to ", end="")
    if user.image_host == "wala":
        try:
            return upload_to_wala(file_path, user.wala_url, img_hash)
        except Exception as e:
            print_red(f"\nError: Failed to upload image to {user.wala_url}: {e}")
            raise SystemExit(1)
        
    elif user.image_host == "imgur":
        try:
            return upload_to_imgur(file_path, user.imgur_client_id)
        except Exception as e:
            print_red(f"\nError: Failed to upload image to Imgur: {e}")
            raise SystemExit(1)
        
    else: 
        return None, None
