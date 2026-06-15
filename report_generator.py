from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd
import os

def generate_pdf_report():
    if not os.path.exists("data/waste_data.csv"):
        return

    df = pd.read_csv("data/waste_data.csv")

    os.makedirs("outputs", exist_ok=True)

    pdf_file = "outputs/waste_report.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph("Smart Waste Management Report", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 12))

    for _, row in df.tail(20).iterrows():
        text = (
            f"Time: {row['Timestamp']} | "
            f"Fill: {row['Fill Percentage']}% | "
            f"Status: {row['Status']} | "
            f"Alert: {row['Alert']}"
        )

        elements.append(Paragraph(text, styles["BodyText"]))
        elements.append(Spacer(1, 6))

    doc.build(elements)

    return pdf_file