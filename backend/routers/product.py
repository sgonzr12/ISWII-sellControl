from fastapi import Depends, APIRouter
from backend.verificator import verifyToken, verifyTokenCURProduct

from DAO.productDAO import ProductDAO
from DAO.product import Product

router = APIRouter()
productDAO = ProductDAO()

@router.get("/", tags=["products"], dependencies=[Depends(verifyToken)])
async def get_all_products(token: str = Depends(verifyToken)) -> list[dict[str, str]]:
    """
    Get all products
    """
    print("Products requested")
    products = productDAO.get_all_products()
    return [product.get_product_JSON() for product in products]

@router.put("/", tags=["products"], dependencies=[Depends(verifyTokenCURProduct)])
async def update_product(product: dict[str, str], token: str = Depends(verifyToken)) -> dict[str, str]:
    """
    Update a product
    """
    print("Product update requested")
    productId = int(product["productId"])
    name = product["name"]
    description = product["description"]
    stock = product["stock"]
    maxStock = product["maxStock"]
    minStock = product["minStock"]
    location = product["location"]
    purchasePrize = product["purchasePrize"]
    sellPrize = product["sellPrize"]
    
    new_product = Product(productId=productId, name=name, description=description, stock=int(stock), maxStock=int(maxStock), minStock=int(minStock), location=location, purchasePrize=float(purchasePrize), sellPrize=float(sellPrize))
       
    #Verify the product
    if not new_product.verify_product():
        print("Product verification failed")
        raise ValueError("Product verification failed")

    #Update the product
    updated_product = productDAO.update_product(new_product)
    return updated_product.get_product_JSON()

@router.post("/", tags=["products"], dependencies=[Depends(verifyToken)])
async def create_product(product: dict[str, str], token: str = Depends(verifyToken)) -> dict[str, str]:
    """
    Create a new product
    """
    print("Product creation requested")
    name = product["name"]
    description = product["description"]
    stock = product["stock"]
    maxStock = product["maxStock"]
    minStock = product["minStock"]  
    location = product["location"]
    purchasePrize = product["purchasePrize"]
    sellPrize = product["sellPrize"]
    
    #Create the product
 
    new_product = Product(name=name, description=description, stock=int(stock), maxStock=int(maxStock), minStock=int(minStock), location=location, purchasePrize=float(purchasePrize), sellPrize=float(sellPrize))
    
    #Verify the product
    if not new_product.ready_to_insert():
        print("Product verification failed")
        raise ValueError("Product verification failed")
    
    new_product = productDAO.create_product(new_product)
    return new_product.get_product_JSON()
    