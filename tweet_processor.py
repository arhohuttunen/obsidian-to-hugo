import re
from dataclasses import dataclass

from typing import List


@dataclass
class Tweet:
    twitter_link: str
    user: str
    tweet_id: str

    def build_hugo_markdown(self):
        return f'{{{{< tweet user="{self.user}" id="{self.tweet_id}" >}}}}'


def get_tweets(text: str) -> List[Tweet]:
    tweets = []
    tweet_regex = r"https:\/\/twitter\.com\/(.*)\/status\/(.*)"
    for match in re.finditer(tweet_regex, text):
        tweet = Tweet(match.group(), match.group(1), match.group(2))
        tweets.append(tweet)
    return tweets


def replace_tweets(text: str) -> str:
    tweets = get_tweets(text)
    for tweet in tweets:
        text = text.replace(tweet.twitter_link, tweet.build_hugo_markdown())
    return text
