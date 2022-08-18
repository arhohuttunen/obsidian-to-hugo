from typing import Protocol, List


class ObsidianElement(Protocol):
    matched_text: str

    def build_hugo_markdown(self) -> str:
        pass


class ObsidianProcessor(Protocol):
    def get_elements(self, text: str) -> List[ObsidianElement]:
        pass

    def replace_elements(self, text: str) -> str:
        elements = self.get_elements(text)
        for element in elements:
            text = text.replace(element.matched_text, element.build_hugo_markdown())
        return text
