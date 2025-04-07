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

def transform_to_html(file: InMemoryUploadedFile) -> str:
    """
    Transform XML content to HTML using XSLT.
    """
    try:
        content: str = read_xml_from_file(file)
        stylesheet = 'stylesheet-ubl.xslt'
        stylesheet_file = os.path.join(settings.BASE_DIR, 'server/api/ubl/' + stylesheet)
        with PySaxonProcessor(license=False) as proc:
            (_, html) = process_by_saxon(proc, content, stylesheet_file)
            return html
    except Exception as e:
        print(f"Error transforming to HTML: {e}")
        return "<html><body>Error transforming to HTML</body></html>"

def process_by_saxon(proc: PySaxonProcessor, content: str, stylesheet_file: str) -> tuple[PyXdmValue, str]:
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

def read_xml_from_file(file: InMemoryUploadedFile) -> str:
    """
    Read XML content from an uploaded file.
    """
    content: str = ''.join(chunk.decode('utf-8') for chunk in file.chunks())
    return content

def validate_peppol(file: InMemoryUploadedFile):
    """
    Validate a Peppol UBL file.
    """
    content_type = file.content_type
    filename = secure_filename(file.name)
    errors = []
    content: str = read_xml_from_file(file)
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
