import unittest
from unittest.mock import MagicMock, patch
import asyncio
import datetime

import sys

sys.path.append("../")
from DAO.invoiceDAO import InvoiceDAO
from DAO.invoice import Invoice, InvoiceModel, ProductInInvoice
from DAO.product import Product

from DAO.employe import Employe
import DAO.employeDAO 
from DAO.client import Client
import DAO.clientDAO
from DAO.deliveryNote import DeliveryNote

from routers import invoice

class TestInvoiceDAO(unittest.TestCase):
    def setUp(self):
        self.mock_invoice_dao = MagicMock(spec=InvoiceDAO)

        # Store original DAO and inject mock
        self.original_dao = invoice.invoiceDAO
        invoice.invoiceDAO = self.mock_invoice_dao

        # Save reference to module
        self.invoice_module = invoice

    def tearDown(self):
        # Restore original DAO
        invoice.invoiceDAO  = self.original_dao

    def test_create_invoice(self):
        async def _async_test():
            # Simulate a token
            invoice_data = {
                "DeliveryNoteID": "72747",
                "clientId": "72747"
            }

            # Create a invoice object to return
            product = Product(productId=1, name="Test Product", description="Test Description", stock=100, minStock=1, maxStock=10, purchasePrice=5.0, sellPrice=10.0)
            invoice_obj = Invoice(
                invoiceID="77345",
                employeId="1",
                clientId="82345",
                products=[(product, 2)],
                invoiceDate=None,
                totalPrice=None
            )

            expected_json = InvoiceModel(
                invoiceID=invoice_obj.invoiceID,
                employeID=invoice_obj.employeId,
                employeName="John Doe",
                clientID=invoice_obj.clientId,
                clientName="Test Company",
                date=datetime.date.today(),
                totalPrice=invoice_obj.calculatePrice(invoice_obj.products),
                products=[ProductInInvoice(id=product.productId, name=product.name, quantity=2)]
            )

            invoice_obj.get_json = MagicMock(return_value=expected_json)

            with patch("routers.invoice.deliveryNoteDAO.get_delivery_note_by_id") as mock_get_delivery_note, \
                 patch("DAO.invoice.Invoice.get_json") as mock_get_json, \
                 patch("routers.invoice.invoiceDAO.check_invoice_exists", return_value=False):
                
                mock_delivery_note = MagicMock(spec=DeliveryNote)
                mock_delivery_note.deliveryNoteID = "72345"
                mock_delivery_note.clientId = "1"
                mock_delivery_note.date = "2023-10-01"
                mock_delivery_note.totalPrice = 100.0
                mock_delivery_note.products = [(product, 2)]

                mock_employee = MagicMock(spec=Employe)
                mock_employee.employeId = "1"
                mock_employee.name = "John Doe"
                DAO.employeDAO.EmployeDAO.get_employee_by_id = mock_employee

                mock_client = MagicMock(spec=Client)
                mock_client.clientId = "1"
                mock_client.CompanyName = "Test Company"
                DAO.clientDAO.ClientDAO.get_client_by_id = mock_client

                # Mock the delivery note DAO method
                mock_get_delivery_note.return_value = mock_delivery_note

                # Mock the DAO method
                self.mock_invoice_dao.create_invoice.return_value = invoice_obj

                await self.invoice_module.create_invoice(invoice_data, token={"sub": "1"})

                # Check if the result matches the expected data
                self.mock_invoice_dao.create_invoice.assert_called_once()

        asyncio.run(_async_test())

    def test_get_all_invoices(self):
        async def _async_test():
            # Create a invoice object to return
            product = Product(productId=1, name="Test Product", description="Test Description", stock=100, minStock=1, maxStock=10, purchasePrice=5.0, sellPrice=10.0)
            invoice_obj = Invoice(
                invoiceID="77345",
                employeId="1",
                clientId="82345",
                products=[(product, 2)],
                invoiceDate=None,
                totalPrice=None
            )

            expected_json = InvoiceModel(
                invoiceID=invoice_obj.invoiceID,
                employeID=invoice_obj.employeId,
                employeName="John Doe",
                clientID=invoice_obj.clientId,
                clientName="Test Company",
                date=datetime.date.today(),
                totalPrice=invoice_obj.calculatePrice(invoice_obj.products),
                products=[ProductInInvoice(id=product.productId, name=product.name, quantity=2)]
            )

            invoice_obj.get_json = MagicMock(return_value=expected_json)

            # Mock the DAO method
            self.mock_invoice_dao.get_all_invoices.return_value = [invoice_obj]

            with patch("routers.invoice.invoiceDAO.get_all_invoices") as mock_get_all_invoices, \
                 patch("DAO.invoice.Invoice.get_json") as mock_get_json:
                mock_get_all_invoices.return_value = [invoice_obj]
                mock_get_json.return_value = {
                    "invoiceID": "77345",
                    "employeID": "1",
                    "employeName": "John Doe",
                    "clientID": "82345",
                    "clientName": "Test Company",
                    "date": datetime.date.today(),
                    "totalPrice": invoice_obj.calculatePrice(invoice_obj.products),
                    "products": [ProductInInvoice(id=product.productId, name=product.name, quantity=2)]
                }

                result = await self.invoice_module.get_all_invoices(token={"sub": "1"})

                # Check if the result matches the expected data
                self.assertEqual(len(result), 1)
                self.assertEqual(result[0].invoiceID, invoice_obj.invoiceID)

        asyncio.run(_async_test())

if __name__ == "__main__":
    unittest.main()