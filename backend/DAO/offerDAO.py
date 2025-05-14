import logging

from fastapi import HTTPException

from connect import get_db_connection 
from DAO.offer import Offer
from DAO.productDAO import ProductDAO
from DAO.product import Product


class OfferDAO:
    def __init__(self):
        """
        Initialize the DAO with a database connection.
        :param db_connection: A database connection object.
        """
        self.db_connection = get_db_connection()
        self.logger = logging.getLogger("appLogger")

    def create_offer(self, offer: Offer)-> Offer:
        """
        Insert a new offer into the database.
        :param offer_data: A dictionary containing offer details.
        :return: The ID of the newly created offer.
        """
        query = """
        INSERT INTO "Offers" ("EmployeID", "ClientID", "Date", "TotalPrice")
        VALUES (%s, %s, %s, %s)
        RETURNING "OfferID";
        """
        logging.debug(f"Creating offer")
        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (
                offer.employeId,
                offer.clientId,
                offer.date,
                offer.TotalPrice
            ))
            offer_id = cursor.fetchone()
            if offer_id is None:
                self.logger.error("No offer ID returned from the database.")
                raise HTTPException(status_code=500, detail="Failed to create offer.")

            # Insert products into ProdOfe table
            for productTup in offer.products:
                prod_query = """
                INSERT INTO "ProdOfe" ("OfferID", "ProductID", "Quantity")
                VALUES (%s, %s, %s);
                """
                product, quantity = productTup
                
                cursor.execute(prod_query, (
                    offer_id,
                    product.productId,
                    quantity
                ))

            self.db_connection.commit()
            logging.info(f"Offer created with ID: {offer_id}")
            return Offer(
                offerID=str(offer_id),
                employeId=offer.employeId,
                clientId=offer.clientId,
                offer_date=offer.date,
                TotalPrice=offer.TotalPrice,
                products=offer.products
            )
                

 

    def get_offer_by_id(self, offer_id: str)-> Offer:
        """
        Retrieve an offer by its ID, including its products.
        :param offer_id: The ID of the offer.
        :return: A dictionary containing the offer details or None if not found.
        """
        query = """
        SELECT * FROM "Offers" WHERE "OfferID" = %s;
        """

        logging.debug(f"Retrieving offer with ID: {offer_id}")

        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (offer_id,))
            result = cursor.fetchone()
            if result:
                # Fetch products related to the offer
                prod_query = """
                SELECT "ProductID", "Quantity"
                FROM "ProdOfe"
                WHERE "OfferID" = %s;
                """
                cursor.execute(prod_query, (offer_id,))
                
                product_dao = ProductDAO()
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
                    TotalPrice=result[4],
                    products=products
                )
                # Return the offer object
                logging.info(f"Offer found: {offer}")
                return offer
            else:
                self.logger.error(f"Offer with ID {offer_id} not found.")
                raise HTTPException(status_code=404, detail="Offer not found.")

    def update_offer(self, updated_offer: Offer)-> bool:
        """
        Update an existing offer in the database.
        :param updated_data: A dictionary containing the updated offer details.
        :return: True if the update was successful, False otherwise.
        """
        query = """
        UPDATE "Offers"
        SET "EmployeID" = %s, "ClientID" = %s, "Date" = %s, "TotalPrice" = %s
        WHERE "OfferID" = %s;
        """

        logging.debug(f"Updating offer: {updated_offer}")

        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (
                updated_offer.employeId,
                updated_offer.clientId,
                updated_offer.date,
                updated_offer.TotalPrice,
                updated_offer.offerID
            ))

            # Update products in ProdOfe table
            delete_query = """
            DELETE FROM "ProdOfe" 
            WHERE "OfferID" = %s;
            """
            cursor.execute(delete_query, (updated_offer.offerID,))

            for productTup in updated_offer.products:
                prod_query = """
                INSERT INTO "ProdOfe" ("OfferID", "ProductID", "Quantity")
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
            prod_query = """
                        DELETE FROM "ProdOfe"
                        WHERE "OfferID" = %s;"
                        """
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
        FROM "Offers";
        """

        logging.debug("Retrieving all offers")

        with self.db_connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

            offers = list[Offer]()
            # Iterate through each offer and fetch its products
            for row in results:
                prod_query = """
                SELECT "ProductID", "Quantity"
                FROM "ProdOfe"
                WHERE "OfferID" = %s;
                """
                cursor.execute(prod_query, (row[0],))
                
                product_dao = ProductDAO()
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
                        TotalPrice=row[4],
                        products=products
                    )
                )
            
            logging.info(f"Retrieved all {len(offers)} offers")
            return offers
        