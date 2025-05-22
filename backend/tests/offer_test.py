import unittest
from unittest.mock import MagicMock, patch
import asyncio
import sys

sys.path.append("../")

with patch('connect.get_db_connection') as mock_db_conn:
    # Create a mock connection
    mock_connection = MagicMock()
    mock_db_conn.return_value = mock_connection

    from DAO.offerDAO import OfferDAO
    from DAO.offer import Offer

    from DAO.product import Product
    from DAO.employe import Employe
    from DAO.client import Client

    from routers import offer

class TestOfferRouter(unittest.TestCase):
    def setUp(self):
        self.mock_offer_dao = MagicMock(spec=OfferDAO)
        self.original_offer_dao = offer.offerDAO
        offer.offerDAO = self.mock_offer_dao

        # Save reference to module
        self.offer_module = offer

    def tearDown(self):
        # Restore original DAOs
        offer.offerDAO = self.original_offer_dao

    def test_create_offer(self):
        async def _async_test():
            # Simulate a offer creation request
            test_data = offer.createOfferModel(
                clientID="1",
                products=[{
                    "id": "1",
                    "quantity": "2"
                }, {
                    "id": "2",
                    "quantity": "3"
                }]
            )

            # Create a Offer object to return
            offer_obj = Offer(
                employeId="1",
                clientId=test_data.clientID,
                products= [
                    (Product(productId=1, name="Product 1", description="Description 1", stock=100, minStock=10, maxStock=50, purchasePrice=5.0, sellPrice=10.0), 2),
                    (Product(productId=2, name="Product 2", description="Description 2", stock=200, minStock=20, maxStock=100, purchasePrice=10.0, sellPrice=20.0), 3)
                ],
            )

            # Use patch context manager to mock the method
            with patch('DAO.employeDAO.EmployeDAO.get_employee_by_id') as mock_get_employee:

                mock_employee = MagicMock(spec=Employe)
                mock_employee.employeId = "1"
                mock_employee.name = "John Doe"
                offer_obj.get_offer_employe = MagicMock(return_value=mock_employee)
                mock_get_employee.return_value = mock_employee

                mock_client = MagicMock(spec=Client)
                mock_client.clientId = "1"
                mock_client.CompanyName = "Test Company"
                offer_obj.get_offer_client = MagicMock(return_value=mock_client)

                offer_obj.get_json()

                # Mock the DAO method
                self.mock_offer_dao.create_offer.return_value = offer_obj

                await self.offer_module.create_offer(test_data, token={"sub": "1"})

                self.mock_offer_dao.create_offer.assert_called_once()

        asyncio.run(_async_test())

    def test_get_all_offers(self):
        async def _async_test():
            # Simulate a request to get all clients
            test_data = offer.createOfferModel(
                clientID="1",
                products=[{
                    "id": "1",
                    "quantity": "2"
                }, {
                    "id": "2",
                    "quantity": "3"
                }]
            )

            # Create a Offer object to return
            offer_obj = Offer(
                employeId="1",
                clientId=test_data.clientID,
                products= [
                    (Product(productId=1, name="Product 1", description="Description 1", stock=100, minStock=10, maxStock=50, purchasePrice=5.0, sellPrice=10.0), 2),
                    (Product(productId=2, name="Product 2", description="Description 2", stock=200, minStock=20, maxStock=100, purchasePrice=10.0, sellPrice=20.0), 3)
                ],
            )

            # Use patch context manager to mock the method
            with patch('DAO.employeDAO.EmployeDAO.get_employee_by_id') as mock_get_employee:

                mock_employee = MagicMock(spec=Employe)
                mock_employee.employeId = "1"
                mock_employee.name = "John Doe"
                offer_obj.get_offer_employe = MagicMock(return_value=mock_employee)
                mock_get_employee.return_value = mock_employee

                mock_client = MagicMock(spec=Client)
                mock_client.clientId = "1"
                mock_client.CompanyName = "Test Company"
                offer_obj.get_offer_client = MagicMock(return_value=mock_client)

                # Mock the DAO method
                self.mock_offer_dao.get_all_offers.return_value = [offer_obj]
                expected_data = [offer_obj.get_json()]

                # Call the function
                result = await self.offer_module.get_all_offers()

                # Check if the result matches the expected data
                self.mock_offer_dao.get_all_offers.assert_called_once()
                self.assertEqual(result, expected_data)


        asyncio.run(_async_test())

    def test_update_offer(self):
        async def _async_test():
            # Simulate a request to update an offer
            test_data = offer.updateOfferModel(
                offerID="1",
                products=[{
                    "id": "1",
                    "quantity": "2"
                }, {
                    "id": "2",
                    "quantity": "3"
                }]
            )

            # Create a Offer object to return
            offer_obj = Offer(
                employeId="1",
                clientId="1",
                products= [
                    (Product(productId=1, name="Product 1", description="Description 1", stock=100, minStock=10, maxStock=50, purchasePrice=5.0, sellPrice=10.0), 2),
                    (Product(productId=2, name="Product 2", description="Description 2", stock=200, minStock=20, maxStock=100, purchasePrice=10.0, sellPrice=20.0), 3)
                ],
            )

            # Use patch context manager to mock the method
            with patch('DAO.employeDAO.EmployeDAO.get_employee_by_id') as mock_get_employee:

                mock_employee = MagicMock(spec=Employe)
                mock_employee.employeId = "1"
                mock_employee.name = "John Doe"
                offer_obj.get_offer_employe = MagicMock(return_value=mock_employee)
                mock_get_employee.return_value = mock_employee

                mock_client = MagicMock(spec=Client)
                mock_client.clientId = "1"
                mock_client.CompanyName = "Test Company"
                offer_obj.get_offer_client = MagicMock(return_value=mock_client)

                # Mock the DAO method
                self.mock_offer_dao.update_offer.return_value = offer_obj

                await self.offer_module.update_offer(test_data, token={"sub": "1"})

                self.mock_offer_dao.update_offer.assert_called_once()

        asyncio.run(_async_test())

    def test_get_no_offers(self):
        async def _async_test():
            # Simulate a request to get all offers
            self.mock_offer_dao.get_all_offers.return_value = []

            # Call the function
            result = await self.offer_module.get_all_offers()

            # Check if the result is an empty list
            self.assertEqual(result, [])

        asyncio.run(_async_test())

    def test_update_offer_no_products(self):
        async def _async_test():
            # Simulate a request to update an offer with no products
            test_data = offer.updateOfferModel(
                offerID="1",
                products=[]
            )

            # Call the function and check for HTTPException
            with self.assertRaises(offer.HTTPException) as context:
                await self.offer_module.update_offer(test_data, token={"sub": "1"})

            self.assertEqual(context.exception.status_code, 400)
            self.assertEqual(context.exception.detail, "At least one product is required")

        asyncio.run(_async_test())

    def test_update_offer_invalid_quantity(self):
        async def _async_test():
            # Simulate a request to update an offer with invalid quantity
            test_data = offer.updateOfferModel(
                offerID="1",
                products=[{
                    "id": "1",
                    "quantity": "-2"
                }]
            )

            # Call the function and check for HTTPException
            with self.assertRaises(offer.HTTPException) as context:
                await self.offer_module.update_offer(test_data, token={"sub": "1"})

            self.assertEqual(context.exception.status_code, 400)
            self.assertEqual(context.exception.detail, "Product quantity must be greater than 0")

        asyncio.run(_async_test())

    def test_update_offer_missing_fields(self):
        async def _async_test():
            # Simulate a request to update an offer with missing fields
            test_data = offer.updateOfferModel(
                offerID="1",
                products=[{
                    "id": "1"
                }]
            )

            # Call the function and check for HTTPException
            with self.assertRaises(offer.HTTPException) as context:
                await self.offer_module.update_offer(test_data, token={"sub": "1"})

            self.assertEqual(context.exception.status_code, 400)
            self.assertEqual(context.exception.detail, "Missing required fields in products")

        asyncio.run(_async_test())

    def test_create_offer_missing_fields(self):
        async def _async_test():
            # Simulate a request to create an offer with missing fields
            test_data = offer.createOfferModel(
                clientID="1",
                products=[{
                    "id": "1"
                }]
            )

            # Call the function and check for HTTPException
            with self.assertRaises(offer.HTTPException) as context:
                await self.offer_module.create_offer(test_data, token={"sub": "1"})

            self.assertEqual(context.exception.status_code, 400)
            self.assertEqual(context.exception.detail, "Missing required fields in products")

        asyncio.run(_async_test())

    def test_create_offer_unauthorized(self):
        async def _async_test():
            # Simulate a request to create an offer with unauthorized access
            test_data = offer.createOfferModel(
                clientID="1",
                products=[{
                    "id": "1",
                    "quantity": "2"
                }]
            )

            # Call the function and check for HTTPException
            with self.assertRaises(offer.HTTPException) as context:
                await self.offer_module.create_offer(test_data, token={"sub": ""})

            self.assertEqual(context.exception.status_code, 401)
            self.assertEqual(context.exception.detail, "Unauthorized")

        asyncio.run(_async_test())

if __name__ == "__main__":
    unittest.main()