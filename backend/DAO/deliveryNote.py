from datetime import date
from typing import Optional, List, Tuple
from pydantic import BaseModel
import logging

  
from DAO.product import Product 
from DAO.client import Client
from DAO.employe import Employe
from DAO.clientDAO import ClientDAO
from DAO.employeDAO import EmployeDAO

class ProductInDeliveryNote(BaseModel):
    id: int
    name: str
    quantity: int

class DeliveryNoteModel(BaseModel):
    DeliveryNoteID: str
    employeID: str
    employeName: str
    clientID: str
    clientName: str
    date: date
    totalPrice: float
    products: List[ProductInDeliveryNote]
 

class DeliveryNote:
    def __init__(self, deliveryNoteID: str, employeId: str, clientId: str, products: List[Tuple[Product, int]], deliveryNoteDate: Optional[date] = None, 
                 totalPrice: Optional[float] = None):
        self.deliveryNoteID = deliveryNoteID
        self.employeId = employeId
        self.clientId = clientId
        self.date = deliveryNoteDate if deliveryNoteDate is not None else date.today()
        self.products = products
        self.totalPrice = totalPrice if totalPrice is not None else self.calculatePrice(self.products)
        self.logger = logging.getLogger("appLogger")

    def __repr__(self):
        return (f"deliveryNote(deliveryNoteID={self.deliveryNoteID}, employeId={self.employeId}, "
                f"clientId={self.clientId}, date={self.date}, totalPrice={self.totalPrice}, "
                f"products={self.products})")
    
    def calculatePrice(self, products: List[Tuple[Product, int]]) -> float:
        total = 0.0
        for product, amount in products:
            total += float(product.sellPrice * amount)
        return total
    
    def get_deliveryNote_client(self) -> Client:
        return ClientDAO().get_client_by_id(self.clientId)
    
    def get_deliveryNote_employe(self) -> Employe:
        return EmployeDAO().get_employee_by_id(self.employeId)

    def get_json(self) -> DeliveryNoteModel:
        return DeliveryNoteModel(
            DeliveryNoteID=self.deliveryNoteID,
            employeID=self.employeId,
            employeName=self.get_deliveryNote_employe().name,
            clientID=str(self.clientId),
            clientName=self.get_deliveryNote_client().CompanyName,
            date=self.date,
            totalPrice=self.TotalPrice,
            products=[ProductInDeliveryNote(id=product.productId, name=product.name, quantity=amount) for product, amount in self.products]
        )
    
    def set_products(self, products: List[tuple[Product, int]]) -> None:
        self.products = products
        self.TotalPrice = self.calculatePrice(products)