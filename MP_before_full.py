from fpdf import FPDF, XPos, YPos

# ----------------------------------------
# 1. Create improved PDF structure (BEFORE)
# ----------------------------------------

pdf = FPDF(orientation='P', unit='mm', format='A4')
pdf.add_page()

margin_left = 20
margin_top = 20

# -------------------------
# Заголовок
# -------------------------
pdf.set_xy(margin_left, margin_top)
pdf.set_font("Helvetica", "B", 20)
pdf.cell(0, 10, "Before: Basic Layout", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

# -------------------------
# Лид
# -------------------------
pdf.set_font("Helvetica", "", 12)
lead_text = (
    "This is the unformatted 'before' version of the layout. "
    "It demonstrates the raw structure prior to redesign and serves as a "
    "reference point for evaluating improvements."
)
pdf.multi_cell(0, 6, lead_text)

# -------------------------
# Инфографика (готовый PNG)
# -------------------------
pdf.ln(4)
pdf.image("chart_before.png", x=margin_left, w=120)

# -------------------------
# Подпись под инфографикой
# -------------------------
pdf.ln(2)
pdf.set_font("Helvetica", "I", 10)
pdf.cell(0, 6, "Figure 1. Basic comparison chart", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

# -------------------------
# Подзаголовок 1
# -------------------------
pdf.ln(5)
pdf.set_font("Helvetica", "B", 14)
pdf.cell(0, 8, "Initial Structure and Limitations", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

# -------------------------
# Основной текст — часть 1
# -------------------------
pdf.set_font("Helvetica", "", 12)
text1 = (
    "The initial layout is intentionally simple. It uses a single-column structure, "
    "minimal spacing, and a basic typographic hierarchy. While functional, this "
    "approach lacks the refinement expected in editorial design. The chart is placed "
    "below the introductory text without alignment rules or visual rhythm, resulting "
    "in a layout that feels unbalanced and unpolished.\n\n"
)
pdf.multi_cell(0, 6, text1)

# -------------------------
# Подзаголовок 2
# -------------------------
pdf.set_font("Helvetica", "B", 14)
pdf.cell(0, 8, "Opportunities for Improvement", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

# -------------------------
# Основной текст — часть 2
# -------------------------
pdf.set_font("Helvetica", "", 12)
text2 = (
    "Despite its simplicity, the baseline layout provides a clear starting point for "
    "enhancement. Introducing a structured grid, consistent margins, and a more "
    "sophisticated typographic system would significantly improve readability. "
    "Additionally, refining the visual style of the chart and integrating it more "
    "harmoniously into the page would create a stronger editorial presence.\n\n"
    "This 'before' version highlights the contrast between raw content and a "
    "professionally designed layout, setting the stage for the improved 'after' "
    "version that follows."
)
pdf.multi_cell(0, 6, text2)

# -------------------------
# Export PDF
# -------------------------
pdf.output("layout_before.pdf")