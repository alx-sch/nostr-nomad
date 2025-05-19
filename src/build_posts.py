"""build_posts.py

Module for building Post objects from Substack export data.

This script reads metadata from a posts.csv file and corresponding HTML content files,
removes duplicated image URLs, builds Post objects, processes images (including optional
upload to new image hosts), and constructs either short-form or long-form content depending
on the user's chosen event type.

Functions:
- build_posts: Main entry point for parsing and building posts.
- get_html_content: Retrieves and cleans HTML content for each post.
- remove_img_duplicate: Cleans HTML by unwrapping <a> tags around images.
"""

# standard imports
import os
import csv

# external imports
from bs4 import BeautifulSoup

# local imports
import imgs
from models import Post, Paths, User
from build_post_shortform import build_shortform
from build_post_longform import build_longform
from errors import EMPTY_HTML_FILES, MISMATCHED_POST_DATA, error_and_exit


def remove_img_duplicate(soup: BeautifulSoup) -> BeautifulSoup:
    """Removes <a> tags around images to avoid duplicated image URLs in Substack exports."""
    if soup is None:
        raise ValueError("soup cannot be None")
    for a in soup.find_all("a"):
        href = a.get("href")
        if a.find("img") or (
            href and href.endswith((".jpg", ".jpeg", ".png", ".webp", ".avif"))
        ):
            a.unwrap()  # Removes the <a> tag but keeps the content (like <img>)
    return soup


def get_html_content(paths: Paths, post_id: str) -> BeautifulSoup:
    """Extracts content from HTML files and removes duplicated image URLs.

    Raises an error if:
    - Any HTML file is empty.
    - The HTML file matching the post_id isn't found.
    """
    for item in paths.html_files:
        if post_id in item:
            with open(item, "r", encoding="utf-8") as file:
                content = file.read()
                if not content:
                    error_and_exit(EMPTY_HTML_FILES)
                soup = remove_img_duplicate(BeautifulSoup(content, "html.parser"))
                return soup

    error_and_exit(
        MISMATCHED_POST_DATA
    )  # If html files don't match with the posts.csv-file, throws an error and exits.


def build_posts(paths: Paths, user: User):
    """Parses posts.csv, extracts metadata, builds Post objects, and processes them."""
    posts: list[Post] = []
    count_imgs = [0, 0]
    count_built = 0

    # Create the cache directory for post conent
    download_dir = os.path.join(paths.cache_root, "posts")
    os.makedirs(download_dir, exist_ok=True)

    with open(paths.posts_csv, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader, None)  # Skips CSV header.

        for line in reader:
            tmp_html_content = get_html_content(paths, line[0])

            post = Post(
                post_id=line[0],
                d_tag=line[0].split(".")[0] + ".nostr-nomad",
                post_date=line[1],
                is_published=(line[2].lower() == "true"),
                title=line[7],
                subtitle=line[8],
                html_content=tmp_html_content,
            )

            if post.is_published:
                imgs.handle_imgs(
                    paths, post, user, count_imgs
                )  # Downloads images to cache and uploads them to the new image host.
                if user.event_type == "blog":
                    build_longform(post, str(post.html_content))
                else:
                    if post.html_content is None:
                       raise ValueError("soup cannot be None")
                    build_shortform(post, post.html_content)
                    # Save post content to a file
                content_file = os.path.join(download_dir, f"{post.post_id}.txt")
                with open(content_file, "w", encoding="utf-8") as f:
                    f.write(post.content)
                count_built += 1
                posts.append(post)

        # Prints out the number of images downloaded/uploaded and posts built.
        if count_imgs[0] > 0:
            print("")

        if count_imgs[0] > 0:
            print(f"⬇️  Downloaded {count_imgs[0]} image(s) to cache.")
            if user.image_host == "substack" or count_imgs[1] == 0:
                print("")

        if user.image_host != "substack" and count_imgs[1] > 0:
            print(f"⬆️  Uploaded {count_imgs[1]} image(s) to ", end="")
            if user.image_host == "wala":
                print(f"{user.wala_url}.\n")
            elif user.image_host == "imgur":
                print("Imgur.\n")

        if count_built > 0:
            print(f"🛠️  Built {count_built} ", end="")
            if user.event_type == "blog":
                print("long-form post(s) for publishing to Nostr.")
            else:
                print("short-form post(s) for publishing to Nostr.")
            print("\n=====================================================\n")

        return posts
