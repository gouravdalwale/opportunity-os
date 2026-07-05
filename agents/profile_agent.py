from utils.gemini import ask_profile_gemini
from utils.skill_loader import load_skill


def analyze_profile(user_input):

    skill = load_skill("skills/profile/SKILL.md")

    prompt = f"""
{skill}

----------------------------------------
USER PROFILE
----------------------------------------

{user_input}

----------------------------------------
TASK
----------------------------------------

Analyze the profile and generate the structured career profile exactly according to your skill definition.
"""

    return ask_profile_gemini(prompt)