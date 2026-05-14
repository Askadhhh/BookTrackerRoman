import json
import os
import tkinter as tk
from tkinter import ttk, messagebox


class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.root.geometry("900x600")

        self.books = []

        # =========================
        # Поля ввода
        # =========================
        form_frame = tk.Frame(root)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Название книги:").grid(
            row=0, column=0, padx=5, pady=5
        )
        self.title_entry = tk.Entry(form_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Автор:").grid(row=1, column=0, padx=5, pady=5)
        self.author_entry = tk.Entry(form_frame, width=30)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Жанр:").grid(row=2, column=0, padx=5, pady=5)
        self.genre_entry = tk.Entry(form_frame, width=30)
        self.genre_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Количество страниц:").grid(
            row=3, column=0, padx=5, pady=5
        )
        self.pages_entry = tk.Entry(form_frame, width=30)
        self.pages_entry.grid(row=3, column=1, padx=5, pady=5)

        # =========================
        # Кнопки
        # =========================
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        add_button = tk.Button(
            button_frame, text="Добавить книгу", command=self.add_book
        )
        add_button.grid(row=0, column=0, padx=10)

        save_button = tk.Button(
            button_frame, text="Сохранить в JSON", command=self.save_books
        )
        save_button.grid(row=0, column=1, padx=10)

        load_button = tk.Button(
            button_frame, text="Загрузить из JSON", command=self.load_books
        )
        load_button.grid(row=0, column=2, padx=10)

        # =========================
        # Фильтрация
        # =========================
        filter_frame = tk.Frame(root)
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Фильтр по жанру:").grid(row=0, column=0, padx=5)
        self.genre_filter = tk.Entry(filter_frame, width=20)
        self.genre_filter.grid(row=0, column=1, padx=5)

        tk.Label(filter_frame, text="Страниц больше:").grid(row=0, column=2, padx=5)
        self.pages_filter = tk.Entry(filter_frame, width=10)
        self.pages_filter.grid(row=0, column=3, padx=5)

        filter_button = tk.Button(
            filter_frame, text="Применить фильтр", command=self.filter_books
        )
        filter_button.grid(row=0, column=4, padx=10)

        show_all_button = tk.Button(
            filter_frame, text="Показать все", command=self.refresh_table
        )
        show_all_button.grid(row=0, column=5, padx=10)

        # =========================
        # Таблица
        # =========================
        columns = ("title", "author", "genre", "pages")

        self.tree = ttk.Treeview(root, columns=columns, show="headings")

        self.tree.heading("title", text="Название")
        self.tree.heading("author", text="Автор")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("pages", text="Страницы")

        self.tree.column("title", width=250)
        self.tree.column("author", width=200)
        self.tree.column("genre", width=150)
        self.tree.column("pages", width=100)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.load_books()

    # =========================
    # Добавление книги
    # =========================
    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages = self.pages_entry.get().strip()

        # Проверка пустых полей
        if not title or not author or not genre or not pages:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        # Проверка числа
        if not pages.isdigit():
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
            return

        book = {"title": title, "author": author, "genre": genre, "pages": int(pages)}

        self.books.append(book)
        self.refresh_table()
        self.clear_entries()

    # =========================
    # Обновление таблицы
    # =========================
    def refresh_table(self, books=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        data = books if books is not None else self.books

        for book in data:
            self.tree.insert(
                "",
                tk.END,
                values=(book["title"], book["author"], book["genre"], book["pages"]),
            )

    # =========================
    # Очистка полей
    # =========================
    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.pages_entry.delete(0, tk.END)

    # =========================
    # Фильтрация
    # =========================
    def filter_books(self):
        genre = self.genre_filter.get().strip().lower()
        pages = self.pages_filter.get().strip()

        filtered = self.books

        if genre:
            filtered = [book for book in filtered if genre in book["genre"].lower()]

        if pages:
            if not pages.isdigit():
                messagebox.showerror("Ошибка", "Фильтр страниц должен быть числом!")
                return

            filtered = [book for book in filtered if book["pages"] > int(pages)]

        self.refresh_table(filtered)

    # =========================
    # Сохранение в JSON
    # =========================
    def save_books(self):
        with open("books.json", "w", encoding="utf-8") as file:
            json.dump(self.books, file, ensure_ascii=False, indent=4)

        messagebox.showinfo("Успех", "Данные сохранены в books.json")

    # =========================
    # Загрузка из JSON
    # =========================
    def load_books(self):
        if os.path.exists("books.json"):
            with open("books.json", "r", encoding="utf-8") as file:
                try:
                    self.books = json.load(file)
                except json.JSONDecodeError:
                    self.books = []

        self.refresh_table()


if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()
