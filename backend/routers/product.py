from fastapi import Depends, APIRouter, HTTPException

from verificator import verifyToken, verifyTokenCURProduct, verifyTokenEmployee

from DAO.productDAO import ProductDAO
from DAO.product import Product

router = APIRouter()
productDAO = ProductDAO()

@router.get("/", tags=["product"], dependencies=[Depends(verifyTokenEmployee)])
async def get_all_products(token: str = Depends(verifyToken)) -> list[dict[str, str]]:
    """
    Get all products
    """
    print("Products requested")
    products = productDAO.get_all_products()
    return [product.get_product_JSON() for product in products]

@router.put("/", tags=["product"], dependencies=[Depends(verifyTokenCURProduct)])
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
    purchasePrice = product["purchasePrice"]
    sellPrice = product["sellPrice"]
    
    new_product = Product(productId=productId, name=name, description=description, stock=int(stock), maxStock=int(maxStock), minStock=int(minStock), purchasePrice=float(purchasePrice), sellPrice=float(sellPrice))

    #Verify the product
    if not new_product.verify_product():
        print("Product verification failed")
        raise HTTPException(status_code=400, detail="Product verification failed")

    #Update the product
    updated_product = productDAO.update_product(new_product)
    return updated_product.get_product_JSON()

@router.post("/", tags=["product"], dependencies=[Depends(verifyTokenCURProduct)])
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
    purchasePrice = product["purchasePrice"]
    sellPrice = product["sellPrice"]
    
    #Create the product
    new_product = Product(name=name, description=description, stock=int(stock), maxStock=int(maxStock), minStock=int(minStock), purchasePrice=float(purchasePrice), sellPrice=float(sellPrice))

    
    #Verify the product
    if not new_product.ready_to_insert():
        print("Product verification failed")
        raise HTTPException(status_code=400, detail="Product verification failed")

    
    new_product = productDAO.create_product(new_product)
    return new_product.get_product_JSON()
    