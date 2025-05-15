from fastapi import Depends, APIRouter, HTTPException
from verificator import verifyTokenEmployee
import logging


from DAO.deliveryNoteDAO import DeliveryNoteDAO
from DAO.productDAO import ProductDAO
from DAO.invoiceDAO import InvoiceDAO
from DAO.invoice import Invoice
from DAO.invoice import InvoiceModel

router = APIRouter()
invoiceDAO = InvoiceDAO()
deliveryNoteDAO = DeliveryNoteDAO()
productDAO = ProductDAO()
logger = logging.getLogger("appLogger")

@router.get("/", tags=["invoice"], dependencies=[Depends(verifyTokenEmployee)])
async def get_all_invoices(token: str = Depends(verifyTokenEmployee)) -> list[InvoiceModel]:
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

@router.post("/", tags=["invoice"], dependencies=[Depends(verifyTokenEmployee)])
async def create_invoice(invoice_data: dict[str,str], token: dict[str,str] = Depends(verifyTokenEmployee)) -> None:
    """
    Create a new invoice
    """
    
    logger.debug("Create invoice requested")
    
    # Extract data from the request
    deliveryNoteID = invoice_data["DeliveryNoteID"]
        
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
    
    try:
        # check if the invoice already exists
        invoice = invoiceDAO.get_invoice_by_id(invoiceID)
        if invoice:
            logger.error("Invoice already exists")
            raise HTTPException(status_code=400, detail="Invoice already exists")
    except HTTPException as e:
        if e.status_code == 404:
            pass
        else:
            raise e
    # Create the invoice
    invoice = Invoice(
        invoiceID=invoiceID,
        employeId=employee_id,
        clientId=delivery_note.clientId,
        invoiceDate=delivery_note.date,
        totalPrice=delivery_note.totalPrice,
        products=delivery_note.products
    )
    