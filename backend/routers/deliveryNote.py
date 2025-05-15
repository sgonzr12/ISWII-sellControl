from fastapi import Depends, APIRouter, HTTPException
from verificator import verifyTokenEmployee
import logging


from DAO.deliveryNoteDAO import DeliveryNoteDAO
from DAO.productDAO import ProductDAO
from DAO.orderDAO import OrderDAO
from DAO.deliveryNote import DeliveryNote
from DAO.deliveryNote import DeliveryNoteModel

router = APIRouter()
orderDAO = OrderDAO()
deliveryNoteDAO = DeliveryNoteDAO()
productDAO = ProductDAO()
logger = logging.getLogger("appLogger")

@router.get("/", tags=["deliveryNote"], dependencies=[Depends(verifyTokenEmployee)])
async def get_all_delivery_notes(token: str = Depends(verifyTokenEmployee)) -> list[DeliveryNoteModel]:
    """
    Get all delivery notes
    """
    logger.debug("Delivery notes requested")
    delivery_notes = deliveryNoteDAO.get_all_delivery_notes()
    if not delivery_notes:
        return []
    delivery_note_json = [delivery_note.get_json() for delivery_note in delivery_notes]
    logger.debug(f"Delivery notes retrieved: {delivery_note_json}")
    return delivery_note_json

@router.post("/", tags=["deliveryNote"], dependencies=[Depends(verifyTokenEmployee)])
async def create_delivery_note(order_data: dict[str,str], token: dict[str,str] = Depends(verifyTokenEmployee)) -> None:
    """
    Create a new delivery note
    """
    
    logger.debug("Create delivery note requested")
    
    # Extract data from the request
    orderID = order_data["orderID"]
    
    if not orderID:
        logger.error("Missing required fields")
        raise HTTPException(status_code=400, detail="Missing required fields")
    
    # Extract employee ID from the token
    employee_id = token["sub"]
    if not employee_id:
        logger.error("Unauthorized access")
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Get order information from the ID
    order = orderDAO.get_order_by_id(orderID)
    if not order:
        logger.error("Order not found")
        raise HTTPException(status_code=404, detail="Order not found")
    

    
    # format the delivery note ID clientID = "cl-xxxxxx" deliveryNoteID = "dn-xxxxxx" with the same xxxxxx
    deliveryNoteID = "dn-" + orderID[3:]
    
    # Check if the order is already delivered
    existing_delivery_note = deliveryNoteDAO.check_delivery_note_exists(deliveryNoteID)
    if existing_delivery_note:
        logger.error("Delivery note already exists")
        raise HTTPException(status_code=400, detail="Delivery note already exists")
    # Create a new DeliveryNote object
    delivery_note = DeliveryNote(
        deliveryNoteID=deliveryNoteID,
        employeId=employee_id,
        clientId=order.clientId,
        products=order.products,
    )
    
    # Insert the new delivery note into the database
    try:
        delivery_note_id = deliveryNoteDAO.create_delivery_note(delivery_note)
        logger.info(f"Delivery note created with ID: {delivery_note_id}")
    except Exception as e:
        logger.error(f"Failed to create delivery note: {e}")
        raise HTTPException(status_code=500, detail="Failed to create delivery note")