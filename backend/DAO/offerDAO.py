import psycopg2.extensions
import logging

from offer import Offer
from product import Product
from productDAO import ProductDAO


class offerDAO:
    def __init__(self, db_connection: psycopg2.extensions.connection):
        """
        Initialize the DAO with a database connection.
        :param db_connection: A database connection object.
        """
        self.db_connection = db_connection
        self.logger = logging.getLogger("appLogger")

    def create_offer(self, offer: Offer)-> int:
        """
        Insert a new offer into the database.
        :param offer_data: A dictionary containing offer details.
        :return: The ID of the newly created offer.
        """
        query = """
        INSERT INTO offers (employeId, clientID, offer_date, totalPrize)
        VALUES (%s, %s, %s, %s)
        RETURNING offerID;
        """

        logging.debug(f"Creating offer: {offer}")

        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (
                offer.employeId,
                offer.clientId,
                offer.date,
                offer.totalPrize
            ))
            
            result = cursor.fetchone()
            if result is None:
                self.logger.error("Failed to insert offer and retrieve its ID.")
                raise ValueError("Failed to insert offer and retrieve its ID.")
            offer_id = result[0]

            # Insert products into ProdOfe table
            for productTup in offer.products:
                # Assuming product is a dictionary with 'Product' and 'quantity'
                prod_query = """
                INSERT INTO ProdOfe (offerID, productID, quantity)
                VALUES (%s, %s, %s);
                """
                product, quantity = productTup  # Unpack the tuple
                cursor.execute(prod_query, (
                    offer_id,
                    product.productId,
                    quantity
                ))

            self.db_connection.commit()
            logging.info(f"Offer created with ID: {offer_id}")
            return offer_id

    def get_offer_by_id(self, offer_id: int)-> Offer:
        """
        Retrieve an offer by its ID, including its products.
        :param offer_id: The ID of the offer.
        :return: A dictionary containing the offer details or None if not found.
        """
        query = """
        SELECT * FROM offers WHERE offerID = %s;
        """

        logging.debug(f"Retrieving offer with ID: {offer_id}")

        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (offer_id,))
            result = cursor.fetchone()
            if result:
                # Fetch products related to the offer
                prod_query = """
                SELECT productID, quantity
                FROM ProdOfe
                WHERE offerID = %s;
                """
                cursor.execute(prod_query, (offer_id,))
                
                product_dao = ProductDAO(self.db_connection)
                products = list[tuple[Product, int]]()
                
                for prod_row in cursor.fetchall():
                    product_id = prod_row[0]
                    quantity = prod_row[1]
                    
                    # Fetch product details from ProductDAO
                    product = product_dao.get_product_by_id(product_id)
                    products.append((product, quantity))
                
                
                # Create an offer object
                offer = Offer(
                    offerID=result[0],
                    employeId=result[1],
                    clientId=result[2],
                    offer_date=result[3],
                    totalPrize=result[4],
                    products=products
                )
                # Return the offer object
                logging.info(f"Offer found: {offer}")
                return offer
            else:
                self.logger.error(f"Offer with ID {offer_id} not found.")
                raise ValueError(f"No offer found with ID {offer_id}.")

    def update_offer(self, updated_offer: Offer)-> bool:
        """
        Update an existing offer in the database.
        :param updated_data: A dictionary containing the updated offer details.
        :return: True if the update was successful, False otherwise.
        """
        query = """
        UPDATE offers
        SET employeId = %s, clientID = %s, offer_date = %s, totalPrize = %s
        WHERE offerID = %s;
        """

        logging.debug(f"Updating offer: {updated_offer}")

        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (
                updated_offer.employeId,
                updated_offer.clientId,
                updated_offer.date,
                updated_offer.totalPrize,
                updated_offer.offerID
            ))

            # Update products in ProdOfe table
            delete_query = "DELETE FROM ProdOfe WHERE offerID = %s;"
            cursor.execute(delete_query, (updated_offer.offerID,))

            for productTup in updated_offer.products:
                prod_query = """
                INSERT INTO ProdOfe (offerID, productID, quantity)
                VALUES (%s, %s, %s);
                """
                product, quantity = productTup
                
                cursor.execute(prod_query, (
                    updated_offer.offerID,
                    product.productId,
                    quantity
                ))

            self.db_connection.commit()
            logging.info(f"Offer updated with ID: {updated_offer.offerID}")
            return cursor.rowcount > 0

    def delete_offer(self, offer_id: int)-> bool:
        """
        Delete an offer from the database.
        :param offer_id: The ID of the offer to delete.
        :return: True if the deletion was successful, False otherwise.
        """
        logging.debug(f"Deleting offer with ID: {offer_id}")

        with self.db_connection.cursor() as cursor:
            # Delete products related to the offer
            prod_query = "DELETE FROM ProdOfe WHERE offerID = %s;"
            cursor.execute(prod_query, (offer_id,))

            # Delete the offer itself
            query = "DELETE FROM offers WHERE offerID = %s;"
            cursor.execute(query, (offer_id,))

            self.db_connection.commit()
            logging.info(f"Offer with ID {offer_id} deleted")
            return cursor.rowcount > 0

    def get_all_offers(self)-> list[Offer]:
        """
        Retrieve all offers from the database, including their products.
        :return: A list of dictionaries containing offer details.
        """
        query = """
        SELECT *
        FROM offers;
        """

        logging.debug("Retrieving all offers")

        with self.db_connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

            offers = list[Offer]()
            # Iterate through each offer and fetch its products
            for row in results:
                prod_query = """
                SELECT productID, quantity
                FROM ProdOfe
                WHERE offerID = %s;
                """
                cursor.execute(prod_query, (row[0],))
                
                product_dao = ProductDAO(self.db_connection)
                products = list[tuple[Product, int]]()
    
                for prod_row in cursor.fetchall():
                    product_id = prod_row[0]
                    quantity = prod_row[1]
                    
                    # Fetch product details from ProductDAO
                    product = product_dao.get_product_by_id(product_id)
                    products.append((product, quantity))
                    
                # Create an offer object
                offers.append(
                    Offer(
                        offerID=row[0],
                        employeId=row[1],
                        clientId=row[2],
                        offer_date=row[3],
                        totalPrize=row[4],
                        products=products
                    )
                )
            
            logging.info(f"Retrieved all {len(offers)} offers")
            return offers
        