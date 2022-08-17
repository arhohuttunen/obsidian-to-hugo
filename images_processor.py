import re
from dataclasses import dataclass

from typing import List


@dataclass
class Image:
    image: str
    caption: str
    file: str

    def build_hugo_markdown(self):
        return f'{{{{< figure src="{self.file}" caption="{self.caption}" theme="light" >}}}}'


def get_images(text: str) -> List[Image]:
    twitter_links = []
    twitter_links_regex = r"!\[(.*)\]\((.*)\)"
    for match in re.finditer(twitter_links_regex, text):
        image = Image(match.group(), match.group(1), match.group(2))
        twitter_links.append(image)
    return twitter_links


def replace_images(text: str) -> str:
    images = get_images(text)
    for image in images:
        text = text.replace(image.image, image.build_hugo_markdown())
    return text
