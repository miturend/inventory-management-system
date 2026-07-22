from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


def generate_receipt(filename, sale, items, total):

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(
        Paragraph("<b>OKEYSAM INVENTORY SYSTEM</b>", styles["Title"])
    )

    elements.append(
        Paragraph("Sales Receipt", styles["Heading2"])
    )

    elements.append(
        Paragraph(f"Sale ID: {sale['SaleID']}", styles["Normal"])
    )

    elements.append(
        Paragraph(f"Customer: {sale['CustomerName']}", styles["Normal"])
    )

    elements.append(
        Paragraph(f"Date: {sale['SaleDate']}", styles["Normal"])
    )

    data = [["Product", "Qty", "Unit Price", "Total"]]

    for item in items:
        data.append([
            item["ProductName"],
            str(item["Quantity"]),
            f"₦{item['UnitPrice']:,.2f}",
            f"₦{item['TotalAmount']:,.2f}"
        ])

    data.append(["", "", "TOTAL", f"₦{total:,.2f}"])

    table = Table(data)

    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BACKGROUND", (0, -1), (-1, -1), colors.lightgrey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))

    elements.append(table)

    doc.build(elements)