"""
Utils
"""

import os
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
from saxonche import PySaxonProcessor, PyXdmValue
from werkzeug.utils import secure_filename

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
    Safely read XML content from an uploaded file.
    Handles UTF-8 BOM and leading whitespace issues.
    """

    # Reset pointer just in case
    file.seek(0)

    # Read full content as bytes
    content_bytes = file.read()

    # Decode using utf-8-sig to remove BOM if present
    content = content_bytes.decode("utf-8-sig")

    # Remove leading whitespace/newlines that break XML parsing
    return content.lstrip()

    # """
    # Read XML content from an uploaded file.
    # """
    # content: str = ''.join(chunk.decode('utf-8') for chunk in file.chunks())
    # return content

def validate_ubl(proc: PySaxonProcessor, content: str, errors: list, flags: list):
    stylesheet = 'CEN-EN16931-UBL'
    stylesheet_file = os.path.join(settings.BASE_DIR, 'server/api/ubl/' + stylesheet + '.xsl')
    (output_value, _) = process_by_saxon(proc, content, stylesheet_file)
    for child in output_value.head.children:
        failed_elements = (element for element in child.children if element.local_name == 'failed-assert')
        for element in failed_elements:
            info = {"stylesheet": stylesheet, "message": element.string_value}
            for attribute in element.attributes:
                info[attribute.local_name] = attribute.string_value
            errors.append(info) if (info["flag"] == "fatal") else flags.append(info)

def validate_en16931_ubl(file: InMemoryUploadedFile):
    """
    Validate a EN 16931 UBL file.
    """
    content_type = file.content_type
    filename = secure_filename(file.name)
    errors = []
    flags = []
    content: str = read_xml_from_file(file)
    with PySaxonProcessor(license=False) as proc:
        validate_ubl(proc, content, errors, flags)

    response = ({
        "version": proc.version,
        "filename": filename,
        "content_type": content_type,
        "valid": not errors,
        "errors": errors,
        "flags": flags,
    })
    return response

def validate_peppol_billing(file: InMemoryUploadedFile):
    """
    Validate a Peppol UBL file.
    """
    content_type = file.content_type
    filename = secure_filename(file.name)
    errors = []
    flags = []
    content: str = read_xml_from_file(file)
    with PySaxonProcessor(license=False) as proc:
        validate_ubl(proc, content, errors, flags)

        stylesheet = 'PEPPOL-EN16931-UBL'
        stylesheet_file = os.path.join(settings.BASE_DIR, 'server/api/ubl/' + stylesheet + '.xsl')
        (output_value, _) = process_by_saxon(proc, content, stylesheet_file)
        for child in output_value.head.children:
            failed_elements = (element for element in child.children if element.local_name == 'failed-assert')
            for element in failed_elements:
                info = {"stylesheet": stylesheet, "message": element.string_value}
                for attribute in element.attributes:
                    info[attribute.local_name] = attribute.string_value
                errors.append(info) if (info["flag"] == "fatal") else flags.append(info)

    # html = transform_to_html(content)

    response = ({
        "version": proc.version,
        "filename": filename,
        "content_type": content_type,
        # "content": content,
        # "output": output,
        "valid": not errors,
        "errors": errors,
        "flags": flags,
        # "html": html,
    })
    return response

def validate_peppol_self_billing(file: InMemoryUploadedFile):
    """
    Validate a Peppol UBL file.
    """
    content_type = file.content_type
    filename = secure_filename(file.name)
    errors = []
    flags = []
    content: str = read_xml_from_file(file)
    with PySaxonProcessor(license=False) as proc:
        validate_ubl(proc, content, errors, flags)

        stylesheet = 'PEPPOL-EN16931-UBL-SB'
        stylesheet_file = os.path.join(settings.BASE_DIR, 'server/api/ubl/' + stylesheet + '.xsl')
        (output_value, _) = process_by_saxon(proc, content, stylesheet_file)
        for child in output_value.head.children:
            failed_elements = (element for element in child.children if element.local_name == 'failed-assert')
            for element in failed_elements:
                info = {"stylesheet": stylesheet, "message": element.string_value}
                for attribute in element.attributes:
                    info[attribute.local_name] = attribute.string_value
                errors.append(info) if (info["flag"] == "fatal") else flags.append(info)

    # html = transform_to_html(content)

    response = ({
        "version": proc.version,
        "filename": filename,
        "content_type": content_type,
        # "content": content,
        # "output": output,
        "valid": not errors,
        "errors": errors,
        "flags": flags,
        # "html": html,
    })
    return response

def validate_peppol_si_ubl(file: InMemoryUploadedFile):
    """
    Validate a Peppol UBL file.
    """
    content_type = file.content_type
    filename = secure_filename(file.name)
    errors = []
    flags = []
    content: str = read_xml_from_file(file)
    with PySaxonProcessor(license=False) as proc:
        validate_ubl(proc, content, errors, flags)

        stylesheet = 'SI-UBL-2_0'
        stylesheet_file = os.path.join(settings.BASE_DIR, 'server/api/ubl/' + stylesheet + '.xsl')
        (output_value, _) = process_by_saxon(proc, content, stylesheet_file)
        for child in output_value.head.children:
            failed_elements = (element for element in child.children if element.local_name == 'failed-assert')
            for element in failed_elements:
                info = {"stylesheet": stylesheet, "message": element.string_value}
                for attribute in element.attributes:
                    info[attribute.local_name] = attribute.string_value
                errors.append(info) if (info["flag"] == "fatal") else flags.append(info)

    response = ({
        "version": proc.version,
        "filename": filename,
        "content_type": content_type,
        "valid": not errors,
        "errors": errors,
        "flags": flags,
    })
    return response

def validate_peppol_nlcius_cii(file: InMemoryUploadedFile):
    """
    Validate a Peppol UBL file.
    """
    content_type = file.content_type
    filename = secure_filename(file.name)
    errors = []
    flags = []
    content: str = read_xml_from_file(file)
    with PySaxonProcessor(license=False) as proc:
        # validate_ubl(proc, content, errors, flags)

        stylesheet = 'NLCIUS-CII-1_0'
        stylesheet_file = os.path.join(settings.BASE_DIR, 'server/api/cii/' + stylesheet + '.xsl')
        (output_value, _) = process_by_saxon(proc, content, stylesheet_file)
        for child in output_value.head.children:
            failed_elements = (element for element in child.children if element.local_name == 'failed-assert')
            for element in failed_elements:
                info = {"stylesheet": stylesheet, "message": element.string_value}
                for attribute in element.attributes:
                    info[attribute.local_name] = attribute.string_value
                errors.append(info) if (info["flag"] == "fatal") else flags.append(info)

    response = ({
        "version": proc.version,
        "filename": filename,
        "content_type": content_type,
        "valid": not errors,
        "errors": errors,
        "flags": flags,
    })
    return response

def validate_en16931_extended_ctc_fr_ubl(file: InMemoryUploadedFile):
    """
    Validate a EN 16931 - EXTENDED CTC FR - UBL file.
    """
    content_type = file.content_type
    filename = secure_filename(file.name)
    errors = []
    flags = []
    content: str = read_xml_from_file(file)
    with PySaxonProcessor(license=False) as proc:
        # validate_ubl(proc, content, errors, flags)

        stylesheet = '20260430_BR-FR-Flux2-Schematron-UBL_V1.3.1'
        stylesheet_file = os.path.join(settings.BASE_DIR, 'server/api/ubl/' + stylesheet + '.xsl')
        (output_value, _) = process_by_saxon(proc, content, stylesheet_file)
        for child in output_value.head.children:
            failed_elements = (element for element in child.children if element.local_name == 'failed-assert')
            for element in failed_elements:
                info = {"stylesheet": stylesheet, "message": element.string_value}
                for attribute in element.attributes:
                    info[attribute.local_name] = attribute.string_value
                errors.append(info) if (info["flag"] == "fatal") else flags.append(info)

    response = ({
        "version": proc.version,
        "filename": filename,
        "content_type": content_type,
        "valid": not errors,
        "errors": errors,
        "flags": flags,
    })
    return response

def validate_cii(proc: PySaxonProcessor, content: str, errors: list, flags: list):
    stylesheet = 'EN16931-CII-validation'
    stylesheet_file = os.path.join(settings.BASE_DIR, 'server/api/cii/' + stylesheet + '.xslt')
    (output_value, _) = process_by_saxon(proc, content, stylesheet_file)
    for child in output_value.head.children:
        failed_elements = (element for element in child.children if element.local_name == 'failed-assert')
        for element in failed_elements:
            info = {"stylesheet": stylesheet, "message": element.string_value}
            for attribute in element.attributes:
                info[attribute.local_name] = attribute.string_value
            errors.append(info) if (info["flag"] == "fatal") else flags.append(info)

def validate_en16931_cii(file: InMemoryUploadedFile):
    """
    Validate a EN 16931 CII file.
    """
    content_type = file.content_type
    filename = secure_filename(file.name)
    errors = []
    flags = []
    content: str = read_xml_from_file(file)
    with PySaxonProcessor(license=False) as proc:
        validate_cii(proc, content, errors, flags)

    response = ({
        "version": proc.version,
        "filename": filename,
        "content_type": content_type,
        "valid": not errors,
        "errors": errors,
        "flags": flags,
    })
    return response

def validate_en16931_extended_ctc_fr_cii(file: InMemoryUploadedFile):
    """
    Validate a EN 16931 - EXTENDED CTC FR - UBL file.
    """
    content_type = file.content_type
    filename = secure_filename(file.name)
    errors = []
    flags = []
    content: str = read_xml_from_file(file)
    with PySaxonProcessor(license=False) as proc:
        # validate_cii(proc, content, errors, flags)

        stylesheet = '20260430_BR-FR-Flux2-Schematron-CII_V1.3.1'
        stylesheet_file = os.path.join(settings.BASE_DIR, 'server/api/cii/' + stylesheet + '.xsl')
        (output_value, _) = process_by_saxon(proc, content, stylesheet_file)
        for child in output_value.head.children:
            failed_elements = (element for element in child.children if element.local_name == 'failed-assert')
            for element in failed_elements:
                info = {"stylesheet": stylesheet, "message": element.string_value}
                for attribute in element.attributes:
                    info[attribute.local_name] = attribute.string_value
                errors.append(info) if (info["flag"] == "fatal") else flags.append(info)

    response = ({
        "version": proc.version,
        "filename": filename,
        "content_type": content_type,
        "valid": not errors,
        "errors": errors,
        "flags": flags,
    })
    return response
