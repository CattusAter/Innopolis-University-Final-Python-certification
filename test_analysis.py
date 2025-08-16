import unittest
from unittest.mock import patch
import pandas as pd
import networkx as nx
from analysis import top_clients, top_products, sales_dynamics, client_graph

class TestAnalysis(unittest.TestCase):
    def setUp(self):
        """Инициализирует тестовые данные."""
        self.db_file = "test_store.db"

    @patch("pandas.read_sql_query")
    @patch("sqlite3.connect")
    def test_top_clients(self, mock_connect, mock_read_sql):
        """Проверяет топ клиентов."""
        mock_read_sql.return_value = pd.DataFrame([
            {"client_name": "Иван Иванов", "order_count": 2},
            {"client_name": "Пётр Петров", "order_count": 1}
        ])
        result = top_clients(self.db_file, n=2)
        self.assertEqual(result, [
            {"client_name": "Иван Иванов", "order_count": 2},
            {"client_name": "Пётр Петров", "order_count": 1}
        ])
        mock_connect.assert_called_once_with(self.db_file)
        mock_read_sql.assert_called_once_with(
            """
    SELECT c.name AS client_name, COUNT(o.id) AS order_count
    FROM clients c
    LEFT JOIN orders o ON c.id = o.client_id
    GROUP BY c.id, c.name
    ORDER BY order_count DESC
    LIMIT ?
    """,
            mock_connect.return_value,
            params=(2,)
        )

    @patch("pandas.read_sql_query")
    @patch("sqlite3.connect")
    def test_top_clients_empty(self, mock_connect, mock_read_sql):
        """Проверяет топ клиентов при пустой базе."""
        mock_read_sql.return_value = pd.DataFrame(columns=["client_name", "order_count"])
        result = top_clients(self.db_file, n=5)
        self.assertEqual(result, [])
        mock_connect.assert_called_once_with(self.db_file)
        mock_read_sql.assert_called_once()

    @patch("pandas.read_sql_query")
    @patch("sqlite3.connect")
    def test_top_products(self, mock_connect, mock_read_sql):
        """Проверяет топ товаров."""
        mock_read_sql.return_value = pd.DataFrame([
            {"product_name": "Ноутбук", "order_count": 3},
            {"product_name": "Телефон", "order_count": 2}
        ])
        result = top_products(self.db_file, n=2)
        self.assertEqual(result, [
            {"product_name": "Ноутбук", "order_count": 3},
            {"product_name": "Телефон", "order_count": 2}
        ])
        mock_connect.assert_called_once_with(self.db_file)
        mock_read_sql.assert_called_once_with(
            """
    SELECT p.name AS product_name, COUNT(o.id) AS order_count
    FROM products p
    LEFT JOIN orders o ON o.id = p.id
    GROUP BY p.id, p.name
    ORDER BY order_count DESC
    LIMIT ?
    """,
            mock_connect.return_value,
            params=(2,)
        )

    @patch("pandas.read_sql_query")
    @patch("sqlite3.connect")
    def test_top_products_empty(self, mock_connect, mock_read_sql):
        """Проверяет топ товаров при пустой базе."""
        mock_read_sql.return_value = pd.DataFrame(columns=["product_name", "order_count"])
        result = top_products(self.db_file, n=5)
        self.assertEqual(result, [])
        mock_connect.assert_called_once_with(self.db_file)
        mock_read_sql.assert_called_once()

    @patch("pandas.read_sql_query")
    @patch("sqlite3.connect")
    def test_sales_dynamics(self, mock_connect, mock_read_sql):
        """Проверяет динамику продаж."""
        mock_read_sql.return_value = pd.DataFrame([
            {"date": "2025-08-16", "total": 50000.0},
            {"date": "2025-08-17", "total": 30000.0}
        ])
        result = sales_dynamics(self.db_file)
        expected = pd.DataFrame([
            {"date": "2025-08-16", "total": 50000.0},
            {"date": "2025-08-17", "total": 30000.0}
        ])
        pd.testing.assert_frame_equal(result, expected, check_dtype=False)
        mock_connect.assert_called_once_with(self.db_file)
        mock_read_sql.assert_called_once_with(
            """
    SELECT date, SUM(total) AS total
    FROM orders
    GROUP BY date
    """,
            mock_connect.return_value
        )

    @patch("pandas.read_sql_query")
    @patch("sqlite3.connect")
    def test_sales_dynamics_empty(self, mock_connect, mock_read_sql):
        """Проверяет динамику продаж при пустой базе."""
        mock_read_sql.return_value = pd.DataFrame(columns=["date", "total"])
        result = sales_dynamics(self.db_file)
        expected = pd.DataFrame(columns=["date", "total"])
        pd.testing.assert_frame_equal(result, expected, check_dtype=False)
        mock_connect.assert_called_once_with(self.db_file)
        mock_read_sql.assert_called_once()

    @patch("pandas.read_sql_query")
    @patch("sqlite3.connect")
    def test_client_graph(self, mock_connect, mock_read_sql):
        """Проверяет граф клиентов."""
        mock_read_sql.return_value = pd.DataFrame([
            {"client1": 1, "client2": 2}
        ])
        result = client_graph(self.db_file)
        self.assertEqual(list(result.nodes), [1, 2])
        self.assertEqual(list(result.edges), [(1, 2)])
        mock_connect.assert_called_once_with(self.db_file)
        mock_read_sql.assert_called_once_with(
            """
    SELECT o1.client_id AS client1, o2.client_id AS client2
    FROM orders o1
    JOIN orders o2 ON o1.id = o2.id AND o1.client_id != o2.client_id
    """,
            mock_connect.return_value
        )

    @patch("pandas.read_sql_query")
    @patch("sqlite3.connect")
    def test_client_graph_empty(self, mock_connect, mock_read_sql):
        """Проверяет граф клиентов при пустой базе."""
        mock_read_sql.return_value = pd.DataFrame(columns=["client1", "client2"])
        result = client_graph(self.db_file)
        self.assertEqual(list(result.nodes), [])
        self.assertEqual(list(result.edges), [])
        mock_connect.assert_called_once_with(self.db_file)
        mock_read_sql.assert_called_once()

if __name__ == "__main__":
    unittest.main()