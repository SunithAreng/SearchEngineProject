import random
from faker import Faker
import xml.etree.ElementTree as ET

fake = Faker()

def generate_long_text():
    # Generate a longer text with multiple paragraphs
    paragraphs = [fake.paragraph() for _ in range(5)]  # Adjust the number of paragraphs as needed
    return ' '.join(paragraphs)


def generate_xml_doc():
    doc = ET.Element('DOC')

    date_part = fake.date_between(start_date='-10y', end_date='today')
    random_part = fake.random_number(4)

    docno = ET.SubElement(doc, 'DOCNO')
    docno.text = f"QA{date_part.strftime('%m%d%y')}-{random_part}"

    docid = ET.SubElement(doc, 'DOCID')
    docid.text = str(random_part)

    date = ET.SubElement(doc, 'DATE')
    date_p = ET.SubElement(date, 'P')
    date_p.text = date_part.strftime('%B %d, %Y, %A, Home Edition')

    section = ET.SubElement(doc, 'SECTION')
    section_p = ET.SubElement(section, 'P')
    section_p.text = fake.random_element(['Politics', 'Business', 'Technology', 'Entertainment', 'Sports'])

    length = ET.SubElement(doc, 'LENGTH')
    length_p = ET.SubElement(length, 'P')
    length_p.text = f"{fake.random_number(2)} words"

    headline = ET.SubElement(doc, 'HEADLINE')
    headline_p = ET.SubElement(headline, 'P')
    headline_p.text = fake.sentence()

    text = ET.SubElement(doc, 'TEXT')
    text_p = ET.SubElement(text, 'P')
    text_p.text = generate_long_text()

    type_elem = ET.SubElement(doc, 'TYPE')
    type_p = ET.SubElement(type_elem, 'P')
    type_p.text = fake.random_element(['News', 'Opinion', 'Analysis'])

    xml_content = ET.tostring(doc, encoding='utf-8').decode('utf-8')
    return xml_content.replace('<P>', '<P>\n').replace('</P>', '\n</P>').replace('><', '>\n<').replace('</DOC>', '</DOC>\n')


# Generate and append 100 XML documents to a single file
with open("qatimes", "w", encoding="utf-8") as file:
    for i in range(1, 10001):
        xml_content = generate_xml_doc()
        file.write(xml_content)
