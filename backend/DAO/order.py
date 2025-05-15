from pydantic import BaseModel
from datetime import date  
from typing import Optional, List, Tuple  

from DAO.employeDAO import EmployeDAO
from DAO.clientDAO import ClientDAO
from DAO.product import Product
from DAO.client import Client
from DAO.employe import Employe

class ProductInOrder(BaseModel):
    id: int
    name: str
    quantity: int

class OrderModel(BaseModel):
    orderID: str
    employeID: str
    employeName: str
    clientID: str
    clientName: str
    date: date
    totalPrice: float
    products: List[ProductInOrder]

class Order:
    def __init__(self, orderID: str, employeId: str, clientId: str, products:List[Tuple[Product, int]], orderDate: Optional[date] = None, 
                 totalPrice: Optional[float] = None):
        self.orderID = orderID
        self.employeId = employeId
        self.clientId = clientId
        self.date = orderDate if orderDate is not None else date.today()
        self.products = products
        self.totalPrice = totalPrice if totalPrice is not None else self.calculatePrice(self.products)

    def __repr__(self):
        return (f"order(orderID={self.orderID}, employeId={self.employeId}, "
                f"clientId={self.clientId}, date={self.date}, totalPrice={self.totalPrice}, "
                f"products={self.products})")
    
    def calculatePrice(self, products: List[Tuple[Product, int]]) -> float:
        total = 0.0
        for product, amount in products:
            total += product.sellPrice * amount
        return total
    
    def get_order_client(self) -> Client:
        return ClientDAO().get_client_by_id(self.clientId)
    
    def get_order_employe(self) -> Employe:
        return EmployeDAO().get_employee_by_id(self.employeId)
    
    def get_json(self) -> OrderModel:
        return OrderModel(
            orderID=self.orderID,
            employeID=self.employeId,
            employeName=self.get_order_employe().name,
            clientID=str(self.clientId),
            clientName=self.get_order_client().CompanyName,
            date=self.date,
            totalPrice=self.TotalPrice,
            products=[ProductInOrder(id=product.productId, name=product.name, quantity=amount) for product, amount in self.products]
        )
    
    def set_products(self, products: List[tuple[Product, int]]) -> None:
        self.products = products
        self.TotalPrice = self.calculatePrice(products)
