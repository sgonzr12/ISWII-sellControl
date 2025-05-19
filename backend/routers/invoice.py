from fastapi import Depends, APIRouter, HTTPException
from verificator import verifyTokenInvoice
from fastapi.responses import FileResponse
import os
import logging

from DAO.deliveryNoteDAO import DeliveryNoteDAO
from DAO.productDAO import ProductDAO
from DAO.invoiceDAO import InvoiceDAO
from DAO.invoice import Invoice
from DAO.invoice import InvoiceModel
import pdf.invoicePDF  as invoicePDF

router = APIRouter()
invoiceDAO = InvoiceDAO()
deliveryNoteDAO = DeliveryNoteDAO()
productDAO = ProductDAO()
logger = logging.getLogger("appLogger")

@router.get("/", tags=["invoice"], dependencies=[Depends(verifyTokenInvoice)])
async def get_all_invoices(token: str = Depends(verifyTokenInvoice)) -> list[InvoiceModel]:
    """
    Get all invoices
    """
    logger.debug("Invoices requested")
    invoices = invoiceDAO.get_all_invoices()
    if not invoices:
        return []
    invoice_json = [invoice.get_json() for invoice in invoices]
    logger.debug(f"Invoices retrieved: {invoice_json}")
    return invoice_json

@router.post("/", tags=["invoice"], dependencies=[Depends(verifyTokenInvoice)])
async def create_invoice(deliveryNote_data: dict[str,str], token: dict[str,str] = Depends(verifyTokenInvoice)) -> None:
    """
    Create a new invoice
    """
    
    logger.debug("Create invoice requested")
    
    # Extract data from the request
    deliveryNoteID = deliveryNote_data["DeliveryNoteID"]

    if not deliveryNoteID:
        logger.error("Missing required fields")
        raise HTTPException(status_code=400, detail="Missing required fields")
    
    # Extract employee ID from the token
    employee_id = token["sub"]
    if not employee_id:
        logger.error("Unauthorized access")
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Get delivery note information from the ID
    delivery_note = deliveryNoteDAO.get_delivery_note_by_id(deliveryNoteID)
    if not delivery_note:
        logger.error("Delivery note not found")
        raise HTTPException(status_code=404, detail="Delivery note not found")
    
    # format the invoice ID clientID = "cl-xxxxxx" invoiceID = "in-xxxxxx" with the same xxxxxx
    invoiceID = "in-" + deliveryNoteID[3:]
    
    # check if the invoice already exists
    existing_invoice = invoiceDAO.check_invoice_exists(invoiceID)
    if existing_invoice:
        logger.error("Invoice already exists")
        raise HTTPException(status_code=400, detail="Invoice already exists")
    # Create the invoice
    invoice = Invoice(
        invoiceID=invoiceID,
        employeId=employee_id,
        clientId=delivery_note.clientId,
        invoiceDate=delivery_note.date,
        totalPrice=delivery_note.totalPrice,
        products=delivery_note.products
    )
    
    # Create the invoice in the database
    invoiceDAO.create_invoice(invoice)
    logger.debug(f"Invoice created: {invoice.get_json()}")

@router.get("/pdf", tags=["invoice"], dependencies=[Depends(verifyTokenInvoice)])
async def get_invoice_pdf(invoiceID: str, token: dict[str,str] = Depends(verifyTokenInvoice)):
    """
    Get the PDF of an invoice
    """
    logger.debug("Get invoice PDF requested")

    if not invoiceID:
        logger.error("Missing invoice ID")
        raise HTTPException(status_code=400, detail="Missing invoice ID")

    # Generate the PDF
    pdf_path = invoicePDF.create_invoice_pdf(invoiceID)

    #extract the filename from the path
    filename = os.path.basename(pdf_path)
    
    if not pdf_path or not os.path.exists(pdf_path):
        logger.error("Failed to generate PDF")
        raise HTTPException(status_code=500, detail="Failed to generate PDF")
    
    return FileResponse(
        path=pdf_path, 
        filename=filename,
        media_type="application/pdf"
    )
    