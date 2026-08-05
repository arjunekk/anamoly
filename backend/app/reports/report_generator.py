"""
Generates a PDF inspection report for a single inspection record.

Uses ReportLab to build a simple, structured one-page report containing
the original image, heatmap, and all inspection details — exactly the
fields specified in the original project spec.
"""

from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib import colors

from app.db.models import Inspection


def generate_inspection_report(inspection: Inspection, output_path: Path):
    """
    Args:
        inspection: an Inspection ORM record (already fetched from the DB).
        output_path: where to save the generated PDF.
    """
    c = canvas.Canvas(str(output_path), pagesize=A4)
    page_width, page_height = A4

    margin = 2 * cm
    y = page_height - margin

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(margin, y, "Inspection Report")
    y -= 1.2 * cm

    c.setFont("Helvetica", 10)
    c.setFillColor(colors.grey)
    c.drawString(margin, y, f"Inspection ID: {inspection.id}")
    y -= 1 * cm

    # Details table (as simple key-value lines, not a fancy Table object —
    # kept simple since this is a small, fixed set of fields)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 11)

    details = [
        ("Product Category", inspection.product_category),
        ("Anomaly Score", f"{inspection.anomaly_score:.4f}"),
        ("Severity", inspection.severity.upper()),
        ("Timestamp", inspection.timestamp.strftime("%Y-%m-%d %H:%M:%S")),
    ]

    for label, value in details:
        c.setFont("Helvetica-Bold", 11)
        c.drawString(margin, y, f"{label}:")
        c.setFont("Helvetica", 11)
        c.drawString(margin + 4 * cm, y, str(value))
        y -= 0.7 * cm

    y -= 0.3 * cm

    # Recommendations (may be multiple lines, stored as "; "-joined string)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin, y, "Recommendations:")
    y -= 0.7 * cm

    c.setFont("Helvetica", 10)
    for rec in inspection.recommendation.split("; "):
        c.drawString(margin + 0.5 * cm, y, f"- {rec}")
        y -= 0.6 * cm

    y -= 0.5 * cm

    # Images: original + heatmap, side by side
    image_display_size = 7 * cm

    original_path = Path(inspection.image_path)
    heatmap_path = Path(inspection.heatmap_path)

    if original_path.exists():
        c.drawImage(
            str(original_path),
            margin,
            y - image_display_size,
            width=image_display_size,
            height=image_display_size,
            preserveAspectRatio=True,
        )
        c.setFont("Helvetica", 9)
        c.drawCentredString(
            margin + image_display_size / 2,
            y - image_display_size - 0.5 * cm,
            "Original Image",
        )

    if heatmap_path.exists():
        heatmap_x = margin + image_display_size + 1 * cm
        c.drawImage(
            str(heatmap_path),
            heatmap_x,
            y - image_display_size,
            width=image_display_size,
            height=image_display_size,
            preserveAspectRatio=True,
        )
        c.drawCentredString(
            heatmap_x + image_display_size / 2,
            y - image_display_size - 0.5 * cm,
            "Anomaly Heatmap",
        )

    c.showPage()
    c.save()