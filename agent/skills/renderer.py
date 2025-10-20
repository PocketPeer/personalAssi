import re
from typing import Dict
from .loader import SkillLoader


class SkillsRenderer:
    def __init__(self, loader: SkillLoader) -> None:
        self.loader = loader

    def render(self, name: str, context: Dict[str, str]) -> str:
        template = self.loader.load(name)
        def replace(match: re.Match) -> str:
            key = match.group(1).strip()
            return str(context.get(key, ""))
        return re.sub(r"\{\{\s*(.*?)\s*\}\}", replace, template)
