import sqlite3
import csv
import json
from typing import List
from models import Client, Product, Order

def create_db(db_file: str) -> None:
    """Создаёт SQLite базу с таблицами для клиентов, товаров и заказов."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            client_id INTEGER,
            date TEXT NOT NULL,
            total REAL NOT NULL,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_products (
            order_id INTEGER,
            product_id INTEGER,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)
    conn.commit()
    conn.close()

def add_client(db_file: str, client: Client) -> None:
    """Добавляет клиента в базу."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clients (id, name, email, phone) VALUES (?, ?, ?, ?)",
                  (client.id, client.name, client.email, client.phone))
    conn.commit()
    conn.close()

def add_product(db_file: str, product: Product) -> None:
    """Добавляет товар в базу."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (id, name, price) VALUES (?, ?, ?)",
                  (product.id, product.name, product.price))
    conn.commit()
    conn.close()

def add_order(db_file: str, order: Order) -> None:
    """Добавляет заказ в базу."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (id, client_id, date, total) VALUES (?, ?, ?, ?)",
                  (order.id, order.client_id, order.date, order.total))
    for product_id in order.product_ids:
        cursor.execute("INSERT INTO order_products (order_id, product_id) VALUES (?, ?)",
                      (order.id, product_id))
    conn.commit()
    conn.close()

def get_all_clients(db_file: str) -> List[Client]:
    """Возвращает всех клиентов из базы."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, phone FROM clients")
    clients = [Client(row[0], row[1], row[2], row[3]) for row in cursor.fetchall()]
    conn.close()
    return clients

def get_all_products(db_file: str) -> List[Product]:
    """Возвращает все товары из базы."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price FROM products")
    products = [Product(row[0], row[1], row[2]) for row in cursor.fetchall()]
    conn.close()
    return products

def get_all_orders(db_file: str) -> List[Order]:
    """Возвращает все заказы из базы."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT id, client_id, date, total FROM orders")
    orders = []
    for row in cursor.fetchall():
        order_id = row[0]
        cursor.execute("SELECT product_id FROM order_products WHERE order_id = ?", (order_id,))
        product_ids = [r[0] for r in cursor.fetchall()]
        products = [p for p in get_all_products(db_file) if p.id in product_ids]
        orders.append(Order(row[0], row[1], product_ids, row[2], products))
    conn.close()
    return orders

def export_to_csv(db_file: str, clients_file: str, products_file: str, orders_file: str) -> None:
    """Экспортирует данные в CSV."""
    clients = get_all_clients(db_file)
    with open(clients_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "name", "email", "phone"])
        for client in clients:
            writer.writerow([client.id, client.name, client.email, client.phone])

    products = get_all_products(db_file)
    with open(products_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "name", "price"])
        for product in products:
            writer.writerow([product.id, product.name, product.price])

    orders = get_all_orders(db_file)
    with open(orders_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "client_id", "product_ids", "date", "total"])
        for order in orders:
            writer.writerow([order.id, order.client_id, order.product_ids, order.date, order.total])

def import_from_csv(db_file: str, clients_file: str, products_file: str, orders_file: str) -> None:
    """Импортирует данные из CSV."""
    try:
        with open(clients_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                client = Client(int(row["id"]), row["name"], row["email"], row["phone"])
                add_client(db_file, client)
    except FileNotFoundError:
        pass

    try:
        with open(products_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                product = Product(int(row["id"]), row["name"], float(row["price"]))
                add_product(db_file, product)
    except FileNotFoundError:
        pass

    try:
        with open(orders_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                product_ids = eval(row["product_ids"])  # Безопасность требует доработки
                products = [p for p in get_all_products(db_file) if p.id in product_ids]
                order = Order(int(row["id"]), int(row["client_id"]), product_ids, row["date"], products)
                add_order(db_file, order)
    except FileNotFoundError:
        pass

def export_to_json(db_file: str, clients_file: str, products_file: str, orders_file: str) -> None:
    """Экспортирует данные в JSON."""
    clients = get_all_clients(db_file)
    with open(clients_file, "w", encoding="utf-8") as f:
        json.dump([{"id": c.id, "name": c.name, "email": c.email, "phone": c.phone} for c in clients], f)

    products = get_all_products(db_file)
    with open(products_file, "w", encoding="utf-8") as f:
        json.dump([{"id": p.id, "name": p.name, "price": p.price} for p in products], f)

    orders = get_all_orders(db_file)
    with open(orders_file, "w", encoding="utf-8") as f:
        json.dump([{"id": o.id, "client_id": o.client_id, "product_ids": o.product_ids, "date": o.date, "total": o.total} for o in orders], f)

def import_from_json(db_file: str, clients_file: str, products_file: str, orders_file: str) -> None:
    """Импортирует данные из JSON."""
    try:
        with open(clients_file, "r", encoding="utf-8") as f:
            clients_data = json.load(f)
            for data in clients_data:
                client = Client(data["id"], data["name"], data["email"], data["phone"])
                add_client(db_file, client)
    except FileNotFoundError:
        pass

    try:
        with open(products_file, "r", encoding="utf-8") as f:
            products_data = json.load(f)
            for data in products_data:
                product = Product(data["id"], data["name"], data["price"])
                add_product(db_file, product)
    except FileNotFoundError:
        pass

    try:
        with open(orders_file, "r", encoding="utf-8") as f:
            orders_data = json.load(f)
            for data in orders_data:
                product_ids = data["product_ids"]
                products = [p for p in get_all_products(db_file) if p.id in product_ids]
                order = Order(data["id"], data["client_id"], product_ids, data["date"], products)
                add_order(db_file, order)
    except FileNotFoundError:
        pass