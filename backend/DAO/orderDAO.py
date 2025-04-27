import psycopg2.extensions
from order import Order
from product import Product
from productDAO import ProductDAO

class OrderDAO:
    def __init__(self, db_connection: psycopg2.extensions.connection):
        """
        Initialize the DAO with a database connection.
        :param db_connection: A database connection object.
        """
        self.db_connection = db_connection

    def create_order(self, order: Order) -> int:
        """
        Insert a new order into the database.
        :param order: An Order object containing order details.
        :return: The ID of the newly created order.
        """
        query = """
        INSERT INTO orders (employeId, clientID, order_date, totalPrize)
        VALUES (%s, %s, %s, %s)
        RETURNING orderID;
        """
        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (
                order.employeId,
                order.clientId,
                order.date,
                order.totalPrize
            ))
            
            result = cursor.fetchone()
            if result is None:
                raise ValueError("Failed to insert order and retrieve its ID.")
            order_id = result[0]

            # Insert products into ProdOrd table
            for productTup in order.products:
                # Assuming product is a dictionary with 'Product' and 'quantity'
                prod_query = """
                INSERT INTO ProdOrd (orderID, productID, quantity)
                VALUES (%s, %s, %s);
                """
                product, quantity = productTup  # Unpack the tuple
                cursor.execute(prod_query, (
                    order_id,
                    product.productId,
                    quantity
                ))

            self.db_connection.commit()
            return order_id
        
    def get_order_by_id(self, order_id: int) -> Order:
        """
        Retrieve an order by its ID, including its products.
        :param order_id: The ID of the order.
        :return: An Order object containing the order details or None if not found.
        """
        query = """
        SELECT *
        FROM orders
        WHERE orderID = %s;
        """
        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (order_id,))
            result = cursor.fetchone()
            if result:

                # Retrieve products for this order
                product_dao = ProductDAO(self.db_connection)
                product_query = """
                SELECT productID, quantity
                    FROM ProdOrd
                    WHERE orderID = %s;
                """
                cursor.execute(product_query, (order_id,))
                products = list[tuple[Product, int]]()
                
                for row in cursor.fetchall():
                    product_id, quantity = row
                    product = product_dao.get_product_by_id(product_id)
                    if product:
                        products.append((product, quantity))
                    else:
                        raise ValueError(f"Product with ID {product_id} not found.")
                # Create and return the Order object
                order = Order(
                    orderID=result[0],
                    employeId=result[1],
                    clientId=result[2],
                    orderDate=result[3],
                    totalPrize=result[4],
                    products=products
                )
            
                return order
            else:
                raise ValueError(f"No order found with ID {order_id}.")
            
    def update_order(self, updated_order: Order) -> bool:
        """
        Update an existing order in the database.
        :param order: An Order object containing updated order details.
        """
        query = """
        UPDATE orders
        SET employeId = %s, clientID = %s, order_date = %s, totalPrize = %s
        WHERE orderID = %s;
        """
        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (
                updated_order.employeId,
                updated_order.clientId,
                updated_order.date,
                updated_order.totalPrize,
                updated_order.orderID
            ))
            
            # Update products in ProdOrd table
            delete_query = """ DELETE FROM ProdOrd WHERE orderID = %s; """
            cursor.execute(delete_query, (updated_order.orderID,))
            
            for productTup in updated_order.products:
                # Assuming product is a dictionary with 'Product' and 'quantity'
                prod_query = """
                INSERT INTO ProdOrd (orderID, productID, quantity)
                VALUES (%s, %s, %s);
                """
                product, quantity = productTup
                cursor.execute(prod_query, (
                    updated_order.orderID,
                    product.productId,
                    quantity
                ))
            self.db_connection.commit()
            return cursor.rowcount > 0
            
    def delete_order(self, order_id: int) -> bool:
        """
        Delete an order from the database.
        :param order_id: The ID of the order to delete.
        :return: True if the deletion was successful, False otherwise.
        """
        with self.db_connection.cursor() as cursor:
            # Delete products associated with the order
            delete_products_query = """
            DELETE FROM ProdOrd
            WHERE orderID = %s;
            """
            cursor.execute(delete_products_query, (order_id,))
            
            # Delete the order itself
            delete_order_query = """
            DELETE FROM orders
            WHERE orderID = %s;
            """
            cursor.execute(delete_order_query, (order_id,))
            
            self.db_connection.commit()
            return cursor.rowcount > 0
        
    def get_all_orders(self) -> list[Order]:
        """
        Retrieve all orders from the database.
        :return: A list of Order objects.
        """
        query = """
        SELECT *
        FROM orders;
        """
        with self.db_connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            orders = list[Order]()
            for row in results:
                order_id, employe_id, client_id, order_date, total_prize = row
                
                # Retrieve products for this order
                product_dao = ProductDAO(self.db_connection)
                product_query = """
                SELECT productID, quantity
                    FROM ProdOrd
                    WHERE orderID = %s;
                """
                cursor.execute(product_query, (order_id,))
                products = list[tuple[Product, int]]()
                
                for row in cursor.fetchall():
                    product_id, quantity = row
                    product = product_dao.get_product_by_id(product_id)
                    if product:
                        products.append((product, quantity))
                    else:
                        raise ValueError(f"Product with ID {product_id} not found.")
                
                # Create and append the Order object to the list
                order = Order(
                    orderID=order_id,
                    employeId=employe_id,
                    clientId=client_id,
                    orderDate=order_date,
                    totalPrize=total_prize,
                    products=products
                )
                
                orders.append(order)
            return orders
        
        
        

