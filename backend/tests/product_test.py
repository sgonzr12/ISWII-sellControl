import unittest
from unittest.mock import MagicMock

import sys
sys.path.append('../')
from DAO import productDAO

from routers import product

class TestProductRouter(unittest.TestCase):

    def setUp(self):
        self.mock_product_dao = MagicMock(spec=productDAO)
        self.product = product

    async def test_create_product(self):
        # Simulate a product creation request
        test_data = {
            "name": "Test Product",
            "description": "Test Description",
            "stock": 10,
            "maxStock": 20,
            "minStock": 5,
            "purchasePrice": 15.0,
            "sellPrice": 25.0
        }
        expected_data = {
            "id": 1,
            "name": "Test Product",
            "description": "Test Description",
            "stock": 10,
            "maxStock": 20,
            "minStock": 5,
            "purchasePrice": 15.0,
            "sellPrice": 25.0
        }
        
        # Mock the DAO method
        self.mock_product_dao.create_product.return_value = expected_data

        result = await self.product.create_product(test_data)

        # Check if the result matches the expected data
        self.mock_product_dao.create_product.assert_called_once_with(test_data)
        self.assertEqual(result, expected_data)

    async def test_get_all_products(self):
        test_data = [{
            "id": 1,
            "name": "Test Product",
            "description": "Test Description",
            "stock": 10,
            "maxStock": 20,
            "minStock": 5,
            "purchasePrice": 15.0,
            "sellPrice": 25.0
        },
        {
            "id": 2,
            "name": "Test Product 2",
            "description": "Test Description 2",
            "stock": 15,
            "maxStock": 25,
            "minStock": 10,
            "purchasePrice": 20.0,
            "sellPrice": 30.0
        }]

        # Mock the DAO method
        self.mock_product_dao.get_all_products.return_value = test_data
        
        
        # Simulate a request to get all products
        expected_data = [
            {
                "id": 1,
                "name": "Test Product 1",
                "description": "Test Description 1",
                "stock": 10,
                "maxStock": 20,
                "minStock": 5,
                "purchasePrice": 15.0,
                "sellPrice": 25.0
            },
            {
                "id": 2,
                "name": "Test Product 2",
                "description": "Test Description 2",
                "stock": 15,
                "maxStock": 25,
                "minStock": 10,
                "purchasePrice": 20.0,
                "sellPrice": 30.0
            }
        ]
        
        # Mock the DAO method
        self.mock_product_dao.get_all_products.return_value = expected_data

        result = await self.product.get_all_products()

        # Check if the result matches the expected data
        self.mock_product_dao.get_all_products.assert_called_once()
        self.assertEqual(result, expected_data)
    
    async def test_update_product(self):
        insert_data = {
            "id": 1,
            "name": "Insert Product",
            "description": "Insert Description",
            "stock": 150,
            "maxStock": 250,
            "minStock": 100,
            "purchasePrice": 2.0,
            "sellPrice": 3.0
        }
        self.mock_product_dao.update_product.return_value = insert_data

        # Simulate a product update request
        test_data = {
            "productId": 1,
            "name": "Updated Product",
            "description": "Updated Description",
            "stock": 15,
            "maxStock": 25,
            "minStock": 10,
            "purchasePrice": 20.0,
            "sellPrice": 30.0
        }

        expected_data = {
            "id": 1,
            "name": "Updated Product",
            "description": "Updated Description",
            "stock": 15,
            "maxStock": 25,
            "minStock": 10,
            "purchasePrice": 20.0,
            "sellPrice": 30.0
        }

        # Mock the DAO method
        self.mock_product_dao.update_product.return_value = expected_data
        result = await self.product.update_product(test_data)

        # Check if the result matches the expected data
        self.mock_product_dao.update_product.assert_called_once_with(test_data)
        self.assertEqual(result, expected_data)

        # Check if the product was updated correctly
        self.assertEqual(result["name"], "Updated Product")

    async def test_update_product_invalid(self):
        # Simulate a product update request with invalid data
        test_data = {
            "productId": 1,
            "name": "",
            "description": "Updated Description",
            "stock": -5,
            "maxStock": 25,
            "minStock": 10,
            "purchasePrice": -20.0,
            "sellPrice": 30.0
        }

        # Mock the DAO method to raise an exception
        self.mock_product_dao.update_product.side_effect = Exception("Product verification failed")

        with self.assertRaises(Exception) as context:
            await self.product.update_product(test_data)
        
        self.assertEqual(str(context.exception), "Product verification failed")

    async def test_create_product_productidnotzero(self):
        # Simulate a product creation request with invalid data
        test_data = {
            "productId": 0,
            "name": "Test Product",
            "description": "Test Description",
            "stock": 10,
            "maxStock": 20,
            "minStock": 5,
            "purchasePrice": 15.0,
            "sellPrice": 25.0
        }

        # Mock the DAO method to raise an exception
        self.mock_product_dao.create_product.side_effect = Exception("Product verification failed")

        with self.assertRaises(Exception) as context:
            await self.product.create_product(test_data)
        
        self.assertEqual(str(context.exception), "Product verification failed")

    async def test_create_product_invalidmaxstock(self):
        # Simulate a product creation request with invalid data
        test_data = {
            "name": "Test Product",
            "description": "Test Description",
            "stock": 10,
            "maxStock": -20,
            "minStock": 5,
            "purchasePrice": 15.0,
            "sellPrice": 25.0
        }

        # Mock the DAO method to raise an exception
        self.mock_product_dao.create_product.side_effect = Exception("Product verification failed")

        with self.assertRaises(Exception) as context:
            await self.product.create_product(test_data)
        
        self.assertEqual(str(context.exception), "Product verification failed")

    async def test_create_product_invalidminstock(self):
        # Simulate a product creation request with invalid data
        test_data = {
            "name": "Test Product",
            "description": "Test Description",
            "stock": 10,
            "maxStock": 20,
            "minStock": -5,
            "purchasePrice": 15.0,
            "sellPrice": 25.0
        }

        # Mock the DAO method to raise an exception
        self.mock_product_dao.create_product.side_effect = Exception("Product verification failed")

        with self.assertRaises(Exception) as context:
            await self.product.create_product(test_data)
        
        self.assertEqual(str(context.exception), "Product verification failed")

    async def test_create_product_invalidstock(self):
        # Simulate a product creation request with invalid data
        test_data = {
            "name": "Test Product",
            "description": "Test Description",
            "stock": 100,
            "maxStock": 20,
            "minStock": 5,
            "purchasePrice": 15.0,
            "sellPrice": 25.0
        }

        # Mock the DAO method to raise an exception
        self.mock_product_dao.create_product.side_effect = Exception("Product verification failed")

        with self.assertRaises(Exception) as context:
            await self.product.create_product(test_data)
        
        self.assertEqual(str(context.exception), "Product verification failed")
    
    async def test_create_product_invalidpurchaseprice(self):
        # Simulate a product creation request with invalid data
        test_data = {
            "name": "Test Product",
            "description": "Test Description",
            "stock": 10,
            "maxStock": 20,
            "minStock": 5,
            "purchasePrice": -15.0,
            "sellPrice": 25.0
        }

        # Mock the DAO method to raise an exception
        self.mock_product_dao.create_product.side_effect = Exception("Product verification failed")

        with self.assertRaises(Exception) as context:
            await self.product.create_product(test_data)
        
        self.assertEqual(str(context.exception), "Product verification failed")
    
    async def test_create_product_invalidsellprice(self):
        # Simulate a product creation request with invalid data
        test_data = {
            "name": "Test Product",
            "description": "Test Description",
            "stock": 10,
            "maxStock": 20,
            "minStock": 5,
            "purchasePrice": 15.0,
            "sellPrice": -25.0
        }

        # Mock the DAO method to raise an exception
        self.mock_product_dao.create_product.side_effect = Exception("Product verification failed")

        with self.assertRaises(Exception) as context:
            await self.product.create_product(test_data)
        
        self.assertEqual(str(context.exception), "Product verification failed")
    
if __name__ == '__main__':
    unittest.main()