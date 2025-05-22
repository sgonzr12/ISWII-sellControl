import unittest
from unittest.mock import MagicMock, patch
import asyncio
import datetime
import sys

sys.path.append("../")

with patch('connect.get_db_connection') as mock_db_conn:
    # Create a mock connection
    mock_connection = MagicMock()
    mock_db_conn.return_value = mock_connection

    from DAO.orderDAO import OrderDAO
    from DAO.order import Order, OrderModel, ProductInOrder

    from DAO.product import Product
    from DAO.offer import Offer
    from DAO.employe import Employe
    import DAO.employeDAO
    from DAO.client import Client
    import DAO.clientDAO

    from routers import order

class TestOrderDAO(unittest.TestCase):

    def setUp(self):
        self.mock_order_dao = MagicMock(spec=OrderDAO)

        # Store original DAO and inject mock
        self.original_dao = order.orderDAO
        order.orderDAO = self.mock_order_dao

        # Save reference to module
        self.order_module = order

    def tearDown(self):
        # Restore original DAO
        order.orderDAO = self.original_dao

    def test_create_order(self):
        async def _async_test():
            # Simulate a token
            order_data = {
                "offerID": "72747"
            }

            # Create a order object to return
            product = Product(productId=1, name="Test Product", description="Test Description", stock=100, minStock=1, maxStock=10, purchasePrice=5.0, sellPrice=10.0)
            order_obj = Order(
                orderID="77345",
                employeId="1",
                clientId="82345",
                products=[(product, 2)],
                orderDate=None,
                totalPrice=None
            )

            expected_json = OrderModel(
                orderID=order_obj.orderID,
                employeID=order_obj.employeId,
                employeName="John Doe",
                clientID=order_obj.clientId,
                date=datetime.date.today(),
                clientName="Test Company",
                products=[ProductInOrder(id=product.productId, name=product.name, quantity=2)],
                totalPrice=order_obj.calculatePrice(order_obj.products),
            )
            
            order_obj.get_json = MagicMock(return_value=expected_json)

            with patch("routers.order.offerDAO.get_offer_by_id") as mock_get_offer, \
                patch("routers.order.Order.get_json") as mock_get_json, \
                patch("routers.order.orderDAO.check_order_exists", return_value=False):

                mock_offer = MagicMock(spec=Offer)
                mock_offer.clientID = "82345"
                mock_offer.products = [(product, 2)]
                mock_get_offer.return_value = mock_offer

                mock_employee = MagicMock(spec=Employe)
                mock_employee.employeId = "1"
                mock_employee.name = "John Doe"
                DAO.employeDAO.EmployeDAO.get_employee_by_id = mock_employee

                mock_client = MagicMock(spec=Client)
                mock_client.clientId = "1"
                mock_client.CompanyName = "Test Company"
                DAO.clientDAO.ClientDAO.get_client_by_id = mock_client

                # Mock the DAO method
                self.mock_order_dao.create_order.return_value = order_obj

                # Call the function
                await self.order_module.create_order(order_data, token={"sub": "1"})

                # Assertions
                self.mock_order_dao.create_order.assert_called_once()

        asyncio.run(_async_test())

    def test_get_all_orders(self):
        async def _async_test():
            # Create a order object to return
            product = Product(productId=1, name="Test Product", description="Test Description", stock=100, minStock=1, maxStock=10, purchasePrice=5.0, sellPrice=10.0)
            order_obj = Order(
                orderID="77345",
                employeId="1",
                clientId="82345",
                products=[(product, 2)],
                orderDate=None,
                totalPrice=None
            )

            expected_json = OrderModel(
                orderID=order_obj.orderID,
                employeID=order_obj.employeId,
                employeName="John Doe",
                clientID=order_obj.clientId,
                date=datetime.date.today(),
                clientName="Test Company",
                products=[ProductInOrder(id=product.productId, name=product.name, quantity=2)],
                totalPrice=order_obj.calculatePrice(order_obj.products),
            )

            order_obj.get_json = MagicMock(return_value=expected_json)

            # Mock the DAO method
            self.mock_order_dao.get_all_orders.return_value = [order_obj]

            with patch("routers.order.orderDAO.get_all_orders") as mock_get_all_orders:
                mock_get_all_orders.return_value = [order_obj]
                
                # Call the function
                result = await self.order_module.get_all_orders(token="1")

                # Assertions
                self.mock_order_dao.get_all_orders.assert_called_once()
                self.assertEqual(len(result), 1)
                self.assertEqual(result[0].orderID, order_obj.orderID)

        asyncio.run(_async_test())

    def test_create_order_missing_fields(self):
        async def _async_test():
            order_data = {
                "offerID": ""
            }

            with self.assertRaises(order.HTTPException) as context:
                await self.order_module.create_order(order_data, token={"sub": "1"})
            self.assertEqual(context.exception.status_code, 400)
            self.assertEqual(context.exception.detail, "Missing required fields")

        asyncio.run(_async_test())

    def test_create_order_unauthorized(self):
        async def _async_test():
            order_data = {
                "offerID": "72747"
            }      

            with self.assertRaises(order.HTTPException) as context:
                await self.order_module.create_order(order_data, token={"sub": ""})
            self.assertEqual(context.exception.status_code, 401)
            self.assertEqual(context.exception.detail, "Unauthorized")

        asyncio.run(_async_test())

    def test_create_order_offer_not_found(self):
        async def _async_test():
            order_data = {
                "offerID": "72747"
            }

            with patch("routers.order.offerDAO.get_offer_by_id", return_value=None):
                with self.assertRaises(order.HTTPException) as context:
                    await self.order_module.create_order(order_data, token={"sub": "1"})

                self.assertEqual(context.exception.status_code, 404)
                self.assertEqual(context.exception.detail, "Offer not found")

        asyncio.run(_async_test())

    def test_get_order_already_exists(self):
        async def _async_test():
            order_data = {
                "offerID": "72747"
            }

            with patch("routers.order.orderDAO.get_order_by_id", return_value=True), \
                patch("routers.order.offerDAO.get_offer_by_id") as mock_get_offer:
                mock_offer = MagicMock(spec=Offer)
                mock_offer.clientID = "82345"
                mock_offer.products = [(Product(productId=1, name="Test Product", description="Test Description", stock=100, minStock=1, maxStock=10, purchasePrice=5.0, sellPrice=10.0), 2)]
                mock_get_offer.return_value = mock_offer

                with self.assertRaises(order.HTTPException) as context:
                    await self.order_module.create_order(order_data, token={"sub": "1"})
                self.assertEqual(context.exception.status_code, 400)
                self.assertEqual(context.exception.detail, "Order already exists")

        asyncio.run(_async_test())

if __name__ == "__main__":
    unittest.main()