import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import io
import os

# ── Page config ────────────────────────────────────────────
st.set_page_config(
    page_title="Resit Penggunaan - Park@Perak",
    page_icon="🅿️",
    layout="centered",
)

st.image("logo.jpg", width=160)
st.title("Resit Penggunaan")
st.markdown("Isi maklumat di bawah dan klik **Jana PDF** untuk muat turun resit.")
st.divider()

# ── Form ───────────────────────────────────────────────────
with st.form("resit_form"):
    pbt = st.text_input("PBT", value="MAJLIS BANDARAYA IPOH")
    nama = st.text_input("Nama", value="MULTICOM COMPUTER ENTERPRISE")
    no_kenderaan = st.text_input("No Kenderaan", value="BRX6666")
    jenis = st.text_input("Jenis Penggunaan", value="PAS BULANAN")

    col1, col2 = st.columns(2)
    with col1:
        tarikh_mula = st.text_input("Tarikh Mula (DD/MM/YYYY)", value="27/06/2026")
    with col2:
        tarikh_tamat = st.text_input("Tarikh Tamat (DD/MM/YYYY)", value="26/07/2026")

    amaun = st.text_input("Amaun", value="RM 85.00")

    submitted = st.form_submit_button("🖨️ Jana PDF", use_container_width=True, type="primary")

# ── Generate PDF ───────────────────────────────────────────
def generate_pdf(pbt, nama, no_kenderaan, jenis, tarikh_mula, tarikh_tamat, amaun):
    buffer = io.BytesIO()
    page_w, page_h = A4
    c = canvas.Canvas(buffer, pagesize=A4)

    margin_left  = 20 * mm
    margin_right = page_w - 20 * mm
    y = page_h

    # ── Header ─────────────────────────────────────────────
    header_top = y - 10 * mm
    logo_size  = 22 * mm

    logo_path = "logo.jpg"
    if os.path.exists(logo_path):
        c.drawImage(
            logo_path,
            margin_left,
            header_top - logo_size,
            width=logo_size,
            height=logo_size,
            preserveAspectRatio=True,
            mask="auto",
        )

    addr_x = margin_left + logo_size + 5 * mm
    addr_y = header_top - 7 * mm
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

    # ── Divider ────────────────────────────────────────────
    rule_y = header_top - logo_size - 5 * mm
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.6)
    c.line(margin_left, rule_y, margin_right, rule_y)

    # ── Title ──────────────────────────────────────────────
    title_y = rule_y - 10 * mm
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(page_w / 2, title_y, "RESIT PENGGUNAAN")

    # ── Fields ─────────────────────────────────────────────
    col1_x   = margin_left
    col2_x   = margin_left + 52 * mm
    fields_y = title_y - 12 * mm
    row_h    = 8 * mm

    fields = [
        ("PBT",               pbt),
        ("ID Pengguna",       ""),
        ("Nama",              nama),
        ("No Kenderaan",      no_kenderaan),
        ("Jenis Penggunaan",  jenis),
        ("Tarikh Penggunaan", f"{tarikh_mula} - {tarikh_tamat}"),
        ("Amaun",             amaun),
    ]

    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    for label, value in fields:
        c.drawString(col1_x, fields_y, label)
        c.drawString(col2_x, fields_y, value)
        fields_y -= row_h

    # ── Bottom rule ────────────────────────────────────────
    bottom_rule_y = fields_y - 4 * mm
    c.setLineWidth(0.6)
    c.line(margin_left, bottom_rule_y, margin_right, bottom_rule_y)

    # ── Footer ─────────────────────────────────────────────
    c.setFont("Helvetica-Oblique", 8)
    note = "Nota: Dokumen ini adalah cetakan komputer. Tiada tandatangan diperlukan."
    c.drawCentredString(page_w / 2, bottom_rule_y - 7 * mm, note)

    c.save()
    buffer.seek(0)
    return buffer


if submitted:
    if not nama or not no_kenderaan or not tarikh_mula or not tarikh_tamat:
        st.error("Sila isi semua medan yang diperlukan.")
    else:
        pdf_buffer = generate_pdf(
            pbt, nama, no_kenderaan, jenis, tarikh_mula, tarikh_tamat, amaun
        )
        filename = f"resit_{no_kenderaan}_{tarikh_mula.replace('/', '-')}.pdf"
        st.success("✅ PDF berjaya dijana!")
        st.download_button(
            label="⬇️ Muat Turun PDF",
            data=pdf_buffer,
            file_name=filename,
            mime="application/pdf",
            use_container_width=True,
        )
