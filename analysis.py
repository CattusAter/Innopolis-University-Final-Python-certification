import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from db import get_all_clients, get_all_products, get_all_orders

def top_clients(db_file: str, n: int = 5) -> list:
    """Возвращает топ N клиентов по числу заказов."""
    orders = get_all_orders(db_file)
    clients = get_all_clients(db_file)
    client_orders = pd.DataFrame(
        [{"client_id": order.client_id} for order in orders]
    ).value_counts("client_id").reset_index(name="order_count")
    client_map = {c.id: c.name for c in clients}
    result = [
        {"client_name": client_map[row["client_id"]], "order_count": row["order_count"]}
        for _, row in client_orders.head(n).iterrows()
        if row["client_id"] in client_map
    ]
    return result

def sales_dynamics(db_file: str) -> pd.DataFrame:
    """Возвращает динамику заказов по датам."""
    orders = get_all_orders(db_file)
    df = pd.DataFrame(
        [{"date": order.date, "total": order.total} for order in orders]
    )
    result = df.groupby("date")["total"].sum().reset_index()
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=result, x="date", y="total")
    plt.title("Динамика заказов по датам")
    plt.xlabel("Дата")
    plt.ylabel("Сумма заказов")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("sales_dynamics.png")
    plt.close()
    return result

def top_products(db_file: str, n: int = 5) -> list:
    """Возвращает топ N товаров по количеству продаж."""
    orders = get_all_orders(db_file)
    products = get_all_products(db_file)
    product_counts = {}
    for order in orders:
        for pid in order.product_ids:
            product_counts[pid] = product_counts.get(pid, 0) + 1
    product_map = {p.id: p.name for p in products}
    result = [
        {"product_name": product_map[pid], "sales_count": count}
        for pid, count in sorted(product_counts.items(), key=lambda x: x[1], reverse=True)[:n]
        if pid in product_map
    ]
    plt.figure(figsize=(10, 6))
    sns.barplot(x=[r["sales_count"] for r in result], y=[r["product_name"] for r in result])
    plt.title("Топ товаров по продажам")
    plt.xlabel("Количество продаж")
    plt.ylabel("Товар")
    plt.tight_layout()
    plt.savefig("top_products.png")
    plt.close()
    return result

def client_graph(db_file: str) -> nx.Graph:
    """Создаёт граф связей клиентов по общим товарам."""
    orders = get_all_orders(db_file)
    clients = get_all_clients(db_file)
    G = nx.Graph()
    for client in clients:
        G.add_node(client.id)
    product_to_clients = {}
    for order in orders:
        for pid in order.product_ids:
            if pid not in product_to_clients:
                product_to_clients[pid] = []
            product_to_clients[pid].append(order.client_id)
    for clients in product_to_clients.values():
        for i, c1 in enumerate(clients):
            for c2 in clients[i + 1:]:
                G.add_edge(c1, c2)
    plt.figure(figsize=(8, 8))
    nx.draw(G, with_labels=True, node_color="lightblue", node_size=500, font_size=10)
    plt.title("Граф связей клиентов по общим товарам")
    plt.savefig("client_graph.png")
    plt.close()
    return G