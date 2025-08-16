import unittest
import sqlite3
import os
from unittest.mock import mock_open, patch
from models import Client, Product, Order
from db import create_db, add_client, add_product, add_order, get_all_clients, get_all_products, get_all_orders, import_from_csv, export_to_csv, import_from_json, export_to_json

class TestDatabase(unittest.TestCase):
    def setUp(self):
        """Инициализирует временную БД перед каждым тестом."""
        self.db_file = "test_store.db"
        create_db(self.db_file)
        self.client = Client(1, "Иван Иванов", "ivan@example.com", "+79991234567")
        self.product = Product(1, "Ноутбук", 50000)
        self.products = [self.product, Product(2, "Телефон", 30000)]
        self.order = Order(1, self.client.id, [p.id for p in self.products], "2025-08-16", self.products)

    def tearDown(self):
        """Удаляет временную БД после теста."""
        if os.path.exists(self.db_file):
            os.remove(self.db_file)

    def test_create_db(self):
        """Проверяет создание таблиц в SQLite."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        self.assertIn(("clients",), tables)
        self.assertIn(("products",), tables)
        self.assertIn(("orders",), tables)
        self.assertIn(("order_products",), tables)
        conn.close()

    def test_add_client(self):
        """Проверяет добавление клиента в БД."""
        add_client(self.db_file, self.client)
        clients = get_all_clients(self.db_file)
        self.assertEqual(len(clients), 1)
        self.assertEqual(clients[0].id, self.client.id)
        self.assertEqual(clients[0].name, self.client.name)

    def test_add_product(self):
        """Проверяет добавление товара в БД."""
        add_product(self.db_file, self.product)
        products = get_all_products(self.db_file)
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].id, self.product.id)
        self.assertEqual(products[0].name, self.product.name)

    def test_add_order(self):
        """Проверяет добавление заказа в БД."""
        add_client(self.db_file, self.client)
        for product in self.products:
            add_product(self.db_file, product)
        add_order(self.db_file, self.order)
        orders = get_all_orders(self.db_file)
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0].id, self.order.id)
        self.assertEqual(orders[0].client_id, self.order.client_id)
        self.assertEqual(orders[0].product_ids, self.order.product_ids)

    def test_get_all_empty(self):
        """Проверяет получение данных из пустой БД."""
        self.assertEqual(get_all_clients(self.db_file), [])
        self.assertEqual(get_all_products(self.db_file), [])
        self.assertEqual(get_all_orders(self.db_file), [])

    def test_export_to_csv(self):
        """Проверяет экспорт данных в CSV."""
        add_client(self.db_file, self.client)
        for product in self.products:
            add_product(self.db_file, product)
        add_order(self.db_file, self.order)
        mock_files = {
            "clients.csv": mock_open().return_value,
            "products.csv": mock_open().return_value,
            "orders.csv": mock_open().return_value
        }
        def mock_open_side_effect(filename, *args, **kwargs):
            return mock_files[filename]
        with patch("builtins.open", side_effect=mock_open_side_effect):
            export_to_csv(self.db_file, "clients.csv", "products.csv", "orders.csv")
            mock_files["clients.csv"].write.assert_any_call("id,name,email,phone\r\n")
            mock_files["clients.csv"].write.assert_any_call("1,Иван Иванов,ivan@example.com,+79991234567\r\n")
            mock_files["products.csv"].write.assert_any_call("id,name,price\r\n")
            mock_files["products.csv"].write.assert_any_call("1,Ноутбук,50000.0\r\n")
            mock_files["products.csv"].write.assert_any_call("2,Телефон,30000.0\r\n")
            mock_files["orders.csv"].write.assert_any_call("id,client_id,product_ids,date,total\r\n")
            mock_files["orders.csv"].write.assert_any_call("1,1,\"[1, 2]\",2025-08-16,80000.0\r\n")

    def test_import_from_csv(self):
        """Проверяет импорт данных из CSV."""
        clients_csv = "id,name,email,phone\n1,Иван Иванов,ivan@example.com,+79991234567\n"
        products_csv = "id,name,price\n1,Ноутбук,50000\n2,Телефон,30000\n"
        orders_csv = "id,client_id,product_ids,date,total\n1,1,\"[1, 2]\",2025-08-16,80000\n"
        mock_files = {
            "clients.csv": mock_open(read_data=clients_csv).return_value,
            "products.csv": mock_open(read_data=products_csv).return_value,
            "orders.csv": mock_open(read_data=orders_csv).return_value
        }
        def mock_open_side_effect(filename, *args, **kwargs):
            return mock_files[filename]
        with patch("builtins.open", side_effect=mock_open_side_effect):
            import_from_csv(self.db_file, "clients.csv", "products.csv", "orders.csv")
        clients = get_all_clients(self.db_file)
        self.assertEqual(len(clients), 1)
        self.assertEqual(clients[0].name, "Иван Иванов")
        products = get_all_products(self.db_file)
        self.assertEqual(len(products), 2)
        self.assertEqual(products[0].name, "Ноутбук")
        orders = get_all_orders(self.db_file)
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0].product_ids, [1, 2])

    def test_import_nonexistent_file(self):
        """Проверяет импорт из несуществующего файла."""
        with patch("builtins.open", side_effect=FileNotFoundError):
            import_from_csv(self.db_file, "clients.csv", "products.csv", "orders.csv")
            self.assertEqual(get_all_clients(self.db_file), [])
            self.assertEqual(get_all_products(self.db_file), [])
            self.assertEqual(get_all_orders(self.db_file), [])

if __name__ == "__main__":
    unittest.main()