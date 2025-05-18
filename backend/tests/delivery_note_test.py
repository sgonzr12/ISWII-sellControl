import unittest
from unittest.mock import MagicMock, patch
import asyncio
import datetime

import sys

sys.path.append("../")
from DAO.deliveryNoteDAO import DeliveryNoteDAO
from DAO.product import Product

from DAO.order import Order
from DAO.deliveryNote import DeliveryNote, DeliveryNoteModel, ProductInDeliveryNote
from DAO.client import Client
from DAO.employe import Employe
from DAO.clientDAO import ClientDAO

from routers import deliveryNote

class TestDeliveryNoteDAO(unittest.TestCase):
    def setUp(self):
        self.mock_delivery_note_dao = MagicMock(spec=DeliveryNoteDAO)

        # Store original DAO and inject mock
        self.original_dao = deliveryNote.deliveryNoteDAO
        deliveryNote.deliveryNoteDAO = self.mock_delivery_note_dao

        # Save reference to module
        self.delivery_note_module = deliveryNote

    def tearDown(self):
        # Restore original DAO
        deliveryNote.deliveryNoteDAO  = self.original_dao

    def test_create_delivery_note(self):
        async def _async_test():
            product = Product(productId=1, name="Test Product", description="Test Description", stock=100, minStock=1, maxStock=10, purchasePrice=5.0, sellPrice=10.0)
            # Simulate a token
            note_data = {
                "deliveryNoteID": "d72747",
                "employeId": "1",
                "clientId": "72747",
                "products": [(product, 2)],
                "deliveryNoteDate": None,
                "totalPrice": None,
                "orderID": "72747"
            }
            
            with patch("routers.order.OrderDAO.get_order_by_id") as mock_get_order:
                mock_order = MagicMock(spec=Order)
                mock_order.clientId = "72747"
                mock_order.products = [(product, 2)]
                mock_get_order.return_value = mock_order

                response = await self.delivery_note_module.create_delivery_note(note_data, token={"sub": "1"})

                self.assertIsNone(response)
                self.mock_delivery_note_dao.create_delivery_note.assert_called_once()

        asyncio.run(_async_test())

    def test_get_all_delivery_notes(self):
        async def _async_test():
            # Simulate a token
            product = Product(productId=1, name="Test Product", description="Test Description", stock=100, minStock=1, maxStock=10, purchasePrice=5.0, sellPrice=10.0)

            note_data_1 = {
                "deliveryNoteID": "d72747",
                "employeId": "1",
                "clientId": "72747",
                "products": [(product, 2)],
                "deliveryNoteDate": None,
                "totalPrice": None,
                "orderID": "72747"
            }
            note_data_2 = {
                "deliveryNoteID": "d72748",
                "employeId": "1",
                "clientId": "72748",
                "products": [(product, 3)],
                "deliveryNoteDate": None,
                "totalPrice": None,
                "orderID": "72748"
            }

            note_obj_1 = DeliveryNote(
                deliveryNoteID=note_data_1["deliveryNoteID"],
                employeId=note_data_1["employeId"],
                clientId=note_data_1["clientId"],
                products=note_data_1["products"],
                deliveryNoteDate=datetime.date.today(),
                totalPrice=100.0
            )

            note_obj_2 = DeliveryNote(
                deliveryNoteID=note_data_2["deliveryNoteID"],
                employeId=note_data_2["employeId"],
                clientId=note_data_2["clientId"],
                products=note_data_2["products"],
                deliveryNoteDate=datetime.date.today(),
                totalPrice=150.0
            )

            expected_json_1 = DeliveryNoteModel(
                DeliveryNoteID=note_data_1["deliveryNoteID"],
                employeID=note_data_1["employeId"],
                employeName="John Doe",
                clientID=note_data_1["clientId"],
                clientName="Test Company",
                products=[ProductInDeliveryNote(
                    id=product.productId,
                    name=product.name,
                    quantity=2
                )],
                totalPrice=100.0,
                date=datetime.date.today()
            )

            expected_json_2 = DeliveryNoteModel(
                DeliveryNoteID=note_data_2["deliveryNoteID"],
                employeID=note_data_2["employeId"],
                employeName="John Doe",
                clientID=note_data_2["clientId"],
                clientName="Test Company",
                products=[ProductInDeliveryNote(
                    id=product.productId,
                    name=product.name,
                    quantity=3
                )],
                totalPrice=150.0,
                date=datetime.date.today()
            )


            with patch("DAO.employeDAO.EmployeDAO.get_employee_by_id") as get_employe_by_id:
                mock_employee = MagicMock(spec=Employe)
                mock_employee.employeId = "1"
                mock_employee.name = "John Doe"
                get_employe_by_id.return_value = mock_employee

                mock_client = MagicMock(spec=Client)
                mock_client.clientId = "72747"
                mock_client.CompanyName = "Test Company"
                ClientDAO.get_client_by_id = mock_client

                note_obj_1.get_json = MagicMock(return_value=expected_json_1)
                note_obj_2.get_json = MagicMock(return_value=expected_json_2)

                self.mock_delivery_note_dao.get_all_delivery_notes.return_value = [note_obj_1,note_obj_2]
                expected_data = [note_obj_1.get_json(), note_obj_2.get_json()]

                response = await self.delivery_note_module.get_all_delivery_notes("1")
                self.assertIsInstance(response, list)
                self.assertEqual(response, expected_data)

        asyncio.run(_async_test())

    def test_creatr_delivery_note_no_orderID(self):
        async def _async_test():
            note_data = {
                "deliveryNoteID": "d72747",
                "employeId": "1",
                "clientId": "72747",
                "products": [],
                "deliveryNoteDate": None,
                "totalPrice": None,
                "orderID": None
            }

            with self.assertRaises(Exception) as context:
                await self.delivery_note_module.create_delivery_note(note_data, token={"sub": "1"})
            self.assertEqual(str(context.exception), "400: Missing required fields")

        asyncio.run(_async_test())

    def test_create_delivery_note_unauthorized(self):
        async def _async_test():
            note_data = {
                "deliveryNoteID": "d72747",
                "employeId": "1",
                "clientId": "72747",
                "products": [],
                "deliveryNoteDate": None,
                "totalPrice": None,
                "orderID": "72747"
            }

            with self.assertRaises(Exception) as context:
                await self.delivery_note_module.create_delivery_note(note_data, token={"sub": ""})
            self.assertEqual(str(context.exception), "401: Unauthorized")

        asyncio.run(_async_test())

    def test_create_delivery_note_order_not_found(self):
        async def _async_test():
            note_data = {
                "deliveryNoteID": "d72747",
                "employeId": "1",
                "clientId": "72747",
                "products": [],
                "deliveryNoteDate": None,
                "totalPrice": None,
                "orderID": "72747"
            }

            with patch("routers.order.OrderDAO.get_order_by_id") as mock_get_order:
                mock_get_order.return_value = None

                with self.assertRaises(Exception) as context:
                    await self.delivery_note_module.create_delivery_note(note_data, token={"sub": "1"})
                self.assertEqual(str(context.exception), "404: Order not found")

        asyncio.run(_async_test())
        
if __name__ == "__main__":
    unittest.main()