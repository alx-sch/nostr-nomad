# standard imports
import os
from dataclasses import dataclass

# external imports
from bs4 import BeautifulSoup


@dataclass
class PlaintextBuilder:
    title_map: dict

    def build_message(self, file_path: str):
        post_id = os.path.basename(file_path).split('.')[0]
        message = self.html_to_text(file_path)
        
        if post_id in self.title_map:
            title = self.title_map[post_id]['title']
            subtitle = self.title_map[post_id]['subtitle']
        else:
            title = ''
            subtitle = ''
            
        message = self.add_titles(message, title, subtitle)
        return {post_id: message}


    def html_to_text(self, file_path: str):
        with open(file_path, 'r', encoding = 'utf-8') as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, 'html.parser')
        result = []

        text_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']

        for element in soup.find_all(text_tags + ['img']):
            if element.name == 'p' and element.find('a', class_='button'):
                continue
            if element.name == 'img':
                image_url = element.get('src')
                if image_url:
                    result.append(image_url)
            elif element.name in text_tags:
                result.append(element.get_text(strip=True))

        return "\n\n".join(result)


    def add_titles(self, message: str, title: str, subtitle: str):
        if subtitle:
            message = f"{subtitle}\n\n{message}"
        if title:
            message = f"[{title}]\n{message}"
        return message

## ADD BUILDER FOR MARDOWN MSGS ##
