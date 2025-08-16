import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from models import Client, Product, Order
from db import create_db, add_client, add_product, add_order, export_to_csv, import_from_csv, get_all_clients, get_all_products, get_all_orders
from analysis import top_clients, sales_dynamics, client_graph
import sqlite3
from datetime import datetime

class StoreApp:
    def __init__(self, db_file: str):
        """Инициализирует GUI."""
        self.db_file = db_file
        create_db(db_file)
        self.root = tk.Tk()
        self.root.title("Магазин")
        self.root.geometry("800x600")

        # Вкладки
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # Вкладка Клиенты
        self.client_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.client_frame, text="Клиенты")
        ttk.Label(self.client_frame, text="Имя").grid(row=0, column=0, padx=5, pady=5)
        self.client_name = ttk.Entry(self.client_frame)
        self.client_name.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(self.client_frame, text="Email").grid(row=1, column=0, padx=5, pady=5)
        self.client_email = ttk.Entry(self.client_frame)
        self.client_email.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(self.client_frame, text="Телефон").grid(row=2, column=0, padx=5, pady=5)
        self.client_phone = ttk.Entry(self.client_frame)
        self.client_phone.grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(self.client_frame, text="Добавить клиента", command=self.add_client).grid(row=3, column=0, columnspan=2, pady=10)
        self.client_tree = ttk.Treeview(self.client_frame, columns=("ID", "Name", "Email", "Phone"), show="headings")
        self.client_tree.heading("ID", text="ID")
        self.client_tree.heading("Name", text="Имя")
        self.client_tree.heading("Email", text="Email")
        self.client_tree.heading("Phone", text="Телефон")
        self.client_tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        self.update_client_tree()

        # Вкладка Товары
        self.product_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.product_frame, text="Товары")
        ttk.Label(self.product_frame, text="Название").grid(row=0, column=0, padx=5, pady=5)
        self.product_name = ttk.Entry(self.product_frame)
        self.product_name.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(self.product_frame, text="Цена").grid(row=1, column=0, padx=5, pady=5)
        self.product_price = ttk.Entry(self.product_frame)
        self.product_price.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(self.product_frame, text="Добавить товар", command=self.add_product).grid(row=2, column=0, columnspan=2, pady=10)
        self.product_tree = ttk.Treeview(self.product_frame, columns=("ID", "Name", "Price"), show="headings")
        self.product_tree.heading("ID", text="ID")
        self.product_tree.heading("Name", text="Название")
        self.product_tree.heading("Price", text="Цена")
        self.product_tree.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        self.update_product_tree()

        # Вкладка Заказы
        self.order_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.order_frame, text="Заказы")
        ttk.Label(self.order_frame, text="ID клиента").grid(row=0, column=0, padx=5, pady=5)
        self.order_client_id = ttk.Entry(self.order_frame)
        self.order_client_id.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(self.order_frame, text="ID товаров (через запятую)").grid(row=1, column=0, padx=5, pady=5)
        self.order_product_ids = ttk.Entry(self.order_frame)
        self.order_product_ids.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(self.order_frame, text="Дата (ГГГГ-ММ-ДД)").grid(row=2, column=0, padx=5, pady=5)
        self.order_date = ttk.Entry(self.order_frame)
        self.order_date.grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(self.order_frame, text="Добавить заказ", command=self.add_order).grid(row=3, column=0, columnspan=2, pady=10)
        self.order_tree = ttk.Treeview(self.order_frame, columns=("ID", "ClientID", "ProductIDs", "Date", "Total"), show="headings")
        self.order_tree.heading("ID", text="ID")
        self.order_tree.heading("ClientID", text="ID клиента")
        self.order_tree.heading("ProductIDs", text="ID товаров")
        self.order_tree.heading("Date", text="Дата")
        self.order_tree.heading("Total", text="Сумма")
        self.order_tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        self.update_order_tree()

        # Вкладка Анализ
        self.analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.analysis_frame, text="Анализ")
        ttk.Button(self.analysis_frame, text="Топ клиентов", command=self.show_top_clients).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(self.analysis_frame, text="Динамика продаж", command=self.show_sales_dynamics).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.analysis_frame, text="Граф клиентов", command=self.show_client_graph).grid(row=0, column=2, padx=5, pady=5)

        # Кнопки экспорта/импорта
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=5)
        ttk.Button(button_frame, text="Экспорт в CSV", command=self.export_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Импорт из CSV", command=self.import_csv).pack(side=tk.LEFT, padx=5)

    def get_next_id(self, table: str) -> int:
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute(f"SELECT MAX(id) FROM {table}")
        result = cursor.fetchone()
        max_id = result[0] if result else None
        conn.close()
        return (max_id or 0) + 1

    def update_client_tree(self):
        """Обновляет таблицу клиентов."""
        for item in self.client_tree.get_children():
            self.client_tree.delete(item)
        clients = get_all_clients(self.db_file)
        for client in clients:
            self.client_tree.insert("", tk.END, values=(client.id, client.name, client.email, client.phone))

    def update_product_tree(self):
        """Обновляет таблицу товаров."""
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        products = get_all_products(self.db_file)
        for product in products:
            self.product_tree.insert("", tk.END, values=(product.id, product.name, product.price))

    def update_order_tree(self):
        """Обновляет таблицу заказов."""
        for item in self.order_tree.get_children():
            self.order_tree.delete(item)
        orders = get_all_orders(self.db_file)
        for order in orders:
            self.order_tree.insert("", tk.END, values=(order.id, order.client_id, order.product_ids, order.date, order.total))

    def add_client(self):
        """Добавляет клиента."""
        name = self.client_name.get().strip()
        email = self.client_email.get().strip()
        phone = self.client_phone.get().strip()
        if not all([name, email, phone]):
            messagebox.showerror("Ошибка", "Заполните все поля")
            return
        try:
            client_id = self.get_next_id("clients")
            client = Client(client_id, name, email, phone)
            add_client(self.db_file, client)
            self.update_client_tree()
            self.client_name.delete(0, tk.END)
            self.client_email.delete(0, tk.END)
            self.client_phone.delete(0, tk.END)
            messagebox.showinfo("Успех", "Клиент добавлен")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить клиента: {str(e)}")

    def add_product(self):
        """Добавляет товар."""
        name = self.product_name.get().strip()
        price = self.product_price.get().strip()
        try:
            price = float(price)
            product_id = self.get_next_id("products")
            product = Product(product_id, name, price)
            add_product(self.db_file, product)
            self.update_product_tree()
            self.product_name.delete(0, tk.END)
            self.product_price.delete(0, tk.END)
            messagebox.showinfo("Успех", "Товар добавлен")
        except ValueError:
            messagebox.showerror("Ошибка", "Цена должна быть числом")

    def add_order(self):
        """Добавляет заказ."""
        client_id = self.order_client_id.get().strip()
        product_ids = self.order_product_ids.get().strip()
        date = self.order_date.get().strip()
        if not (client_id and product_ids and date):
            messagebox.showerror("Ошибка", "Заполните все поля")
            return
        try:
            client_id = int(client_id)
            product_ids = [int(pid.strip()) for pid in product_ids.split(",") if pid.strip()]
            # Проверка существования клиента
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM clients WHERE id = ?", (client_id,))
            if not cursor.fetchone():
                conn.close()
                messagebox.showerror("Ошибка", "Клиент не существует")
                return
            # Проверка существования товаров
            for pid in product_ids:
                cursor.execute("SELECT id FROM products WHERE id = ?", (pid,))
                if not cursor.fetchone():
                    conn.close()
                    messagebox.showerror("Ошибка", f"Товар с ID {pid} не существует")
                    return
            # Проверка формата даты
            datetime.strptime(date, "%Y-%m-%d")
            # Создание списка продуктов для Order
            products = []
            cursor.execute("SELECT id, name, price FROM products WHERE id IN ({})".format(",".join("?" * len(product_ids))), product_ids)
            for row in cursor.fetchall():
                products.append(Product(row[0], row[1], row[2]))
            conn.close()
            order_id = self.get_next_id("orders")
            order = Order(order_id, client_id, product_ids, date, products)
            add_order(self.db_file, order)
            self.update_order_tree()
            self.order_client_id.delete(0, tk.END)
            self.order_product_ids.delete(0, tk.END)
            self.order_date.delete(0, tk.END)
            messagebox.showinfo("Успех", "Заказ добавлен")
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def export_csv(self):
        """Экспортирует данные в CSV."""
        export_to_csv(self.db_file, "clients.csv", "products.csv", "orders.csv")
        self.update_client_tree()
        self.update_product_tree()
        self.update_order_tree()
        messagebox.showinfo("Успех", "Данные экспортированы в CSV")

    def import_csv(self):
        """Импортирует данные из CSV."""
        try:
            import_from_csv(self.db_file, "clients.csv", "products.csv", "orders.csv")
            self.update_client_tree()
            self.update_product_tree()
            self.update_order_tree()
            messagebox.showinfo("Успех", "Данные импортированы из CSV")
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файлы CSV не найдены")

    def show_top_clients(self):
        """Показывает топ клиентов."""
        result = top_clients(self.db_file, n=5)
        message = "\n".join([f"{r['client_name']}: {r['order_count']} заказов" for r in result])
        messagebox.showinfo("Топ клиентов", message or "Нет данных")

    def get_sales_dynamics_data(self):
        """Возвращает данные для динамики продаж без отображения."""
        return sales_dynamics(self.db_file)

    def show_sales_dynamics(self):
        """Показывает динамику продаж."""
        df = self.get_sales_dynamics_data()
        if df.empty:
            messagebox.showinfo("Динамика продаж", "Нет данных")
            return
        # Создаём новое окно для графика
        graph_window = tk.Toplevel(self.root)
        graph_window.title("Динамика продаж")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.lineplot(data=df, x="date", y="total", ax=ax)
        ax.set_title("Динамика заказов по датам")
        ax.set_xlabel("Дата")
        ax.set_ylabel("Сумма заказов")
        ax.tick_params(axis="x", rotation=45)
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def get_client_graph_data(self):
        """Возвращает данные для графа клиентов без отображения."""
        return client_graph(self.db_file)

    def show_client_graph(self):
        """Показывает граф клиентов."""
        G = self.get_client_graph_data()
        if not G.nodes:
            messagebox.showinfo("Граф клиентов", "Нет данных")
            return
        # Создаём новое окно для графика
        graph_window = tk.Toplevel(self.root)
        graph_window.title("Граф клиентов")
        fig, ax = plt.subplots(figsize=(6, 4))
        nx.draw(G, with_labels=True, node_color="lightblue", node_size=500, font_size=10, ax=ax)
        ax.set_title("Граф связей клиентов по общим товарам")
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def run(self):
        """Запускает приложение."""
        self.root.mainloop()

if __name__ == "__main__":
    app = StoreApp("store.db")
    app.run()