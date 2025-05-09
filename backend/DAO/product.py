class Product:
    def __init__(self, name: str, description: str, stock: int, maxStock: int, minStock: int, location: str, purchasePrize: float, sellPrize: float, productId: int = 0):
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
        
    def get_product_JSON(self) -> dict[str, str]:
        """
        Convert the product object to a JSON-compatible dictionary.
        :return: A dictionary representation of the product.
        """
        return {
            "productId": str(self.productId),
            "name": self.name,
            "description": self.description,
            "stock": str(self.stock),
            "maxStock": str(self.maxStock),
            "minStock": str(self.minStock),
            "location": self.location,
            "purchasePrize": str(self.purchasePrize),
            "sellPrize": str(self.sellPrize)
        }
    
    def verify_product(self) -> bool:
        """
        Verify if the product has all the required fields.
        :return: True if the product is valid, False otherwise.
        """
        return all([
            self.name,
            self.description,
            
            self.maxStock >= 0,
            self.minStock >= 0,
            self.maxStock >= self.minStock,
            self.minStock <= self.stock <= self.maxStock,
            
            self.location,
            self.purchasePrize >= 0,
            self.sellPrize >= 0
        ])
        
    def ready_to_insert(self) -> bool:
        """
        Check if the product is ready to be inserted into the database.
        :return: True if the product is ready to be inserted, False otherwise.
        """
        return all([
            
            self.productId == 0,
            self.name,
            self.description,
            
            self.maxStock >= 0,
            self.minStock >= 0,
            self.maxStock >= self.minStock,
            self.minStock <= self.stock <= self.maxStock,
            
            self.location,
            self.purchasePrize >= 0,
            self.sellPrize >= 0
        ])