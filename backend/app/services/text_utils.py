import re


def sentence_case(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text).strip()
    if not text:
        return text
    chars = list(text)
    capitalize_next = True
    for i, ch in enumerate(chars):
        if capitalize_next and ch.isalpha():
            chars[i] = ch.upper()
            capitalize_next = False
        elif ch in ".!?":
            capitalize_next = True
    return "".join(chars)


def split_sentences(text: str) -> list[str]:
    text = re.sub(r"\r\n?", "\n", text)
    sentences = re.split(r"(?<=[.!?。！？])\s+", text.strip())
    return [s.strip() for s in sentences if s.strip()]


def batch_list(items, batch_size: int):
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]
