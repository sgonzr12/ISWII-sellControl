import psycopg2.extensions
from product import Product

class ProductDAO:
    def __init__(self, db_connection: psycopg2.extensions.connection):
        """
        Initialize the ProductDAO with a database connection.
        :param db_connection: A database connection object.
        """
        self.db_connection = db_connection

    def create_product(self, product: Product) -> int:
        """
        Insert a new product into the database.
        :param product: A Product object containing product details.
        :return: The ID of the newly created product.
        """
        query = """
        INSERT INTO products (productId, name, description, stock, maxStock, minStock, location, purchasePrize, sellPrize)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING productId;
        """
        cursor = self.db_connection.cursor()
        try:
            cursor.execute(query, (
                product.productId, product.name, product.description, product.stock,
                product.maxStock, product.minStock, product.location,
                product.purchasePrize, product.sellPrize
            ))
            self.db_connection.commit()
            result = cursor.fetchone()
            if result is None:
                raise ValueError("No product ID returned from the database.")
            return result[0]
        finally:
            cursor.close()

    def get_product_by_id(self, product_id: int) -> Product:
        """
        Retrieve a product by its ID.
        :param product_id: The ID of the product to retrieve.
        """
        cursor = self.db_connection.cursor()
        try:
            query = "SELECT * FROM products WHERE productId = %s;"
            cursor.execute(query, (product_id,))
            result = cursor.fetchone()
            if result:
                return Product(
                    productId=result[0],
                    name=result[1],
                    description=result[2],
                    stock=result[3],
                    maxStock=result[4],
                    minStock=result[5],
                    location=result[6],
                    purchasePrize=result[7],
                    sellPrize=result[8]
                )
            else:
                raise ValueError(f"Product with ID {product_id} not found.")
        finally:
            cursor.close()

    def update_product(self, product_id: int, updated_product: Product) -> bool:
        """
        Update an existing product in the database.
        :param product_id: The ID of the product to update.
        :param updated_product: A dictionary containing updated product details.
        :return: True if the update was successful, False otherwise.
        """
        query = """
        UPDATE products
        SET name = %s, description = %s, price = %s, stock = %s
        WHERE productId = %s;
        """
        cursor = self.db_connection.cursor()
        try:
            cursor.execute(query, (
                updated_product.name, updated_product.description,
                updated_product.purchasePrize, updated_product.stock, product_id
            ))
            self.db_connection.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()

    def delete_product(self, product_id: int) -> bool:
        """
        Delete a product from the database.
        :param product_id: The ID of the product to delete.
        :return: True if the deletion was successful, False otherwise.
        """
        query = "DELETE FROM products WHERE productId = %s;"
        cursor = self.db_connection.cursor()
        try:
            cursor.execute(query, (product_id,))
            self.db_connection.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()
            
    def get_all_products(self) -> list[Product]:
        """
        Retrieve all products from the database.
        :return: A list of Product objects.
        """
        cursor = self.db_connection.cursor()
        try:
            query = "SELECT * FROM products;"
            cursor.execute(query)
            results = cursor.fetchall()
            return [
                Product(
                    productId=row[0],
                    name=row[1],
                    description=row[2],
                    stock=row[3],
                    maxStock=row[4],
                    minStock=row[5],
                    location=row[6],
                    purchasePrize=row[7],
                    sellPrize=row[8]
                )
                for row in results
            ]
        finally:
            cursor.close()
        