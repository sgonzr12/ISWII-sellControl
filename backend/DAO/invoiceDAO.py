import psycopg2.extensions
from invoice import Invoice
from product import Product
from productDAO import ProductDAO

class InvoiceDAO:
    def __init__(self, db_connection: psycopg2.extensions.connection):
        """
        Initialize the DAO with a database connection.
        :param db_connection: A database connection object.
        """
        self.db_connection = db_connection

    def create_invoice(self, invoice: Invoice) -> int:
        """
        Insert a new invoice into the database.
        :param invoice: An Invoice object containing invoice details.
        :return: The ID of the newly created invoice.
        """
        query = """
        INSERT INTO invoices (employeId, clientID, invoice_date, totalPrize)
        VALUES (%s, %s, %s, %s)
        RETURNING invoiceID;
        """
        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (
                invoice.employeId,
                invoice.clientId,
                invoice.invoiceDate,
                invoice.totalPrize
            ))
            
            result = cursor.fetchone()
            if result is None:
                raise ValueError("Failed to insert invoice and retrieve its ID.")
            invoice_id = result[0]

            # Insert products into ProdInv table
            for productTup in invoice.products:
                # Assuming product is a dictionary with 'Product' and 'quantity'
                prod_query = """
                INSERT INTO ProdInv (invoiceID, productID, quantity)
                VALUES (%s, %s, %s);
                """
                product, quantity = productTup  # Unpack the tuple
                cursor.execute(prod_query, (
                    invoice_id,
                    product.productId,
                    quantity
                ))

            self.db_connection.commit()
            return invoice_id
        
    def get_invoice_by_id(self, invoice_id: int) -> Invoice:
        """
        Retrieve an invoice by its ID, including its products.
        :param invoice_id: The ID of the invoice.
        :return: An Invoice object containing the invoice details or None if not found.
        """
        query = """
        SELECT * FROM invoices WHERE invoiceID = %s;
        """
        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (invoice_id,))
            result = cursor.fetchone()
            if result:
                #fetch products related to the invoice
                product_dao = ProductDAO(self.db_connection)
                prod_query = """
                SELECT productID, quantity
                FROM ProdInv
                WHERE invoiceID = %s;
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
                    totalPrize=result[4],
                    products=products
                )
                return invoice
            else:
                raise ValueError(f"Invoice with ID {invoice_id} not found.")
            
    def update_invoice(self, updated_invoice: Invoice) -> bool:
        """
        Update an existing invoice in the database.
        :param invoice: An Invoice object containing updated invoice details.
        :return: True if the update was successful, False otherwise.
        """
        query = """
        UPDATE invoices
        SET employeId = %s, clientId = %s, invoice_date = %s, totalPrize = %s
        WHERE invoiceID = %s;
        """
        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (
                updated_invoice.employeId,
                updated_invoice.clientId,
                updated_invoice.invoiceDate,
                updated_invoice.totalPrize,
                updated_invoice.invoiceID
            ))
            
            # Update products in ProdInv table
            delete_query = """
            DELETE FROM ProdInv
            WHERE invoiceID = %s;
            """
            cursor.execute(delete_query, (updated_invoice.invoiceID,))
            
            for productTup in updated_invoice.products:
                prod_query = """
                INSERT INTO ProdInv (invoiceID, productID, quantity)
                VALUES (%s, %s, %s);
                """
                product, quantity = productTup
                cursor.execute(prod_query, (
                    updated_invoice.invoiceID,
                    product.productId,
                    quantity
                ))
                
            self.db_connection.commit()
            return cursor.rowcount > 0
    
    
    def delete_invoice(self, invoice_id: int) -> bool:
        """
        Delete an invoice from the database.
        :param invoice_id: The ID of the invoice to delete.
        :return: True if the deletion was successful, False otherwise.
        """
        
        with self.db_connection.cursor() as cursor:
            # Delete products from ProdInv table
            delete_query = """
            DELETE FROM ProdInv
            WHERE invoiceID = %s;
            """
            cursor.execute(delete_query, (invoice_id,))
            
            # Delete the invoice itself
            query = """
            DELETE FROM invoices
            WHERE invoiceID = %s;
            """
            cursor.execute(query, (invoice_id,))
            self.db_connection.commit()
            return cursor.rowcount > 0
        
    
    def get_all_invoices(self) -> list[Invoice]:
        """
        Retrieve all invoices from the database.
        :return: A list of Invoice objects.
        """
        query = """
        SELECT * FROM invoices;
        """
        with self.db_connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            invoices = list[Invoice]()
            # Iterate through each invoice and fetch its products
            for result in results:
                
                
                prod_query = """
                SELECT productID, quantity
                FROM ProdInv
                WHERE invoiceID = %s;
                """
                cursor.execute(prod_query, (result[0],))
                
                products = list[tuple[Product, int]]()
                product_dao = ProductDAO(self.db_connection)
                
                for product_id, quantity in cursor.fetchall():
                    product = product_dao.get_product_by_id(product_id)
                    products.append((product, quantity))
                    
                invoices.append(Invoice(
                    invoiceID=result[0],
                    employeId=result[1],
                    clientId=result[2],
                    invoiceDate=result[3],
                    totalPrize=result[4],
                    products=products
                ))
            return invoices
        