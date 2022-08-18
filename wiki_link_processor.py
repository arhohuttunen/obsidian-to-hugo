import re
from dataclasses import dataclass

from typing import List

from obsidian_processor import ObsidianElement, ObsidianProcessor


@dataclass
class WikiLink(ObsidianElement):
    matched_text: str
    link: str
    text: str

    def build_hugo_markdown(self):
        return f'[{self.text}](/{self.link})'


class WikiLinkProcessor(ObsidianProcessor):
    def get_elements(self, text: str) -> List[WikiLink]:
        wiki_links = []
        wiki_link_regex = r"\[\[(.*?)\]\]"
        for match in re.finditer(wiki_link_regex, text):
            # check for an alias
            if "|" in match.group(1):
                link, text = match.group(1).split("|")
            else:
                link = match.group(1)
                text = match.group(1)

            # if the link ends with `index` remove it
            if link.endswith("index"):
                link = link[:-5]

            # if the link ends with `_index` remove it
            if link.endswith("_index"):
                link = link[:-6]

            wiki_link = WikiLink(match.group(), link, text)
            wiki_links.append(wiki_link)
        return wiki_links
