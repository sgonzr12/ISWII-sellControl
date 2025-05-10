import logging
from fastapi import HTTPException
from DAO.product import Product
from connect import get_db_connection

class ProductDAO:
    def __init__(self):
        """
        Initialize the ProductDAO with a database connection.
        :param db_connection: A database connection object.
        """
        self.db_connection = get_db_connection()
        self.logger = logging.getLogger("appLogger")

    def create_product(self, product: Product) -> Product:
        """
        Insert a new product into the database.
        :param product: A Product object containing product details.
        :return: The ID of the newly created product.
        """
        
        query = """
        INSERT INTO "Products" ("ProductID", "Name", "Description", "Stock", "MaxStock", "MinStock", "PurchasePrice", "SellPrice")
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING "ProductID";
        """

        
        
        cursor = self.db_connection.cursor()
        logging.debug(f"Creating product: {product}")

        try:
            cursor.execute(query, (
                product.productId, product.name, product.description, product.stock,
                product.maxStock, product.minStock,
                product.purchasePrice, product.sellPrice
            ))
            self.db_connection.commit()
            result = cursor.fetchone()
            if result is None:
                self.logger.error("No product ID returned from the database.")
                raise HTTPException(status_code=500, detail="Failed to create product.")

            logging.info(f"Product created with ID: {result[0]}")
            return product
        finally:
            cursor.close()

    def get_product_by_id(self, product_id: int) -> Product:
        """
        Retrieve a product by its ID.
        :param product_id: The ID of the product to retrieve.
        """
        cursor = self.db_connection.cursor()
        logging.debug(f"Retrieving product with ID: {product_id}")

        try:
            query = """SELECT * 
                    FROM "Products" 
                    WHERE "ProductID" = %s;"""
            cursor.execute(query, (product_id,))
            result = cursor.fetchone()
            if result:
                logging.info(f"Product found: {result}")
                return Product(
                    productId=result[0],
                    name=result[1],
                    description=result[2],
                    stock=result[3],
                    maxStock=result[4],
                    minStock=result[5],
                    purchasePrice=result[7],
                    sellPrice=result[8]
                )
            else:
                self.logger.error(f"Product with ID {product_id} not found.")
                raise HTTPException(status_code=404, detail="Product not found.")
        finally:
            cursor.close()

    def update_product(self,product: Product) -> Product:
        """
        Update an existing product in the database.
        :param product_id: The ID of the product to update.
        :param updated_product: A dictionary containing updated product details.
        :return: True if the update was successful, False otherwise.
        """
        query = """
        UPDATE "Products"
        SET "Name" = %s, "Description" = %s, "Stock" = %s, "MaxStock" = %s, "MinStock" = %s, "PurchasePrice" = %s, "SellPrice" = %s
        WHERE "ProductID" = %s;
        """
        cursor = self.db_connection.cursor()
        logging.debug(f"Updating product with ID: {product.productId}")
        
        

        try:
            cursor.execute(query, (
                product.name, product.description, product.stock,
                product.maxStock, product.minStock,
                product.purchasePrice, product.sellPrice,
                product.productId
            ))

            self.db_connection.commit()
            if cursor.rowcount == 0:
                self.logger.error(f"Product with ID {product.productId} not found.")
                raise HTTPException(status_code=404, detail="Product not found.")
            
            logging.info(f"Product with ID {product.productId} updated successfully.")
            return product
        except Exception as e:
            self.logger.error(f"Error updating product with ID {product.productId}: {e}")
            raise HTTPException(status_code=500, detail="Failed to update product.")
        finally:
            cursor.close()

    def delete_product(self, product_id: int) -> bool:
        """
        Delete a product from the database.
        :param product_id: The ID of the product to delete.
        :return: True if the deletion was successful, False otherwise.
        """
        query = """DELETE FROM "Products" WHERE "ProductID" = %s;"""
        cursor = self.db_connection.cursor()
        logging.debug(f"Deleting product with ID: {product_id}")

        try:
            cursor.execute(query, (product_id,))
            
            self.db_connection.commit()
            logging.info(f"Product with ID {product_id} deleted successfully.")
            if cursor.rowcount == 0:
                self.logger.error(f"Product with ID {product_id} not found.")
                raise HTTPException(status_code=404, detail="Product not found.")
            return cursor.rowcount > 0
        except Exception as e:
            self.logger.error(f"Error deleting product with ID {product_id}: {e}")
            raise HTTPException(status_code=500, detail="Failed to delete product.")
        finally:
            cursor.close()
            
    def get_all_products(self) -> list[Product]:
        """
        Retrieve all products from the database.
        :return: A list of Product objects.
        """
        cursor = self.db_connection.cursor()
        logging.debug("Retrieving all products")

        try:
            query = """
                    SELECT * FROM "Products"
                    """
            cursor.execute(query)
            results = cursor.fetchall()

            logging.info(f"Retrieved all {len(results)} products")
            return [

                Product(
                    productId=row[0],
                    name=row[1],
                    description=row[2],
                    stock=row[3],
                    maxStock=row[4],
                    minStock=row[5],
                    purchasePrice=row[7],
                    sellPrice=row[8]
                )
                for row in results
            ]
        except Exception as e:
            self.logger.error(f"Error retrieving all products: {e}")
            raise HTTPException(status_code=500, detail="Failed to retrieve products.")
        finally:
            cursor.close()
        