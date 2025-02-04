import xml.etree.ElementTree as ET
import re

def extract_person_pages(dump_file, output_dir):
    # Define the namespace to handle properly
    namespaces = {'mediawiki': 'http://www.mediawiki.org/xml/export-0.11/'}

    # Parse the XML dump file
    with open(dump_file, "r", encoding="utf-8") as file:
        context = ET.iterparse(file, events=("start", "end"))

        # Iterate through the XML elements
        for event, elem in context:
            if event == "end" and elem.tag == f"{{{namespaces['mediawiki']}}}page":
                # Extract title and text content
                title = ""
                text = ""

                for child in elem:
                    if child.tag == f"{{{namespaces['mediawiki']}}}title":
                        title = child.text
                    elif child.tag == f"{{{namespaces['mediawiki']}}}revision":
                        for subchild in child:
                            if subchild.tag == f"{{{namespaces['mediawiki']}}}text":
                                text = subchild.text

                # Check if the text contains "nationality" in a person-like context
                if text:
                    # Look for "nationality" with personal data context, e.g., in infobox
                    if re.search(r"(\|.*nationality.*=\s*\[\[.*\]\])", text, re.IGNORECASE):
                        # Save the content if it's a person page
                        file_name = f"{output_dir}/{title.replace(' ', '_')}.txt"
                        with open(file_name, "w", encoding="utf-8") as out_file:
                            out_file.write(f"Title: {title}\n")
                            out_file.write(f"Content:\n{text}")
                        print(f"Saved {title} to {file_name}")

                # Reset for next page
                elem.clear()


# Example usage
dump_file = "sample_html/enwiki-20241101-pages-articles-multistream5.xml-p558392p958045"  # Path to your XML file
output_dir = "person_pages"  # Directory to save the extracted person pages

# Create output directory if it doesn't exist
import os
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Call the function to process the dump file
extract_person_pages(dump_file, output_dir)
