import re


def clean_text(text: str) -> str:
    # 1. Remove page delimiters
    text = text.replace("-----This is the end of the page-----", " ")

    # 2. Remove repeated headers/footers (customize patterns)
    patterns = [
        r"JPMorgan Chase.*?\n",
        r"Page \d+ of \d+",
        r"\n\d+\n",
        r"4/17/26, 7:32 PM",
        r"jpm-20251231",
        r"https\S+"

    ]
    for p in patterns:
        text = re.sub(p, " ", text, flags=re.IGNORECASE)

    # 3. Remove excessive newlines
    text = re.sub(r"\n{2,}", "\n", text)

    # 4. Remove very short/noisy lines
    lines = text.split("\n")
    cleaned_lines = [line.strip() for line in lines if len(line.strip()) > 30]
    text = "\n".join(cleaned_lines)

    # 5. Normalize spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()
