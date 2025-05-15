from datetime import date  
from typing import Optional, List  
from pydantic import BaseModel

from DAO.product import Product  
from DAO.clientDAO import ClientDAO
from DAO.client import Client
from DAO.employeDAO import EmployeDAO
from DAO.employe import Employe

class ProductInOffer(BaseModel):
    id: int
    name: str
    quantity: int

class OfferModel(BaseModel):
    offerID: str
    employeID: str
    employeName: str
    clientID: str
    clientName: str
    date: date
    totalPrice: float
    products: List[ProductInOffer]


class Offer:
    def __init__(self, employeId: str, clientId: str, products:List[tuple[Product, int]], offer_date: Optional[date] = None, 
                 TotalPrice: Optional[float] = None, offerID: str = ""):
        self.offerID = offerID
        self.employeID = employeId
        self.clientID = clientId
        self.date = offer_date if offer_date is not None else date.today()
        self.products = products
        self.TotalPrice = TotalPrice if TotalPrice is not None else self.calculatePrice(self.products)

    def __repr__(self):
        return (f"offer(offerID={self.offerID}, employeId={self.employeID}, "
                f"clientId={self.clientID}, date={self.date}, TotalPrice={self.TotalPrice}, "
                f"products={self.products})")
        
    def get_offer_client(self) -> Client:
        return ClientDAO().get_client_by_id(self.clientID)
    
    def get_offer_employe(self) -> Employe:
        return EmployeDAO().get_employee_by_id(self.employeID)
    
    def calculatePrice(self, products: List[tuple[Product, int]]) -> float:
        total = 0.0
        for product, amount in products:
            total += float(product.sellPrice * amount)
        return total
    
    def get_json(self) -> OfferModel:
        return OfferModel(
            offerID=self.offerID,
            employeID=self.employeID,
            employeName=self.get_offer_employe().name,
            clientID=str(self.clientID),
            clientName=self.get_offer_client().CompanyName,
            date=self.date,
            totalPrice=self.TotalPrice,
            products=[ProductInOffer(id=product.productId, name=product.name, quantity=amount) for product, amount in self.products]
        )
    
    def set_products(self, products: List[tuple[Product, int]]) -> None:
        self.products = products
        self.TotalPrice = self.calculatePrice(products)

