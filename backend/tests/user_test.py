import unittest
from unittest.mock import MagicMock, patch
import asyncio
import sys

sys.path.append("../")

with patch('connect.get_db_connection') as mock_db_conn:
    # Create a mock connection
    mock_connection = MagicMock()
    mock_db_conn.return_value = mock_connection

    from DAO.employeDAO import EmployeDAO
    from DAO.employe import Employe

    from routers import user as employe

class TestEmployeDAO(unittest.TestCase):
    def setUp(self):
        self.mock_employe_dao = MagicMock(spec=EmployeDAO)

        # Store original DAO and inject mock
        self.original_dao = employe.employeDAO
        employe.employeDAO = self.mock_employe_dao

        # Save reference to module
        self.employe_module = employe

    def tearDown(self):
        # Restore original DAO
        employe.employeDAO  = self.original_dao

    def test_get_user(self):
        async def _async_test():
            # Simulate a token
            test_token = {
                "sub": "test_id",
                "name": "Test",
                "family_name": "User",
                "email": "test@example.com"
            }
            # Create a employee object to return
            employee_obj = Employe(
                employe_id=test_token["sub"],
                name=test_token["name"],
                family_name=test_token["family_name"],
                email=test_token["email"],
                rol=0
            )
            # Expected JSON data that will be returned
            expected_data = employee_obj.getUserJSON()
            # Mock the DAO method
            self.mock_employe_dao.retriveOrCreate.return_value = employee_obj
            result = await self.employe_module.get_user(test_token)
            # Check if the result matches the expected data
            self.mock_employe_dao.retriveOrCreate.assert_called_once()
            self.assertEqual(result, expected_data)

        asyncio.run(_async_test())

    def test_update_user(self):
        async def _async_test():
            # Simulate a employee creation request
            test_data = {
                "employe_id": "12345",
                "name": "John",
                "family_name": "Doe",
                "email": "john.doe@example.com",
                "rol": "0"
            }

            # Create a employee object to return
            employee_obj = Employe(
                employe_id=test_data["employe_id"],
                name=test_data["name"],
                family_name=test_data["family_name"],
                email=test_data["email"],
                rol=int(test_data["rol"])
            )

            # Expected JSON data that will be returned
            expected_data = employee_obj.getUserJSON()

            # Mock the DAO method
            self.mock_employe_dao.update_employee.return_value = employee_obj

            result = await self.employe_module.update_user(test_data)

            # Check if the result matches the expected data
            self.mock_employe_dao.update_employee.assert_called_once()
            self.assertEqual(result, expected_data)

        asyncio.run(_async_test())

    def test_get_all_users(self):
        async def _async_test():
            # Simulate a employee creation request
            test_data = {
                "employe_id": "12345",
                "name": "John",
                "family_name": "Doe",
                "email": "john.doe@example.com",
                "rol": "0"
            }

            # Create a employee object to return
            employee_obj = Employe(
                employe_id=test_data["employe_id"],
                name=test_data["name"],
                family_name=test_data["family_name"],
                email=test_data["email"],
                rol=int(test_data["rol"])
            )

            # Expected JSON data that will be returned
            expected_data = employee_obj.getUserJSON()

            # Mock the DAO method
            self.mock_employe_dao.get_all_employees.return_value = [employee_obj]

            result = await self.employe_module.get_all_users()

            # Check if the result matches the expected data
            self.mock_employe_dao.get_all_employees.assert_called_once()
            self.assertEqual(result, [expected_data])

        asyncio.run(_async_test())
    
    def test_update_user_invalid_rol(self):
        async def _async_test():
            # Simulate a employee creation request
            test_data = {
                "employe_id": "12345",
                "name": "John",
                "family_name": "Doe",
                "email": "john.doe@example.com",
                "rol": "5"
            }

            # Mock the DAO method
            self.mock_employe_dao.update_employee.side_effect = ValueError("rol must be between 1 and 4")

            with self.assertRaises(ValueError):
                await self.employe_module.update_user(test_data)

        asyncio.run(_async_test()) 

if __name__ == "__main__":
    unittest.main()