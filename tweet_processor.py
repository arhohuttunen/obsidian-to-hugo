import re
from dataclasses import dataclass

from typing import List

from obsidian_processor import ObsidianElement, ObsidianProcessor


@dataclass
class Tweet(ObsidianElement):
    matched_text: str
    user: str
    tweet_id: str

    def build_hugo_markdown(self):
        return f'{{{{< tweet user="{self.user}" id="{self.tweet_id}" >}}}}'


class TweetProcessor(ObsidianProcessor):
    def get_elements(self, text: str) -> List[Tweet]:
        tweets = []
        tweet_regex = r"https:\/\/twitter\.com\/(.*)\/status\/(.*)"
        for match in re.finditer(tweet_regex, text):
            tweet = Tweet(match.group(), match.group(1), match.group(2))
            tweets.append(tweet)
        return tweets
