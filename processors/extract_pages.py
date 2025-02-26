import xml.etree.ElementTree as ET
import re

def extract_person_pages(html_path):
    namespaces = {'mediawiki': 'http://www.mediawiki.org/xml/export-0.11/'}

    with open(html_path, "r", encoding="utf-8") as file:
        context = ET.iterparse(file, events=("start", "end"))

        for event, elem in context:
            if event == "end" and elem.tag == f"{{{namespaces['mediawiki']}}}page":
                title = ""
                text = ""

                for child in elem:
                    if child.tag == f"{{{namespaces['mediawiki']}}}title":
                        title = child.text
                    elif child.tag == f"{{{namespaces['mediawiki']}}}revision":
                        for subchild in child:
                            if subchild.tag == f"{{{namespaces['mediawiki']}}}text":
                                text = subchild.text

                if text and re.search(r"birth_date", text):
                    print(f"Extracted {title}")
                    yield {
                        'title': title,
                        'content': text
                    }

                elem.clear()

def extract_pages_spark(file_path):
    return [(file_path, p["title"], p["content"]) for p in extract_person_pages(file_path)]