import json
import sqlite3
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(BASE_DIR, "catalog.json")
DB_FILE = os.path.join(BASE_DIR, "shop.db")

def load_catalog(path: str) -> list:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def init_db(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    cursor.executescript("""
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS categories;

        CREATE TABLE categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT NOT NULL
        );

        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            price REAL NOT NULL,
            category_id INTEGER NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        );
    """)
    conn.commit()

def normalize_and_save(conn: sqlite3.Connection, catalog: list) -> None:
    cursor = conn.cursor()

    categories_seen = {}
    for item in catalog:
        cat = item["category"]
        key = (cat["name"], cat["description"])
        if key not in categories_seen:
            categories_seen[key] = None

    for (name, description) in categories_seen.keys():
        cursor.execute(
            "INSERT INTO categories (name, description) VALUES (?, ?)",
            (name, description),
        )
        categories_seen[(name, description)] = cursor.lastrowid

    for item in catalog:
        cat = item["category"]
        category_id = categories_seen[(cat["name"], cat["description"])]
        cursor.execute(
            "INSERT INTO products (product_name, price, category_id) VALUES (?, ?, ?)",
            (item["product_name"], item["price"], category_id),
        )
    conn.commit()

def main():
    if not os.path.exists(JSON_FILE):
        print(" Файл catalog.json не найден!")
        return

    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    catalog = load_catalog(JSON_FILE)
    print(f" Прочитано записей из JSON: {len(catalog)}")

    conn = sqlite3.connect(DB_FILE)
    try:
        init_db(conn)
        normalize_and_save(conn, catalog)
        print(" Данные успешно нормализованы и сохранены в shop.db")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
