#!/usr/bin/env python3
"""
Standardize text formatting in the DOCX to proper academic paper format.

Rules:
- Title: 黑体, 18pt, bold, black, center
- Heading 1: 黑体, 16pt, bold, black
- Heading 2: 黑体, 14pt, bold, black
- Heading 3: 黑体, 12pt, bold, black
- Body text (Normal): 宋体, 12pt, NOT bold, black, first-line indent 0.74cm
- Figure captions: 宋体, 10.5pt, NOT bold, black, center
- Table captions: 宋体, 10.5pt, NOT bold, black, center
- Blockquotes/notes: 宋体, 10.5pt, NOT bold, black, center
- List Bullet: 宋体, 12pt, NOT bold, black
"""

import re
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


def set_run_font(run, cn_font, en_font='Times New Roman'):
    """Set CJK and Western font for a run."""
    run.font.name = en_font
    r = run._element
    rPr = r.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.insert(0, rFonts)
    rFonts.set(qn('w:ascii'), en_font)
    rFonts.set(qn('w:hAnsi'), en_font)
    rFonts.set(qn('w:eastAsia'), cn_font)


def set_run_color(run, color='000000'):
    """Set font color using RGB hex."""
    run.font.color.rgb = RGBColor(int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16))


def remove_highlight(run):
    """Remove highlight/shading from a run."""
    rPr = run._element.find(qn('w:rPr'))
    if rPr is not None:
        highlight = rPr.find(qn('w:highlight'))
        if highlight is not None:
            rPr.remove(highlight)
        shading = rPr.find(qn('w:shd'))
        if shading is not None:
            rPr.remove(shading)


def is_figure_caption(text):
    return bool(re.match(r'^图\d+', text.strip()))


def is_table_caption(text):
    return bool(re.match(r'^表\d+', text.strip()))


def is_blockquote_note(text):
    # Blockquote notes typically start with citation markers
    t = text.strip()
    return t.startswith('（引自') or t.startswith('（自绘') or t.startswith('（建议') or t.startswith('（详见')


def standardize_docx(input_path, output_path):
    doc = Document(input_path)

    for para in doc.paragraphs:
        style = para.style.name
        text = para.text.strip()

        if style == 'Title':
            # Title: 黑体 18pt bold black center
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in para.runs:
                set_run_font(run, '黑体')
                run.font.size = Pt(18)
                run.font.bold = True
                set_run_color(run)
                remove_highlight(run)

        elif style == 'Heading 1':
            # Heading 1: 黑体 16pt bold black
            for run in para.runs:
                set_run_font(run, '黑体')
                run.font.size = Pt(16)
                run.font.bold = True
                set_run_color(run)
                remove_highlight(run)

        elif style == 'Heading 2':
            # Heading 2: 黑体 14pt bold black
            for run in para.runs:
                set_run_font(run, '黑体')
                run.font.size = Pt(14)
                run.font.bold = True
                set_run_color(run)
                remove_highlight(run)

        elif style == 'Heading 3':
            # Heading 3: 黑体 12pt bold black
            for run in para.runs:
                set_run_font(run, '黑体')
                run.font.size = Pt(12)
                run.font.bold = True
                set_run_color(run)
                remove_highlight(run)

        elif style == 'List Bullet':
            # List: 宋体 12pt not bold black
            for run in para.runs:
                set_run_font(run, '宋体')
                run.font.size = Pt(12)
                run.font.bold = False
                set_run_color(run)
                remove_highlight(run)

        elif style == 'Normal':
            if is_figure_caption(text) or is_table_caption(text):
                # Caption: 宋体 10.5pt not bold black center
                para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                pf = para.paragraph_format
                pf.space_before = Pt(6)
                pf.space_after = Pt(3)
                for run in para.runs:
                    set_run_font(run, '宋体')
                    run.font.size = Pt(10.5)
                    run.font.bold = False
                    set_run_color(run)
                    remove_highlight(run)

            elif is_blockquote_note(text):
                # Note: 宋体 10.5pt not bold black center
                para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                pf = para.paragraph_format
                pf.space_before = Pt(3)
                pf.space_after = Pt(6)
                for run in para.runs:
                    set_run_font(run, '宋体')
                    run.font.size = Pt(10.5)
                    run.font.bold = False
                    set_run_color(run)
                    remove_highlight(run)

            else:
                # Body text: 宋体 12pt not bold black
                # First-line indent 0.74cm (2 Chinese chars)
                pf = para.paragraph_format
                pf.first_line_indent = Cm(0.74)
                pf.space_before = Pt(3)
                pf.space_after = Pt(3)
                pf.line_spacing = 1.5
                for run in para.runs:
                    set_run_font(run, '宋体')
                    run.font.size = Pt(12)
                    run.font.bold = False
                    set_run_color(run)
                    remove_highlight(run)

    # Also standardize table cell text
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    for run in para.runs:
                        set_run_font(run, '宋体')
                        run.font.size = Pt(10.5)
                        run.font.bold = False
                        set_run_color(run)
                        remove_highlight(run)
                    para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.save(output_path)
    print(f"Standardized DOCX saved to: {output_path}")


if __name__ == '__main__':
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(base_dir, '02_综述报告', '遥感影像路网与建筑物提取方法综述_修改版.docx')
    output_path = os.path.join(base_dir, '02_综述报告', '遥感影像路网与建筑物提取方法综述_格式标准化.docx')
    standardize_docx(input_path, output_path)
