"""Keyword-based content filter for post moderation."""

_BAD_WORDS: list[str] = [
    "시발", "씨발", "ㅅㅂ", "ㅆㅂ",
    "병신", "ㅂㅅ",
    "지랄", "ㅈㄹ",
    "개새끼", "개새",
    "꺼져", "닥쳐",
    "미친놈", "미친년",
    "죽어", "뒤져",
    "씹", "좆",
    "느금마", "니엄마",
    "엠창",
    "ㅗ",
]


def check_content(title: str, content: str) -> tuple[bool, str, list[str]]:
    """Check title and content for inappropriate keywords.

    Returns:
        (is_flagged, reason, matched_words)
    """
    text = f"{title} {content}".lower()
    matched: list[str] = []
    for word in _BAD_WORDS:
        if word in text:
            matched.append(word)

    if matched:
        return True, "부적절한 표현이 감지되었습니다", matched
    return False, "", []
