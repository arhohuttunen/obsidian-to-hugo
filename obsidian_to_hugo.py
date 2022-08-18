import os
import shutil
from distutils.dir_util import copy_tree

from callout_processor import CalloutProcessor
from image_processor import ImageProcessor
from tweet_processor import TweetProcessor
from wiki_link_processor import WikiLinkProcessor
from youtube_link_processor import YoutubeLinkProcessor


class ObsidianToHugo:
    def __init__(
        self,
        obsidian_vault_dir: str,
        hugo_content_dir: str,
    ) -> None:
        self.obsidian_vault_dir = obsidian_vault_dir
        self.hugo_content_dir = hugo_content_dir
        self.processors = [
            WikiLinkProcessor(),
            YoutubeLinkProcessor(),
            ImageProcessor(),
            TweetProcessor(),
            CalloutProcessor()
        ]

    def process(self) -> None:
        self.clear_hugo_content_dir()
        self.copy_obsidian_vault_to_hugo_content_dir()
        self.process_content()

    def clear_hugo_content_dir(self) -> None:
        shutil.rmtree(self.hugo_content_dir)
        os.mkdir(self.hugo_content_dir)

    def copy_obsidian_vault_to_hugo_content_dir(self) -> None:
        copy_tree(self.obsidian_vault_dir, self.hugo_content_dir)
        # We don't want to have the .obsidian folder in the hugo content directory.
        if os.path.isdir(os.path.join(self.hugo_content_dir, ".obsidian")):
            shutil.rmtree(os.path.join(self.hugo_content_dir, ".obsidian"))

    def process_content(self) -> None:
        for root, dirs, files in os.walk(self.hugo_content_dir):
            for file in files:
                if file.endswith(".md"):
                    with open(os.path.join(root, file), "r") as f:
                        text = f.read()
                    for processor in self.processors:
                        text = processor.replace_elements(text)
                    with open(os.path.join(root, file), "w") as f:
                        f.write(text)
