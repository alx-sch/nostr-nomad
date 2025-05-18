""" build_post_shortform.py

Handles the construction of long-form Nostr events from Substack-style posts.

This module extracts plain text and image URLs from HTML content,
prepends optional title and subtitle, and sets up the post object
for a short-form Nostr event (kind 1).
"""

# external imports
from bs4 import BeautifulSoup

# local imports
from models import Post


def html_to_text(content: BeautifulSoup) -> str:
    """Extracts readable text and image URLs from an BeautifulSoup object.
    Converts headings and paragraph content into plain text and includes image URLs inline.
    Skips button-style links."""
    result = []

    text_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']

    for element in content.find_all(text_tags + ['img']):
        if element.name == 'p' and element.find('a', class_='button'):
            continue
        if element.name == 'img':
            image_url = element.get('src')
            if image_url:
                result.append(image_url)
        elif element.name in text_tags:
            result.append(element.get_text(strip=True))

    return "\n\n".join(result)


def add_titles(message: str, title: str, subtitle: str) -> str:
    """Prepends the title and subtitle to the message body.s
    Title is wrapped in brackets and appears at the top. Subtitle appears below it if present."""
    if subtitle:
        message = f"{subtitle}\n\n{message}"
    if title:
        message = f"[{title}]\n{message}"
    return (message)


def build_shortform(post: Post, html_content: BeautifulSoup):
    """Prepares the post for a Nostr short-form event (kind 1).
    Extracts readable text from HTML, prepends title/subtitle, and assigns the correct event kind."""
    message = html_to_text(html_content)
    post.content = add_titles(message, post.title, post.subtitle)
    post.kind = 1
