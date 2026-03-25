import math
from fpdf import FPDF

# -----------------------------
# UNITS
# -----------------------------
PT_TO_MM = 0.352778

# -----------------------------
# COLOURS
# -----------------------------
COLOR_ACCENT    = (69, 123, 157)    # #457B9D
COLOR_BODY      = (60, 60, 60)      # #3C3C3C
COLOR_MUTED     = (100, 100, 100)   # #646464
COLOR_HEADER_BG = (177, 210, 218)   # #B1D2DA

# -----------------------------
# TYPOGRAPHY
# -----------------------------
BASE_FONT_PT = 9
BASELINE_PT  = BASE_FONT_PT * 1.2
BASELINE_MM  = BASELINE_PT * PT_TO_MM

# -----------------------------
# PAGE
# -----------------------------
PAGE_WIDTH_MM  = 210
PAGE_HEIGHT_MM = 297

# -----------------------------
# PRINT SAFE ZONE
# -----------------------------
PRINT_MARGIN_MM = 10  # minimum safe zone for printing

# -----------------------------
# HEADER / FOOTER
# -----------------------------
HEADER_HEIGHT_MM = 12
FOOTER_HEIGHT_MM = 10

# -----------------------------
# MARGINS — content starts below header
# -----------------------------
MARGIN_TOP_MM    = PRINT_MARGIN_MM + HEADER_HEIGHT_MM + 11  # 33mm
MARGIN_LEFT_MM   = 20
MARGIN_RIGHT_MM  = 20
MARGIN_BOTTOM_MM = PRINT_MARGIN_MM + FOOTER_HEIGHT_MM + 6  # 26mm

# -----------------------------
# CONTENT
# -----------------------------
CONTENT_WIDTH_MM = PAGE_WIDTH_MM - MARGIN_LEFT_MM - MARGIN_RIGHT_MM

# -----------------------------
# COLUMNS
# -----------------------------
COLUMN_GAP_MM   = 8
COLUMN_WIDTH_MM = (CONTENT_WIDTH_MM - COLUMN_GAP_MM) / 2

# -----------------------------
# VERTICAL SPACING
# -----------------------------
V_SPACING_MM               = 6
LEAD_TO_GRAPHIC_SPACING_MM = V_SPACING_MM * 1.5


class StyledPDF(FPDF):

    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=False)
        
        # fonts must be registered before add_page()
        # because header() is called automatically on add_page()
        self.add_font("Inter-Regular",  "", "Inter-Regular.ttf")
        self.add_font("Inter-Light",    "", "Inter-Light.ttf")
        self.add_font("Inter-SemiBold", "", "Inter-SemiBold.ttf")
        self.add_font("Inter-Black",    "", "Inter-Black.ttf")
        self.add_font("Inter-Italic",   "", "Inter-Italic.ttf")
        
        self.add_page()
        self.set_margins(MARGIN_LEFT_MM, MARGIN_TOP_MM, MARGIN_RIGHT_MM)

    # -----------------------------
    # HEADER
    # -----------------------------
    def header(self):
        self.image("header.png", x=0, y=0, w=PAGE_WIDTH_MM)
    
    # -----------------------------
    # FOOTER
    # -----------------------------
    def footer(self):
        footer_y = PAGE_HEIGHT_MM - PRINT_MARGIN_MM - FOOTER_HEIGHT_MM
        self.image("footer.png", x=0, y=footer_y, w=PAGE_WIDTH_MM)

    # -----------------------------
    # BASELINE GRID
    # -----------------------------
    def snap_to_grid(self, y_mm):
        if y_mm < MARGIN_TOP_MM:
            return MARGIN_TOP_MM
        steps = (y_mm - MARGIN_TOP_MM) / BASELINE_MM
        return MARGIN_TOP_MM + math.ceil(steps) * BASELINE_MM

    # -----------------------------
    # AUTO-FIT TITLE FONT SIZE
    # -----------------------------
    def fit_title_font_size(self, text, max_pt=32, min_pt=20):
        for size in range(max_pt, min_pt - 1, -1):
            self.set_font("Inter-Black", size=size)
            if self.get_string_width(text) <= CONTENT_WIDTH_MM:
                return size
        return min_pt

    # -----------------------------
    # TITLE
    # -----------------------------
    def add_title(self, text):
        size = self.fit_title_font_size(text)
        self.set_font("Inter-Black", size=size)
        self.set_text_color(*COLOR_ACCENT)
        self.set_xy(MARGIN_LEFT_MM, MARGIN_TOP_MM)
        self.multi_cell(CONTENT_WIDTH_MM, size * 0.45, text)
        self.title_bottom = self.get_y()

    # -----------------------------
    # LEAD
    # -----------------------------
    def add_lead(self, text, size=14):
        self.set_font("Inter-Light", size=size)
        self.set_text_color(*COLOR_BODY)
        y = self.title_bottom + V_SPACING_MM
        self.set_xy(MARGIN_LEFT_MM, y)
        self.multi_cell(CONTENT_WIDTH_MM, size * 0.45, text)
        self.lead_bottom = self.get_y()

    # -----------------------------
    # CAPTION
    # -----------------------------
    def add_caption(self, text):
        self.set_font("Inter-Italic", size=10)
        self.set_text_color(*COLOR_MUTED)
        self.set_y(self.get_y() + 2)
        self.set_x(MARGIN_LEFT_MM)
        self.multi_cell(CONTENT_WIDTH_MM, 4, text)

    # -----------------------------
    # JUSTIFIED LINE
    # -----------------------------
    def render_justified(self, text, x, y, width):
        words = text.split()
        if len(words) <= 1:
            self.set_xy(x, y)
            self.cell(width, BASELINE_MM, text)
            return
        total_word_width = sum(self.get_string_width(w) for w in words)
        extra_space = (width - total_word_width) / (len(words) - 1)
        cx = x
        for i, word in enumerate(words):
            self.set_xy(cx, y)
            self.cell(self.get_string_width(word), BASELINE_MM, word)
            if i < len(words) - 1:
                cx += self.get_string_width(word) + extra_space

    # -----------------------------
    # TWO-COLUMN BALANCED FLOW
    # -----------------------------
    def flow_two_columns(self, blocks):

        col1_x = MARGIN_LEFT_MM
        col2_x = MARGIN_LEFT_MM + COLUMN_WIDTH_MM + COLUMN_GAP_MM
        top_y = self.snap_to_grid(self.get_y())

        # --- step 1: expand blocks into flat line list ---
        def expand_to_lines(blocks):
            lines = []
            first_block = True
            for block in blocks:
                if block["type"] == "subheading":
                    if not first_block:
                        lines.append({"type": "gap", "text": ""})
                    lines.append({"type": "subheading", "text": block["text"]})
                else:
                    self.set_font("Inter-Regular", size=BASE_FONT_PT)
                    words = block["text"].split()
                    current = ""
                    block_lines = []
                    for word in words:
                        test = current + " " + word if current else word
                        if self.get_string_width(test) <= COLUMN_WIDTH_MM:
                            current = test
                        else:
                            block_lines.append(current)
                            current = word
                    if current:
                        block_lines.append(current)
                    for j, bl in enumerate(block_lines):
                        lines.append({
                            "type": "body",
                            "text": bl,
                            "last": j == len(block_lines) - 1
                        })
                first_block = False
            return lines

        all_lines = expand_to_lines(blocks)
        total = len(all_lines)
        half = total / 2

        # --- step 2: find split point ---
        def is_valid_split(lines, split):
            if split == 0 or split == len(lines):
                return True
            if lines[split - 1]["type"] == "gap":
                return False
            for i in range(split - 1, -1, -1):
                if lines[i]["type"] == "subheading":
                    body_after = sum(
                        1 for l in lines[i + 1:split]
                        if l["type"] == "body"
                    )
                    if body_after < 2:
                        return False
                    break
                elif lines[i]["type"] == "body":
                    break
            return True

        split = round(half)
        for delta in range(0, total):
            for candidate in [round(half) + delta, round(half) - delta]:
                if 0 < candidate < total and is_valid_split(all_lines, candidate):
                    split = candidate
                    break
            else:
                continue
            break

        col1_lines = all_lines[:split]
        col2_lines = all_lines[split:]

        # --- step 3: render one column from flat line list ---
        def render_lines(line_list, x):
            y = top_y
            for line in line_list:
                if line["type"] == "gap":
                    y += BASELINE_MM
                elif line["type"] == "subheading":
                    self.set_font("Inter-SemiBold", size=BASE_FONT_PT + 2)
                    self.set_text_color(*COLOR_ACCENT)
                    self.set_xy(x, y)
                    self.cell(COLUMN_WIDTH_MM, BASELINE_MM, line["text"].upper())
                    y += BASELINE_MM
                else:
                    self.set_font("Inter-Regular", size=BASE_FONT_PT)
                    self.set_text_color(*COLOR_BODY)
                    if line.get("last", True):
                        # last line of paragraph — left align
                        self.set_xy(x, y)
                        self.cell(COLUMN_WIDTH_MM, BASELINE_MM, line["text"])
                    else:
                        self.render_justified(line["text"], x, y, COLUMN_WIDTH_MM)
                    y += BASELINE_MM
            return y

        # --- step 4: render both columns ---
        y1 = render_lines(col1_lines, col1_x)
        y2 = render_lines(col2_lines, col2_x)
        self.set_y(max(y1, y2))