"""
Utils
"""

import os
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
from saxonche import PySaxonProcessor, PyXdmValue
from werkzeug.utils import secure_filename
from lxml import etree
#import lxml.etree.ElementTree as ET

def transform_to_html(content: str) -> str:
    """
    Transform XML content to HTML using XSLT.
    """
    try:
        # stylesheet = 'SFTI_BIS-BILLING-3.xsl'
        stylesheet = 'Stylesheet_BIS-BILLING-3_Invoice+CreditNote.xsl'
        stylesheet_file = os.path.join(settings.BASE_DIR, 'server/api/ubl/presentation/' + stylesheet)
        # with open(stylesheet_file, 'r', encoding='UTF-8') as file:
            # xml_content = file.read()
            # xslt_root = etree.XML(xml_content.encode())
        xslt_tree = etree.parse(stylesheet_file)
        xslt_root = xslt_tree.getroot()
        transform = etree.XSLT(xslt_root)
        doc = etree.XML(content.encode())
        result = transform(doc)
        # result = etree.tostring(result, pretty_print=True, encoding='UTF-8', xml_declaration=True).decode('UTF-8')
        html = etree.tostring(result.getroot())
        print("hello world")
        return html
    except Exception as e:
        print(f"Error transforming to HTML: {e}")
        return f"<html><body>Error transforming to HTML</body></html>"

def process_by_saxon(proc: PySaxonProcessor, content: str, stylesheet_file: str) -> PyXdmValue:
    """
    Process a file using Saxon-HE.
    """
    # with PySaxonProcessor(license=False) as proc:
    # https://www.saxonica.com/saxon-c/doc12/html/saxonc.html
    xsltproc = proc.new_xslt30_processor()
    document = proc.parse_xml(xml_text=content)
    executable = xsltproc.compile_stylesheet(stylesheet_file=stylesheet_file)
    output = executable.transform_to_string(xdm_node=document)
    output_value: PyXdmValue = executable.transform_to_value(xdm_node=document)
    return (output_value, output)

def validate_peppol(file: InMemoryUploadedFile):
    """
    Validate a Peppol UBL file.
    """
    content_type = file.content_type
    filename = secure_filename(file.name)
    errors = []

    content: str = ''.join(chunk.decode('utf-8') for chunk in file.chunks())      

    with PySaxonProcessor(license=False) as proc:
        stylesheet = 'CEN-EN16931-UBL.xsl'
        stylesheet_file = os.path.join(settings.BASE_DIR, 'server/api/ubl/' + stylesheet)
        (output_value, _) = process_by_saxon(proc, content, stylesheet_file)
        for child in output_value.head.children:
            failed_elements = (element for element in child.children if element.local_name == 'failed-assert')
            for element in failed_elements:
                info = {"stylesheet": stylesheet, "message": element.string_value}
                for attribute in element.attributes:
                    info[attribute.local_name] = attribute.string_value
                errors.append(info)

        stylesheet = 'PEPPOL-EN16931-UBL.xsl'
        stylesheet_file = os.path.join(settings.BASE_DIR, 'server/api/ubl/' + stylesheet)
        (output_value, _) = process_by_saxon(proc, content, stylesheet_file)
        for child in output_value.head.children:
            failed_elements = (element for element in child.children if element.local_name == 'failed-assert')
            for element in failed_elements:
                info = {"stylesheet": stylesheet, "message": element.string_value}
                for attribute in element.attributes:
                    info[attribute.local_name] = attribute.string_value
                errors.append(info)

    # html = transform_to_html(content)

    response = ({
        "version": proc.version,
        "filename": filename,
        "content_type": content_type,
        # "content": content,
        # "output": output,
        "valid": not errors,
        "errors": errors,
        # "html": html,
    })
    return response
