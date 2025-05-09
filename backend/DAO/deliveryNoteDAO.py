import psycopg2.extensions
import logging

from deliveryNote import DeliveryNote
from product import Product
from productDAO import ProductDAO

class DeliveryNoteDAO:
    def __init__(self, db_connection: psycopg2.extensions.connection):
        """
        Initialize the DAO with a database connection.
        :param db_connection: A database connection object.
        """
        self.db_connection = db_connection
        self.logger = logging.getLogger("appLogger")

    def create_delivery_note(self, delivery_note: DeliveryNote) -> int:
        """
        Insert a new delivery note into the database.
        :param delivery_note: A DeliveryNote object containing delivery note details.
        :return: The ID of the newly created delivery note.
        """
        query = """
        INSERT INTO delivery_notes (employeId, clientID, delivery_date, totalPrize)
        VALUES (%s, %s, %s, %s)
        RETURNING deliveryNoteID;
        """

        logging.debug(f"Creating delivery note: {delivery_note}")

        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (
                delivery_note.employeId,
                delivery_note.clientId,
                delivery_note.date,
                delivery_note.totalPrize
            ))
            
            result = cursor.fetchone()
            if result is None:
                self.logger.error("Failed to insert delivery note and retrieve its ID.")
                raise ValueError("Failed to insert delivery note and retrieve its ID.")
            delivery_note_id = result[0]

            # Insert products into ProdDel table
            for productTup in delivery_note.products:
                # Assuming product is a dictionary with 'Product' and 'quantity'
                prod_query = """
                INSERT INTO ProdDel (deliveryNoteID, productID, quantity)
                VALUES (%s, %s, %s);
                """
                product, quantity = productTup  # Unpack the tuple
                cursor.execute(prod_query, (
                    delivery_note_id,
                    product.productId,
                    quantity
                ))

            self.db_connection.commit()
            logging.info(f"Delivery note created with ID: {delivery_note_id}")
            return delivery_note_id
    
    
    def get_delivery_note_by_id(self, delivery_note_id: int) -> DeliveryNote:
        """
        Retrieve a delivery note by its ID, including its products.
        :param delivery_note_id: The ID of the delivery note.
        :return: A DeliveryNote object containing the delivery note details or None if not found.
        """
        query = """
        SELECT *
        FROM delivery_notes
        WHERE deliveryNoteID = %s;
        """

        logging.debug(f"Retrieving delivery note with ID: {delivery_note_id}")

        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (delivery_note_id,))
            result = cursor.fetchone()
            if result:
                # Retrieve products associated with this delivery note
                product_dao = ProductDAO(self.db_connection)
                product_query = """
                SELECT productID, quantity
                FROM ProdDel
                WHERE deliveryNoteID = %s;
                """
                cursor.execute(product_query, (delivery_note_id,))
                products = list[tuple[Product, int]]()
                for row in cursor.fetchall():
                    product_id, quantity = row
                    product = product_dao.get_product_by_id(product_id)
                    products.append((product, quantity))
                
                # Create a DeliveryNote object
                delivery_note = DeliveryNote(
                    deliveryNoteID=result[0],
                    employeId=result[1],
                    clientId=result[2],
                    deliveryNoteDate=result[3],
                    totalPrize=result[4],
                    products=products
                )

                # Return the DeliveryNote object
                logging.info(f"Delivery note found: {delivery_note}")
                return delivery_note
            else:
                self.logger.error(f"Delivery note with ID {delivery_note_id} not found.")
                raise ValueError(f"Delivery note with ID {delivery_note_id} not found.")
    
    def update_delivery_note(self, updated_delivery_note: DeliveryNote) -> bool:
        """
        Update an existing delivery note in the database.
        :param delivery_note: A DeliveryNote object containing updated delivery note details.
        :return: True if the update was successful, False otherwise.
        """
        query = """
        UPDATE delivery_notes
        SET employeId = %s, clientID = %s, delivery_date = %s, totalPrize = %s
        WHERE deliveryNoteID = %s;
        """

        logging.debug(f"Updating delivery note: {updated_delivery_note}")

        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (
                updated_delivery_note.employeId,
                updated_delivery_note.clientId,
                updated_delivery_note.date,
                updated_delivery_note.totalPrize,
                updated_delivery_note.deliveryNoteID
            ))
            
            # Update products in ProdDel table
            delete_query = "DELETE FROM ProdDel WHERE deliveryNoteID = %s;"
            cursor.execute(delete_query, (updated_delivery_note.deliveryNoteID,))
            # Insert updated products
            for productTup in updated_delivery_note.products:
                prod_query = """
                INSERT INTO ProdDel (deliveryNoteID, productID, quantity)
                VALUES (%s, %s, %s);
                """
                product, quantity = productTup
                cursor.execute(prod_query, (
                    updated_delivery_note.deliveryNoteID,
                    product.productId,
                    quantity
                ))
                
            self.db_connection.commit()
            logging.info(f"Delivery note updated with ID: {updated_delivery_note.deliveryNoteID}")
            return cursor.rowcount > 0
        
        
    def delete_delivery_note(self, delivery_note_id: int) -> bool:
        """
        Delete a delivery note from the database.
        :param delivery_note_id: The ID of the delivery note to delete.
        :return: True if the deletion was successful, False otherwise.
        """

        logging.debug(f"Deleting delivery note with ID: {delivery_note_id}")
        
        with self.db_connection.cursor() as cursor:
            # Delete products related to the delivery note
            prod_query = "DELETE FROM ProdDel WHERE deliveryNoteID = %s;"
            cursor.execute(prod_query, (delivery_note_id,))
            
            # Delete the delivery note itself
            query = "DELETE FROM delivery_notes WHERE deliveryNoteID = %s;"
            cursor.execute(query, (delivery_note_id,))

            self.db_connection.commit()
            logging.info(f"Delivery note with ID {delivery_note_id} deleted")
            return cursor.rowcount > 0
        
    def get_all_delivery_notes(self) -> list[DeliveryNote]:
        """
        Retrieve all delivery notes from the database.
        :return: A list of DeliveryNote objects.
        """
        query = "SELECT * FROM delivery_notes;"

        logging.debug("Retrieving all delivery notes")

        with self.db_connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            delivery_notes = list[DeliveryNote]()
            for row in results:
                # Retrieve products associated with this delivery note
                product_dao = ProductDAO(self.db_connection)
                product_query = """
                SELECT productID, quantity
                FROM ProdDel
                WHERE deliveryNoteID = %s;
                """
                cursor.execute(product_query, (row[0],))
                products = list[tuple[Product, int]]()
                
                for prod_row in cursor.fetchall():
                    product_id, quantity = prod_row
                    product = product_dao.get_product_by_id(product_id)
                    products.append((product, quantity))
                
                # Create a DeliveryNote object
                delivery_note = DeliveryNote(
                    deliveryNoteID=row[0],
                    employeId=row[1],
                    clientId=row[2],
                    deliveryNoteDate=row[3],
                    totalPrize=row[4],
                    products=products
                )
                delivery_notes.append(delivery_note)
            
            logging.info(f"Retrieved all {len(delivery_notes)} delivery notes")
            return delivery_notes
        