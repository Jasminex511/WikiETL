import re

def extract_infobox(text):
    stack = []
    start_idx = text.find("{{Infobox officeholder")
    if start_idx == -1:
        return None
    idx = start_idx
    while idx < len(text):
        if text[idx:idx + 2] == "{{":
            stack.append("{{")
            idx += 2
        elif text[idx:idx + 2] == "}}":
            stack.pop()
            idx += 2
            if not stack:
                return text[start_idx:idx]
        else:
            idx += 1
    return None

def extract_fields(infobox_content):
    if not infobox_content:
        return None

    profile = {
        "Name": re.search(r"\|name\s*=\s*(.+)", infobox_content).group(1).strip() if re.search(r"\|name\s*=\s*(.+)", infobox_content) else None,
        "Birthday": re.search(r"\|birth_date\s*=\s*\{\{Birth date and age\|(\d+\|\d+\|\d+)", infobox_content).group(1).replace("|", "-") if re.search(r"\|birth_date\s*=\s*\{\{Birth date and age\|(\d+\|\d+\|\d+)", infobox_content) else None,
        "Nationality": re.search(r"\|nationality\s*=\s*\[\[(.+?)\]\]", infobox_content).group(1).strip() if re.search(r"\|nationality\s*=\s*\[\[(.+?)\]\]", infobox_content) else None,
        "Keywords": [m.strip() for m in re.findall(r"\|occupation\s*=\s*\{\{hlist\|(.+?)\}\}", infobox_content)[0].split("|")] if re.findall(r"\|occupation\s*=\s*\{\{hlist\|(.+?)\}\}", infobox_content) else None,
        "Spouse": re.search(r"\|spouse\s*=\s+\{\{marriage\|\[\[.*?\|(.+?)\]\]", infobox_content).group(1).strip() if re.search(r"\|spouse\s*=\s+\{\{marriage\|\[\[.*?\|(.+?)\]\]", infobox_content) else None
    }
    return profile

def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text_content = file.read()

    infobox_content = extract_infobox(text_content)
    if not infobox_content:
        print("Infobox not found.")
        return None

    print("Extracted Infobox:\n", infobox_content)

    profile = extract_fields(infobox_content)
    return profile
