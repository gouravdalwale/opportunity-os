from utils.gemini import ask_roadmap_gemini
from utils.skill_loader import load_skill


def generate_roadmap(context):

    skill = load_skill("skills/roadmap/SKILL.md")

    prompt = f"""
{skill}

----------------------------------------
CONTEXT
----------------------------------------

{context}

----------------------------------------
TASK
----------------------------------------

Generate a personalized 30-day roadmap according to your skill definition.
"""

    return ask_roadmap_gemini(prompt)