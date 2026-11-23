
import re
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR

def create_ppt(slide_text):

    prs = Presentation()
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)

    slide = None
    body = None

    for line in slide_text.splitlines():

        line = line.strip()

        if not line:
            continue

        match = re.match(r"^slide\s*(\d+)\s*:\s*(.*)$", line, re.I)

        if match:
            number = int(match.group(1))

            slide = prs.slides.add_slide(prs.slide_layouts[6])

            slide.background.fill.solid()
            slide.background.fill.fore_color.rgb = RGBColor(245, 248, 253)

            # Top blue header
            header = slide.shapes.add_shape(
                1, Inches(0), Inches(0),
                Inches(13.33), Inches(1.35)
            )
            header.fill.solid()
            header.fill.fore_color.rgb = RGBColor(20, 50, 100)
            header.line.fill.background()

            # Slide title
            title_box = slide.shapes.add_textbox(
                Inches(0.7), Inches(0.3),
                Inches(12), Inches(0.8)
            )

            title = title_box.text_frame
            title.text = match.group(2)
            title.paragraphs[0].font.size = Pt(30)
            title.paragraphs[0].font.bold = True
            title.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)

            # Content area
            content_box = slide.shapes.add_textbox(
                Inches(0.9), Inches(1.8),
                Inches(11.5), Inches(4.8)
            )

            body = content_box.text_frame
            body.word_wrap = True
            body.vertical_anchor = MSO_ANCHOR.MIDDLE
            body.margin_left = Inches(0.2)
            body.margin_right = Inches(0.2)

            # Footer
            footer = slide.shapes.add_textbox(
                Inches(0.7), Inches(7.0),
                Inches(12), Inches(0.3)
            )
            footer.text_frame.text = (
                f"Research Presentation                         {number} / 8"
            )
            footer.text_frame.paragraphs[0].font.size = Pt(11)
            footer.text_frame.paragraphs[0].font.color.rgb = RGBColor(90, 100, 120)

        elif slide is not None:

            line = line.lstrip("-•* ").strip()

            if not line:
                continue

            if len(body.paragraphs) == 1 and not body.paragraphs[0].text:
                p = body.paragraphs[0]
            else:
                p = body.add_paragraph()

            p.text = "•  " + line
            p.font.size = Pt(23)
            p.font.color.rgb = RGBColor(40, 50, 70)
            p.space_after = Pt(22)

    if len(prs.slides) != 8:
        raise ValueError("Please generate exactly 8 slides.")

    filename = "Research_Presentation.pptx"
    prs.save(filename)

    return filename
