#!/usr/bin/env python3
"""
Convert 综述正文_for_docx.md to a formatted DOCX.
Requirements:
- 标题黑体 (SimHei)
- 正文宋体12pt (SimSun)
- 图片居中宽14cm
- 图注10.5pt居中
"""

import os
import re
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


def set_run_font(run, font_name_cn, font_name_en='Times New Roman', size_pt=None, bold=False):
    """Set font for a run with proper CJK support."""
    run.font.name = font_name_en
    r = run._element
    rPr = r.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.insert(0, rFonts)
    rFonts.set(qn('w:eastAsia'), font_name_cn)
    if size_pt:
        run.font.size = Pt(size_pt)
    run.font.bold = bold


def set_paragraph_format(para, space_before=0, space_after=0, line_spacing=1.5,
                         first_line_indent=None, alignment=None):
    """Set paragraph formatting."""
    pf = para.paragraph_format
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing = line_spacing
    if first_line_indent is not None:
        pf.first_line_indent = Cm(first_line_indent)
    if alignment is not None:
        para.alignment = alignment


def add_image_with_caption(doc, img_path, alt_text):
    """Add centered image with 14cm width and caption below."""
    # Resolve image path relative to project root
    if not os.path.isabs(img_path):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        img_path = os.path.join(base_dir, img_path)
    
    if not os.path.exists(img_path):
        print(f"Warning: image not found: {img_path}")
        para = doc.add_paragraph()
        run = para.add_run(f"[Image not found: {os.path.basename(img_path)}]")
        set_run_font(run, '宋体', size_pt=10.5)
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        return

    # Add image paragraph (centered)
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = para.add_run()
    run.add_picture(img_path, width=Cm(14))
    set_paragraph_format(para, space_before=6, space_after=3)

    # Add caption (10.5pt, centered)
    caption_para = doc.add_paragraph()
    caption_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = caption_para.add_run(alt_text)
    set_run_font(run, '宋体', size_pt=10.5)
    set_paragraph_format(caption_para, space_before=0, space_after=6)


def parse_table(lines, start_idx):
    """Parse a markdown table starting at start_idx. Returns (table_rows, end_idx)."""
    rows = []
    i = start_idx
    while i < len(lines) and lines[i].strip().startswith('|'):
        line = lines[i].strip()
        # Skip separator line (contains only |, -, :, spaces)
        if re.match(r'^[\|\s\-:]+$', line):
            i += 1
            continue
        cells = [c.strip() for c in line.split('|')[1:-1]]
        rows.append(cells)
        i += 1
    return rows, i


def add_table(doc, rows):
    """Add a formatted table to the document."""
    if not rows:
        return
    num_cols = len(rows[0])
    table = doc.add_table(rows=len(rows), cols=num_cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = 'Table Grid'
    
    for i, row_data in enumerate(rows):
        row = table.rows[i]
        for j, cell_text in enumerate(row_data):
            if j >= num_cols:
                break
            cell = row.cells[j]
            cell.text = cell_text
            # Format cell text
            for paragraph in cell.paragraphs:
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in paragraph.runs:
                    set_run_font(run, '宋体', size_pt=10.5)
                # If header row, make bold
                if i == 0:
                    for run in paragraph.runs:
                        run.font.bold = True
                        set_run_font(run, '黑体', size_pt=10.5)
    
    # Set table width to page width (A4 ~ 16cm usable)
    tbl = table._tbl
    tblPr = tbl.tblPr if tbl.tblPr is not None else OxmlElement('w:tblPr')
    tblW = OxmlElement('w:tblW')
    tblW.set(qn('w:w'), '5000')
    tblW.set(qn('w:type'), 'pct')
    tblPr.append(tblW)


def process_inline_formatting(paragraph, text):
    """Process bold, italic, and other inline markdown formatting."""
    # Pattern for **bold**
    parts = re.split(r'(\*\*.*?\*\*)', text)
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            run = paragraph.add_run(part[2:-2])
            set_run_font(run, '宋体', size_pt=12, bold=True)
        else:
            run = paragraph.add_run(part)
            set_run_font(run, '宋体', size_pt=12)


def convert_md_to_docx(md_path, output_path):
    doc = Document()
    
    # Set default font for document
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(12)
    rPr = style.element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.insert(0, rFonts)
    rFonts.set(qn('w:eastAsia'), '宋体')
    
    # Set page margins (A4)
    sections = doc.sections[0]
    sections.page_width = Cm(21)
    sections.page_height = Cm(29.7)
    sections.top_margin = Cm(2.54)
    sections.bottom_margin = Cm(2.54)
    sections.left_margin = Cm(3.17)
    sections.right_margin = Cm(3.17)
    
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    i = 0
    in_blockquote = False
    blockquote_lines = []
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Handle blockquotes (figure captions / notes)
        if stripped.startswith('>'):
            # Accumulate blockquote lines
            bq_text = stripped[1:].strip()
            # Check if next line continues the blockquote
            j = i + 1
            while j < len(lines) and lines[j].strip().startswith('>'):
                bq_text += ' ' + lines[j].strip()[1:].strip()
                j += 1
            
            para = doc.add_paragraph()
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = para.add_run(bq_text)
            set_run_font(run, '宋体', size_pt=10.5)
            set_paragraph_format(para, space_before=3, space_after=6)
            i = j
            continue
        
        # Empty lines
        if not stripped:
            i += 1
            continue
        
        # Horizontal rule
        if stripped == '---':
            doc.add_paragraph()
            i += 1
            continue
        
        # Headings
        if stripped.startswith('# '):
            text = stripped[2:]
            para = doc.add_heading(level=0)
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = para.add_run(text)
            set_run_font(run, '黑体', size_pt=18, bold=True)
            set_paragraph_format(para, space_before=12, space_after=12)
            i += 1
            continue
        elif stripped.startswith('## '):
            text = stripped[3:]
            para = doc.add_heading(level=1)
            run = para.add_run(text)
            set_run_font(run, '黑体', size_pt=16, bold=True)
            set_paragraph_format(para, space_before=12, space_after=6)
            i += 1
            continue
        elif stripped.startswith('### '):
            text = stripped[4:]
            para = doc.add_heading(level=2)
            run = para.add_run(text)
            set_run_font(run, '黑体', size_pt=14, bold=True)
            set_paragraph_format(para, space_before=10, space_after=6)
            i += 1
            continue
        elif stripped.startswith('#### '):
            text = stripped[5:]
            para = doc.add_heading(level=3)
            run = para.add_run(text)
            set_run_font(run, '黑体', size_pt=12, bold=True)
            set_paragraph_format(para, space_before=8, space_after=4)
            i += 1
            continue
        
        # Images: ![alt](path)
        img_match = re.match(r'!\[(.*?)\]\((.*?)\)', stripped)
        if img_match:
            alt_text = img_match.group(1)
            img_path = img_match.group(2)
            add_image_with_caption(doc, img_path, alt_text)
            i += 1
            continue
        
        # Tables
        if stripped.startswith('|'):
            rows, end_idx = parse_table(lines, i)
            add_table(doc, rows)
            i = end_idx
            continue
        
        # Unordered lists
        if stripped.startswith('- ') or stripped.startswith('* '):
            text = stripped[2:]
            para = doc.add_paragraph(style='List Bullet')
            process_inline_formatting(para, text)
            set_paragraph_format(para, space_before=3, space_after=3,
                                 first_line_indent=0)
            i += 1
            continue
        
        # Regular paragraph
        para = doc.add_paragraph()
        process_inline_formatting(para, stripped)
        set_paragraph_format(para, space_before=3, space_after=3,
                             first_line_indent=0.74)  # 2 chars ~ 0.74cm
        i += 1
    
    doc.save(output_path)
    print(f"DOCX saved to: {output_path}")


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    md_path = os.path.join(base_dir, '02_综述报告', '综述正文_for_docx.md')
    output_path = os.path.join(base_dir, '02_综述报告', '遥感影像路网与建筑物提取方法综述_重绘版.docx')
    convert_md_to_docx(md_path, output_path)
