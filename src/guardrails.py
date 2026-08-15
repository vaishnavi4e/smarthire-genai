import re


BLOCKED_PATTERNS = [
    r"\b(password|otp|one[- ]time password)\b",
    r"\b(credit card|cvv|bank account)\b",
    r"\b(hack|malware|virus|ransomware)\b",
]


def check_input(text: str) -> tuple[bool, str]:
    """
    Check user input for unsafe or sensitive requests.
    """

    if not text or not text.strip():
        return False, "Please enter a question or request."

    lowered = text.lower()

    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, lowered):
            return (
                False,
                "I can't help with sensitive credentials, financial "
                "information, or harmful cyber activities."
            )

    return True, "Input accepted."


def sanitize_text(text: str) -> str:
    """
    Remove excessive whitespace from generated/display text.
    """

    return re.sub(r"\s+", " ", text).strip()