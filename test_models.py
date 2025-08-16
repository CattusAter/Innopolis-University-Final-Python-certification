import unittest
import re
from models import Client, Product, Order

class TestClient(unittest.TestCase):
    def test_create_client_valid(self):
        """Проверяет создание клиента с валидными данными."""
        client = Client(1, "Иван Иванов", "ivan@example.com", "+79991234567")
        self.assertEqual(client.id, 1)
        self.assertEqual(client.name, "Иван Иванов")
        self.assertEqual(client.email, "ivan@example.com")
        self.assertEqual(client.phone, "+79991234567")

    def test_invalid_email(self):
        """Проверяет, что невалидный email вызывает исключение."""
        with self.assertRaises(ValueError):
            Client(2, "Анна Петрова", "invalid_email", "+79991234568")

    def test_invalid_phone(self):
        """Проверяет, что невалидный телефон вызывает исключение."""
        with self.assertRaises(ValueError):
            Client(3, "Пётр Сидоров", "petr@example.com", "12345")

    def test_client_repr(self):
        """Проверяет строковое представление клиента."""
        client = Client(1, "Иван Иванов", "ivan@example.com", "+79991234567")
        self.assertEqual(repr(client), "Client(client_id=1, name=Иван Иванов, email=ivan@example.com, phone=+79991234567)")

class TestProduct(unittest.TestCase):
    def test_create_product_valid(self):
        """Проверяет создание товара с валидными данными."""
        product = Product(1, "Ноутбук", 50000)
        self.assertEqual(product.id, 1)
        self.assertEqual(product.name, "Ноутбук")
        self.assertEqual(product.price, 50000)

    def test_negative_price(self):
        """Проверяет, что отрицательная цена вызывает исключение."""
        with self.assertRaises(ValueError):
            Product(2, "Телефон", -1000)

    def test_product_repr(self):
        """Проверяет строковое представление товара."""
        product = Product(1, "Ноутбук", 50000)
        self.assertEqual(repr(product), "Product(client_id=1, name=Ноутбук, price=50000)")

class TestOrder(unittest.TestCase):
    def test_create_order_valid(self):
        """Проверяет создание заказа с валидными данными."""
        client = Client(1, "Иван Иванов", "ivan@example.com", "+79991234567")
        products = [Product(1, "Ноутбук", 50000), Product(2, "Телефон", 30000)]
        order = Order(1, client.id, [p.id for p in products], "2025-08-16", products)
        self.assertEqual(order.id, 1)
        self.assertEqual(order.client_id, client.id)
        self.assertEqual(order.product_ids, [1, 2])
        self.assertEqual(order.total, 80000)

    def test_order_total_calculation(self):
        """Проверяет расчёт общей стоимости заказа."""
        products = [Product(1, "Ноутбук", 50000), Product(2, "Телефон", 30000)]
        order = Order(1, 1, [1, 2], "2025-08-16", products)
        self.assertEqual(order.total, 80000)

    def test_order_repr(self):
        """Проверяет строковое представление заказа."""
        client = Client(1, "Иван Иванов", "ivan@example.com", "+79991234567")
        products = [Product(1, "Ноутбук", 50000)]
        order = Order(1, client.id, [1], "2025-08-16", products)
        self.assertEqual(repr(order), "Order(client_id=1, client_id=1, product_ids=[1], date=2025-08-16, total=50000)")

if __name__ == "__main__":
    unittest.main()