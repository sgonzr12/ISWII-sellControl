from datetime import date  
from product import Product
from typing import Optional, List, Tuple  

class Order:
    def __init__(self, orderID: int, employeId: int, clientId: int, orderDate: Optional[date] = None, 
                 totalPrize: Optional[float] = None, products: Optional[List[Tuple[Product, int]]] = None):
        self.orderID = orderID
        self.employeId = employeId
        self.clientId = clientId
        self.date = orderDate if orderDate is not None else date.today()
        self.products = products if products is not None else []
        self.totalPrize = totalPrize if totalPrize is not None else self.calculatePrice(self.products)

    def __repr__(self):
        return (f"order(orderID={self.orderID}, employeId={self.employeId}, "
                f"clientId={self.clientId}, date={self.date}, totalPrize={self.totalPrize}, "
                f"products={self.products})")
    
    def calculatePrice(self, products: List[Tuple[Product, int]]) -> float:
        total = 0.0
        for product, amount in products:
            total += product.sellPrice * amount
        return total
