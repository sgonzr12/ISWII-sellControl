from fastapi import Depends, APIRouter, HTTPException
from verificator import  verifyTokenEmployee, verifyTokenCreateOrder
from fastapi.responses import FileResponse
import os
import logging

from DAO.offerDAO import OfferDAO
from DAO.productDAO import ProductDAO
from DAO.orderDAO import OrderDAO
from DAO.order import Order
from DAO.order import OrderModel
import pdf.orderPDF  as orderPDF

router = APIRouter()
orderDAO = OrderDAO()
offerDAO = OfferDAO()
productDAO = ProductDAO()
logger = logging.getLogger("appLogger")

@router.get("/", tags=["order"], dependencies=[Depends(verifyTokenEmployee)])
async def get_all_orders(token: str = Depends(verifyTokenEmployee)) -> list[OrderModel]:
    """
    Get all orders
    """
    logger.debug("Orders requested")
    orders = orderDAO.get_all_orders()
    if not orders:
        return []
    order_json = [order.get_json() for order in orders]
    logger.debug(f"Orders retrieved: {order_json}")
    return order_json

@router.post("/", tags=["order"], dependencies=[Depends(verifyTokenCreateOrder)])
async def create_order(offer_data: dict[str,str], token: dict[str,str] = Depends(verifyTokenEmployee)) -> None:
    """
    Create a new order
    """
    
    logger.debug("Create order requested")
    
    # Extract data from the request
    offerID = offer_data["offerID"]

    if not offerID:
        logger.error("Missing required fields")
        raise HTTPException(status_code=400, detail="Missing required fields")
    
    # Extract employee ID from the token
    employee_id = token["sub"]
    if not employee_id:
        logger.error("Unauthorized access")
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Get offer information from the ID
    offer = offerDAO.get_offer_by_id(offerID)
    
    if not offer:
        logger.error("Offer not found")
        raise HTTPException(status_code=404, detail="Offer not found")
    
    # format the order ID offerID = "of-xxxxxx" orderID = "or-xxxxxx" with the same xxxxxx
    orderID = "or-" + offerID[3:]
    
    # check if the order already exists
    existing_order = orderDAO.check_order_exists(orderID)
    if existing_order:
        logger.error("Order already exists")
        raise HTTPException(status_code=400, detail="Order already exists")
    # Create the order 
    order = Order(orderID=orderID, employeId=employee_id, clientId=offer.clientID, products=offer.products)
    orderDAO.create_order(order)
    logger.debug(f"Order created: {order.get_json()}")

@router.get("/pdf", tags=["order"], dependencies=[Depends(verifyTokenEmployee)])
async def get_order_pdf(orderID: str, token: dict[str,str] = Depends(verifyTokenEmployee)):
    """
    Get the PDF of an order
    """
    logger.debug("Get order PDF requested")

    if not orderID:
        logger.error("Missing order ID")
        raise HTTPException(status_code=400, detail="Missing order ID")

    # Generate the PDF
    pdf_path = orderPDF.create_order_pdf(orderID)

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

    
