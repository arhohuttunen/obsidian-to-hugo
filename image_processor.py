import re
from dataclasses import dataclass

from typing import List

from obsidian_processor import ObsidianElement, ObsidianProcessor


@dataclass
class Image(ObsidianElement):
    matched_text: str
    caption: str
    file: str

    def build_hugo_markdown(self):
        return f'{{{{< figure src="{self.file}" caption="{self.caption}" theme="light" >}}}}'


class ImageProcessor(ObsidianProcessor):
    def get_elements(self, text: str) -> List[ObsidianElement]:
        twitter_links = []
        twitter_links_regex = r"!\[(.*)\]\((.*)\)"
        for match in re.finditer(twitter_links_regex, text):
            image = Image(match.group(), match.group(1), match.group(2))
            twitter_links.append(image)
        return twitter_links
