import re
from dataclasses import dataclass

from typing import List

from obsidian_processor import ObsidianProcessor, ObsidianElement


@dataclass
class Callout(ObsidianElement):
    matched_text: str
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


class CalloutProcessor(ObsidianProcessor):
    def get_elements(self, text: str) -> List[Callout]:
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
