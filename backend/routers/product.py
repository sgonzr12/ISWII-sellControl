from fastapi import Depends, APIRouter
from backend.verificator import verifyToken, verifyTokenCURProduct

from DAO.productDAO import ProductDAO

router = APIRouter()
productDAO = ProductDAO()

@router.get("/", tags=["products"], dependencies=[Depends(verifyTokenCURProduct)])
async def get_all_products(token: str = Depends(verifyToken)) -> list[dict[str, str]]:
    """
    Get all products
    """
    print("Products requested")
    products = productDAO.get_all_products()
    return [product.get_product_JSON() for product in products]