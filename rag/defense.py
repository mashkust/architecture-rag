"""Защита RAG-бота от prompt injection и утечки вредоносных строк."""

import re

INJECTION_PATTERNS = [
    r"ignore all instructions",
    r"ignore (all|any|the) (previous|prior) instructions",
    r"disregard (all|the|previous)",
    r"system prompt",
    r"forget (everything|all)",
    r"output\s*:",
]

SECRET_PATTERNS = [
    r"swordfish",
    r"root\s*:",
    r"password\s*[:=]",
    r"superpassword",
    r"суперпароль",
]

REFUSAL = "I don't know."


def sanitize_context(text: str) -> str:
    lines = text.splitlines()
    clean = []
    for line in lines:
        if any(re.search(pattern, line, re.IGNORECASE) for pattern in INJECTION_PATTERNS):
            continue
        clean.append(line)
    return "\n".join(clean)


def guard_output(answer: str) -> str:
    if any(re.search(pattern, answer, re.IGNORECASE) for pattern in SECRET_PATTERNS):
        return REFUSAL
    return answer
