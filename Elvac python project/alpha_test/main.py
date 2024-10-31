import tkinter as tk
from tkinter import messagebox
import sqlite3
patient_db = 'users.db'
def connect_to_db():
    conn = sqlite3.connect('my_database.db')  # Создание или подключение к БД
    cursor = conn.cursor()
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )'''
    )
    conn.commit()
    conn.close()

def add_user(name):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def get_users():
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_user(user_id):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("SQLite User Manager")
        
        # Поле для ввода имени
        self.name_label = tk.Label(root, text="Name:")
        self.name_label.grid(row=0, column=0)
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=0, column=1)
        
        # Кнопка для добавления пользователя
        self.add_button = tk.Button(root, text="Add User", command=self.add_user)
        self.add_button.grid(row=0, column=2)
        
        # Поле для отображения списка пользователей
        self.user_list = tk.Listbox(root)
        self.user_list.grid(row=1, column=0, columnspan=3)
        
        # Кнопка для удаления пользователя
        self.delete_button = tk.Button(root, text="Delete User", command=self.delete_user)
        self.delete_button.grid(row=2, column=0)
        
        # Кнопка для обновления списка пользователей
        self.view_button = tk.Button(root, text="View Users", command=self.view_users)
        self.view_button.grid(row=2, column=1)
        
    def add_user(self):
        name = self.name_entry.get()
        if name:
            add_user(name)
            messagebox.showinfo("Success", "User added!")
            self.name_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Error", "Please enter a name")
    
    def view_users(self):
        self.user_list.delete(0, tk.END)
        users = get_users()
        for user in users:
            self.user_list.insert(tk.END, f"{user[0]}. {user[1]}")
    
    def delete_user(self):
        selected_user = self.user_list.get(tk.ACTIVE)
        if selected_user:
            user_id = int(selected_user.split(".")[0])  # Получаем ID пользователя из строки
            delete_user(user_id)
            messagebox.showinfo("Success", "User deleted!")
            self.view_users()
        else:
            messagebox.showwarning("Error", "Please select a user to delete")

if __name__ == "__main__":
    connect_to_db()
    root = tk.Tk()
    app = App(root)
    root.mainloop()
