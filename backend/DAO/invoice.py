from datetime import date  
from typing import Optional, List, Tuple 
from pydantic import BaseModel

from DAO.product import Product
from DAO.client import Client
from DAO.employe import Employe
from DAO.clientDAO import ClientDAO
from DAO.employeDAO import EmployeDAO

class ProductInInvoice(BaseModel):
    id: int
    name: str
    quantity: int

class InvoiceModel(BaseModel):
    invoiceID: str
    employeID: str
    employeName: str
    clientID: str
    clientName: str
    date: date
    totalPrice: float
    products: List[ProductInInvoice] 

class Invoice:
    def __init__(self, invoiceID: str, employeId: str, clientId: str, products: List[Tuple[Product, int]], invoiceDate: Optional[date] = None, 
                 totalPrice: Optional[float] = None):
        self.invoiceID = invoiceID
        self.employeId = employeId
        self.clientId = clientId
        self.date = invoiceDate if invoiceDate is not None else date.today()
        self.products = products
        self.totalPrice = totalPrice if totalPrice is not None else self.calculatePrice(self.products)

    def __repr__(self):
        return (f"invoice(invoiceID={self.invoiceID}, employeId={self.employeId}, "
                f"clientId={self.clientId}, date={self.date}, totalPrice={self.totalPrice}, "
                f"products={self.products})")
    
    def calculatePrice(self, products: List[Tuple[Product, int]]) -> float:
        total = 0.0
        for product, amount in products:
            total += float(product.sellPrice * amount)
        return total
    
    def get_invoce_client(self) -> Client:
        return ClientDAO().get_client_by_id(self.clientId)
    
    def get_invoice_employe(self) -> Employe:
        return EmployeDAO().get_employee_by_id(self.employeId)

    def get_json(self) -> InvoiceModel:
        return InvoiceModel(
            invoiceID=self.invoiceID,
            employeID=self.employeId,
            employeName=self.get_invoice_employe().name,
            clientID=str(self.clientId),
            clientName=self.get_invoce_client().CompanyName,
            date=self.date,
            totalPrice=self.totalPrice,
            products=[ProductInInvoice(id=product.productId, name=product.name, quantity=amount) for product, amount in self.products]
        )
