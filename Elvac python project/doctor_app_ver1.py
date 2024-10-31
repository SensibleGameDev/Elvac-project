import tkinter as tk
from tkinter import messagebox
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
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Vaccinations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                iin TEXT NOT NULL,
                vaccine_name TEXT NOT NULL,
                date_given DATE NOT NULL,
                dose_number INTEGER NOT NULL
            )
        ''')
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

        self.vaccine_entries = []
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
        cursor.execute("""
            INSERT INTO Vaccinations (iin, vaccine_name, date_given, dose_number)
            VALUES (?, ?, ?, ?)
        """, (iin, vaccine_name, date_given, int(dose_number)))
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
        cursor.execute("SELECT vaccine_name, date_given, dose_number FROM Vaccinations WHERE LOWER(iin) = LOWER(?)", (iin,))
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

        for vaccine in self.vaccination_data:
            tk.Label(self.root, text=f"Vaccine Name: {vaccine[0]}, Date Given: {vaccine[1]}, Dose Number: {vaccine[2]}", font=self.font_style).pack(pady=5)

        tk.Button(self.root, text="Back", command=self.show_patient_screen, font=self.font_style).pack(pady=10)

    def update_vaccination_data(self):
        iin = self.iin_entry.get().strip()
        if not iin:
            messagebox.showerror("Error", "Please enter IIN.")
            return

        conn = sqlite3.connect('vaccination_passport.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Vaccinations WHERE LOWER(iin) = LOWER(?)", (iin,))
        self.vaccination_data = cursor.fetchall()
        
        if not self.vaccination_data:
            messagebox.showinfo("Info", "No vaccination records found to update.")
            conn.close()
            return

        self.vaccine_entries = []
        for record in self.vaccination_data:
            frame = tk.Frame(self.root)
            frame.pack(pady=5)
            vaccine_name = tk.StringVar(value=record[1])
            date_given = tk.StringVar(value=record[2])
            dose_number = tk.StringVar(value=record[3])

            tk.Label(frame, text="Vaccine Name", font=self.font_style).pack(side=tk.LEFT)
            entry_name = tk.Entry(frame, textvariable=vaccine_name, font=self.font_style)
            entry_name.pack(side=tk.LEFT)

            tk.Label(frame, text="Date Given", font=self.font_style).pack(side=tk.LEFT)
            entry_date = tk.Entry(frame, textvariable=date_given, font=self.font_style)
            entry_date.pack(side=tk.LEFT)

            tk.Label(frame, text="Dose Number", font=self.font_style).pack(side=tk.LEFT)
            entry_dose = tk.Entry(frame, textvariable=dose_number, font=self.font_style)
            entry_dose.pack(side=tk.LEFT)

            self.vaccine_entries.append((entry_name, entry_date, entry_dose))

        tk.Button(self.root, text="Update Records", command=self.update_records, font=self.font_style).pack(pady=10)
    def update_records(self):
            iin = self.iin_entry.get().strip()
            if not iin:
                messagebox.showerror("Error", "Please enter IIN.")
                return

            conn = sqlite3.connect('vaccination_passport.db')
            cursor = conn.cursor()

            for idx, entry in enumerate(self.vaccine_entries):
                name, date, dose = entry
                record_id = self.vaccination_data[idx][0]  # Извлекаем ID записи из данных

                cursor.execute("""
                    UPDATE Vaccinations 
                    SET vaccine_name = ?, date_given = ?, dose_number = ? 
                    WHERE id = ?
                """, (name.get(), date.get(), dose.get(), record_id))

            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Vaccination records updated successfully.")
            self.show_patient_screen()

if __name__ == "__main__":
    root = tk.Tk()
    app = VaccinationApp(root)
    root.geometry("600x400")
    root.mainloop()
