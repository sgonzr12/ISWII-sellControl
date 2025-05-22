import unittest
from unittest.mock import MagicMock, patch
import asyncio
import sys

sys.path.append("../")

with patch('connect.get_db_connection') as mock_db_conn:
    # Create a mock connection
    mock_connection = MagicMock()
    mock_db_conn.return_value = mock_connection

    from DAO.clientDAO import ClientDAO
    from DAO.client import Client

    from routers import client

class TestClientRouter(unittest.TestCase):
    def setUp(self):
        self.mock_client_dao = MagicMock(spec=ClientDAO)

        # Store original DAO and inject mock
        self.original_dao = client.clientDAO
        client.clientDAO = self.mock_client_dao
        
        # Save reference to module
        self.client_module = client

    def tearDown(self):
        # Restore original DAO
        client.clientDAO = self.original_dao

    def test_create_client(self):
        async def _async_test():
            # Simulate a client creation request
            test_data = {
                "CompanyName": "Test Company",
                "CIF": "12345678A",
                "address": "123 Test St",
                "email": "test@example.com",
                "phone": "123456789",
                "contact": "John Doe"
            }

            # Create a Client object to return
            client_obj = Client(
                CompanyName=test_data["CompanyName"],
                CIF=test_data["CIF"],
                address=test_data["address"],
                email=test_data["email"],
                phone=int(test_data["phone"]),
                contact=test_data["contact"]
            )

            # Expected JSON data that will be returned
            expected_data = client_obj.getClientJSON()

            # Mock the DAO method
            self.mock_client_dao.create_client.return_value = client_obj

            result = await self.client_module.create_client(test_data)

            # Check if the result matches the expected data
            self.mock_client_dao.create_client.assert_called_once()
            self.assertEqual(result, expected_data)

        asyncio.run(_async_test())

    def test_get_all_clients(self):
        async def _async_test():
            # Simulate a request to get all clients
            test_data = [
                {
                    "CompanyName": "Test Company",
                    "CIF": "12345678A",
                    "address": "123 Test St",
                    "email": "test@example.com",
                    "phone": "123456789",
                    "contact": "John Doe"
                },
                {
                    "CompanyName": "Another Company",
                    "CIF": "87654321B",
                    "address": "456 Another St",
                    "email": "another@example.com",
                    "phone": "987654321",
                    "contact": "Jane Smith"
                }
            ]

            # Create Client objects to return
            client_obj1 = Client(
                CompanyName=test_data[0]["CompanyName"],
                CIF=test_data[0]["CIF"],
                address=test_data[0]["address"],
                email=test_data[0]["email"],
                phone=int(test_data[0]["phone"]),
                contact=test_data[0]["contact"]
            )
            client_obj2 = Client(
                CompanyName=test_data[1]["CompanyName"],
                CIF=test_data[1]["CIF"],
                address=test_data[1]["address"],
                email=test_data[1]["email"],
                phone=int(test_data[1]["phone"]),
                contact=test_data[1]["contact"]
            )

            # Mock the DAO method
            self.mock_client_dao.get_all_clients.return_value = [client_obj1, client_obj2]
            expected_data = [client_obj1.getClientJSON(), client_obj2.getClientJSON()]

            result = await self.client_module.get_all_clients()

            # Check if the result matches the expected data
            self.mock_client_dao.get_all_clients.assert_called_once()
            self.assertEqual(result, expected_data)

        asyncio.run(_async_test())

    def test_update_client(self):
        async def _async_test():
            # Simulate a client update request
            test_data = {
                "clientID": "0",
                "CompanyName": "Updated Company",
                "CIF": "12345678A",
                "address": "789 Updated St",
                "email": "updated@example.com",
                "phone": "123456789",
                "contact": "John Doe"
            }

            # Create a Client object to return
            client_obj = Client(
                clientID=int(test_data["clientID"]),
                CompanyName=test_data["CompanyName"],
                CIF=test_data["CIF"],
                address=test_data["address"],
                email=test_data["email"],
                phone=int(test_data["phone"]),
                contact=test_data["contact"]
            )

            # Mock the DAO method
            self.mock_client_dao.update_client.return_value = client_obj
            expected_data = client_obj.getClientJSON()

            result = await self.client_module.update_client(test_data)

            # Check if the result matches the expected data
            self.mock_client_dao.update_client.assert_called_once()
            self.assertEqual(result, expected_data)

        asyncio.run(_async_test())

    def test_create_client_invalid_company_name(self):
        async def _async_test():
            # Simulate a client creation request with invalid company name
            test_data = {
                "CompanyName": "",
                "CIF": "12345678A",
                "address": "123 Test St",
                "email": "test@example.com",
                "phone": "123456789",
                "contact": "John Doe"
            }

            # Mock the DAO method to raise an exception
            self.mock_client_dao.create_client.side_effect = Exception("Client verification failed, missing fields")

            # Check if the exception is raised
            with self.assertRaises(Exception) as context:
                await self.client_module.create_client(test_data)

            self.assertEqual(str(context.exception), "400: Client verification failed, missing fields")
        
        asyncio.run(_async_test())

    def test_create_client_invalid_cif(self):
        async def _async_test():
            # Simulate a client creation request with invalid cif
            test_data = {
                "CompanyName": "Test Company",
                "CIF": "",
                "address": "123 Test St",
                "email": "test@example.com",
                "phone": "123456789",
                "contact": "John Doe"
            }

            # Mock the DAO method to raise an exception
            self.mock_client_dao.create_client.side_effect = Exception("Client verification failed, missing fields")

            # Check if the exception is raised
            with self.assertRaises(Exception) as context:
                await self.client_module.create_client(test_data)

            self.assertEqual(str(context.exception), "400: Client verification failed, missing fields")
        
        asyncio.run(_async_test())

    def test_create_client_invalid_address(self):
        async def _async_test():
            # Simulate a client creation request with invalid address
            test_data = {
                "CompanyName": "Test Company",
                "CIF": "12345678A",
                "address": "",
                "email": "test@example.com",
                "phone": "123456789",
                "contact": "John Doe"
            }

            # Mock the DAO method to raise an exception
            self.mock_client_dao.create_client.side_effect = Exception("Client verification failed, missing fields")

            # Check if the exception is raised
            with self.assertRaises(Exception) as context:
                await self.client_module.create_client(test_data)

            self.assertEqual(str(context.exception), "400: Client verification failed, missing fields")
        
        asyncio.run(_async_test())

    def test_create_client_invalid_email(self):
        async def _async_test():
            # Simulate a client creation request with invalid email
            test_data = {
                "CompanyName": "Test Company",
                "CIF": "12345678A",
                "address": "123 Test St",
                "email": "",
                "phone": "123456789",
                "contact": "John Doe"
            }

            # Mock the DAO method to raise an exception
            self.mock_client_dao.create_client.side_effect = Exception("Client verification failed, missing fields")

            # Check if the exception is raised
            with self.assertRaises(Exception) as context:
                await self.client_module.create_client(test_data)

            self.assertEqual(str(context.exception), "400: Client verification failed, missing fields")
        
        asyncio.run(_async_test())

    def test_create_client_invalid_phone(self):
        async def _async_test():
            # Simulate a client creation request with invalid phone
            test_data = {
                "CompanyName": "Test Company",
                "CIF": "12345678A",
                "address": "123 Test St",
                "email": "test@example.com",
                "phone": "0",
                "contact": "John Doe"
            }

            # Mock the DAO method to raise an exception
            self.mock_client_dao.create_client.side_effect = Exception("Client verification failed, missing fields")

            # Check if the exception is raised
            with self.assertRaises(Exception) as context:
                await self.client_module.create_client(test_data)

            self.assertEqual(str(context.exception), "400: Client verification failed, missing fields")
        
        asyncio.run(_async_test())

    def test_create_client_invalid_contact(self):
        async def _async_test():
            # Simulate a client creation request with invalid contact
            test_data = {
                "CompanyName": "Test Company",
                "CIF": "12345678A",
                "address": "123 Test St",
                "email": "test@example.com",
                "phone": "123456789",
                "contact": ""
            }

            # Mock the DAO method to raise an exception
            self.mock_client_dao.create_client.side_effect = Exception("Client verification failed, missing fields")

            # Check if the exception is raised
            with self.assertRaises(Exception) as context:
                await self.client_module.create_client(test_data)

            self.assertEqual(str(context.exception), "400: Client verification failed, missing fields")
        
        asyncio.run(_async_test())

if __name__ == "__main__":
    unittest.main()