from fastapi import Depends, APIRouter, HTTPException
from verificator import verifyTokenEmployee
import logging


from DAO.offerDAO import OfferDAO
from DAO.productDAO import ProductDAO
from DAO.orderDAO import OrderDAO
from DAO.order import Order
from DAO.order import OrderModel

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

@router.post("/", tags=["order"], dependencies=[Depends(verifyTokenEmployee)])
async def create_order(orfer_data: dict[str,str], token: dict[str,str] = Depends(verifyTokenEmployee)) -> None:
    """
    Create a new order
    """
    
    logger.debug("Create order requested")
    
    # Extract data from the request
    offerID = orfer_data["offerID"]
    
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
    
    # Check if the order already exists
    existing_order = orderDAO.get_order_by_id(orderID)
    if existing_order:
        logger.error("Order already exists")
        raise HTTPException(status_code=400, detail="Order already exists")
    
    # Create the order 
    order = Order(orderID=orderID, employeId=employee_id, clientId=offer.clientID, products=offer.products)
    orderDAO.create_order(order)
    logger.debug(f"Order created: {order.get_json()}")
    
