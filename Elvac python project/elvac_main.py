import sqlite3
import hashlib
import tkinter as tk
from tkinter import messagebox


def create_database():
    conn = sqlite3.connect('vaccination_passport.db')
    cursor = conn.cursor()

    # Таблица People с полем для хранения пароля
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS People (
            id INTEGER PRIMARY KEY,
            iin TEXT UNIQUE NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Остальные таблицы как раньше...
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS HealthIndicators (
            id INTEGER PRIMARY KEY,
            iin TEXT NOT NULL,
            blood_pressure TEXT,
            cholesterol_level TEXT,
            blood_sugar TEXT,
            FOREIGN KEY (iin) REFERENCES People (iin)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS DispensaryRecords (
            id INTEGER PRIMARY KEY,
            iin TEXT NOT NULL,
            is_on_dispensary BOOLEAN NOT NULL,
            notes TEXT,
            FOREIGN KEY (iin) REFERENCES People (iin)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Vaccinations (
            id INTEGER PRIMARY KEY,
            iin TEXT NOT NULL,
            vaccine_name TEXT NOT NULL,
            date_given TEXT NOT NULL,
            dose_number INTEGER NOT NULL,
            FOREIGN KEY (iin) REFERENCES People (iin)
        )
    ''')

    conn.commit()
    conn.close()

create_database()

# Хеширование пароля
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Регистрация пользователя
def register_user(iin, first_name, last_name, password):
    hashed_password = hash_password(password)
    conn = sqlite3.connect('vaccination_passport.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO People (iin, first_name, last_name, password) VALUES (?, ?, ?, ?)", 
                       (iin, first_name, last_name, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "A user with this IIN already exists.")
        conn.close()
        return False
    conn.close()
    return True

# Аутентификация пользователя
def authenticate_user(iin, password):
    hashed_password = hash_password(password)
    conn = sqlite3.connect('vaccination_passport.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM People WHERE iin = ? AND password = ?", (iin, hashed_password))
    user = cursor.fetchone()
    conn.close()
    return user

# Основной класс приложения
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Electronic Vaccination Passport")
        self.root.geometry("800x600")  # Установка размера окна
        self.font_style = ("Arial", 16)  # Задание стиля и размера шрифта
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()
        
        tk.Label(self.root, text="IIN", font=self.font_style).grid(row=0, column=0, pady=5, padx=5)
        tk.Label(self.root, text="Password", font=self.font_style).grid(row=1, column=0, pady=5, padx=5)

        self.iin_entry = tk.Entry(self.root, font=self.font_style)
        self.iin_entry.grid(row=0, column=1, pady=5, padx=5)
        self.password_entry = tk.Entry(self.root, show="*", font=self.font_style)
        self.password_entry.grid(row=1, column=1, pady=5, padx=5)

        tk.Button(self.root, text="Login", command=self.login, font=self.font_style).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Register", command=self.create_register_screen, font=self.font_style).grid(row=3, column=0, columnspan=2, pady=5)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_register_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Register New User", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(self.root, text="IIN", font=self.font_style).grid(row=1, column=0, pady=5, padx=5)
        tk.Label(self.root, text="First Name", font=self.font_style).grid(row=2, column=0, pady=5, padx=5)
        tk.Label(self.root, text="Last Name", font=self.font_style).grid(row=3, column=0, pady=5, padx=5)
        tk.Label(self.root, text="Password", font=self.font_style).grid(row=4, column=0, pady=5, padx=5)

        self.reg_iin_entry = tk.Entry(self.root, font=self.font_style)
        self.reg_iin_entry.grid(row=1, column=1, pady=5, padx=5)
        self.reg_first_name_entry = tk.Entry(self.root)
        self.reg_first_name_entry.grid(row=2, column=1, pady=5, padx=5)
        self.reg_last_name_entry = tk.Entry(self.root)
        self.reg_last_name_entry.grid(row=3, column=1, pady=5, padx=5)
        self.reg_password_entry = tk.Entry(self.root, show="*")
        self.reg_password_entry.grid(row=4, column=1, pady=5, padx=5)

        tk.Button(self.root, text="Register", command=self.register, font=self.font_style).grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Back to Login", command=self.create_login_screen, font=self.font_style).grid(row=6, column=0, columnspan=2, pady=5)

    def register(self):
        iin = self.reg_iin_entry.get()
        first_name = self.reg_first_name_entry.get()
        last_name = self.reg_last_name_entry.get()
        password = self.reg_password_entry.get()

        if iin and first_name and last_name and password:
            if register_user(iin, first_name, last_name, password):
                messagebox.showinfo("Success", "User registered successfully")
                self.create_login_screen()
            else:
                messagebox.showerror("Error", "Registration failed. Try again.")
        else:
            messagebox.showerror("Error", "Please fill all fields")

    def login(self):
        iin = self.iin_entry.get()
        password = self.password_entry.get()

        user = authenticate_user(iin, password)
        if user:
            self.show_user_info(user)
        else:
            messagebox.showerror("Error", "Invalid IIN or Password")

    def show_user_info(self, user):
        self.clear_screen()

        iin = user[1]
        first_name = user[2]
        last_name = user[3]

        tk.Label(self.root, text=f"Welcome, {first_name} {last_name}", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        health_data = self.get_health_data(iin)
        tk.Label(self.root, text="Health Indicators:", font=self.font_style).grid(row=1, column=0, columnspan=2, pady=5)
        tk.Label(self.root, text=f"Blood Pressure: {health_data[0]}", font=self.font_style).grid(row=2, column=0, columnspan=2, pady=5)
        tk.Label(self.root, text=f"Cholesterol Level: {health_data[1]}", font=self.font_style).grid(row=3, column=0, columnspan=2, pady=5)
        tk.Label(self.root, text=f"Blood Sugar: {health_data[2]}", font=self.font_style).grid(row=4, column=0, columnspan=2, pady=5)

        dispensary_data = self.get_dispensary_data(iin)
        tk.Label(self.root, text="Dispensary Record:", font=self.font_style).grid(row=5, column=0, columnspan=2, pady=5)
        tk.Label(self.root, text=f"On Dispensary: {'Yes' if dispensary_data[0] else 'No'}", font=self.font_style).grid(row=6, column=0, columnspan=2, pady=5)
        tk.Label(self.root, text=f"Notes: {dispensary_data[1]}", font=self.font_style).grid(row=7, column=0, columnspan=2, pady=5)

        vaccination_data = self.get_vaccination_data(iin)
        tk.Label(self.root, text="Vaccination Records:", font=self.font_style).grid(row=8, column=0, columnspan=2, pady=5)
        for idx, record in enumerate(vaccination_data):
            tk.Label(self.root, text=f"{record[0]} on {record[1]} (Dose: {record[2]})", font=self.font_style).grid(row=9 + idx, column=0, columnspan=2, pady=2)

    def get_health_data(self, iin):
        conn = sqlite3.connect('vaccination_passport.db')
        cursor = conn.cursor()
        cursor.execute("SELECT blood_pressure, cholesterol_level, blood_sugar FROM HealthIndicators WHERE iin = ?", (iin,))
        health_data = cursor.fetchone()
        conn.close()
        return health_data if health_data else ("N/A", "N/A", "N/A")

    def get_dispensary_data(self, iin):
        conn = sqlite3.connect('vaccination_passport.db')
        cursor = conn.cursor()
        cursor.execute("SELECT is_on_dispensary, notes FROM DispensaryRecords WHERE iin = ?", (iin,))
        dispensary_data = cursor.fetchone()
        conn.close()
        return dispensary_data if dispensary_data else (False, "No notes")

    def get_vaccination_data(self, iin):
        conn = sqlite3.connect('vaccination_passport.db')
        cursor = conn.cursor()
        cursor.execute("SELECT vaccine_name, date_given, dose_number FROM Vaccinations WHERE iin = ?", (iin,))
        vaccination_data = cursor.fetchall()
        conn.close()
        return vaccination_data if vaccination_data else [("No vaccines recorded", "N/A", "N/A")]


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
    




