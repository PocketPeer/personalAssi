from pathlib import Path
from typing import Dict


class SkillLoader:
    def __init__(self, base_dir: str = "agent/skills") -> None:
        self.base_dir = Path(base_dir)

    def load(self, name: str) -> str:
        # name like "morning_brief" -> morning_brief.skill.md
        path = self.base_dir / f"{name}.skill.md"
        if not path.exists():
            raise FileNotFoundError(f"Skill template not found: {path}")
        return path.read_text(encoding="utf-8")
