import re
from dataclasses import dataclass

from typing import List


@dataclass
class YoutubeLink:
    youtube_link: str
    video_id: str

    def build_hugo_markdown(self):
        return f'{{{{< youtube {self.video_id} >}}}}\n<br/>'


def get_youtube_links(text: str) -> List[YoutubeLink]:
    youtube_links = []
    youtube_links_regex = r"https?:\/\/(?:www\.)?youtube\.com\/watch\?v=(.*)"
    for match in re.finditer(youtube_links_regex, text):
        youtube_link = YoutubeLink(match.group(), match.group(1))
        youtube_links.append(youtube_link)
    return youtube_links


def replace_youtube_links(text: str) -> str:
    links = get_youtube_links(text)
    for link in links:
        text = text.replace(link.youtube_link, link.build_hugo_markdown())
    return text
