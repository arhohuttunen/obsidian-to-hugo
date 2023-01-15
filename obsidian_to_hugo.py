import os
import shutil

from callout_processor import CalloutProcessor
from image_processor import ImageProcessor
from tweet_processor import TweetProcessor
from wiki_link_processor import WikiLinkProcessor
from youtube_link_processor import YoutubeLinkProcessor


class ObsidianToHugo:
    def __init__(
        self,
        obsidian_vault_dir: str,
        hugo_dir: str,
    ) -> None:
        self.obsidian_vault_dir = obsidian_vault_dir
        self.hugo_content_dir = f"{hugo_dir}/content/post"
        self.hugo_media_dir = f"{hugo_dir}/assets/media"
        self.processors = [
            WikiLinkProcessor(),
            YoutubeLinkProcessor(),
            ImageProcessor(),
            TweetProcessor(),
            CalloutProcessor()
        ]

    def process(self) -> None:
        self.copy_obsidian_vault_to_hugo_content_dir()
        self.copy_obsidian_vault_to_hugo_media_dir()
        self.process_content()


    def copy_obsidian_vault_to_hugo_content_dir(self) -> None:
        shutil.copytree(self.obsidian_vault_dir, self.hugo_content_dir, ignore=shutil.ignore_patterns(".obsidian", "_*"), dirs_exist_ok=True)

    def copy_obsidian_vault_to_hugo_media_dir(self) -> None:
        shutil.copytree(f"{self.obsidian_vault_dir}/_media", self.hugo_media_dir, dirs_exist_ok=True)

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
