import psycopg2.extensions
from ofert import Ofert
from product import Product
from productDAO import ProductDAO


class OfertDAO:
    def __init__(self, db_connection: psycopg2.extensions.connection):
        """
        Initialize the DAO with a database connection.
        :param db_connection: A database connection object.
        """
        self.db_connection = db_connection

    def create_ofert(self, ofert: Ofert)-> int:
        """
        Insert a new ofert into the database.
        :param ofert_data: A dictionary containing ofert details.
        :return: The ID of the newly created ofert.
        """
        query = """
        INSERT INTO oferts (employeId, clientID, ofert_date, totalPrize)
        VALUES (%s, %s, %s, %s)
        RETURNING ofertID;
        """
        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (
                ofert.employeId,
                ofert.clientId,
                ofert.date,
                ofert.totalPrize
            ))
            
            result = cursor.fetchone()
            if result is None:
                raise ValueError("Failed to insert ofert and retrieve its ID.")
            ofert_id = result[0]

            # Insert products into ProdOfe table
            for productTup in ofert.products:
                # Assuming product is a dictionary with 'Product' and 'quantity'
                prod_query = """
                INSERT INTO ProdOfe (ofertID, productID, quantity)
                VALUES (%s, %s, %s);
                """
                product, quantity = productTup  # Unpack the tuple
                cursor.execute(prod_query, (
                    ofert_id,
                    product.productId,
                    quantity
                ))

            self.db_connection.commit()
            return ofert_id

    def get_ofert_by_id(self, ofert_id: int)-> Ofert:
        """
        Retrieve an ofert by its ID, including its products.
        :param ofert_id: The ID of the ofert.
        :return: A dictionary containing the ofert details or None if not found.
        """
        query = """
        SELECT * FROM oferts WHERE ofertID = %s;
        """
        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (ofert_id,))
            result = cursor.fetchone()
            if result:
                # Fetch products related to the ofert
                prod_query = """
                SELECT productID, quantity
                FROM ProdOfe
                WHERE ofertID = %s;
                """
                cursor.execute(prod_query, (ofert_id,))
                
                products = list[tuple[Product, int]]()
                
                # Fetch all products related to the ofert
                for prod_row in cursor.fetchall():
                    product_id = prod_row[0]
                    quantity = prod_row[1]
                    
                    # Fetch product details from ProductDAO
                    product_dao = ProductDAO(self.db_connection)
                    product = product_dao.get_product_by_id(product_id)
                    products.append((product, quantity))
                
                
                # Create an Ofert object
                ofert = Ofert(
                    ofertID=result[0],
                    employeId=result[1],
                    clientId=result[2],
                    ofert_date=result[3],
                    totalPrize=result[4],
                    products=products
                )
                # Return the Ofert object
                return ofert
            else:
                raise ValueError(f"No ofert found with ID {ofert_id}.")

    def update_ofert(self, updated_ofert: Ofert)-> bool:
        """
        Update an existing ofert in the database.
        :param ofert_id: The ID of the ofert to update.
        :param updated_data: A dictionary containing the updated ofert details.
        :return: True if the update was successful, False otherwise.
        """
        query = """
        UPDATE oferts
        SET employeId = %s, clientID = %s, ofert_date = %s, totalPrize = %s
        WHERE ofertID = %s;
        """
        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (
                updated_ofert.employeId,
                updated_ofert.clientId,
                updated_ofert.date,
                updated_ofert.totalPrize,
                updated_ofert.ofertID
            ))

            # Update products in ProdOfe table
            delete_query = "DELETE FROM ProdOfe WHERE ofertID = %s;"
            cursor.execute(delete_query, (updated_ofert.ofertID,))

            for productTup in updated_ofert.products:
                prod_query = """
                INSERT INTO ProdOfe (ofertID, productID, quantity)
                VALUES (%s, %s, %s);
                """
                product, quantity = productTup
                
                cursor.execute(prod_query, (
                    updated_ofert.ofertID,
                    product.productId,
                    quantity
                ))

            self.db_connection.commit()
            return cursor.rowcount > 0

    def delete_ofert(self, ofert_id: int)-> bool:
        """
        Delete an ofert from the database.
        :param ofert_id: The ID of the ofert to delete.
        :return: True if the deletion was successful, False otherwise.
        """
        with self.db_connection.cursor() as cursor:
            # Delete products related to the ofert
            prod_query = "DELETE FROM ProdOfe WHERE ofertID = %s;"
            cursor.execute(prod_query, (ofert_id,))

            # Delete the ofert itself
            query = "DELETE FROM oferts WHERE ofertID = %s;"
            cursor.execute(query, (ofert_id,))
            self.db_connection.commit()
            return cursor.rowcount > 0

    # TODO: Implement the get_all_oferts method
    def get_all_oferts(self)-> list[Ofert]:
        """
        Retrieve all oferts from the database, including their products.
        :return: A list of dictionaries containing ofert details.
        """
        query = """
        SELECT ofertID, employeId, clientID, ofert_date, totalPrize
        FROM oferts;
        """
        with self.db_connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

            oferts = list[Ofert]()
            # Iterate through each ofert and fetch its products
            for row in results:
                prod_query = """
                SELECT productID, quantity
                FROM ProdOfe
                WHERE ofertID = %s;
                """
                cursor.execute(prod_query, (row[0],))
                products = list[tuple[Product, int]]()
                
                for prod_row in cursor.fetchall():
                    product_id = prod_row[0]
                    quantity = prod_row[1]
                    
                    # Fetch product details from ProductDAO
                    product_dao = ProductDAO(self.db_connection)
                    product = product_dao.get_product_by_id(product_id)
                    products.append((product, quantity))
                    
                # Create an Ofert object
                oferts.append(
                    Ofert(
                        ofertID=row[0],
                        employeId=row[1],
                        clientId=row[2],
                        ofert_date=row[3],
                        totalPrize=row[4],
                        products=products
                    )
                )
            return oferts
        