'''
import tkinter as tk
from tkinter import ttk, messagebox

def center_window(window, width=600, height=400):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f"{width}x{height}+{x}+{y}")

class VaccinationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vaccination Passport Management")

        # Центрируем окно
        center_window(self.root, 600, 400)

        # Создаем таблицу для пациентов
        self.patient_tree = ttk.Treeview(self.root, columns=("Name", "IIN"), show='headings')
        self.patient_tree.heading("Name", text="Name")
        self.patient_tree.heading("IIN", text="IIN")

        # Пример данных о пациентах
        self.patients = [
            ("John Doe", "123456789012"),
            ("Jane Smith", "987654321098"),
        ]

        # Вставляем данные о пациентах в таблицу
        for patient in self.patients:
            self.patient_tree.insert("", tk.END, values=patient)

        self.patient_tree.pack(pady=10)

        # Кнопка для отображения вакцин пациента
        tk.Button(self.root, text="Show Vaccinations", command=self.show_vaccinations).pack(pady=10)

        # Создаем таблицу для вакцин
        self.vaccine_tree = ttk.Treeview(self.root, columns=("Vaccine Name", "Date"), show='headings')
        self.vaccine_tree.heading("Vaccine Name", text="Vaccine Name")
        self.vaccine_tree.heading("Date", text="Date")

        self.vaccine_tree.pack(pady=10)

    def show_vaccinations(self):
        # Очистка предыдущих данных
        for item in self.vaccine_tree.get_children():
            self.vaccine_tree.delete(item)

        # Пример данных о вакцинах для выбранного пациента (можно адаптировать)
        # Здесь используется фиксированный набор данных, замените его на ваши данные
        vaccines = [
            ("Vaccine A", "2022-01-15"),
            ("Vaccine B", "2022-07-20"),
        ]

        # Вставляем данные о вакцинах в таблицу
        for vaccine in vaccines:
            self.vaccine_tree.insert("", tk.END, values=vaccine)

if __name__ == "__main__":
    root = tk.Tk()
    app = VaccinationApp(root)
    root.mainloop()
'''
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

class VaccinationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vaccination Passport Management")
        self.font_style = ("Arial", 12)

        # Создание базы данных и таблицы, если не существует
        self.create_db()

        # Начальный экран
        self.create_initial_screen()

    def create_db(self):
        conn = sqlite3.connect('vaccination_passport.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE,
                            password TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS Vaccinations (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            iin TEXT NOT NULL,
                            vaccine_name TEXT NOT NULL,
                            date_given DATE NOT NULL,
                            dose_number INTEGER NOT NULL)''')
        conn.commit()
        conn.close()

    def create_initial_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Welcome to Vaccination Passport Management", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="Login", command=self.show_login_screen, font=self.font_style).pack(pady=5)
        tk.Button(self.root, text="Register", command=self.show_register_screen, font=self.font_style).pack(pady=5)

    def show_login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Login", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Username", font=self.font_style).pack(pady=5)
        self.username_entry = tk.Entry(self.root, font=self.font_style)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password", font=self.font_style).pack(pady=5)
        self.password_entry = tk.Entry(self.root, show='*', font=self.font_style)
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Login", command=self.login_user, font=self.font_style).pack(pady=10)

    def show_register_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Register", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Username", font=self.font_style).pack(pady=5)
        self.new_username_entry = tk.Entry(self.root, font=self.font_style)
        self.new_username_entry.pack(pady=5)

        tk.Label(self.root, text="Password", font=self.font_style).pack(pady=5)
        self.new_password_entry = tk.Entry(self.root, show='*', font=self.font_style)
        self.new_password_entry.pack(pady=5)

        tk.Button(self.root, text="Register", command=self.register_user, font=self.font_style).pack(pady=10)

    def register_user(self):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please fill all fields.")
            return

        conn = sqlite3.connect('vaccination_passport.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful.")
            self.show_login_screen()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")
        finally:
            conn.close()

    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = sqlite3.connect('vaccination_passport.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            messagebox.showinfo("Success", "Login successful.")
            self.show_patient_screen()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def show_patient_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Patient Vaccination Management", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="IIN", font=self.font_style).pack(pady=5)
        self.iin_entry = tk.Entry(self.root, font=self.font_style)
        self.iin_entry.pack(pady=5)

        tk.Button(self.root, text="Add Vaccination Record", command=self.add_vaccination_screen, font=self.font_style).pack(pady=5)
        tk.Button(self.root, text="Search Vaccination Records", command=self.search_patient, font=self.font_style).pack(pady=5)

        tk.Button(self.root, text="Update Vaccination Records", command=self.update_vaccination_data, font=self.font_style).pack(pady=5)

    def add_vaccination_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Add Vaccination Record", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="IIN", font=self.font_style).pack(pady=5)
        self.iin_entry = tk.Entry(self.root, font=self.font_style)
        self.iin_entry.pack(pady=5)

        tk.Label(self.root, text="Vaccine Name", font=self.font_style).pack(pady=5)
        self.vaccine_name_entry = tk.Entry(self.root, font=self.font_style)
        self.vaccine_name_entry.pack(pady=5)

        tk.Label(self.root, text="Date Given (YYYY-MM-DD)", font=self.font_style).pack(pady=5)
        self.date_given_entry = tk.Entry(self.root, font=self.font_style)
        self.date_given_entry.pack(pady=5)

        tk.Label(self.root, text="Dose Number", font=self.font_style).pack(pady=5)
        self.dose_number_entry = tk.Entry(self.root, font=self.font_style)
        self.dose_number_entry.pack(pady=5)

        tk.Button(self.root, text="Add", command=self.add_vaccination, font=self.font_style).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_patient_screen, font=self.font_style).pack(pady=5)

    def add_vaccination(self):
        iin = self.iin_entry.get().strip()
        vaccine_name = self.vaccine_name_entry.get().strip()
        date_given = self.date_given_entry.get().strip()
        dose_number = self.dose_number_entry.get().strip()

        if not iin or not vaccine_name or not date_given or not dose_number:
            messagebox.showerror("Error", "Please fill all fields.")
            return

        conn = sqlite3.connect('vaccination_passport.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Vaccinations (iin, vaccine_name, date_given, dose_number) VALUES (?, ?, ?, ?)",
                       (iin, vaccine_name, date_given, int(dose_number)))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Vaccination record added successfully.")
        self.show_patient_screen()

    def search_patient(self):
        iin = self.iin_entry.get().strip()
        if not iin:
            messagebox.showerror("Error", "Please enter IIN.")
            return

        conn = sqlite3.connect('vaccination_passport.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, vaccine_name, date_given, dose_number FROM Vaccinations WHERE LOWER(iin) = LOWER(?)", (iin,))
        self.vaccination_data = cursor.fetchall()
        conn.close()

        if self.vaccination_data:
            self.show_vaccination_data()
        else:
            messagebox.showinfo("Info", "No vaccination records found for this patient.")

    def show_vaccination_data(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Vaccination Records", font=("Arial", 16)).pack(pady=10)

        # Создаем таблицу
        self.tree = ttk.Treeview(self.root, columns=("ID", "Vaccine Name", "Date Given", "Dose Number"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Vaccine Name", text="Vaccine Name")
        self.tree.heading("Date Given", text="Date Given")
        self.tree.heading("Dose Number", text="Dose Number")

        for vaccine in self.vaccination_data:
            self.tree.insert("", tk.END, values=vaccine)

        self.tree.pack(pady=10)

        tk.Button(self.root, text="Back", command=self.show_patient_screen, font=self.font_style).pack(pady=10)

    def update_vaccination_data(self):
        iin = self.iin_entry.get().strip()
        if not iin:
            messagebox.showerror("Error", "Please enter IIN.")
            return

        conn = sqlite3.connect('vaccination_passport.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, vaccine_name, date_given, dose_number FROM Vaccinations WHERE LOWER(iin) = LOWER(?)", (iin,))
        self.vaccination_data = cursor.fetchall()
        conn.close()

        if self.vaccination_data:
            self.show_update_vaccination_screen()
        else:
            messagebox.showinfo("Info", "No vaccination records found for this patient.")

    def show_update_vaccination_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Update Vaccination Record", font=("Arial", 16)).pack(pady=10)

        self.update_tree = ttk.Treeview(self.root, columns=("ID", "Vaccine Name", "Date Given", "Dose Number"), show='headings')
        self.update_tree.heading("ID", text="ID")
        self.update_tree.heading("Vaccine Name", text="Vaccine Name")
        self.update_tree.heading("Date Given", text="Date Given")
        self.update_tree.heading("Dose Number", text="Dose Number")

        for vaccine in self.vaccination_data:
            self.update_tree.insert("", tk.END, values=vaccine)

        self.update_tree.pack(pady=10)

        tk.Label(self.root, text="Select Record ID to Update", font=self.font_style).pack(pady=5)
        self.record_id_entry = tk.Entry(self.root, font=self.font_style)
        self.record_id_entry.pack(pady=5)

        tk.Button(self.root, text="Update", command=self.perform_update, font=self.font_style).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_patient_screen, font=self.font_style).pack(pady=5)

    def perform_update(self):
        record_id = self.record_id_entry.get().strip()
        if not record_id:
            messagebox.showerror("Error", "Please enter Record ID.")
            return

        conn = sqlite3.connect('vaccination_passport.db')
        cursor = conn.cursor()

        # Получаем новые данные из таблицы
        selected_item = self.update_tree.selection()
        if selected_item:
            vaccine_data = self.update_tree.item(selected_item, 'values')
            # Обновляем данные, например, изменим имя вакцины
            new_vaccine_name = self.vaccine_name_entry.get().strip()
            new_date_given = self.date_given_entry.get().strip()
            new_dose_number = self.dose_number_entry.get().strip()

            cursor.execute("UPDATE Vaccinations SET vaccine_name=?, date_given=?, dose_number=? WHERE id=?",
                           (new_vaccine_name, new_date_given, int(new_dose_number), record_id))
            conn.commit()
            messagebox.showinfo("Success", "Vaccination record updated successfully.")
        else:
            messagebox.showerror("Error", "No record selected for update.")

        conn.close()
        self.show_patient_screen()

if __name__ == "__main__":
    root = tk.Tk()
    app = VaccinationApp(root)
    root.mainloop()
