from style import (
    StyledPDF,
    MARGIN_LEFT_MM,
    CONTENT_WIDTH_MM,
    V_SPACING_MM,
    LEAD_TO_GRAPHIC_SPACING_MM
)

# ---------------------------------------
# CREATE PDF
# ---------------------------------------
pdf = StyledPDF()

# ---------------------------------------
# TITLE
# ---------------------------------------
pdf.add_title("AFTER: REFINED MAGAZINE LAYOUT")

# ---------------------------------------
# LEAD
# ---------------------------------------
pdf.add_lead(
    "A redesigned, modern layout with structured grid, improved typography, "
    "and a contemporary visual style suitable for editorial and portfolio use."
)

# ---------------------------------------
# CHART
# ---------------------------------------
pdf.set_y(pdf.lead_bottom + LEAD_TO_GRAPHIC_SPACING_MM)
pdf.image("chart_after.png", x=MARGIN_LEFT_MM, w=CONTENT_WIDTH_MM)

# ---------------------------------------
# CAPTION
# ---------------------------------------
pdf.add_caption("Figure 1. Improved comparison chart with modern color palette.")

# ---------------------------------------
# GAP BEFORE TEXT BLOCK
# ---------------------------------------
pdf.set_y(pdf.get_y() + V_SPACING_MM)

# ---------------------------------------
# TEXT BLOCKS
# ---------------------------------------
blocks = [
    {
        "type": "subheading",
        "text": "Refined Visual Hierarchy"
    },
    {
        "type": "body",
        "text": (
            "The redesigned layout introduces a clear visual hierarchy that guides the reader "
            "through the content with intention. Larger typographic elements, consistent spacing, "
            "and a structured rhythm create a more engaging reading experience. The use of the "
            "Inter typeface reinforces clarity and modernity, while the refined grid ensures that "
            "every element aligns harmoniously."
        )
    },
    {
        "type": "subheading",
        "text": "Enhanced Editorial Structure"
    },
    {
        "type": "body",
        "text": (
            "The two-column layout reflects real editorial design practices used in magazines and "
            "professional reports. This structure improves readability by breaking the text into "
            "manageable segments, creating a natural flow across the page. Balanced margins and "
            "consistent column widths contribute to a polished, publication-ready appearance."
        )
    },
    {
        "type": "subheading",
        "text": "Modernized Data Presentation"
    },
    {
        "type": "body",
        "text": (
            "The updated chart integrates seamlessly into the visual system of the page. Its "
            "contemporary color palette, improved contrast, and balanced proportions enhance both "
            "clarity and aesthetic appeal. Rather than functioning as a standalone element, the "
            "chart now contributes to the overall editorial identity of the layout, reinforcing "
            "the modern and cohesive design language."
        )
    },
]

# ---------------------------------------
# TWO-COLUMN TEXT FLOW
# ---------------------------------------
pdf.flow_two_columns(blocks)

# ---------------------------------------
# SAVE
# ---------------------------------------
pdf.output("layout_after.pdf")