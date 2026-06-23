"""
Resit Penggunaan - Park@Perak
===============================
Edit the variables in the CONFIG section below each month, then run:
    python3 generate_resit.py

Output: resit_penggunaan.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import os

# ─────────────────────────────────────────────────────────────
#  CONFIG — Edit these values each month
# ─────────────────────────────────────────────────────────────
NAMA            = "MULTICOM COMPUTER ENTERPRISE"
NO_KENDERAAN    = "BRX6666"
TARIKH_MULA     = "27/06/2026"
TARIKH_TAMAT    = "26/07/2026"
AMAUN           = "RM 85.00"

# Fixed values (usually unchanged)
PBT              = "MAJLIS BANDARAYA IPOH"
JENIS_PENGGUNAAN = "PAS BULANAN"
OUTPUT_FILE      = "resit_penggunaan.pdf"
LOGO_PATH        = "logo.jpg"   # place logo.jpg in the same folder
# ─────────────────────────────────────────────────────────────


def draw_receipt(c, width, height):
    margin_left  = 20 * mm
    margin_right = width - 20 * mm
    y = height

    # ── Header (logo left, address right) — NO frame ───────
    header_top    = y - 10 * mm
    logo_size     = 22 * mm

    # Logo
    if os.path.exists(LOGO_PATH):
        c.drawImage(
            LOGO_PATH,
            margin_left,
            header_top - logo_size,
            width=logo_size,
            height=logo_size,
            preserveAspectRatio=True,
            mask="auto",
        )

    # Address text (right of logo)
    addr_x  = margin_left + logo_size + 5 * mm
    addr_y  = header_top - 7 * mm
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    for line in [
        "Bahagian Kerajaan Tempatan",
        "Aras B, Bangunan Perak Darul Ridzuan",
        "Jalan Panglima Bukit Gantang Wahab",
        "30000 Ipoh, Perak",
    ]:
        c.drawString(addr_x, addr_y, line)
        addr_y -= 4.5 * mm

    # ── Horizontal rule under header ───────────────────────
    rule_y = header_top - logo_size - 5 * mm
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.6)
    c.line(margin_left, rule_y, margin_right, rule_y)

    # ── Title ───────────────────────────────────────────────
    title_y = rule_y - 10 * mm
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(width / 2, title_y, "RESIT PENGGUNAAN")

    # ── Fields ──────────────────────────────────────────────
    col1_x   = margin_left
    col2_x   = margin_left + 52 * mm
    fields_y = title_y - 12 * mm
    row_h    = 8 * mm

    fields = [
        ("PBT",               PBT),
        ("ID Pengguna",       ""),
        ("Nama",              NAMA),
        ("No Kenderaan",      NO_KENDERAAN),
        ("Jenis Penggunaan",  JENIS_PENGGUNAAN),
        ("Tarikh Penggunaan", f"{TARIKH_MULA} - {TARIKH_TAMAT}"),
        ("Amaun",             AMAUN),
    ]

    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    for label, value in fields:
        c.drawString(col1_x, fields_y, label)
        c.drawString(col2_x, fields_y, value)
        fields_y -= row_h

    # ── Bottom rule ─────────────────────────────────────────
    bottom_rule_y = fields_y - 4 * mm
    c.setLineWidth(0.6)
    c.line(margin_left, bottom_rule_y, margin_right, bottom_rule_y)

    # ── Footer note ─────────────────────────────────────────
    c.setFont("Helvetica-Oblique", 8)
    note = "Nota: Dokumen ini adalah cetakan komputer. Tiada tandatangan diperlukan."
    c.drawCentredString(width / 2, bottom_rule_y - 7 * mm, note)


def main():
    page_w, page_h = A4
    c = canvas.Canvas(OUTPUT_FILE, pagesize=A4)
    draw_receipt(c, page_w, page_h)
    c.save()
    print(f"✅  Saved: {OUTPUT_FILE}")
    print(f"   Nama           : {NAMA}")
    print(f"   No Kenderaan   : {NO_KENDERAAN}")
    print(f"   Tarikh         : {TARIKH_MULA} - {TARIKH_TAMAT}")
    print(f"   Amaun          : {AMAUN}")


if __name__ == "__main__":
    main()
