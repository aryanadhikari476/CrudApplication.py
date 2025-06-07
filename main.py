import sqlite3
from typing import List, Tuple, Optional

class Database:
    def __init__(self, db_name: str = "items.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def create_item(self, name: str, description: str) -> int:
        self.cursor.execute(
            "INSERT INTO items (name, description) VALUES (?, ?)",
            (name, description)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def read_item(self, item_id: int) -> Optional[Tuple]:
        self.cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        return self.cursor.fetchone()

    def read_all_items(self) -> List[Tuple]:
        self.cursor.execute("SELECT * FROM items")
        return self.cursor.fetchall()

    def update_item(self, item_id: int, name: str, description: str) -> bool:
        self.cursor.execute(
            "UPDATE items SET name = ?, description = ? WHERE id = ?",
            (name, description, item_id)
        )
        self.conn.commit()
        return self.cursor.rowcount > 0

    def delete_item(self, item_id: int) -> bool:
        self.cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def __del__(self):
        self.conn.close()

def print_menu():
    print("\n=== CRUD Application Menu ===")
    print("1. Create new item")
    print("2. Read all items")
    print("3. Read specific item")
    print("4. Update item")
    print("5. Delete item")
    print("6. Exit")
    print("===========================")

def main():
    db = Database()
    
    while True:
        print_menu()
        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            name = input("Enter item name: ")
            description = input("Enter item description: ")
            item_id = db.create_item(name, description)
            print(f"Item created successfully with ID: {item_id}")

        elif choice == "2":
            items = db.read_all_items()
            if items:
                print("\nAll Items:")
                for item in items:
                    print(f"ID: {item[0]}, Name: {item[1]}, Description: {item[2]}, Created: {item[3]}")
            else:
                print("No items found.")

        elif choice == "3":
            item_id = int(input("Enter item ID: "))
            item = db.read_item(item_id)
            if item:
                print(f"\nItem found:")
                print(f"ID: {item[0]}, Name: {item[1]}, Description: {item[2]}, Created: {item[3]}")
            else:
                print("Item not found.")

        elif choice == "4":
            item_id = int(input("Enter item ID to update: "))
            name = input("Enter new name: ")
            description = input("Enter new description: ")
            if db.update_item(item_id, name, description):
                print("Item updated successfully.")
            else:
                print("Item not found.")

        elif choice == "5":
            item_id = int(input("Enter item ID to delete: "))
            if db.delete_item(item_id):
                print("Item deleted successfully.")
            else:
                print("Item not found.")

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
