import re

class Client:
    """Клиент интернет-магазина."""
    def __init__(self, client_id: int, name: str, email: str, phone: str):
        """
        Инициализирует клиента.

        Args:
            client_id (int): Уникальный идентификатор.
            name (str): Имя клиента.
            email (str): Электронная почта.
            phone (str): Номер телефона.

        Raises:
            ValueError: Если email или phone невалидны.
        """
        self.id = client_id
        self.name = name.strip()
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValueError("Невалидный email")
        self.email = email
        if not re.match(r'^\+\d{10,12}$', phone):
            raise ValueError("Невалидный телефон")
        self.phone = phone

    def __repr__(self):
        return f"Client(client_id={self.id}, name={self.name}, email={self.email}, phone={self.phone})"

class Product:
    """Товар в интернет-магазине."""
    def __init__(self, product_id: int, name: str, price: float):
        """
        Инициализирует товар.

        Args:
            product_id (int): Уникальный идентификатор.
            name (str): Название товара.
            price (float): Цена товара.

        Raises:
            ValueError: Если цена отрицательная.
        """
        self.id = product_id
        self.name = name.strip()
        if price < 0:
            raise ValueError("Цена не может быть отрицательной")
        self.price = price

    def __repr__(self):
        return f"Product(client_id={self.id}, name={self.name}, price={self.price})"

class Order:
    """Заказ в интернет-магазине."""
    def __init__(self, order_id: int, client_id: int, product_ids: list[int], date: str, products: list[Product]):
        """
        Инициализирует заказ.

        Args:
            order_id (int): Уникальный идентификатор.
            client_id (int): ID клиента.
            product_ids (list[int]): Список ID товаров.
            date (str): Дата заказа (YYYY-MM-DD).
            products (list[Product]): Список объектов товаров для расчёта total.

        Raises:
            ValueError: Если товары отсутствуют.
        """
        self.id = order_id
        self.client_id = client_id
        self.product_ids = product_ids
        self.date = date
        self.total = sum(p.price for p in products) if products else 0

    def __repr__(self):
        return f"Order(client_id={self.id}, client_id={self.client_id}, product_ids={self.product_ids}, date={self.date}, total={self.total})"