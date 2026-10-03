"""Build the editable English Assignment 3 report from real browser screenshots.

Usage:
    python scripts/build_report.py --name "First Last" --group "SE-2401" \
        --repo "https://github.com/USERNAME/REPOSITORY"

Requires python-docx and Pillow. Run the browser verification first so that
docs/screenshots and docs/verification.json describe the final website.
The optional --draft flag leaves conspicuous placeholders for missing evidence.
"""

from __future__ import annotations

import argparse
import io
import json
import math
import re
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION_START
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SCREENSHOTS = ROOT / "docs" / "screenshots"
REQUIRED = [
    *(f"{kind}-{width}.png" for kind in ("full", "districts", "garage")
      for width in (375, 768, 1280)),
    "navbar-mobile.png", "accordion-open.png", "about-mobile.png", "about-desktop.png",
    "garage-modal.png",
]
TITLE = "Night Tokyo"
REFERENCES = [
    ("Bootstrap 5.3: Getting started", "https://getbootstrap.com/docs/5.3/getting-started/introduction/"),
    ("Bootstrap 5.3: Grid system", "https://getbootstrap.com/docs/5.3/layout/grid/"),
    ("Bootstrap 5.3: Display utilities", "https://getbootstrap.com/docs/5.3/utilities/display/"),
    ("Bootstrap 5.3: Navbar", "https://getbootstrap.com/docs/5.3/components/navbar/"),
    ("Bootstrap 5.3: Accordion", "https://getbootstrap.com/docs/5.3/components/accordion/"),
    ("Bootstrap 5.3: Modals", "https://getbootstrap.com/docs/5.3/components/modal/"),
    ("MDN: Using media queries", "https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_media_queries/Using_media_queries"),
]


def shade(cell, fill="EDF2F5"):
    props = cell._tc.get_or_add_tcPr()
    el = OxmlElement("w:shd")
    el.set(qn("w:fill"), fill)
    props.append(el)


def prevent_split(row):
    element = OxmlElement("w:cantSplit")
    row._tr.get_or_add_trPr().append(element)


def table(doc, headers, rows):
    result = doc.add_table(rows=1, cols=len(headers))
    result.style = "Light Shading Accent 1"
    result.alignment = WD_TABLE_ALIGNMENT.CENTER
    for cell, label in zip(result.rows[0].cells, headers):
        cell.text = label
        shade(cell, "DCEAF0")
        for run in cell.paragraphs[0].runs:
            run.bold = True
    repeat = OxmlElement("w:tblHeader")
    result.rows[0]._tr.get_or_add_trPr().append(repeat)
    for values in rows:
        row = result.add_row()
        prevent_split(row)
        for cell, value in zip(row.cells, values):
            cell.text = str(value)
    doc.add_paragraph()
    return result


def code(doc, value):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(5)
    p.paragraph_format.space_after = Pt(10)
    run = p.add_run(value.strip())
    run.font.name = "Consolas"
    run.font.size = Pt(9)
    shade_par = OxmlElement("w:shd")
    shade_par.set(qn("w:fill"), "F2F5F7")
    p._p.get_or_add_pPr().append(shade_par)
    return p


def setup_section(section, landscape=False):
    section.page_width = Inches(11.69 if landscape else 8.27)
    section.page_height = Inches(8.27 if landscape else 11.69)
    section.left_margin = Inches(.7)
    section.right_margin = Inches(.7)
    section.top_margin = Inches(.66)
    section.bottom_margin = Inches(.62)
    section.header_distance = Inches(.28)
    section.footer_distance = Inches(.28)


def new_section(doc, landscape=False):
    section = doc.add_section(WD_SECTION_START.NEW_PAGE)
    setup_section(section, landscape)
    return section


def caption(doc, text):
    p = doc.add_paragraph(text)
    p.style = "Caption"
    p.paragraph_format.space_after = Pt(6)
    return p


def image_bytes(image):
    target = io.BytesIO()
    image.save(target, format="PNG")
    target.seek(0)
    return target


def screenshot(doc, filename, label, draft=False, complete=False):
    """Keep all image pixels; split tall captures into numbered reading panels.

    Phones use two columns on portrait pages. Tablet images use the full
    portrait page width. Desktop images use landscape pages. Consecutive
    slices cover the entire original screenshot with no scaling of its source
    pixels and no omitted vertical interval.
    """
    source = SCREENSHOTS / filename
    if not source.exists():
        if draft:
            new_section(doc)
            doc.add_heading(label, level=2)
            doc.add_paragraph(f"[SCREENSHOT REQUIRED: docs/screenshots/{filename}]")
            return
        raise FileNotFoundError(f"Missing screenshot: {source}")
    with Image.open(source) as opened:
        image = opened.convert("RGB")
    width, height = image.size
    mobile = width <= 500
    landscape = width >= 1000
    display_width = 3.15 if mobile else (10.15 if landscape else 6.75)
    # Leave generous space for title, caption, and the Word table's end paragraph.
    display_height = 8.4 if mobile else (5.3 if landscape else 8.4)
    crop_height = max(1, int(width * display_height / display_width))
    panels = [image.crop((0, top, width, min(top + crop_height, height)))
              for top in range(0, height, crop_height)]
    per_page = 2 if mobile else 1
    total_pages = math.ceil(len(panels) / per_page)
    for page_index in range(total_pages):
        new_section(doc, landscape)
        suffix = f" — sheet {page_index + 1}/{total_pages}" if total_pages > 1 else ""
        doc.add_heading(label + suffix, level=2)
        prefix = "Complete page capture" if complete else "Section / interaction capture"
        caption(doc, f"{prefix} • capture size: {width} × {height}px • source: {filename}")
        selected = panels[page_index * per_page:(page_index + 1) * per_page]
        if mobile:
            row = doc.add_table(rows=1, cols=2)
            row.alignment = WD_TABLE_ALIGNMENT.CENTER
            row.autofit = False
            for cell in row.rows[0].cells:
                cell.width = Inches(3.35)
            for index, panel in enumerate(selected):
                cell = row.cell(0, index)
                paragraph = cell.paragraphs[0]
                paragraph.paragraph_format.space_after = Pt(3)
                paragraph.add_run().add_picture(image_bytes(panel), width=Inches(display_width))
                top = (page_index * per_page + index) * crop_height
                p = cell.add_paragraph(f"Pixels {top}–{min(top + crop_height, height) - 1}")
                p.style = "Caption"
            prevent_split(row.rows[0])
        else:
            panel = selected[0]
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(3)
            p.add_run().add_picture(image_bytes(panel), width=Inches(display_width))
            top = page_index * crop_height
            caption(doc, f"Vertical pixels {top}–{min(top + crop_height, height) - 1} of {height}.")
        if len(panels) > 1 and page_index == 0:
            caption(doc, "Read consecutive panels from left to right, then continue on the next sheet. No page content is omitted.")


def verification_summary(doc, data):
    """Present the site's recorded checks without unrelated environment logs."""
    def yes_no(value):
        return "Yes" if value is True else "No" if value is False else "Not recorded"

    def visible(value):
        return "Visible" if value is True else "Hidden" if value is False else "Not recorded"

    passed = data.get("passed")
    doc.add_paragraph("Browser verification passed." if passed is True else
                      "The browser verification did not record an overall pass.")
    doc.add_paragraph("These results are read from docs/verification.json. The original JSON and scripts/verify_site.py provide the complete measurements and reproducible checks.")
    views = data.get("viewports", [])
    table(doc, ("Viewport", "District columns", "Garage columns", "Horizontal overflow", "District heading"), [
        (f"{view.get('width', '?')}px", view.get("customColumns", "Not recorded"),
         view.get("bootstrapColumns", "Not recorded"), yes_no(view.get("horizontalOverflow")),
         view.get("headingSize", "Not recorded")) for view in views
    ])
    table(doc, ("Viewport", "Story order", "Phone hint", "Edition label", "Menu button"), [
        (f"{view.get('width', '?')}px",
         "Text above image" if view.get("aboutTextFirstOnPhone") is True else
         "Image left; text right" if view.get("aboutImageFirstOnDesktop") is True else "Not recorded",
         visible(view.get("phoneHintVisible")), visible(view.get("editionVisible")),
         visible(view.get("navbarToggleVisible"))) for view in views
    ])
    interactions = data.get("interactions", {})
    labels = {
        "mobileNavbar": "Mobile navigation",
        "accordion": "Field-notes accordion",
        "garageModals": "Garage modals",
        "keyboardDismiss": "Keyboard interaction",
        "pureHTMLCSS": "Architecture (Zero custom JS)",
        "tokyoClock": "Tokyo clock",
    }
    table(doc, ("Interaction / feature", "Recorded result"), [
        (labels.get(key, key), value) for key, value in interactions.items()
    ])
    if views and all(view.get("allImagesLoaded") is True for view in views):
        doc.add_paragraph("All page images loaded at each of the three required widths.")
    if views and all(view.get("localFontsLoaded") is True for view in views):
        doc.add_paragraph("The local fonts loaded at each of the three required widths.")
    if views and all(view.get("missingAnchors") == [] for view in views):
        doc.add_paragraph("All tested in-page navigation targets exist.")
    if data.get("consoleErrors") == [] and data.get("failedRequests") == []:
        doc.add_paragraph("The verification recorded no page JavaScript errors or failed project-resource requests.")
    extra = data.get("additionalWidthsWithoutOverflow", [])
    if extra:
        doc.add_paragraph("Additional widths checked without horizontal overflow: " + ", ".join(f"{value}px" for value in extra) + ".")


def build(args):
    missing = [name for name in REQUIRED if not (SCREENSHOTS / name).exists()]
    if missing and not args.draft:
        raise SystemExit("Report evidence is incomplete. Generate these screenshots first:\n  " + "\n  ".join(missing))
    doc = Document()
    setup_section(doc.sections[0])
    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(10.5)
    normal.paragraph_format.space_after = Pt(7)
    normal.paragraph_format.line_spacing = 1.08
    for name in ("Title", "Heading 1", "Heading 2", "Heading 3"):
        doc.styles[name].font.name = "Calibri"
        doc.styles[name].font.color.rgb = RGBColor.from_string("173B4F")
    doc.styles["Caption"].font.size = Pt(8)
    doc.styles["Caption"].font.color.rgb = RGBColor.from_string("52616B")
    header = doc.sections[0].header.paragraphs[0]
    header.text = f"{TITLE.upper()}  /  ASSIGNMENT 03"
    header.style = "Caption"
    footer = doc.sections[0].footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    footer.add_run("Assignment 3  •  ")
    page = OxmlElement("w:fldSimple")
    page.set(qn("w:instr"), "PAGE")
    footer._p.append(page)
    doc.core_properties.title = f"Assignment 3 — {TITLE}"
    doc.core_properties.subject = "Responsive Web Design: Media Queries and Bootstrap Grid"
    doc.core_properties.author = args.name

    doc.add_paragraph("WEB TECHNOLOGIES", "Subtitle")
    doc.add_heading("Assignment 3", level=0)
    doc.add_heading(TITLE, level=1)
    doc.add_paragraph("Responsive Web Design\nMedia Queries + Bootstrap Grid", "Subtitle")
    doc.add_paragraph("An English-language editorial website about Tokyo after dark, its districts, and Japanese car culture.")
    table(doc, ("Submission detail", "Value"), [
        ("Student", args.name), ("Group", args.group),
        ("GitHub repository", args.repo),
        ("Source files", "index.html · style.css · assets/ (Pure HTML5 & CSS3, Zero Custom JavaScript)"),
        ("Required viewport widths", "375px · 768px · 1280px"),
    ])
    if args.name.startswith("[") or args.group.startswith("[") or args.repo.startswith("["):
        p = doc.add_paragraph("Before submission: replace every bracketed identity/repository placeholder and save the report with your own name. Review and rewrite explanations in your own words so that you can defend the code.")
        p.runs[0].font.color.rgb = RGBColor.from_string("A5442A")
    if args.draft and missing:
        doc.add_paragraph("DRAFT — some screenshot evidence is still missing. This version is not ready for submission.")

    new_section(doc)
    doc.add_heading("Project overview and setup", level=1)
    doc.add_paragraph("The page combines an atmospheric Tokyo night theme with two approaches to responsive layout. The district cards use a custom CSS Grid. The hero, story, garage, and field notes use Bootstrap containers, rows, columns, components, and utilities.")
    table(doc, ("Section", "Purpose", "Layout approach"), [
        ("#home", "Opening title, night-city visual, section links", "Bootstrap"),
        ("#districts", "Three places to explore after dark", "Custom CSS Grid + min-width media queries"),
        ("#about", "Editorial text and a supporting image", "Bootstrap columns + responsive ordering"),
        ("#garage", "Three Japanese car cards", "Bootstrap responsive columns + cards"),
        ("#field-notes", "Expandable practical notes", "Bootstrap grid + accordion"),
    ])
    doc.add_paragraph("Bootstrap 5.3.8 is connected through its CDN. The local style.css is linked after Bootstrap, allowing the custom colors, typography, and surfaces to override its defaults. The Bootstrap JavaScript bundle appears before the closing body tag and natively powers the collapsible navbar, accordion, and garage modals.")
    code(doc, '<meta name="viewport" content="width=device-width, initial-scale=1">\n<!-- Bootstrap CSS is loaded first, then style.css. -->\n<link rel="stylesheet" href="style.css">')
    doc.add_paragraph("The viewport tag makes the browser use the device width for layout. Both approaches start with the phone layout and add wider-screen changes. The layout does not depend on floats, fixed card widths, or absolute positioning.")

    doc.add_heading("Task 1 — Media queries by hand", level=1)
    doc.add_paragraph("The #districts section contains three repeated district cards. All classes inside this section are custom classes. The section does not use Bootstrap containers, rows, columns, cards, or utility classes for its layout.")
    doc.add_paragraph("The base .district-grid rule creates one flexible column. At 768px, a min-width media query changes the grid to two columns. At 992px, a second query changes it to three. The tablet breakpoint also changes the heading size and section spacing, so the queries adjust more than the number of columns.")
    code(doc, '.district-grid {\n  display: grid;\n  grid-template-columns: minmax(0, 1fr);\n}\n@media (min-width: 768px) {\n  .district-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }\n  /* The district heading and spacing also change here. */\n}\n@media (min-width: 992px) {\n  .district-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }\n}')
    doc.add_paragraph("This excerpt shows the layout logic; style.css contains the complete rules. minmax(0, 1fr) lets each column share the available space and shrink without forcing a horizontal overflow. Card images scale with their card, so the layout can adapt between the three required test widths.")
    table(doc, ("Viewport", "Columns", "Reason"), [
        ("375px", "1", "Only the mobile base rule applies."),
        ("768px", "2", "The first min-width query applies."),
        ("1280px", "3", "Both queries apply; the 992px rule sets three columns."),
    ])
    for width in (375, 768, 1280):
        screenshot(doc, f"districts-{width}.png", f"Task 1 evidence — Districts at {width}px", args.draft)

    new_section(doc)
    doc.add_heading("Task 2 — Bootstrap grid and components", level=1)
    doc.add_paragraph("The remaining sections use Bootstrap's container → row → column structure. The garage repeats col-12 col-md-6 col-lg-4 on each card wrapper: twelve of twelve grid units on a phone, six of twelve from 768px, and four of twelve from 992px. This produces the same 1 → 2 → 3 card arrangement as the custom district grid.")
    code(doc, '<div class="container">\n  <div class="row">\n    <div class="col-12 col-md-6 col-lg-4">\n      <article class="card">...</article>\n    </div>\n    <!-- Repeat the card column for the other two cars. -->\n  </div>\n</div>')
    doc.add_paragraph("The #about section has a text column and an image column. The text uses order-1 order-lg-2; the image uses the opposite order. On phones, the text is first and the image follows below. At the large breakpoint the columns sit next to each other, with the image on the left. The text remains first in the source order so the main explanation is encountered before the image.")
    doc.add_paragraph("The desktop status label uses d-none d-md-inline-flex, so it is hidden below 768px. A separate phone hint uses d-md-none, so it appears only below 768px. Bootstrap spacing, flex, and text utilities handle recurring alignment and spacing around these sections.")
    doc.add_paragraph("The navbar uses navbar-expand-lg. Below 992px, its navigation links collapse into a menu controlled by the menu button; at larger widths, the links are displayed inline. Each link targets a real section ID. The page also includes Bootstrap cards and an accordion. The accordion lets the reader expand a field note without displaying all of its content at once.")
    doc.add_paragraph("The garage buttons open dedicated Bootstrap modals with rich editorial stories for each vehicle. The modals and all other interactive components (collapsible navbar and accordion) operate 100% natively via Bootstrap 5.3 data attributes (data-bs-toggle, data-bs-target, data-bs-dismiss) and the official CDN bundle. In accordance with assignment requirements, the project uses zero custom JavaScript, preserving strict separation of concerns and robust standard-compliant behavior.")
    table(doc, ("Requirement", "Implementation on this page"), [
        ("Responsive card grid", "#garage: col-12 col-md-6 col-lg-4"),
        ("Stacked columns + priority", "#about: text first on phones; responsive order-* classes"),
        ("Responsive visibility", "d-none d-md-inline-flex and d-md-none"),
        ("Responsive navigation", "navbar-expand-lg + Bootstrap collapse"),
        ("Additional components", "Garage cards, the field-notes accordion, and the garage modals"),
        ("Utilities", "Responsive display, order, spacing, flex, and text classes"),
        ("Architecture", "Pure HTML5 & CSS3 with Bootstrap 5.3 CDN bundle (Zero custom JS)"),
    ])
    for width in (375, 768, 1280):
        screenshot(doc, f"garage-{width}.png", f"Task 2 evidence — Garage at {width}px", args.draft)
    for filename, label in [
        ("about-mobile.png", "Task 2 evidence — Text comes first on phones"),
        ("about-desktop.png", "Task 2 evidence — Two columns and desktop ordering"),
        ("navbar-mobile.png", "Task 2 evidence — Expanded mobile menu"),
        ("accordion-open.png", "Task 2 evidence — Expanded field note"),
        ("garage-modal.png", "Task 2 evidence — Native Bootstrap modal window"),
    ]:
        screenshot(doc, filename, label, args.draft)

    new_section(doc)
    doc.add_heading("Task 3 — Comparing the two approaches", level=1)
    table(doc, ("Aspect", "Custom media queries: districts", "Bootstrap grid: garage / other sections"), [
        ("Layout code", "The district grid needs a base grid rule and two min-width rules in style.css.", "Each garage column uses col-12 col-md-6 col-lg-4 in the HTML; Bootstrap supplies the breakpoint rules."),
        ("Design control", "District heading size, card spacing, and the grid can be tuned together in a section-specific query.", "Bootstrap handles column widths and gutters; local CSS adds the Tokyo colors, borders, and typography."),
        ("Changing the layout", "Changing the laptop district count means editing grid-template-columns in the 992px query.", "Changing the garage to four cards per row would use col-lg-3 on each wrapper."),
        ("Speed and reuse", "The repeated district layout is small, but its responsive rules must be written and maintained.", "The same responsive column pattern can be reused across sections; collapse and accordion already provide interaction."),
        ("Ordering and visibility", "Equivalent behavior would require additional custom order and display rules.", "The about section uses order-*; the status label and phone hint use d-* utilities."),
    ])
    doc.add_paragraph("I would choose custom media queries for a distinctive section such as the districts, where the spacing and heading need to change together with the card layout. I would choose Bootstrap for repeated card layouts and page structure, especially when the page also needs a responsive navbar or accordion. Combining both approaches keeps the district design flexible while making the rest of this page quicker to maintain.")
    doc.add_heading("Conclusion", level=1)
    doc.add_paragraph("I learned how to build a mobile-first layout with both CSS Grid media queries and Bootstrap's responsive columns. I learned how breakpoints produce one, two, and three cards per row, and how ordering and display utilities help prioritize content on smaller screens. I also learned why checking several viewport widths matters: a layout can look correct on a laptop and still overflow or become difficult to read on a phone.")

    new_section(doc)
    doc.add_heading("Defense Guide & Theoretical Answers", level=1)
    doc.add_paragraph("The practical defense accounts for 70 of the 100 total evaluation points. Below are the key theoretical concepts, code justifications, and answers to questions commonly asked during laboratory defense:")
    defense_qa = [
        ("What does responsive design mean?",
         "A design approach where the layout automatically adapts to the available viewport width while preserving visual hierarchy, readability, and interaction usability across mobile, tablet, and desktop devices."),
        ("What is the layout viewport and why is the meta tag mandatory?",
         '<meta name="viewport" content="width=device-width, initial-scale=1"> instructs mobile browsers to set the layout viewport width to the device\'s physical screen width (in CSS pixels) and sets the initial zoom scale to 1. Without it, mobile browsers assume a desktop page, render at a virtual 980px width, and scale down, breaking media queries and the Bootstrap grid.'),
        ("Why is this architecture strictly mobile-first?",
         "Base CSS rules define styles for narrow phone screens without any media query wrappers. Progressive min-width media queries (@media (min-width: 768px), @media (min-width: 992px)) layer on multi-column layouts and larger typography for wider viewports. This ensures fast rendering on mobile devices and eliminates redundant desktop overrides."),
        ("Why is style.css linked after Bootstrap CSS in the head?",
         "In CSS, when rules have equal specificity, the cascade gives priority to the rule defined latest in document order. Linking style.css after the Bootstrap stylesheet allows custom theme tokens, typography, and handmade grid styles to cleanly override Bootstrap defaults."),
        ("Why does the project use zero custom JavaScript?",
         "The assignment curriculum focuses strictly on CSS media queries and Bootstrap's responsive grid system. By relying exclusively on standard HTML5 data-attributes (data-bs-toggle, data-bs-target, data-bs-dismiss) and the official Bootstrap CDN bundle, all interactive components (mobile menu toggler, accordion panels, and car modals) operate declaratively and reliably with zero runtime errors, zero custom scripts, and clean separation of concerns."),
        ("How does the handmade section change at breakpoints?",
         "At 375px: 1 column (minmax(0, 1fr)). At 768px: 2 columns (repeat(2, minmax(0, 1fr))), heading font-size grows from 2.75rem to 3.35rem, and card gap changes. At 992px: 3 columns (repeat(3, minmax(0, 1fr))), heading layout switches to flex-direction: row and font-size reaches 3.8rem."),
        ("How do Bootstrap columns stack and reorder in Task 2?",
         "The garage cards use col-12 col-md-6 col-lg-4, creating 1 column on phones (12/12), 2 columns on tablets (6/12), and 3 columns on laptops (4/12). In the About section, the text column has order-1 order-lg-2 while the image has order-2 order-lg-1; this ensures the important editorial text appears first on phones and swaps to the right side on laptops."),
    ]
    for question, answer in defense_qa:
        p = doc.add_paragraph()
        run_q = p.add_run(f"Q: {question}\n")
        run_q.bold = True
        run_q.font.color.rgb = RGBColor.from_string("173B4F")
        run_a = p.add_run(f"A: {answer}")
        p.paragraph_format.space_after = Pt(6)

    new_section(doc)
    doc.add_heading("Verification evidence", level=1)
    verification_path = ROOT / "docs" / "verification.json"
    if verification_path.exists():
        data = json.loads(verification_path.read_text(encoding="utf-8-sig"))
        verification_summary(doc, data)
    else:
        doc.add_paragraph("No automated verification record was available when this report was generated. The screenshots document the captured states, but this report does not claim that automated browser checks passed. Generate docs/verification.json and rebuild the report to include those results.")
    doc.add_heading("References", level=2)
    doc.add_paragraph("The assignment specification and the following technical references support the implementation and its explanation:")
    for name, url in REFERENCES:
        doc.add_paragraph(f"{name}\n{url}")

    new_section(doc)
    doc.add_heading("Appendix — The complete page at three widths", level=1)
    doc.add_paragraph("The following evidence includes the complete page captured at 375px, 768px, and 1280px. Tall screenshots are divided into consecutive panels for readability; the pixel ranges show where each panel belongs. Together, the panels reproduce the full original screenshot without omitting content.")
    doc.add_paragraph("The original PNG files remain available in docs/screenshots/full-375.png, full-768.png, and full-1280.png. Use those files to inspect the captures at their original resolution.")
    for width in (375, 768, 1280):
        screenshot(doc, f"full-{width}.png", f"Complete page — {width}px", args.draft, complete=True)

    output_dir = ROOT / "docs"
    output_dir.mkdir(parents=True, exist_ok=True)
    safe_name = re.sub(r"[^\w-]+", "_", args.name, flags=re.UNICODE).strip("_")
    if args.name == "[Your full name]":
        safe_name = "YourName"
    destination = Path(args.output) if args.output else output_dir / f"Assignment3_{safe_name}.docx"
    doc.save(destination)
    print(f"Saved report: {destination}")
    try:
        import comtypes.client
        pdf_destination = destination.with_suffix(".pdf")
        word = comtypes.client.CreateObject("Word.Application")
        word.Visible = False
        wdoc = word.Documents.Open(str(destination.resolve()))
        wdoc.SaveAs(str(pdf_destination.resolve()), FileFormat=17)
        wdoc.Close()
        word.Quit()
        print(f"Saved PDF report: {pdf_destination}")
    except Exception as e:
        print(f"Note: PDF export skipped ({e}). DOCX generated successfully.")
    if missing:
        print(f"Draft placeholders: {len(missing)} missing screenshots")
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", default="Tamerlan Aitpayev")
    parser.add_argument("--group", default="SE-2401")
    parser.add_argument("--repo", default="https://github.com/TamerlanAitpayev/web3")
    parser.add_argument("--output", help="Optional DOCX output path")
    parser.add_argument("--draft", action="store_true", help="Allow visibly marked missing screenshots")
    args = parser.parse_args()
    build(args)


if __name__ == "__main__":
    main()
