# SPDX-FileCopyrightText: 2025 Jack Baril
# SPDX-License-Identifier: AGPL-3.0-or-later

import html

from docx import Document
from docx.text.run import Run

from config import (
    DOCX_BODY_COLOR_FILTER,
    DOCX_HEADER_COLOR_FILTER,
    TEXT_BODY_COLOR,
    TEXT_HEADER_COLOR,
)

DOCX_XML_NAMESPACE = (
    "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
)


def convert_docx_to_html(docx_file_path):
    docx = Document(docx_file_path)
    html_paragraphs = []
    for paragraph in docx.paragraphs:
        if paragraph.text.strip():
            html_paragraph = _extract_formatted_paragraph(paragraph)
            html_paragraphs.append(html_paragraph)

    return "".join(html_paragraphs)


def create_html_document(body_content, paragraph_spacing_px):
    return (
        "<html><head><style>"
        f"p {{ margin: {paragraph_spacing_px}px 0; }}"
        f"</style></head><body>{body_content}</body></html>"
    )


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
    return f"<p>{paragraph_content}</p>"


def _extract_formatted_run_text(run_element, paragraph):
    for run in paragraph.runs:
        if run._element is run_element and run.text.strip():
            return _format_run_text(run)
    return ""


def _extract_formatted_hyperlink_text(hyperlink_element, paragraph):
    run_elements = hyperlink_element.findall(f".//{{{DOCX_XML_NAMESPACE}}}r")
    formatted_texts = []
    for run_element in run_elements:
        run = Run(run_element, paragraph)
        if run.text.strip():
            formatted_text = _format_run_text(run)
            formatted_texts.append(formatted_text)

    return "".join(formatted_texts)


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
    return f"{opening_text}{colored_text}{closing_text}"


def _get_run_text_color(run):
    rgb_color = run.font.color.rgb
    if rgb_color is None:
        return f" style='color: {TEXT_BODY_COLOR}'"
    hex_color = f"#{rgb_color}"
    if hex_color == DOCX_BODY_COLOR_FILTER:
        return f" style='color: {TEXT_BODY_COLOR}'"
    elif hex_color == DOCX_HEADER_COLOR_FILTER:
        return f" style='color: {TEXT_HEADER_COLOR}'"
    return f" style='color: {hex_color}'"
