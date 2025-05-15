from fastapi import HTTPException
import logging

from connect import get_db_connection
from DAO.order import Order
from DAO.product import Product
from DAO.productDAO import ProductDAO

class OrderDAO:
    def __init__(self):
        """
        Initialize the DAO with a database connection.
        :param db_connection: A database connection object.
        """
        self.db_connection = get_db_connection()
        self.logger = logging.getLogger("appLogger")

    def create_order(self, order: Order) -> None:
        """
        Insert a new order into the database.
        :param order: An Order object containing order details.
        :return: The ID of the newly created order.
        """
        query = """
        INSERT INTO "Orders" ("OrderID", "EmployeID", "ClientID", "Date", "TotalPrice")
        VALUES (%s, %s, %s, %s, %s)
        """

        logging.debug(f"Creating order: {order}")

        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (
                order.orderID,
                order.employeId,
                order.clientId,
                order.date,
                order.totalPrice
            ))

            # Insert products into ProdOrd table
            for productTup in order.products:
                # Assuming product is a dictionary with 'Product' and 'quantity'
                prod_query = """
                INSERT INTO "ProdOrd" ("OrderID", "ProductID", "Quantity")
                VALUES (%s, %s, %s);
                """
                product, quantity = productTup  # Unpack the tuple
                cursor.execute(prod_query, (
                    order.orderID,
                    product.productId,
                    quantity
                ))

            self.db_connection.commit()
            logging.info(f"Order created with ID: {order.orderID}")
        
    def get_order_by_id(self, order_id: str) -> Order:
        """
        Retrieve an order by its ID, including its products.
        :param order_id: The ID of the order.
        :return: An Order object containing the order details or None if not found.
        """
        query = """
        SELECT *
        FROM "Orders"
        WHERE "OrderID" = %s;
        """

        logging.debug(f"Retrieving order with ID: {order_id}")

        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (order_id,))
            result = cursor.fetchone()
            if result:

                # Retrieve products for this order
                product_dao = ProductDAO()
                product_query = """
                SELECT "ProductID", "Quantity"
                    FROM "ProdOrd"
                    WHERE "OrderID" = %s;
                """
                cursor.execute(product_query, (order_id,))
                products = list[tuple[Product, int]]()
                
                for row in cursor.fetchall():
                    product_id, quantity = row
                    product = product_dao.get_product_by_id(product_id)
                    if product:
                        products.append((product, quantity))
                    else:
                        logging.error(f"Product with ID {product_id} not found.")
                        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found.")
                # Create and return the Order object
                order = Order(
                    orderID=result[0],
                    employeId=result[1],
                    clientId=result[2],
                    orderDate=result[3],
                    totalPrice=result[4],
                    products=products
                )
            
                logging.info(f"Order found: {order}")
                return order
            else:
                self.logger.error(f"Order with ID {order_id} not found.")
                raise HTTPException(status_code=404, detail="Order not found")
            
    def update_order(self, updated_order: Order) -> bool:
        """
        Update an existing order in the database.
        :param order: An Order object containing updated order details.
        """
        query = """
        UPDATE "Orders"
        SET "EmployeID" = %s, "ClientID" = %s, "Date" = %s, "TotalPrice" = %s
        WHERE "OrderID" = %s;
        """

        logging.debug(f"Updating order: {updated_order}")

        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (
                updated_order.employeId,
                updated_order.clientId,
                updated_order.date,
                updated_order.totalPrice,
                updated_order.orderID
            ))
            
            # Update products in ProdOrd table
            delete_query = """ DELETE FROM "ProdOrd" WHERE "OrderID" = %s; """
            cursor.execute(delete_query, (updated_order.orderID,))
            
            for productTup in updated_order.products:
                # Assuming product is a dictionary with 'Product' and 'quantity'
                prod_query = """
                INSERT INTO ProdOrd ("OrderID", productID, quantity)
                VALUES (%s, %s, %s);
                """
                product, quantity = productTup
                cursor.execute(prod_query, (
                    updated_order.orderID,
                    product.productId,
                    quantity
                ))

            self.db_connection.commit()
            logging.info(f"Order updated with ID: {updated_order.orderID}")
            return cursor.rowcount > 0
            
    def delete_order(self, order_id: int) -> bool:
        """
        Delete an order from the database.
        :param order_id: The ID of the order to delete.
        :return: True if the deletion was successful, False otherwise.
        """

        logging.debug(f"Deleting order with ID: {order_id}")

        with self.db_connection.cursor() as cursor:
            # Delete products associated with the order
            delete_products_query = """
            DELETE FROM "ProdOrd"
            WHERE "OrderID" = %s;
            """
            cursor.execute(delete_products_query, (order_id,))
            
            # Delete the order itself
            delete_order_query = """
            DELETE FROM "Orders"
            WHERE "OrderID" = %s;
            """
            cursor.execute(delete_order_query, (order_id,))
            
            self.db_connection.commit()
            logging.info(f"Order with ID {order_id} deleted")
            return cursor.rowcount > 0
        
    def get_all_orders(self) -> list[Order]:
        """
        Retrieve all orders from the database.
        :return: A list of Order objects.
        """
        query = """
        SELECT *
        FROM "Orders";
        """

        logging.debug("Retrieving all orders")

        with self.db_connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            orders = list[Order]()
            for row in results:
                order_id, employe_id, client_id, order_date, total_Price = row
                
                # Retrieve products for this order
                product_dao = ProductDAO()
                product_query = """
                SELECT "ProductID", "Quantity"
                    FROM "ProdOrd"
                    WHERE "OrderID" = %s;
                """
                cursor.execute(product_query, (order_id,))
                products = list[tuple[Product, int]]()
                
                for row in cursor.fetchall():
                    product_id, quantity = row
                    product = product_dao.get_product_by_id(product_id)
                    if product:
                        products.append((product, quantity))
                    else:
                        logging.error(f"Product with ID {product_id} not found.")
                        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found.")
                
                # Create and append the Order object to the list
                order = Order(
                    orderID=order_id,
                    employeId=employe_id,
                    clientId=client_id,
                    orderDate=order_date,
                    totalPrice=total_Price,
                    products=products
                )
                
                orders.append(order)
            
            logging.info(f"Retrieved all {len(orders)} orders")
            return orders