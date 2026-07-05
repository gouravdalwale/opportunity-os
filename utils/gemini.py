print("🔥 LOADED utils/gemini.py FROM GROQ VERSION")
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

profile_client = Groq(api_key=os.getenv("PROFILE_API_KEY"))
opportunity_client = Groq(api_key=os.getenv("OPPORTUNITY_API_KEY"))
roadmap_client = Groq(api_key=os.getenv("ROADMAP_API_KEY"))

MODEL = "openai/gpt-oss-120b"


def ask_profile_gemini(prompt):
    try:
        print("🔥 USING GROQ")
        response = profile_client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Error: {str(e)}"


def ask_opportunity_gemini(prompt):
    try:
        print("🔥 USING GROQ")
        response = opportunity_client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Error: {str(e)}"


def ask_opportunity_gemini_with_tools(prompt, tools=None):
    """
    Query the Opportunity model with optional function tool schemas.
    Returns the full message choice to handle potential tool calls.
    """
    try:
        print("🔥 USING GROQ WITH TOOLS")
        kwargs = {
            "model": MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
        }
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"
            
        response = opportunity_client.chat.completions.create(**kwargs)
        return response.choices[0].message

    except Exception as e:
        print(f"❌ Error in ask_opportunity_gemini_with_tools: {str(e)}")
        raise e


def ask_roadmap_gemini(prompt):
    try:
        print("🔥 USING GROQ")
        response = roadmap_client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Error: {str(e)}"