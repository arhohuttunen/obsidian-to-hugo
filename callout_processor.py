import re
from dataclasses import dataclass

from typing import List


@dataclass
class Callout:
    callout: str
    type: str
    title: str
    lines: [str]

    def build_hugo_markdown(self):
        markdown = f'{{{{% callout {self.type} %}}}}\n'
        if self.title != '':
            markdown += f'**{self.title}**\n'
        for line in self.lines:
            markdown += line + '\n'
        markdown += f'{{{{% /callout %}}}}\n'
        return markdown


def get_callouts(text: str) -> List[Callout]:
    callouts = []
    callouts_regex = r"\>\[!(.*)\]\s*(.*)?\n(?:\>.*\n)*"
    for match in re.finditer(callouts_regex, text):
        callout = match.group()
        lines = []
        line_regex = r"\>(.*)\n"
        for inner in re.finditer(line_regex, callout):
            lines.append(inner.group(1))
        first = lines.pop(0)
        title_regex = r"\[!(?:.*)\]\s*(.*)?"
        title = re.match(title_regex, first)

        callout = Callout(match.group(), match.group(1), title.group(1), lines)
        callouts.append(callout)
    return callouts


def replace_callouts(text: str) -> str:
    callouts = get_callouts(text)
    for callout in callouts:
        text = text.replace(callout.callout, callout.build_hugo_markdown())
    return text
