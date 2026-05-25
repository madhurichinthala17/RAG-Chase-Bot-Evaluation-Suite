import re

def split_by_sections(text):
    pattern = r"(Item\s+\d+[A-Z]?\..*?)"

    splits = re.split(pattern, text)

    sections = []
    current_section = ""

    for part in splits:
        if re.match(pattern, part):
            if current_section:
                sections.append(current_section)
            current_section = part
        else:
            current_section += part

    if current_section:
        sections.append(current_section)

    return sections
