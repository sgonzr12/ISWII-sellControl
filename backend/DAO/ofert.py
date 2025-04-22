from datetime import date  # Add this import at the top of the file if not already present
from product import Product  # Adjust the import based on your project structure
from typing import Optional, List, Tuple  # Add these imports at the top of the file if not already present

class Ofert:
    def __init__(self, ofertID: int, employeId: int, clientId: int, ofert_date: Optional[date] = None, 
                 totalPrize: Optional[float] = None, products: Optional[List[Tuple[Product, int]]] = None):
        self.ofertID = ofertID
        self.employeId = employeId
        self.clientId = clientId
        self.date = ofert_date if ofert_date is not None else date.today()
        self.products = products if products is not None else []
        self.totalPrize = totalPrize if totalPrize is not None else self.calculatePrice(self.products)

    def __repr__(self):
        return (f"Ofert(ofertID={self.ofertID}, employeId={self.employeId}, "
                f"clientId={self.clientId}, date={self.date}, totalPrize={self.totalPrize}, "
                f"products={self.products})")
    
    def calculatePrice(self, products: List[Tuple[Product, int]]) -> float:
        total = 0.0
        for product, amount in products:
            total += product.sellPrize * amount
        return total
