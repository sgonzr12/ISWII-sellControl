from datetime import date  
from product import Product
from typing import Optional, List, Tuple  

class deliveryNote:
    def __init__(self, deliveryNoteID: int, employeId: int, clientId: int, deliveryNoteDate: Optional[date] = None, 
                 totalPrize: Optional[float] = None, products: Optional[List[Tuple[Product, int]]] = None):
        self.deliveryNoteID = deliveryNoteID
        self.employeId = employeId
        self.clientId = clientId
        self.date = deliveryNoteDate if deliveryNoteDate is not None else date.today()
        self.products = products if products is not None else []
        self.totalPrize = totalPrize if totalPrize is not None else self.calculatePrice(self.products)

    def __repr__(self):
        return (f"deliveryNote(deliveryNoteID={self.deliveryNoteID}, employeId={self.employeId}, "
                f"clientId={self.clientId}, date={self.date}, totalPrize={self.totalPrize}, "
                f"products={self.products})")
    
    def calculatePrice(self, products: List[Tuple[Product, int]]) -> float:
        total = 0.0
        for product, amount in products:
            total += product.sellPrize * amount
        return total
