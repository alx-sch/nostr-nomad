""" imgs.py

Handles image extraction, downloading, caching, uploading, and URL replacement 
for posts containing HTML content.

Main functionalities:
- Extract image URLs from post HTML.
- Download images to local cache if not already cached.
- Upload images to remote hosting (e.g., WALA or Imgur).
- Replace image URLs in post HTML content for long-form posts.
- Maintain a cache to avoid redundant downloads and uploads.
"""

# standard imports
import os
from io import BytesIO
from urllib.request import urlopen
from urllib.parse import urlparse

# external imports
from bs4 import BeautifulSoup
from PIL import Image, UnidentifiedImageError
import pillow_avif # Pillow plugin for AVIF support, keep it

# local imports
from models import Post, Paths, User
from imgs_uploader import upload_image
from utils import (
    sha256_hash,
    load_cache, 
    save_cache,
    print_yellow,
    ITALIC,
    RESET
)


def replace_img_urls(post: Post, new_url: str, index: int):
    """
    Replaces the `src` of the <img> tag at the given index in post HTML content
    with a new URL, while preserving alt, width, height, and style attributes.

    Parameters:
        post (Post): The post object containing HTML content.
        new_url (str): The new image URL to set.
        index (int): The index of the <img> tag to update.
    """

    # Makes a temp soup based on current html content.
    soup = BeautifulSoup(str(post.html_content), "html.parser") 

    # Find all <img> tags and select the one at the specified index
    img_tags = soup.find_all("img")
    if 0 <= index < len(img_tags): # If index is within img_tags range.
        img = img_tags[index] # Picks the right image - corresponding to the correct URL.

        # Extracts original image attributes, or sets to empty if nothing there.
        alt = img.get("alt", "")
        width = img.get("width", "")
        height = img.get("height", "")
        style = img.get("style", "display: block; max-width: 100%; height: auto;")

        # Clear original attributes and set new values with new URL.
        img.attrs = {
            "src": new_url,
            "alt": alt,
            "width": width,
            "height": height,
            "style": style,
        }

    post.html_content = soup # Updates html_content with the new image attributes.


def get_ext_from_url(url):
    """ Extracts the file extension from a URL.
    If the extension is not one of the common image formats, defaults to '.jpg'."""
    path = urlparse(url).path
    ext = os.path.splitext(path)[1].lower()
    if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.avif']:
        return ext
    return '.jpg'


def should_upload(user: User, image_format: str):
    """ Determines if an image should be uploaded based on the user's image host
    and the image format."""
    if user.image_host == "substack":
        return False
    if user.image_host == "wala":
        return True 
    if user.image_host == "imgur":
        return (image_format.upper() in ['JPEG', 'PNG', 'GIF'])
    
    
def download_image_data(url: str) -> bytes:
    """ Downloads image data from a URL and returns it as bytes."""
    print(f"Downloading image from {ITALIC}{url}{RESET}...")
    with urlopen(url) as response:
        return response.read()


def download_images(paths: Paths, post: Post, user: User, url: str, i: int, cache: dict):
    """
    Downloads an image from a URL, converts format if needed, and returns path and status flags.

    Returns:
        tuple: (filepath (str), downloaded (bool), uploadable (bool))
    """      
    download_dir = os.path.join(paths.cache_root, "images")
    os.makedirs(download_dir, exist_ok=True)
    
    ext = get_ext_from_url(url)
    if ext == '.jpeg':
        ext = '.jpg' # same same, just to standardize
    
    filename = f"{post.post_id}_{i}{ext}"
    filepath = os.path.join(download_dir, filename)
    
    # Check if the image is already cached; checking like this as extensuion might be different.
    for k in cache.keys():
        if os.path.splitext(k)[0] == f"{post.post_id}_{i}":
            return None, False, False
        
    img_data = download_image_data(url)
    
    try:
        image = Image.open(BytesIO(img_data))
        orig_format = image.format
    except UnidentifiedImageError:
        # Save raw bytes anyway
        with open(filepath, "wb") as f:
            f.write(img_data)
        if (user.image_host == "imgur"):    
            print_yellow(f"Warning: Image format not supported for rehosting: {filename}. Using original URL.\n")
        uploadable = should_upload(user, 'UNKNOWN')
        return (filepath, True, uploadable)
    
    # Determine final format
    if user.image_host == "imgur":
        if orig_format.upper() not in ['JPEG', 'PNG', 'GIF']: # Imgur does not support AVIF, WEBP, ...
            image = image.convert('RGB')
            final_ext = '.jpg'
            final_format = 'JPEG'
        else:
            final_ext = ext
            final_format = orig_format.upper()
    else: # if no upload ("substack") or no limiting format ("wala"), use existing format
        final_ext = ext
        final_format = orig_format.upper()
        
    filename = f"{post.post_id}_{i}{final_ext}"
    filepath = os.path.join(download_dir, filename)
    
    image.save(filepath, final_format)
    uploadable = should_upload(user, final_format)
        
    return (filepath, True, uploadable)


def	extract_image_urls(paths: Paths, post: Post):
    """
    Extracts all image URLs from a post's HTML content and stores them in the post and paths objects.

    Parameters:
        paths (Paths): Object containing image_urls list to collect URLs globally.
        post (Post): Post object with html_content and image_urls list.
    """
    img_tags = post.html_content.find_all("img")  # Find all <img> tags in the HTML content.

    for img in img_tags:
        src = img.get("src")  # Get the 'src' attribute of each <img> tag.
        if src: # Only add if src attribute exists and is not empty.
            post.image_urls.append(src)
            paths.image_urls.append(src)


def handle_imgs(paths: Paths, post: Post, user: User, counts: list[int]):
    """
    Downloads images, and if applicable, uploads them to a new hosting servers
    and updates image URLs in the post accordingly.
    Uses a cache to avoid redundant downloads and uploads.

    Parameters:
        paths (Paths): Paths object with cache locations.
        post (Post): Post object containing HTML content and image metadata.
        user (User): User object with event_type and hosting server info.
        counts (list[int, int]): List tracking counts of downloaded/uploaded images.
    """
    new_url = None
    extract_image_urls(paths, post)
    urls = post.image_urls
    cache = load_cache(paths.cache_imgs)
    
    # Download images from the URLs and uploads them to new hosting server, if applicable.
    for i, url in enumerate(urls): 
        filepath, downloaded, uploadable = download_images(paths, post, user, url, i, cache)
        if not filepath: # If the image is already cached, skip to the next one.
            continue
        filename = os.path.basename(filepath)
        local_hash = sha256_hash(filepath)
        if filename not in cache:
            cache[filename] = {
                "ori_url": url,
                "new_url": None,
                "delete_token": None,
                "local_hash": local_hash
            }
  
        if downloaded: 
            counts[0] += 1
            
        if (uploadable and local_hash not in post.image_hashes):
            new_url, delete_token = upload_image(filepath, user, local_hash)
            if not new_url:
                print_yellow(f"→ Image upload failed for {filename}. Using original URL.")
                counts[1] -= 1
            cache[filename]["new_url"] = new_url
            cache[filename]["delete_token"] = delete_token
            counts[1] += 1
        post.image_hashes.append(local_hash)
 
        if (new_url):
            replace_img_urls(post, new_url, i) # Replaces the old image url of the content to point to the new URL.
            post.new_image_urls.append(new_url) # Adds to the list of the new image urls.

    save_cache(paths.cache_imgs, cache)   # Save the updated cache
