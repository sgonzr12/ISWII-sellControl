from fastapi import Depends, APIRouter, HTTPException
from verificator import verifyTokenEmployee
from pydantic import BaseModel
from fastapi.responses import FileResponse
import os
import logging


from DAO.offerDAO import OfferDAO
from DAO.productDAO import ProductDAO
from DAO.product import Product
from DAO.offer import Offer
from DAO.offer import OfferModel

import pdf.offerPDF  as offerPDF





router = APIRouter()
offerDAO = OfferDAO()
productDAO = ProductDAO()
logger = logging.getLogger("appLogger")

@router.get("/", tags=["offer"], dependencies=[Depends(verifyTokenEmployee)])
async def get_all_offers(token: str = Depends(verifyTokenEmployee)) -> list[OfferModel]:
    """
    Get all offers
    """
    logger.debug("Offers requested")
    offers = offerDAO.get_all_offers()
    if not offers:
        return []
    offer_json = [offer.get_json() for offer in offers]
    logger.debug(f"Offers retrieved: {offer_json}")
    return offer_json

class createOfferModel(BaseModel):
    clientID: str
    products: list[dict[str, str]]

@router.post("/", tags=["offer"], dependencies=[Depends(verifyTokenEmployee)])
async def create_offer(offer: createOfferModel, token: dict[str,str] = Depends(verifyTokenEmployee)) -> None:
    """
    Create a new offer
    """
    
    logger.debug("Create offer requested")
    logger.debug(f"Offer data: {offer}")
    
    # Extract data from the request
    client_id = offer.clientID
    products_list = offer.products
    
    if not client_id:
        logger.error("Missing required fields")
        raise HTTPException(status_code=400, detail="Missing required fields")
    
    # Extract employee ID from the token
    employee_id = token["sub"]
    if not employee_id:
        logger.error("Unauthorized access")
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    products: list[tuple[Product, int]] = []
    logger.debug("processing products")
    for product_data in products_list:
        product_id = product_data.get("id")
        quantity = product_data.get("quantity")
        
        if not product_id or not quantity:
            logger.error("Missing required fields in products")
            raise HTTPException(status_code=400, detail="Missing required fields in products")
        
        # check product quantity > 0
        if int(quantity) <= 0:
            logger.error("Product quantity must be greater than 0")
            raise HTTPException(status_code=400, detail="Product quantity must be greater than 0")
        
        # Get the product from the database
        product = productDAO.get_product_by_id(int(product_id))
        if not product:
            logger.error(f"Product with ID {product_id} not found")
            raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")
        
        # Append the product and its quantity to the list
        products.append((product, int(quantity)))

        
    # Create the offer
    new_offer = Offer(
        employeId=employee_id,
        clientId=client_id,
        products=products
    )
    new_offer = offerDAO.create_offer(new_offer)
    if not new_offer:
        logger.error("Failed to create offer")
        raise HTTPException(status_code=500, detail="Failed to create offer")
    

class updateOfferModel(BaseModel):
    offerID: str
    products: list[dict[str, str]]
    

@router.put("/", tags=["offer"], dependencies=[Depends(verifyTokenEmployee)])
async def update_offer(offer: updateOfferModel, token: dict[str,str] = Depends(verifyTokenEmployee)) -> None:
    """
    Update an existing offer
    """
    logger.debug("Update offer requested")
    
    # Extract data from the request
    offer_id = offer.offerID
    products_data = offer.products
        
    if not offer_id:
        logger.error("Missing offer ID")
        raise HTTPException(status_code=400, detail="Missing offer ID")
    
    if not products_data:
        logger.error("No products provided")
        raise HTTPException(status_code=400, detail="At least one product is required")
    
    # Extract employee ID from the token
    employee_id = token.get("sub")
    if not employee_id:
        logger.error("Unauthorized access")
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    products: list[tuple[Product, int]] = []
    logger.debug("Processing products")

    for product_data in products_data:

        product_id = product_data.get("id")

        quantity = product_data.get("quantity")

        
        if not product_id or not quantity:
            logger.error("Missing required fields in products")
            raise HTTPException(status_code=400, detail="Missing required fields in products")
        
        # check product quantity > 0
        if int(quantity) <= 0:
            logger.error("Product quantity must be greater than 0")
            raise HTTPException(status_code=400, detail="Product quantity must be greater than 0")

        
        # Get the product from the database
        product = productDAO.get_product_by_id(int(product_id))
        if not product:
            logger.error(f"Product with ID {product_id} not found")
            raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")
        
        # Append the product and its quantity to the list
        products.append((product, int(quantity)))
    # find existing offer
    logger.debug(f"Finding offer with ID {offer_id}")
    existing_offer = offerDAO.get_offer_by_id(offer_id)
    if not existing_offer:
        logger.error(f"Offer with ID {offer_id} not found")
        raise HTTPException(status_code=404, detail=f"Offer with ID {offer_id} not found")
    # Update the offer
    existing_offer.set_products(products)
    
    logger.debug("Updating offer in database")
    new_offer = offerDAO.update_offer(existing_offer)
    
    if not new_offer:
        logger.error("Failed to update offer")
        raise HTTPException(status_code=500, detail="Failed to update offer")
    
    logger.debug(f"Offer {offer_id} updated successfully")

@router.get("/pdf", tags=["offer"], dependencies=[Depends(verifyTokenEmployee)])
async def get_offer_pdf(offerID: str, token: dict[str,str] = Depends(verifyTokenEmployee)):
    """
    Get the PDF of an offer
    """
    logger.debug("Get offer PDF requested")

    if not offerID:
        logger.error("Missing offer ID")
        raise HTTPException(status_code=400, detail="Missing offer ID")
    
    # Generate the PDF
    pdf_path = offerPDF.create_offer_pdf(offerID)
    
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
