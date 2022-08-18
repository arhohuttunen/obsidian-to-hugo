import re
from dataclasses import dataclass

from typing import List

from obsidian_processor import ObsidianElement, ObsidianProcessor


@dataclass
class YoutubeLink(ObsidianElement):
    matched_text: str
    video_id: str

    def build_hugo_markdown(self):
        return f'{{{{< youtube {self.video_id} >}}}}\n<br/>'


class YoutubeLinkProcessor(ObsidianProcessor):
    def get_elements(self, text: str) -> List[YoutubeLink]:
        youtube_links = []
        youtube_links_regex = r"https?:\/\/(?:www\.)?youtube\.com\/watch\?v=(.*)"
        for match in re.finditer(youtube_links_regex, text):
            youtube_link = YoutubeLink(match.group(), match.group(1))
            youtube_links.append(youtube_link)
        return youtube_links
