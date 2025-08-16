import unittest
from unittest.mock import patch, MagicMock
from models import Client, Product, Order
from gui import StoreApp
import pandas as pd
import tkinter as tk

class TestStoreApp(unittest.TestCase):
    def setUp(self):
        """Инициализирует тестовые данные."""
        self.db_file = "test_store.db"

    @patch("db.create_db")
    @patch("db.get_all_clients")
    @patch("sqlite3.connect")
    @patch("db.add_client")
    @patch("tkinter.messagebox.showinfo")
    @patch("tkinter.messagebox.showerror")
    @patch("tkinter.ttk.Entry")
    @patch("tkinter.ttk.Button")
    @patch("tkinter.ttk.Treeview")
    @patch("tkinter.ttk.Frame")
    @patch("tkinter.ttk.Notebook")
    @patch("tkinter.Tk")
    def test_add_client(self, mock_tk, mock_notebook, mock_frame, mock_treeview, mock_button, mock_entry,
                        mock_showerror, mock_showinfo, mock_add_client, mock_connect, mock_get_all_clients,
                        mock_create_db):
        """Проверяет добавление клиента через GUI."""
        mock_create_db.return_value = None
        mock_get_all_clients.return_value = []
        mock_treeview.return_value = MagicMock()
        mock_treeview.return_value.delete = MagicMock()  # Для update_client_tree
        mock_treeview.return_value.insert = MagicMock()
        mock_entry.side_effect = [MagicMock() for _ in range(8)]
        mock_button.return_value = MagicMock()
        mock_frame.return_value = MagicMock()
        mock_notebook.return_value = MagicMock()
        app = StoreApp(self.db_file)
        app.client_name = MagicMock()
        app.client_email = MagicMock()
        app.client_phone = MagicMock()
        app.client_name.get = MagicMock(return_value="Иван Иванов")
        app.client_email.get = MagicMock(return_value="ivan.ivanov@example.com")  # Более строгий email
        app.client_phone.get = MagicMock(return_value="+799912345678")  # 12 цифр
        app.client_name.delete = MagicMock()
        app.client_email.delete = MagicMock()
        app.client_phone.delete = MagicMock()
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None
        mock_connection.commit = MagicMock()
        mock_connection.__enter__.return_value = mock_connection
        mock_connection.__exit__.return_value = None
        app.add_client()
        mock_add_client.assert_called_once_with(
            self.db_file, Client(1, "Иван Иванов", "ivan.ivanov@example.com", "+799912345678")
        )
        app.client_name.delete.assert_called_once_with(0, tk.END)
        app.client_email.delete.assert_called_once_with(0, tk.END)
        app.client_phone.delete.assert_called_once_with(0, tk.END)
        mock_showinfo.assert_called_once_with("Успех", "Клиент добавлен")
        mock_showerror.assert_not_called()

    @patch("db.create_db")
    @patch("db.get_all_clients")
    @patch("sqlite3.connect")
    @patch("db.add_client")
    @patch("tkinter.messagebox.showinfo")
    @patch("tkinter.messagebox.showerror")
    @patch("tkinter.ttk.Entry")
    @patch("tkinter.ttk.Button")
    @patch("tkinter.ttk.Treeview")
    @patch("tkinter.ttk.Frame")
    @patch("tkinter.ttk.Notebook")
    @patch("tkinter.Tk")
    def test_add_client(self, mock_tk, mock_notebook, mock_frame, mock_treeview, mock_button, mock_entry,
                        mock_showerror, mock_showinfo, mock_add_client, mock_connect, mock_get_all_clients,
                        mock_create_db):
        """Проверяет добавление клиента через GUI."""
        print(f"Arguments received: {locals()}")  # Отладка аргументов
        mock_create_db.return_value = None
        mock_get_all_clients.return_value = []
        mock_treeview.return_value = MagicMock()
        mock_entry.side_effect = [MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock(),
                                  MagicMock(), MagicMock()]  # Для всех Entry в __init__
        mock_button.return_value = MagicMock()
        mock_frame.return_value = MagicMock()
        mock_notebook.return_value = MagicMock()
        app = StoreApp(self.db_file)
        app.client_name = MagicMock()
        app.client_email = MagicMock()
        app.client_phone = MagicMock()
        app.client_name.get = MagicMock(return_value="Иван Иванов")
        app.client_email.get = MagicMock(return_value="ivan@example.com")
        app.client_phone.get = MagicMock(return_value="+79991234567")
        app.client_name.delete = MagicMock()
        app.client_email.delete = MagicMock()
        app.client_phone.delete = MagicMock()
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None  # Пустая таблица
        mock_connection.commit = MagicMock()
        mock_connection.__enter__.return_value = mock_connection
        mock_connection.__exit__.return_value = None
        try:
            print(
                f"Calling add_client with: name={app.client_name.get()}, email={app.client_email.get()}, phone={app.client_phone.get()}")
            app.add_client()
        except Exception as e:
            print(f"Exception in add_client: {str(e)}")
        if mock_showerror.called:
            print(f"showerror called with: {mock_showerror.call_args}")
        mock_add_client.assert_called_once_with(
            self.db_file, Client(1, "Иван Иванов", "ivan@example.com", "+79991234567")
        )
        app.client_name.delete.assert_called_once_with(0, tk.END)
        app.client_email.delete.assert_called_once_with(0, tk.END)
        app.client_phone.delete.assert_called_once_with(0, tk.END)
        mock_showinfo.assert_called_once_with("Успех", "Клиент добавлен")
        mock_showerror.assert_not_called()

    @patch("db.get_all_clients")
    @patch("db.get_all_products")
    @patch("db.get_all_orders")
    @patch("sqlite3.connect")
    @patch("db.add_client")
    @patch("tkinter.messagebox.showerror")
    @patch("tkinter.messagebox.showinfo")
    @patch("tkinter.Tk")
    def test_add_client_empty_fields(self, mock_tk, mock_showinfo, mock_showerror, mock_add_client, mock_connect, mock_get_all_orders, mock_get_all_products, mock_get_all_clients):
        """Проверяет ошибку при пустых полях клиента."""
        mock_get_all_clients.return_value = []
        mock_get_all_products.return_value = []
        mock_get_all_orders.return_value = []
        app = StoreApp(self.db_file)
        app.client_name = MagicMock()
        app.client_email = MagicMock()
        app.client_phone = MagicMock()
        app.client_name.get = MagicMock(return_value="")
        app.client_email.get = MagicMock(return_value="ivan@example.com")
        app.client_phone.get = MagicMock(return_value="+79991234567")
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (0,)
        app.add_client()
        mock_showerror.assert_called_once_with("Ошибка", "Заполните все поля")
        mock_showinfo.assert_not_called()
        mock_add_client.assert_not_called()

    @patch("db.get_all_clients")
    @patch("db.get_all_products")
    @patch("db.get_all_orders")
    @patch("sqlite3.connect")
    @patch("db.add_product")
    @patch("tkinter.messagebox.showinfo")
    @patch("tkinter.messagebox.showerror")
    @patch("tkinter.Tk")
    def test_add_product(self, mock_tk, mock_showerror, mock_showinfo, mock_add_product, mock_connect, mock_get_all_orders, mock_get_all_products, mock_get_all_clients):
        """Проверяет добавление товара через GUI."""
        mock_get_all_clients.return_value = []
        mock_get_all_products.return_value = []
        mock_get_all_orders.return_value = []
        app = StoreApp(self.db_file)
        app.product_name = MagicMock()
        app.product_price = MagicMock()
        app.product_name.get = MagicMock(return_value="Ноутбук")
        app.product_price.get = MagicMock(return_value="50000")
        app.product_name.delete = MagicMock()
        app.product_price.delete = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (0,)
        app.add_product()
        mock_add_product.assert_called_once_with(
            self.db_file, Product(1, "Ноутбук", 50000.0)
        )
        app.product_name.delete.assert_called_once_with(0, tk.END)
        app.product_price.delete.assert_called_once_with(0, tk.END)
        mock_showinfo.assert_called_once_with("Успех", "Товар добавлен")
        mock_showerror.assert_not_called()

    @patch("db.get_all_clients")
    @patch("db.get_all_products")
    @patch("db.get_all_orders")
    @patch("sqlite3.connect")
    @patch("db.add_product")
    @patch("tkinter.messagebox.showerror")
    @patch("tkinter.messagebox.showinfo")
    @patch("tkinter.Tk")
    def test_add_product_invalid_price(self, mock_tk, mock_showinfo, mock_showerror, mock_add_product, mock_connect, mock_get_all_orders, mock_get_all_products, mock_get_all_clients):
        """Проверяет ошибку при неверной цене."""
        mock_get_all_clients.return_value = []
        mock_get_all_products.return_value = []
        mock_get_all_orders.return_value = []
        app = StoreApp(self.db_file)
        app.product_name = MagicMock()
        app.product_price = MagicMock()
        app.product_name.get = MagicMock(return_value="Ноутбук")
        app.product_price.get = MagicMock(return_value="invalid")
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (0,)
        app.add_product()
        mock_showerror.assert_called_once_with("Ошибка", "Цена должна быть числом")
        mock_showinfo.assert_not_called()
        mock_add_product.assert_not_called()

    @patch("db.get_all_clients")
    @patch("db.get_all_products")
    @patch("db.get_all_orders")
    @patch("db.add_order")
    @patch("sqlite3.connect")
    @patch("tkinter.messagebox.showinfo")
    @patch("tkinter.messagebox.showerror")
    @patch("tkinter.Tk")
    def test_add_order(self, mock_tk, mock_showerror, mock_showinfo, mock_connect, mock_add_order, mock_get_all_orders, mock_get_all_products, mock_get_all_clients):
        """Проверяет добавление заказа через GUI."""
        mock_get_all_clients.return_value = []
        mock_get_all_products.return_value = []
        mock_get_all_orders.return_value = []
        app = StoreApp(self.db_file)
        app.order_client_id = MagicMock()
        app.order_product_ids = MagicMock()
        app.order_date = MagicMock()
        app.order_client_id.get = MagicMock(return_value="1")
        app.order_product_ids.get = MagicMock(return_value="1,2")
        app.order_date.get = MagicMock(return_value="2025-08-16")
        app.order_client_id.delete = MagicMock()
        app.order_product_ids.delete = MagicMock()
        app.order_date.delete = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.side_effect = [(0,), (1,), (1,), (2,)]  # Для get_next_id("orders"), client_id, product_id 1, product_id 2
        mock_cursor.fetchall.return_value = [(1, "Ноутбук", 50000), (2, "Телефон", 30000)]
        app.add_order()
        mock_add_order.assert_called_once_with(
            self.db_file,
            Order(1, 1, [1, 2], "2025-08-16", [
                Product(1, "Ноутбук", 50000),
                Product(2, "Телефон", 30000)
            ], total=80000)  # Добавляем total
        )
        app.order_client_id.delete.assert_called_once_with(0, tk.END)
        app.order_product_ids.delete.assert_called_once_with(0, tk.END)
        app.order_date.delete.assert_called_once_with(0, tk.END)
        mock_showinfo.assert_called_once_with("Успех", "Заказ добавлен")
        mock_showerror.assert_not_called()

    @patch("db.get_all_clients")
    @patch("db.get_all_products")
    @patch("db.get_all_orders")
    @patch("db.add_order")
    @patch("sqlite3.connect")
    @patch("tkinter.messagebox.showerror")
    @patch("tkinter.messagebox.showinfo")
    @patch("tkinter.Tk")
    def test_add_order_empty_fields(self, mock_tk, mock_showinfo, mock_showerror, mock_connect, mock_add_order, mock_get_all_orders, mock_get_all_products, mock_get_all_clients):
        """Проверяет ошибку при пустых полях заказа."""
        mock_get_all_clients.return_value = []
        mock_get_all_products.return_value = []
        mock_get_all_orders.return_value = []
        app = StoreApp(self.db_file)
        app.order_client_id = MagicMock()
        app.order_product_ids = MagicMock()
        app.order_date = MagicMock()
        app.order_client_id.get = MagicMock(return_value="")
        app.order_product_ids.get = MagicMock(return_value="1,2")
        app.order_date.get = MagicMock(return_value="2025-08-16")
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (0,)
        app.add_order()
        mock_showerror.assert_called_once_with("Ошибка", "Заполните все поля")
        mock_showinfo.assert_not_called()
        mock_add_order.assert_not_called()

    @patch("db.get_all_clients")
    @patch("db.get_all_products")
    @patch("db.get_all_orders")
    @patch("db.add_order")
    @patch("sqlite3.connect")
    @patch("tkinter.messagebox.showerror")
    @patch("tkinter.messagebox.showinfo")
    @patch("tkinter.Tk")
    def test_add_order_invalid_client(self, mock_tk, mock_showinfo, mock_showerror, mock_connect, mock_add_order, mock_get_all_orders, mock_get_all_products, mock_get_all_clients):
        """Проверяет ошибку при несуществующем клиенте."""
        mock_get_all_clients.return_value = []
        mock_get_all_products.return_value = []
        mock_get_all_orders.return_value = []
        app = StoreApp(self.db_file)
        app.order_client_id = MagicMock()
        app.order_product_ids = MagicMock()
        app.order_date = MagicMock()
        app.order_client_id.get = MagicMock(return_value="1")
        app.order_product_ids.get = MagicMock(return_value="1,2")
        app.order_date.get = MagicMock(return_value="2025-08-16")
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.side_effect = [(0,), None]  # Для get_next_id("orders"), client_id
        mock_cursor.fetchall.return_value = [(1, "Ноутбук", 50000), (2, "Телефон", 30000)]
        app.add_order()
        mock_showerror.assert_called_once_with("Ошибка", "Клиент не существует")
        mock_add_order.assert_not_called()
        mock_showinfo.assert_not_called()

    @patch("db.get_all_clients")
    @patch("db.get_all_products")
    @patch("db.get_all_orders")
    @patch("db.add_order")
    @patch("sqlite3.connect")
    @patch("tkinter.messagebox.showerror")
    @patch("tkinter.messagebox.showinfo")
    @patch("tkinter.Tk")
    def test_add_order_invalid_date(self, mock_tk, mock_showinfo, mock_showerror, mock_connect, mock_add_order, mock_get_all_orders, mock_get_all_products, mock_get_all_clients):
        """Проверяет ошибку при неверном формате даты."""
        mock_get_all_clients.return_value = []
        mock_get_all_products.return_value = []
        mock_get_all_orders.return_value = []
        app = StoreApp(self.db_file)
        app.order_client_id = MagicMock()
        app.order_product_ids = MagicMock()
        app.order_date = MagicMock()
        app.order_client_id.get = MagicMock(return_value="1")
        app.order_product_ids.get = MagicMock(return_value="1,2")
        app.order_date.get = MagicMock(return_value="invalid_date")
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.side_effect = [(0,), (1,), (1,), (2,)]
        mock_cursor.fetchall.return_value = [(1, "Ноутбук", 50000), (2, "Телефон", 30000)]
        app.add_order()
        mock_showerror.assert_called_once_with("Ошибка", "time data 'invalid_date' does not match format '%Y-%m-%d'")
        mock_add_order.assert_not_called()
        mock_showinfo.assert_not_called()

    @patch("db.get_all_clients")
    @patch("db.get_all_products")
    @patch("db.get_all_orders")
    @patch("sqlite3.connect")
    @patch("db.export_to_csv")
    @patch("tkinter.messagebox.showinfo")
    @patch("tkinter.messagebox.showerror")
    @patch("tkinter.Tk")
    def test_export_to_csv(self, mock_tk, mock_showerror, mock_showinfo, mock_export_to_csv, mock_connect, mock_get_all_orders, mock_get_all_products, mock_get_all_clients):
        """Проверяет вызов экспорта в CSV."""
        mock_get_all_clients.return_value = []
        mock_get_all_products.return_value = []
        mock_get_all_orders.return_value = []
        app = StoreApp(self.db_file)
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (0,)
        app.export_csv()
        mock_export_to_csv.assert_called_once_with(
            self.db_file, "clients.csv", "products.csv", "orders.csv"
        )
        mock_showinfo.assert_called_once_with("Успех", "Данные экспортированы в CSV")
        mock_showerror.assert_not_called()

    @patch("db.get_all_clients")
    @patch("db.get_all_products")
    @patch("db.get_all_orders")
    @patch("sqlite3.connect")
    @patch("db.import_from_csv")
    @patch("tkinter.messagebox.showinfo")
    @patch("tkinter.messagebox.showerror")
    @patch("tkinter.Tk")
    def test_import_from_csv(self, mock_tk, mock_showerror, mock_showinfo, mock_import_from_csv, mock_connect, mock_get_all_orders, mock_get_all_products, mock_get_all_clients):
        """Проверяет вызов импорта из CSV."""
        mock_get_all_clients.return_value = []
        mock_get_all_products.return_value = []
        mock_get_all_orders.return_value = []
        app = StoreApp(self.db_file)
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (0,)
        app.import_csv()
        mock_import_from_csv.assert_called_once_with(
            self.db_file, "clients.csv", "products.csv", "orders.csv"
        )
        mock_showinfo.assert_called_once_with("Успех", "Данные импортированы из CSV")
        mock_showerror.assert_not_called()

    @patch("db.get_all_clients")
    @patch("db.get_all_products")
    @patch("db.get_all_orders")
    @patch("sqlite3.connect")
    @patch("db.import_from_csv")
    @patch("tkinter.messagebox.showerror")
    @patch("tkinter.messagebox.showinfo")
    @patch("tkinter.Tk")
    def test_import_from_csv_not_found(self, mock_tk, mock_showinfo, mock_showerror, mock_import_from_csv, mock_connect, mock_get_all_orders, mock_get_all_products, mock_get_all_clients):
        """Проверяет ошибку при отсутствии CSV файлов."""
        mock_get_all_clients.return_value = []
        mock_get_all_products.return_value = []
        mock_get_all_orders.return_value = []
        app = StoreApp(self.db_file)
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (0,)
        mock_import_from_csv.side_effect = FileNotFoundError
        app.import_csv()
        mock_import_from_csv.assert_called_once_with(
            self.db_file, "clients.csv", "products.csv", "orders.csv"
        )
        mock_showerror.assert_called_once_with("Ошибка", "Файлы CSV не найдены")
        mock_showinfo.assert_not_called()

    @patch("db.get_all_clients")
    @patch("db.get_all_products")
    @patch("db.get_all_orders")
    @patch("sqlite3.connect")
    @patch("analysis.top_clients")
    @patch("tkinter.messagebox.showinfo")
    @patch("tkinter.messagebox.showerror")
    @patch("tkinter.Tk")
    def test_show_top_clients(self, mock_tk, mock_showerror, mock_showinfo, mock_top_clients, mock_connect, mock_get_all_orders, mock_get_all_products, mock_get_all_clients):
        """Проверяет вызов топ клиентов."""
        mock_get_all_clients.return_value = []
        mock_get_all_products.return_value = []
        mock_get_all_orders.return_value = []
        app = StoreApp(self.db_file)
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (0,)
        mock_top_clients.return_value = [
            {"client_name": "Иван Иванов", "order_count": 2}
        ]
        app.show_top_clients()
        mock_top_clients.assert_called_once_with(self.db_file, n=5)
        mock_showinfo.assert_called_once_with("Топ клиентов", "Иван Иванов: 2 заказов")
        mock_showerror.assert_not_called()

    @patch("db.get_all_clients")
    @patch("db.get_all_products")
    @patch("db.get_all_orders")
    @patch("sqlite3.connect")
    @patch("analysis.sales_dynamics")
    @patch("tkinter.Tk")
    def test_get_sales_dynamics_data(self, mock_tk, mock_sales_dynamics, mock_connect, mock_get_all_orders, mock_get_all_products, mock_get_all_clients):
        """Проверяет получение данных динамики продаж без отображения."""
        mock_get_all_clients.return_value = []
        mock_get_all_products.return_value = []
        mock_get_all_orders.return_value = []
        app = StoreApp(self.db_file)
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (0,)
        mock_sales_dynamics.return_value = pd.DataFrame(columns=["date", "total"])
        result = app.get_sales_dynamics_data()
        mock_sales_dynamics.assert_called_once_with(self.db_file)
        pd.testing.assert_frame_equal(
            result,
            pd.DataFrame(columns=["date", "total"]),
            check_dtype=False
        )

    @patch("db.get_all_clients")
    @patch("db.get_all_products")
    @patch("db.get_all_orders")
    @patch("sqlite3.connect")
    @patch("analysis.client_graph")
    @patch("tkinter.Tk")
    def test_get_client_graph_data(self, mock_tk, mock_client_graph, mock_connect, mock_get_all_orders, mock_get_all_products, mock_get_all_clients):
        """Проверяет получение данных графа клиентов без отображения."""
        mock_get_all_clients.return_value = []
        mock_get_all_products.return_value = []
        mock_get_all_orders.return_value = []
        app = StoreApp(self.db_file)
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (0,)
        mock_graph = MagicMock()
        mock_graph.nodes = []
        mock_graph.edges = []
        mock_client_graph.return_value = mock_graph
        result = app.get_client_graph_data()
        mock_client_graph.assert_called_once_with(self.db_file)
        self.assertEqual(len(result.nodes), 0)
        self.assertEqual(len(result.edges), 0)

if __name__ == "__main__":
    unittest.main()