class Product:
    def __init__(self, productId: int, name: str, description: str, stock: int, maxStock: int, minStock: int, location: str, purchasePrize: float, sellPrize: float):
        self.productId = productId
        self.name = name
        self.description = description
        self.stock = stock
        self.maxStock = maxStock
        self.minStock = minStock
        self.location = location
        self.purchasePrize = purchasePrize
        self.sellPrize = sellPrize

    def __repr__(self):
        return (f"Product(productId={self.productId}, name={self.name}, "
                f"description={self.description}, stock={self.stock}, maxStock={self.maxStock}, "
                f"minStock={self.minStock}, location={self.location}, "
                f"purchasePrize={self.purchasePrize}, sellPrize={self.sellPrize})")