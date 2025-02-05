import xml.etree.ElementTree as ET
import re

def extract_person_pages(html_path):
    namespaces = {'mediawiki': 'http://www.mediawiki.org/xml/export-0.11/'}
    result = []

    with open(html_path, "r", encoding="utf-8") as file:
        context = ET.iterparse(file, events=("start", "end"))

        i = 0
        for event, elem in context:
            if i > 0:
                break
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

                if text:
                    if re.search(r"birth_date", text):
                        result.append({
                            'title': title,
                            'content': text
                        })
                        print(f"Extracted {title}")
                        i += 1

                elem.clear()
    print(result)
    return result

extract_person_pages("sample_html/enwiki-20241101-pages-articles-multistream1.xml")