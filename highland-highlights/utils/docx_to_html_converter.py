import html

from docx import Document
from docx.text.run import Run

from config import (
    DOCX_BODY_COLOR_FILTER,
    DOCX_HEADER_COLOR_FILTER,
    DOCX_XML_NAMESPACE,
    PARAGRAPH_SPACING,
    TEXT_BODY_COLOR,
    TEXT_HEADER_COLOR,
)


def convert_docx_to_html(docx_file_path):
    docx = Document(docx_file_path)
    html_paragraphs = []
    for paragraph in docx.paragraphs:
        if paragraph.text.strip():
            html_paragraph = _extract_formatted_paragraph(paragraph)
            html_paragraphs.append(html_paragraph)

    body_content = "".join(html_paragraphs)
    html_document = f"<html><body>{body_content}</body></html>"
    return html_document


def _extract_formatted_paragraph(paragraph):
    html_elements = []
    for paragraph_element in paragraph._element:
        tag = paragraph_element.tag.split("}")[-1]
        match tag:
            case "r":
                html_element = _extract_formatted_run_text(
                    paragraph_element, paragraph
                )
                html_elements.append(html_element)
            case "hyperlink":
                html_element = _extract_formatted_hyperlink_text(
                    paragraph_element, paragraph
                )
                html_elements.append(html_element)

    paragraph_content = "".join(html_elements)
    html_paragraph = (
        f"<p style='margin: {PARAGRAPH_SPACING}px 0;'>{paragraph_content}</p>"
    )
    return html_paragraph


def _extract_formatted_run_text(run_element, paragraph):
    for run in paragraph.runs:
        if run._element is run_element and run.text.strip():
            formatted_text = _format_run_text(run)
            return formatted_text
    return ""


def _extract_formatted_hyperlink_text(hyperlink_element, paragraph):
    run_elements = hyperlink_element.findall(f".//{{{DOCX_XML_NAMESPACE}}}r")
    formatted_texts = []
    for run_element in run_elements:
        run = Run(run_element, paragraph)
        if run.text.strip():
            formatted_text = _format_run_text(run)
            formatted_texts.append(formatted_text)

    hyperlink_text = "".join(formatted_texts)
    return hyperlink_text


def _format_run_text(run):
    opening_tags = []
    closing_tags = []
    if run.italic:
        opening_tags.append("<i>")
        closing_tags.append("</i>")
    if run.underline:
        opening_tags.append("<u>")
        closing_tags.append("</u>")
    if run.font.strike:
        opening_tags.append("<s>")
        closing_tags.append("</s>")

    text_color_attribute = _get_run_text_color(run)
    escaped_text = html.escape(run.text)
    colored_text = f"<span{text_color_attribute}>{escaped_text}</span>"

    opening_text = "".join(opening_tags)
    closing_text = "".join(reversed(closing_tags))
    formatted_text = f"{opening_text}{colored_text}{closing_text}"
    return formatted_text


def _get_run_text_color(run):
    rgb_color = run.font.color.rgb
    hex_color = f"#{rgb_color}"
    if rgb_color is None or hex_color == DOCX_BODY_COLOR_FILTER:
        return f" style='{TEXT_BODY_COLOR}'"
    elif hex_color == DOCX_HEADER_COLOR_FILTER:
        return f" style='{TEXT_HEADER_COLOR}'"
    return f" style='color: {hex_color}'"
