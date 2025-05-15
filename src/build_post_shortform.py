# external imports
from bs4 import BeautifulSoup

# local imports
from models import Posts


def html_to_text(content: BeautifulSoup) -> str:
    """Extracts readable text and image URLs from an BeautifulSoup object."""
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
    """Adds title and subtitle to the beginning of a message."""
    if subtitle:
        message = f"{subtitle}\n\n{message}"
    if title:
        message = f"[{title}]\n{message}"
    return (message)


def build_shortform(post: Posts, html_content: BeautifulSoup):
    """Adds the correct content format (plaintext message with title and subtitle if available)
    and event kind for a shortform event."""
    message = html_to_text(html_content)
    post.content = add_titles(message, post.title, post.subtitle)
    post.kind = 1
