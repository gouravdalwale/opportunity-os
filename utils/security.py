INJECTION_PATTERNS = [
    "ignore previous instructions",
    "ignore all previous instructions",
    "system prompt",
    "developer message",
    "reveal your prompt",
    "reveal system prompt",
    "bypass safety",
    "jailbreak",
    "act as the system",
    "forget your instructions",
]

def contains_prompt_injection(text: str) -> bool:
    text = text.lower()

    return any(pattern in text for pattern in INJECTION_PATTERNS)