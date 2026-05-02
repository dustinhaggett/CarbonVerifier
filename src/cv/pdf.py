"""Markdown → PDF via ReportLab.

Handles a small but useful subset of Markdown sufficient for the audit reports:
- # / ## / ### / #### headings
- paragraphs (blank-line-separated)
- - / * unordered lists
- |-delimited tables (header row + alignment row + data rows)
- > blockquotes
- **bold** and *italic* inline

Returns a bytes blob for st.download_button. No tempfiles touched."""

from __future__ import annotations

import re
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


def _md_inline(text: str) -> str:
    """Convert a small subset of Markdown inline markers to ReportLab's mini-HTML."""
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"__(.+?)__", r"<b>\1</b>", text)
    text = re.sub(r"(?<![\*\w])\*([^\*\n]+?)\*(?!\*)", r"<i>\1</i>", text)
    text = re.sub(r"(?<![_\w])_([^_\n]+?)_(?!_)", r"<i>\1</i>", text)
    text = re.sub(r"`([^`]+)`", r'<font face="Courier">\1</font>', text)
    return text


def _styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "Title": ParagraphStyle(
            "Title", parent=base["Title"], fontSize=20,
            textColor=colors.HexColor("#1e1b4b"), spaceAfter=14,
        ),
        "H1": ParagraphStyle(
            "H1", parent=base["Heading1"], fontSize=17,
            textColor=colors.HexColor("#1e1b4b"), spaceBefore=10, spaceAfter=10,
        ),
        "H2": ParagraphStyle(
            "H2", parent=base["Heading2"], fontSize=14,
            textColor=colors.HexColor("#7c3aed"), spaceBefore=8, spaceAfter=6,
        ),
        "H3": ParagraphStyle(
            "H3", parent=base["Heading3"], fontSize=12,
            textColor=colors.HexColor("#1e1b4b"), spaceBefore=6, spaceAfter=4,
        ),
        "Body": ParagraphStyle(
            "Body", parent=base["BodyText"], fontSize=10, leading=14, spaceAfter=6,
        ),
        "Quote": ParagraphStyle(
            "Quote", parent=base["BodyText"], fontSize=10, leading=14,
            leftIndent=18, textColor=colors.HexColor("#475569"), spaceAfter=6,
        ),
        "List": ParagraphStyle(
            "List", parent=base["BodyText"], fontSize=10, leading=14,
            leftIndent=14, bulletIndent=2, spaceAfter=2,
        ),
    }


def _parse_table(rows: list[str]) -> Table | None:
    data: list[list[str]] = []
    for r in rows:
        if re.match(r"^\|[\s\-:|]+\|?\s*$", r):
            continue
        cells = [c.strip() for c in r.strip().strip("|").split("|")]
        data.append(cells)
    if not data:
        return None
    flow_data = [[Paragraph(_md_inline(c), _styles()["Body"]) for c in row] for row in data]
    t = Table(flow_data, hAlign="LEFT", repeatRows=1)
    t.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e1b4b")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#cbd5e1")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ])
    )
    return t


def markdown_to_flowables(md_text: str, styles: dict) -> list:
    flow: list = []
    para_buf: list[str] = []
    lines = md_text.split("\n")

    def flush():
        nonlocal para_buf
        if para_buf:
            joined = " ".join(s.strip() for s in para_buf if s.strip())
            if joined:
                flow.append(Paragraph(_md_inline(joined), styles["Body"]))
            para_buf = []

    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line:
            flush()
            i += 1
            continue

        if line.startswith("#### "):
            flush()
            flow.append(Paragraph(_md_inline(line[5:]), styles["H3"]))
        elif line.startswith("### "):
            flush()
            flow.append(Paragraph(_md_inline(line[4:]), styles["H3"]))
        elif line.startswith("## "):
            flush()
            flow.append(Paragraph(_md_inline(line[3:]), styles["H2"]))
        elif line.startswith("# "):
            flush()
            flow.append(Paragraph(_md_inline(line[2:]), styles["H1"]))
        elif line.startswith("- ") or line.startswith("* "):
            flush()
            flow.append(Paragraph("• " + _md_inline(line[2:]), styles["List"]))
        elif line.startswith("> "):
            flush()
            flow.append(Paragraph(_md_inline(line[2:]), styles["Quote"]))
        elif line.startswith("|"):
            flush()
            tbl_rows: list[str] = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                tbl_rows.append(lines[i])
                i += 1
            tbl = _parse_table(tbl_rows)
            if tbl is not None:
                flow.append(tbl)
                flow.append(Spacer(1, 6))
            continue
        elif line.startswith("---") or line.startswith("***"):
            flush()
            flow.append(Spacer(1, 8))
        else:
            para_buf.append(line)
        i += 1

    flush()
    return flow


def markdown_to_pdf_bytes(md_text: str, title: str | None = None, subtitle: str | None = None) -> bytes:
    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=letter,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch,
        title=title or "CarbonVerifier Audit Report",
        author="CarbonVerifier",
    )
    styles = _styles()
    flow: list = []
    if title:
        flow.append(Paragraph(title, styles["Title"]))
        if subtitle:
            flow.append(Paragraph(subtitle, styles["Body"]))
        flow.append(Spacer(1, 12))
    flow.extend(markdown_to_flowables(md_text, styles))
    doc.build(flow)
    return buf.getvalue()
