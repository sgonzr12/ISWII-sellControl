import unittest
from unittest.mock import MagicMock
import asyncio

import sys
sys.path.append('../')
from DAO.productDAO import ProductDAO
from DAO.product import Product

from routers import product

class TestProductRouter(unittest.TestCase):
    def setUp(self):
        self.mock_product_dao = MagicMock(spec=ProductDAO)

        # Store original DAO and inject mock
        self.original_dao = product.productDAO
        product.productDAO = self.mock_product_dao
        
        # Save reference to module
        self.product_module = product

    def tearDown(self):
        # Restore original DAO
        product.productDAO = self.original_dao

    def test_create_product(self):
        async def _async_test():
            # Simulate a product creation request
            test_data = {
                "name": "Test Product",
                "description": "Test Description",
                "stock": "10",
                "maxStock": "20",
                "minStock": "5",
                "purchasePrice": "15.0",
                "sellPrice": "25.0"
            }

            # Create a Product object to return
            product_obj = Product(
                name=test_data["name"],
                description=test_data["description"],
                stock=int(test_data["stock"]),
                maxStock=int(test_data["maxStock"]),
                minStock=int(test_data["minStock"]),
                purchasePrice=float(test_data["purchasePrice"]),
                sellPrice=float(test_data["sellPrice"])
            )

            # Expected JSON data that will be returned
            expected_data = product_obj.get_product_JSON()
            
            # Mock the DAO method
            self.mock_product_dao.create_product.return_value = product_obj

            result = await self.product_module.create_product(test_data)

            # Check if the result matches the expected data
            self.mock_product_dao.create_product.assert_called_once()
            self.assertEqual(result, expected_data)

        asyncio.run(_async_test())

    def test_get_all_products(self):   
        async def _async_test():     
            # Simulate a request to get all products
            test_data = [
                {
                    "name": "Test Product 1",
                    "description": "Test Description 1",
                    "stock": "10",
                    "maxStock": "20",
                    "minStock": "5",
                    "purchasePrice": "15.0",
                    "sellPrice": "25.0"
                },
                {
                    "name": "Test Product 2",
                    "description": "Test Description 2",
                    "stock": "15",
                    "maxStock": "25",
                    "minStock": "10",
                    "purchasePrice": "20.0",
                    "sellPrice": "30.0"
                }
            ]
            
            # Create Product objects to return
            product_obj_1 = Product(
                name=test_data[0]["name"],
                description=test_data[0]["description"],
                stock=int(test_data[0]["stock"]),
                maxStock=int(test_data[0]["maxStock"]),
                minStock=int(test_data[0]["minStock"]),
                purchasePrice=float(test_data[0]["purchasePrice"]),
                sellPrice=float(test_data[0]["sellPrice"])
            )
            product_obj_2 = Product(
                name=test_data[1]["name"],
                description=test_data[1]["description"],
                stock=int(test_data[1]["stock"]),
                maxStock=int(test_data[1]["maxStock"]),
                minStock=int(test_data[1]["minStock"]),
                purchasePrice=float(test_data[1]["purchasePrice"]),
                sellPrice=float(test_data[1]["sellPrice"])
            )

            # Mock the DAO method
            self.mock_product_dao.get_all_products.return_value = [product_obj_1, product_obj_2]
            expected_data = [product_obj_1.get_product_JSON(), product_obj_2.get_product_JSON()]

            result = await self.product_module.get_all_products()

            # Check if the result matches the expected data
            self.mock_product_dao.get_all_products.assert_called_once()
            self.assertEqual(result, expected_data)

        asyncio.run(_async_test())
    
    def test_update_product(self):
        async def _async_test():
            # Simulate a product update request
            test_data = {
                "productId": "0",
                "name": "Insert Product",
                "description": "Insert Description",
                "stock": "150",
                "maxStock": "250",
                "minStock": "100",
                "purchasePrice": "2.0",
                "sellPrice": "3.0"
            }

            # Create a Product object to return
            product_obj = Product(
                productId=int(test_data["productId"]),
                name=test_data["name"],
                description=test_data["description"],
                stock=int(test_data["stock"]),
                maxStock=int(test_data["maxStock"]),
                minStock=int(test_data["minStock"]),
                purchasePrice=float(test_data["purchasePrice"]),
                sellPrice=float(test_data["sellPrice"])
            )

            # Mock the DAO method
            self.mock_product_dao.update_product.return_value = product_obj
            expected_data = product_obj.get_product_JSON()

            result = await self.product_module.update_product(test_data)

            # Check if the result matches the expected data
            self.mock_product_dao.update_product.assert_called_once()
            self.assertEqual(result, expected_data)

        asyncio.run(_async_test())

    def test_update_product_invalid(self):
        async def _async_test():
            # Simulate a product update request with invalid data
            test_data = {
                "productId": "1",
                "name": "",
                "description": "Updated Description",
                "stock": "-5",
                "maxStock": "25",
                "minStock": "10",
                "purchasePrice": "-20.0",
                "sellPrice": "30.0"
            }

            # Mock the DAO method to raise an exception
            self.mock_product_dao.update_product.side_effect = Exception("Product verification failed")

            with self.assertRaises(Exception) as context:
                await self.product_module.update_product(test_data)
            
            self.assertEqual(str(context.exception), "400: Product verification failed")
        
        asyncio.run(_async_test())

    def test_create_product_invalid_productid(self):
        async def _async_test():
            # Simulate a product creation request with invalid data
            test_data = {
                "productId": "123",
                "name": "Test Product",
                "description": "Test Description",
                "stock": "10",
                "maxStock": "20",
                "minStock": "5",
                "purchasePrice": "15.0",
                "sellPrice": "25.0"
            }

            # Mock the DAO method to raise an exception
            self.mock_product_dao.create_product.side_effect = Exception("Product verification failed")

            with self.assertRaises(Exception) as context:
                await self.product_module.create_product(test_data)

            self.assertEqual(str(context.exception), "Product verification failed")
        
        asyncio.run(_async_test())

    def test_create_product_invalid_maxstock(self):
        async def _async_test():
            # Simulate a product creation request with invalid data
            test_data = {
                "name": "Test Product",
                "description": "Test Description",
                "stock": "10",
                "maxStock": "-20",
                "minStock": "5",
                "purchasePrice": "15.0",
                "sellPrice": "25.0"
            }

            # Mock the DAO method to raise an exception
            self.mock_product_dao.create_product.side_effect = Exception("Product verification failed")

            with self.assertRaises(Exception) as context:
                await self.product_module.create_product(test_data)

            self.assertEqual(str(context.exception), "400: Product verification failed")

        asyncio.run(_async_test())

    def test_create_product_invalid_minstock(self):
        async def _async_test():
            # Simulate a product creation request with invalid data
            test_data = {
                "name": "Test Product",
                "description": "Test Description",
                "stock": "10",
                "maxStock": "20",
                "minStock": "-5",
                "purchasePrice": "15.0",
                "sellPrice": "25.0"
            }

            # Mock the DAO method to raise an exception
            self.mock_product_dao.create_product.side_effect = Exception("Product verification failed")

            with self.assertRaises(Exception) as context:
                await self.product_module.create_product(test_data)

            self.assertEqual(str(context.exception), "400: Product verification failed")

        asyncio.run(_async_test())

    def test_create_product_invalid_stock(self):
        async def _async_test():
            # Simulate a product creation request with invalid data
            test_data = {
                "name": "Test Product",
                "description": "Test Description",
                "stock": "10",
                "maxStock": "20",
                "minStock": "-5",
                "purchasePrice": "15.0",
                "sellPrice": "25.0"
            }

            # Mock the DAO method to raise an exception
            self.mock_product_dao.create_product.side_effect = Exception("Product verification failed")

            with self.assertRaises(Exception) as context:
                await self.product_module.create_product(test_data)

            self.assertEqual(str(context.exception), "400: Product verification failed")

        asyncio.run(_async_test())

    def test_create_product_invalid_purchaseprice(self):
        async def _async_test():
            # Simulate a product creation request with invalid data
            test_data = {
                "name": "Test Product",
                "description": "Test Description",
                "stock": "10",
                "maxStock": "20",
                "minStock": "5",
                "purchasePrice": "-15.0",
                "sellPrice": "25.0"
            }

            # Mock the DAO method to raise an exception
            self.mock_product_dao.create_product.side_effect = Exception("Product verification failed")

            with self.assertRaises(Exception) as context:
                await self.product_module.create_product(test_data)

            self.assertEqual(str(context.exception), "400: Product verification failed")

        asyncio.run(_async_test())

    def test_create_product_invalid_sellprice(self):
        async def _async_test():
            # Simulate a product creation request with invalid data
            test_data = {
                "name": "Test Product",
                "description": "Test Description",
                "stock": "10",
                "maxStock": "20",
                "minStock": "5",
                "purchasePrice": "15.0",
                "sellPrice": "-25.0"
            }

            # Mock the DAO method to raise an exception
            self.mock_product_dao.create_product.side_effect = Exception("Product verification failed")

            with self.assertRaises(Exception) as context:
                await self.product_module.create_product(test_data)

            self.assertEqual(str(context.exception), "400: Product verification failed")

        asyncio.run(_async_test())

    def test_create_product_stock_invalidmaxmin(self):
        async def _async_test():
            # Simulate a product creation request with invalid data
            test_data = {
                "name": "Test Product",
                "description": "Test Description",
                "stock": "50",
                "maxStock": "20",
                "minStock": "5",
                "purchasePrice": "15.0",
                "sellPrice": "25.0"
            }

            # Mock the DAO method to raise an exception
            self.mock_product_dao.create_product.side_effect = Exception("Product verification failed")

            with self.assertRaises(Exception) as context:
                await self.product_module.create_product(test_data)

            self.assertEqual(str(context.exception), "400: Product verification failed")

        asyncio.run(_async_test())

if __name__ == '__main__':
    unittest.main()