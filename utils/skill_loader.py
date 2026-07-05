from pathlib import Path


def load_skill(skill_path):
    """
    Loads an Agent Skill (SKILL.md)
    """

    with open(
        Path(skill_path),
        "r",
        encoding="utf-8"
    ) as f:

        return f.read()