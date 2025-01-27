import tkinter as tk
from tkinter import ttk
import sqlite3
from data_page import DataPage  # Import the new DataPage class

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Modern Tkinter App")
        self.geometry("800x600")

        # Create main containers
        self.sidebar = ttk.Frame(self, width=200, style='Sidebar.TFrame')
        self.content = ttk.Frame(self, style='Content.TFrame')

        # Layout main containers
        self.sidebar.pack(side="left", fill="y")
        self.content.pack(side="right", fill="both", expand=True)

        # Create sidebar buttons
        ttk.Button(self.sidebar, text="Home", command=self.show_home).pack(pady=10)
        ttk.Button(self.sidebar, text="Data", command=self.show_data).pack(pady=10)

        # Initialize database
        self.init_database()

        # Show initial content
        self.show_home()

    def init_database(self):
        conn = sqlite3.connect('app_data.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS items
                     (id INTEGER PRIMARY KEY, name TEXT)''')
        # Add some sample data if the table is empty
        c.execute("SELECT COUNT(*) FROM items")
        if c.fetchone()[0] == 0:
            for i in range(20):
                c.execute("INSERT INTO items (name) VALUES (?)", (f"Item {i+1}",))
        conn.commit()
        conn.close()

    def show_home(self):
        self.clear_content()
        ttk.Label(self.content, text="Welcome to the Home Page").pack(pady=20)

    def show_data(self):
        self.clear_content()
        data_page = DataPage(self.content, 'app_data.db')
        data_page.pack(fill=tk.BOTH, expand=True)

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = App()
    
    # Apply a modern style
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('Sidebar.TFrame', background='#2c3e50')
    style.configure('Content.TFrame', background='#ecf0f1')
    
    app.mainloop()