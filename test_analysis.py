import unittest
import os
import pandas as pd
from unittest.mock import patch
from datetime import datetime
from models import Client, Product, Order
from db import create_db, add_client, add_product, add_order, get_all_clients, get_all_products, get_all_orders
from analysis import top_clients, sales_dynamics, top_products, client_graph

class TestAnalysis(unittest.TestCase):
    def setUp(self):
        """Инициализирует временную БД и тестовые данные."""
        self.db_file = "test_store.db"
        create_db(self.db_file)
        self.clients = [
            Client(1, "Иван Иванов", "ivan@example.com", "+79991234567"),
            Client(2, "Анна Петрова", "anna@example.com", "+79997654321")
        ]
        self.products = [
            Product(1, "Ноутбук", 50000),
            Product(2, "Телефон", 30000)
        ]
        self.orders = [
            Order(1, 1, [1], "2025-08-01", [self.products[0]]),
            Order(2, 1, [1, 2], "2025-08-02", self.products),
            Order(3, 2, [2], "2025-08-03", [self.products[1]])
        ]
        for client in self.clients:
            add_client(self.db_file, client)
        for product in self.products:
            add_product(self.db_file, product)
        for order in self.orders:
            add_order(self.db_file, order)

    def tearDown(self):
        """Удаляет временную БД после теста."""
        if os.path.exists(self.db_file):
            os.remove(self.db_file)

    def test_top_clients(self):
        """Проверяет топ клиентов по числу заказов."""
        result = top_clients(self.db_file, n=2)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["client_name"], "Иван Иванов")
        self.assertEqual(result[0]["order_count"], 2)
        self.assertEqual(result[1]["client_name"], "Анна Петрова")
        self.assertEqual(result[1]["order_count"], 1)

    def test_sales_dynamics(self):
        """Проверяет динамику заказов по датам."""
        with patch("matplotlib.pyplot.savefig") as mocked_savefig:
            result = sales_dynamics(self.db_file)
            self.assertTrue(mocked_savefig.called)
        expected = pd.DataFrame([
            {"date": "2025-08-01", "total": 50000.0},
            {"date": "2025-08-02", "total": 80000.0},
            {"date": "2025-08-03", "total": 30000.0}
        ])
        pd.testing.assert_frame_equal(
            result.reset_index()[["date", "total"]],
            expected,
            check_dtype=False
        )

    def test_top_products(self):
        """Проверяет топ товаров по количеству продаж."""
        with patch("matplotlib.pyplot.savefig") as mocked_savefig:
            result = top_products(self.db_file, n=2)
            self.assertTrue(mocked_savefig.called)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["product_name"], "Ноутбук")
        self.assertEqual(result[0]["sales_count"], 2)
        self.assertEqual(result[1]["product_name"], "Телефон")
        self.assertEqual(result[1]["sales_count"], 2)

    def test_client_graph(self):
        """Проверяет граф связей клиентов по общим товарам."""
        with patch("matplotlib.pyplot.savefig") as mocked_savefig:
            graph = client_graph(self.db_file)
            self.assertTrue(mocked_savefig.called)
        self.assertEqual(len(graph.nodes), 2)  # Два клиента
        self.assertEqual(len(graph.edges), 2)  # Две связи (Ноутбук и Телефон)

if __name__ == "__main__":
    unittest.main()