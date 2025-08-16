import pandas as pd
import sqlite3
import networkx as nx

def top_clients(db_file: str, n: int = 5) -> list:
    """Возвращает топ N клиентов по количеству заказов."""
    conn = sqlite3.connect(db_file)
    query = """
    SELECT c.name AS client_name, COUNT(o.id) AS order_count
    FROM clients c
    LEFT JOIN orders o ON c.id = o.client_id
    GROUP BY c.id, c.name
    ORDER BY order_count DESC
    LIMIT ?
    """
    df = pd.read_sql_query(query, conn, params=(n,))
    conn.close()
    if df.empty:
        return []
    return df.to_dict("records")

def top_products(db_file: str, n: int = 5) -> list:
    """Возвращает топ N товаров по количеству заказов."""
    conn = sqlite3.connect(db_file)
    query = """
    SELECT p.name AS product_name, COUNT(o.id) AS order_count
    FROM products p
    LEFT JOIN orders o ON o.id = p.id
    GROUP BY p.id, p.name
    ORDER BY order_count DESC
    LIMIT ?
    """
    df = pd.read_sql_query(query, conn, params=(n,))
    conn.close()
    if df.empty:
        return []
    return df.to_dict("records")

def sales_dynamics(db_file: str) -> pd.DataFrame:
    """Возвращает динамику продаж по датам."""
    conn = sqlite3.connect(db_file)
    query = """
    SELECT date, SUM(total) AS total
    FROM orders
    GROUP BY date
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    if df.empty:
        return pd.DataFrame(columns=["date", "total"])
    return df

def client_graph(db_file: str) -> nx.Graph:
    """Создаёт граф связей клиентов по общим товарам."""
    conn = sqlite3.connect(db_file)
    query = """
    SELECT o1.client_id AS client1, o2.client_id AS client2
    FROM orders o1
    JOIN orders o2 ON o1.id = o2.id AND o1.client_id != o2.client_id
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    graph = nx.Graph()
    for _, row in df.iterrows():
        graph.add_edge(row["client1"], row["client2"])
    return graph