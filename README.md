# AI Report Redesign | Python & PDF

Transforming AI-generated PDF reports into polished, publication-ready documents using Python and a custom corporate design system.

## What This Project Does

Takes a typical AI-generated PDF — default fonts, arbitrary layout, no visual identity — and redesigns it using Python with fpdf2. The result is an editorial-quality document with structured typography, balanced two-column layout, and full corporate branding.

## Before & After

| Before | After |
|--------|-------|
| Default fonts, no hierarchy | Inter typeface, baseline grid |
| Arbitrary colors | Corporate palette #457B9D / #B1D2DA |
| Chart dropped in | Chart visually integrated |
| No brand identity | Header, footer, GreenGrid identity |

## Files

- `style.py` — style module: constants, colors, fonts, layout functions
- `MP_after_full.py` — main file, generates the redesigned PDF
- `MP_before_full.py` — baseline AI-generated version
- `chart_before.png` / `chart_after.png` — data visualization before and after

## Tools

- Python 3
- fpdf2
- Matplotlib
- Inter typeface

## Portfolio

Full project with visuals: <a href="https://www.behance.net/gallery/246330715/AI-Report-Redesign-Python-PDF" target="_blank">Behance</a>
