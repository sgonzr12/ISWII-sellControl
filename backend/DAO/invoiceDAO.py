import logging

from connect import get_db_connection
from DAO.invoice import Invoice
from DAO.product import Product
from DAO.productDAO import ProductDAO

class InvoiceDAO:
    def __init__(self):
        """
        Initialize the DAO with a database connection.
        :param db_connection: A database connection object.
        """
        self.db_connection = get_db_connection()
        self.logger = logging.getLogger("appLogger")

    def create_invoice(self, invoice: Invoice) -> None:
        """
        Insert a new invoice into the database.
        :param invoice: An Invoice object containing invoice details.
        :return: The ID of the newly created invoice.
        """
        query = """
        INSERT INTO "Invoices" ("InvoiceID", "EmployeID", "ClientID", "Date", "TotalPrice")
        VALUES (%s, %s, %s, %s, %s)
        """

        logging.debug(f"Creating invoice: {invoice}")

        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (
                invoice.invoiceID,
                invoice.employeId,
                invoice.clientId,
                invoice.date,
                invoice.totalPrice
            ))

            # Insert products into ProdInv table
            for productTup in invoice.products:
                # Assuming product is a dictionary with 'Product' and 'quantity'
                prod_query = """
                INSERT INTO "ProdInv" ("InvoiceID", "ProductID", "Quantity")
                VALUES (%s, %s, %s);
                """
                product, quantity = productTup  # Unpack the tuple
                cursor.execute(prod_query, (
                    invoice.invoiceID,
                    product.productId,
                    quantity
                ))

            self.db_connection.commit()
            logging.info(f"Invoice created with ID: {invoice.invoiceID}")
            
        
    def get_invoice_by_id(self, invoice_id: str) -> Invoice:
        """
        Retrieve an invoice by its ID, including its products.
        :param invoice_id: The ID of the invoice.
        :return: An Invoice object containing the invoice details or None if not found.
        """
        query = """
        SELECT * FROM "Invoices" WHERE "InvoiceID" = %s;
        """

        logging.debug(f"Retrieving invoice with ID: {invoice_id}")

        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (invoice_id,))
            result = cursor.fetchone()
            if result:
                #fetch products related to the invoice
                product_dao = ProductDAO()
                prod_query = """
                SELECT "ProductID", "Quantity"
                FROM "ProdInv"
                WHERE "InvoiceID" = %s;
                """
                cursor.execute(prod_query, (invoice_id,))
                
                products = list[tuple[Product, int]]()
                for product_id, quantity in cursor.fetchall():
                    product = product_dao.get_product_by_id(product_id)
                    products.append((product, quantity))
                
                invoice = Invoice(
                    invoiceID=result[0],
                    employeId=result[1],
                    clientId=result[2],
                    invoiceDate=result[3],
                    totalPrice=result[4],
                    products=products
                )

                logging.info(f"Invoice found: {invoice}")
                return invoice
            else:
                self.logger.error(f"Invoice with ID {invoice_id} not found.")
                raise ValueError(f"Invoice with ID {invoice_id} not found.")
            
    def update_invoice(self, updated_invoice: Invoice) -> bool:
        """
        Update an existing invoice in the database.
        :param invoice: An Invoice object containing updated invoice details.
        :return: True if the update was successful, False otherwise.
        """
        query = """
        UPDATE "Invoices"
        SET "EmployeId" = %s, "ClientId" = %s, "Date" = %s, "TotalPrice" = %s
        WHERE "InvoiceID" = %s;
        """

        logging.debug(f"Updating invoice: {updated_invoice}")

        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (
                updated_invoice.employeId,
                updated_invoice.clientId,
                updated_invoice.date,
                updated_invoice.totalPrice,
                updated_invoice.invoiceID
            ))
            
            # Update products in ProdInv table
            delete_query = """
            DELETE FROM "ProdInv"
            WHERE "InvoiceID" = %s;
            """
            cursor.execute(delete_query, (updated_invoice.invoiceID,))
            
            for productTup in updated_invoice.products:
                prod_query = """
                INSERT INTO "ProdInv" ("InvoiceID", "ProductID", "Quantity")
                VALUES (%s, %s, %s);
                """
                product, quantity = productTup
                cursor.execute(prod_query, (
                    updated_invoice.invoiceID,
                    product.productId,
                    quantity
                ))
                
            self.db_connection.commit()
            logging.info(f"Invoice updated with ID: {updated_invoice.invoiceID}")
            return cursor.rowcount > 0
    
    
    def delete_invoice(self, invoice_id: int) -> bool:
        """
        Delete an invoice from the database.
        :param invoice_id: The ID of the invoice to delete.
        :return: True if the deletion was successful, False otherwise.
        """
        
        logging.debug(f"Deleting invoice with ID: {invoice_id}")

        with self.db_connection.cursor() as cursor:
            # Delete products from ProdInv table
            delete_query = """
            DELETE FROM "ProdInv"
            WHERE "InvoiceID" = %s;
            """
            cursor.execute(delete_query, (invoice_id,))
            
            # Delete the invoice itself
            query = """
            DELETE FROM "Invoices"
            WHERE "InvoiceID" = %s;
            """
            cursor.execute(query, (invoice_id,))

            self.db_connection.commit()
            logging.info(f"Invoice with ID {invoice_id} deleted")
            return cursor.rowcount > 0
        
    
    def get_all_invoices(self) -> list[Invoice]:
        """
        Retrieve all invoices from the database.
        :return: A list of Invoice objects.
        """
        query = """
        SELECT * FROM "Invoices";
        """

        logging.debug("Retrieving all invoices")

        with self.db_connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            invoices = list[Invoice]()
            # Iterate through each invoice and fetch its products
            for result in results:
                
                
                prod_query = """
                SELECT "ProductID", "Quantity"
                FROM "ProdInv"
                WHERE "InvoiceID" = %s;
                """
                cursor.execute(prod_query, (result[0],))
                
                products = list[tuple[Product, int]]()
                product_dao = ProductDAO()
                
                for product_id, quantity in cursor.fetchall():
                    product = product_dao.get_product_by_id(product_id)
                    products.append((product, quantity))
                    
                invoices.append(Invoice(
                    invoiceID=result[0],
                    employeId=result[1],
                    clientId=result[2],
                    invoiceDate=result[3],
                    totalPrice=result[4],
                    products=products
                ))
            
            logging.info(f"Retrieved all {len(invoices)} invoices")
            return invoices
        