from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen.canvas import Canvas
import os

from DAO.deliveryNoteDAO import DeliveryNoteDAO
from DAO.clientDAO import ClientDAO



deliveryNoteDAO = DeliveryNoteDAO()
clientDAO = ClientDAO()

def create_delivery_note_pdf(deliveryNoteID: str) -> str:
    filepath = "backend/pdf/"
    
    #clear the path (delete all pdf files in the directory)
    # Clear all PDF files in the directory
    for file in os.listdir(filepath):
        if file.endswith('.pdf'):
            os.remove(os.path.join(filepath, file))

    delivery_note = deliveryNoteDAO.get_delivery_note_by_id(deliveryNoteID)
    client = clientDAO.get_client_by_id(delivery_note.clientId)

    delivery_noteJSON = delivery_note.get_json()

    filename = f"{deliveryNoteID}_{delivery_note.date}.pdf"
    pdf_file = filepath + filename
    
    c = Canvas(pdf_file, pagesize=A4)
    width, height = A4
    styles = getSampleStyleSheet()

    # Margins
    x_margin = 30
    y = height - 50

    # 1. Logo and Company Info
    # Get the directory of the current script file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logopath = os.path.join(current_dir, "images", "sellcontrol.png")
    
    # Check if logo file exists before drawing
    if os.path.exists(logopath):
        c.drawImage(logopath, x_margin, y - 70, width=50, height=50, mask="auto",) #type:ignore
    else:
        print(f"Warning: Logo file not found at {logopath}")
    
    c.setFont("Helvetica-Bold", 20)
    c.drawString(x_margin + 100, y - 30, "sellcontrol")  # Moved text more to the left

    # 2. delivery note metadata
    # Create a header style for the title
    header_style = styles['Normal'].clone('DeliveryNoteHeaderStyle')
    header_style.textColor = colors.white

    delivery_note_info = [
        [Paragraph("<b>Delivery Note Information</b>", header_style)],
        [Paragraph(
            f"<b>creation date:</b> {delivery_note.date}<br/>"
            f"<b>Delivery Note ID:</b> {deliveryNoteID}<br/>"
            f"<b>created by:</b> {delivery_noteJSON.employeName}<br/>",
            styles["Normal"]) 
        ]
    ]
    
    # Create the table with proper column structure
    delivery_note_table = Table(delivery_note_info, colWidths=[250])
    delivery_note_table.setStyle(TableStyle([
        ("GRID", (0, 1), (-1, -1), 0.5, colors.grey),  # Grid only for data rows
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("BACKGROUND", (0, 0), (0, 0), colors.darkblue),  # Header background color
        ("ALIGN", (0, 0), (0, 0), "CENTER"),  # Center the header text
    ]))

    # Draw the delivery note table on the canvas
    delivery_note_table.wrapOn(c, width, height)
    delivery_note_table.drawOn(c, width - x_margin - 250, y - 150)
    
    # 3. Client Sections
    # Create a white text style for the header
    header_style = styles['Normal'].clone('HeaderStyle')
    header_style.textColor = colors.white
    
    address_data = [
        [
            Paragraph("<b>Client</b>", header_style),
        ],
        [
            Paragraph(
                f"<b>Company Name:</b> {client.CompanyName}<br/>"
                f"<b>Address:</b> {client.address}<br/>"
                f"<b>Phone:</b> {str(client.phone)}", 
                styles["Normal"]
            ),
        ]
    ]
    address_table = Table(address_data, colWidths=[width/2 - x_margin, width/2 - x_margin])
    address_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    address_table.wrapOn(c, width, height)
    address_table.drawOn(c, x_margin, y - 250)

    # 4. Product Table
    product_data = [["Product ID", "Product Name", "Description", "Quantity", "Unit Price", "Total Price"]]
    for product, quantity in delivery_note.products:
        unit_price = product.sellPrice
        total_price = quantity * unit_price
        product_data.append([
            str(product.productId),
            product.name,
            product.description,
            str(quantity),
            f"{unit_price:.2f} €",
            f"{total_price:.2f} €"
        ])
    product_table = Table(product_data, colWidths=[60, 100, 140, 60, 80, 80])
    product_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ]))
    product_table.wrapOn(c, width, height)
    product_table.drawOn(c, x_margin, y - 400)


    # Total Price
    c.setFont("Helvetica-Bold", 14)
    c.drawRightString(width - x_margin, 100, f"TOTAL DELIVERY NOTE PRICE: {delivery_note.totalPrice:.2f} €")

    c.save()
    
    # Return the path to the PDF file
    return pdf_file
