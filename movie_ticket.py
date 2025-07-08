import mysql.connector
from datetime import date, timedelta
import tkinter as tk
from tkinter import ttk, messagebox
import re

class MovieBookingSystem:
    def __init__(self):
        self.db = self.connect_to_database()
        self.cursor = self.db.cursor()
        self.initialize_database()
        self.cost = 0
        self.food_items = []
        self.movie = None
        self.cinema = None
        self.date = None
        self.time = None
        self.seat_type = None
        self.selected_seats = []

    def connect_to_database(self):
        try:
            return mysql.connector.connect(
                host='localhost',
                user='root',
                password='maariakh',
                auth_plugin='mysql_native_password'
            )
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            exit(1)

    def initialize_database(self):
        self.cursor.execute('CREATE DATABASE IF NOT EXISTS MOVIEBOOKING;')
        self.cursor.execute('USE MOVIEBOOKING;')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS MOVIEBOOKINGS (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                NAME VARCHAR(30),
                MOBILENUMBER VARCHAR(20),
                MOVIE VARCHAR(50),
                CINEMA VARCHAR(40),
                DATE_SELECTED DATE,
                SHOWTIME VARCHAR(20),
                SEAT_TYPE VARCHAR(30),
                QUANTITY INT,
                TOTAL_COST DECIMAL(10, 2)
            );
        ''')
        self.db.commit()

    def create_main_window(self):
        self.root = tk.Tk()
        self.root.geometry('800x600')
        self.root.title('NEWERA BOOKINGS')
        self.root.configure(background='orange')

        tk.Label(self.root,
                text='WELCOME TO NEWERA BOOKINGS',
                font=('Bauhaus 93', 30),
                bg='orange').pack(pady=20)

        tk.Button(self.root,
                  text='BOOK TICKETS', 
                  bg='yellow', 
                  font=('Arial', 15), 
                  command=self.booking_window).pack(pady=10)

        tk.Button(self.root, 
                text='ADD TICKETS',
                bg='blue',
                font=('Arial', 15),
                command=self.update_booking_window).pack(pady=10)
 
        tk.Button(self.root,
                text='CANCEL BOOKING',
                bg='red',
                font=('Arial', 15),
                command=self.cancel_booking_window).pack(pady=10)

        self.root.mainloop()

    def booking_window(self):
        booking_window = tk.Toplevel(self.root)
        booking_window.geometry('700x500')
        booking_window.title('MOVIE BOOKING')
        booking_window.configure(background='black')

        cities = ["BANGALORE", "DELHI", "CHENNAI", "MUMBAI", "HYDERABAD", "KOLKATA"]
        
        tk.Label(booking_window,
                text="CHOOSE YOUR CITY",
                bg='black',
                fg='white').grid(row=0, column=0, pady=10, padx=10)

        city_box = ttk.Combobox(
            booking_window,
            values=cities
        )
 
        city_box.grid(
            row=0,
            column=1,
            pady=10,
            padx=10
        )
        city_box.set("Select a city")

        tk.Button(
            booking_window,
            text='SUBMIT',
            command=lambda: self.select_cinema(booking_window, city_box.get())).grid(row=0, column=2, pady=10, padx=10)

    def select_cinema(self, window, city):

        cinemas = {
            "BANGALORE": ['Mantri Square', 'Gopalan Arena', 'PVR ORION', 'PHEONIX GRAND'],
            "DELHI": ['INOX CITY CENTRE', 'Inox GATEWAY MALL', 'PVR SQAURE ARENA', 'MADAN CINEMAS'],
            "MUMBAI": ['Viviana Mall', 'Bachchan Mall', 'PVR Malaad', 'Kasturba Fun Cinemas'],
            "KOLKATA": ['Inox HURIA MALL', 'PVR YEZHINU ROAD', 'NAGESH ARENA PVT', 'CHATERJEE SHOWS ARENA'],
            "CHENNAI": ['MARIS CINEMAS', 'CHENNAI SPENZER MALL', 'PVR AMPA SKYWALK', 'Inox T NAGAR COMPLEX'],
            "HYDERABAD": ['INOX KACHIBOWLI', 'PVR RAMOJI CITY', 'Inox GALERO MALL', 'HINDUJA Theatre']
        }

        tk.Label(window, text="CHOOSE YOUR CINEMA", bg='black', fg='white').grid(row=1, column=0, pady=10, padx=10)
        cinema_box = ttk.Combobox(window, values=cinemas[city])
        cinema_box.grid(row=1, column=1, pady=10, padx=10)
        cinema_box.set("Select a cinema")

        tk.Button(window, text='SUBMIT', command=lambda: self.select_movie(window, cinema_box.get())).grid(row=1, column=2, pady=10, padx=10)

    def select_movie(self, window, cinema):
        self.cinema = cinema
        movies = [
            'BEAST', 'MASTER', 'JAI BHIM', 'SOORARAI POTTRU', 'MAHAAN', 'ASURAN', '3', '24',
            '83', 'MS DHONI THE UNTOLD STORY', 'BEAUTY AND THE BEAST', 'PUSHPA', 'ARJUN REDDY',
            'SURYAVANSHI', 'RACE', 'KIRIK PARTY', 'ONE CUT TWO CUT', 'HUMSAFR',
            'SPIDERMAN FAR FROM HOME', 'SINGHAM', 'VIP 2', 'ANNATTHE', 'VIKRAM'
        ]

        tk.Label(window, text="CHOOSE YOUR MOVIE", bg='black', fg='white').grid(row=2, column=0, pady=10, padx=10)
        movie_box = ttk.Combobox(window, values=movies)
        movie_box.grid(row=2, column=1, pady=10, padx=10)
        movie_box.set("Select a movie")

        tk.Button(window, text='SUBMIT', command=lambda: self.select_date(window, movie_box.get())).grid(row=2, column=2, pady=10, padx=10)

    def select_date(self, window, movie):
        self.movie = movie
        dates = [date.today() + timedelta(days=i) for i in range(4)]
        date_strings = [d.strftime("%Y-%m-%d") for d in dates]

        tk.Label(window, text="CHOOSE DATE", bg='black', fg='white').grid(row=3, column=0, pady=10, padx=10)
        date_box = ttk.Combobox(window, values=date_strings)
        date_box.grid(row=3, column=1, pady=10, padx=10)
        date_box.set("Select a date")

        tk.Button(window, text='SUBMIT', command=lambda: self.select_time(window, date_box.get())).grid(row=3, column=2, pady=10, padx=10)

    def select_time(self, window, date):
        self.date = date
        times = ['10:40 AM', '12:45 PM', '03:55 PM', '07:45 PM', '09:55 PM', '12:30 AM']

        tk.Label(window, text="CHOOSE SHOWTIME", bg='black', fg='white').grid(row=4, column=0, pady=10, padx=10)
        time_box = ttk.Combobox(window, values=times)
        time_box.grid(row=4, column=1, pady=10, padx=10)
        time_box.set("Select a time")

        tk.Button(window, text='SUBMIT', command=lambda: self.select_seat_type(window, time_box.get())).grid(row=4, column=2, pady=10, padx=10)

    def select_seat_type(self, window, time):
        self.time = time
        seat_types = ['CLASSIC Rs.250', 'PRIME Rs.300', 'RECLINER Rs.460']

        tk.Label(window, text="CHOOSE SEAT TYPE", bg='black', fg='white').grid(row=5, column=0, pady=10, padx=10)
        seat_type_box = ttk.Combobox(window, values=seat_types)
        seat_type_box.grid(row=5, column=1, pady=10, padx=10)
        seat_type_box.set("Select seat type")

        tk.Button(window, text='SUBMIT', command=lambda: self.select_seats(window, seat_type_box.get())).grid(row=5, column=2, pady=10, padx=10)

    def select_seats(self, window, seat_type):
        self.seat_type = seat_type.split()[0]
        seat_window = tk.Toplevel(window)
        seat_window.geometry('600x400')
        seat_window.title('Select Seats')

        seats = self.generate_seats(self.seat_type)

        tk.Label(seat_window, text="SCREEN", bg='gray', fg='white', width=50).pack(pady=20)

        seat_frame = tk.Frame(seat_window)
        seat_frame.pack(pady=20)

        self.selected_seats = []

        for i, seat in enumerate(seats):
            btn = tk.Button(seat_frame, text=seat, width=3, command=lambda s=seat: self.toggle_seat(s))
            btn.grid(row=i//10, column=i%10, padx=2, pady=2)

        tk.Button(seat_window, text='CONFIRM SEATS', command=lambda: self.confirm_booking(seat_window, self.seat_type)).pack(pady=20)

    def generate_seats(self, seat_type):
        if seat_type == 'CLASSIC':
            return [f"{chr(i)}{j}" for i in range(65, 69) for j in range(1, 11)]
        elif seat_type == 'PRIME':
            return [f"{chr(i)}{j}" for i in range(69, 73) for j in range(1, 11)]
        else:  # RECLINER
            return [f"{chr(i)}{j}" for i in range(73, 74) for j in range(1, 11)]

    def toggle_seat(self, seat):
        if seat in self.selected_seats:
            self.selected_seats.remove(seat)
            # Update button color (you might need to store button references)
        else:
            self.selected_seats.append(seat)
            # Update button color

    def confirm_booking(self, window, seat_type):
        if not self.selected_seats:
            messagebox.showerror("Error", "Please select at least one seat.")
            return

        price = {'CLASSIC': 250, 'PRIME': 300, 'RECLINER': 460}
        total_cost = len(self.selected_seats) * price[seat_type]

        confirm = messagebox.askyesno("Confirm Booking", f"Total cost: Rs.{total_cost}\nDo you want to proceed?")
        if confirm:
            self.process_payment(window, total_cost)

    def process_payment(self, window, amount):
        payment_window = tk.Toplevel(window)
        payment_window.geometry('400x300')
        payment_window.title('Payment')

        tk.Label(payment_window, text=f"Total Amount: Rs.{amount}").pack(pady=10)

        tk.Label(payment_window, text="Name:").pack(pady=5)
        name_entry = tk.Entry(payment_window)
        name_entry.pack(pady=5)

        tk.Label(payment_window, text="Mobile Number:").pack(pady=5)
        mobile_entry = tk.Entry(payment_window)
        mobile_entry.pack(pady=5)

        tk.Label(payment_window, text="Credit Card Number:").pack(pady=5)
        card_entry = tk.Entry(payment_window)
        card_entry.pack(pady=5)

        tk.Button(payment_window, text="Pay", command=lambda: self.complete_booking(
            payment_window, name_entry.get(), mobile_entry.get(), card_entry.get(), amount
        )).pack(pady=20)

    def complete_booking(self, window, name, mobile, card, amount):
        card = card.replace(' ','')
        if not self.validate_inputs(name, mobile, card):
            messagebox.showerror("Error", "Please enter valid details.")
            return

        try:
            self.cursor.execute('''
                INSERT INTO MOVIEBOOKINGS (NAME, MOBILENUMBER, MOVIE, CINEMA, DATE_SELECTED, SHOWTIME, SEAT_TYPE, QUANTITY, TOTAL_COST)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (name, mobile, self.movie, self.cinema, self.date, self.time, self.seat_type, len(self.selected_seats), amount))
            self.db.commit()
            messagebox.showinfo("Success", "Booking completed successfully!")
            window.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"An error occurred: {err}")

    def validate_inputs(self, name, mobile, card):
        if not name or not re.match(r'^[A-Za-z\s]+$', name):
            return False
        if not mobile or not re.match(r'^\d{10}$', mobile):
            return False
        if not card or not re.match(r'^\d{16}$', card):
            return False
        return True

    def update_booking_window(self):
        update_window = tk.Toplevel(self.root)
        update_window.geometry('400x200')
        update_window.title('Update Booking')

        tk.Label(update_window, text="Enter your name:").pack(pady=10)
        name_entry = tk.Entry(update_window)
        name_entry.pack(pady=5)

        tk.Button(update_window, text="Search", command=lambda: self.search_booking(update_window, name_entry.get())).pack(pady=20)

    def search_booking(self, window, name):
        try:
            self.cursor.execute('SELECT * FROM MOVIEBOOKINGS WHERE NAME = %s', (name,))
            booking = self.cursor.fetchone()
            print(booking)
            if booking:
                self.show_update_options(window, booking)
            else:
                messagebox.showerror("Error", "No booking found with that name.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"An error occurred: {err}")

    def show_update_options(self, window, booking):
        update_options = tk.Toplevel(window)
        update_options.geometry('400x300')
        update_options.title('Update Options')

        tk.Label(update_options, text=f"Current booking: {booking[3]} at {booking[4]}").pack(pady=10)
        tk.Label(update_options, text=f"Current seats: {booking[7]}").pack(pady=5)

        tk.Button(update_options, text="Add Tickets", command=lambda: self.add_tickets(update_options, booking)).pack(pady=10)
        tk.Button(update_options, text="Change Date/Time", command=lambda: self.change_datetime(update_options, booking)).pack(pady=10)

    def add_tickets(self, window, booking):
        add_window = tk.Toplevel(window)
        add_window.geometry('300x200')
        add_window.title('Add Tickets')

        tk.Label(add_window, text="Number of tickets to add:").pack(pady=10)
        ticket_entry = tk.Entry(add_window)
        ticket_entry.pack(pady=5)

        tk.Button(add_window, text="Confirm", command=lambda: self.process_ticket_addition(add_window, booking, ticket_entry.get())).pack(pady=20)

    def process_ticket_addition(self, window, booking, additional_tickets):
        try:
            additional_tickets = int(additional_tickets)
            if additional_tickets <= 0:
                raise ValueError("Number of tickets must be positive")

            new_quantity = int(booking[7]) + int(additional_tickets)
            new_cost = int(booking[8]) + (additional_tickets * (int(booking[8]) / int(booking[7])))  # Assuming same price per ticket

            self.cursor.execute('''
                UPDATE MOVIEBOOKINGS 
                SET QUANTITY = %s, TOTAL_COST = %s 
                WHERE NAME = %s
            ''', (new_quantity, new_cost, booking[0]))
            self.db.commit()

            messagebox.showinfo("Success", f"Added {additional_tickets} tickets. New total: {new_quantity}")
            window.destroy()

        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"An error occurred: {err}")

    def change_datetime(self, window, booking):
        change_window = tk.Toplevel(window)
        change_window.geometry('400x300')
        change_window.title('Change Date/Time')

        dates = [date.today() + timedelta(days=i) for i in range(7)]
        date_strings = [d.strftime("%Y-%m-%d") for d in dates]

        tk.Label(change_window, text="New Date:").pack(pady=5)
        date_box = ttk.Combobox(change_window, values=date_strings)
        date_box.pack(pady=5)

        times = ['10:40 AM', '12:45 PM', '03:55 PM', '07:45 PM', '09:55 PM', '12:30 AM']
        
        tk.Label(change_window, text="New Time:").pack(pady=5)
        time_box = ttk.Combobox(change_window, values=times)
        time_box.pack(pady=5)

        tk.Button(change_window, text="Confirm", command=lambda: self.process_datetime_change(
            change_window, booking, date_box.get(), time_box.get()
        )).pack(pady=20)

    def process_datetime_change(self, window, booking, new_date, new_time):
        if not new_date or not new_time:
            messagebox.showerror("Error", "Please select both date and time")
            return

        try:
            self.cursor.execute('''
                UPDATE MOVIEBOOKINGS 
                SET DATE_SELECTED = %s, SHOWTIME = %s 
                WHERE NAME = %s
            ''', (new_date, new_time, booking[0]))
            self.db.commit()

            messagebox.showinfo("Success", f"Booking updated to {new_date} at {new_time}")
            window.destroy()

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"An error occurred: {err}")

    def cancel_booking_window(self):
        cancel_window = tk.Toplevel(self.root)
        cancel_window.geometry('400x200')
        cancel_window.title('Cancel Booking')

        tk.Label(cancel_window, text="Enter your name:").pack(pady=10)
        name_entry = tk.Entry(cancel_window)
        name_entry.pack(pady=5)

        tk.Button(cancel_window, text="Search", command=lambda: self.search_for_cancellation(cancel_window, name_entry.get())).pack(pady=20)

    def search_for_cancellation(self, window, name):
        try:
            self.cursor.execute('SELECT * FROM MOVIEBOOKINGS WHERE NAME = %s', (name,))
            booking = self.cursor.fetchone()
            if booking:
                self.confirm_cancellation(window, booking)
            else:
                messagebox.showerror("Error", "No booking found with that name.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"An error occurred: {err}")

    def confirm_cancellation(self, window, booking):
        confirm_window = tk.Toplevel(window)
        confirm_window.geometry('400x300')
        confirm_window.title('Confirm Cancellation')

        tk.Label(confirm_window, text=f"Booking details:").pack(pady=10)
        tk.Label(confirm_window, text=f"Movie: {booking[3]}").pack(pady=5)
        tk.Label(confirm_window, text=f"Cinema: {booking[4]}").pack(pady=5)
        tk.Label(confirm_window, text=f"Date: {booking[5]}").pack(pady=5)
        tk.Label(confirm_window, text=f"Time: {booking[6]}").pack(pady=5)
        tk.Label(confirm_window, text=f"Seats: {booking[7]}").pack(pady=5)

        tk.Label(confirm_window, text="Are you sure you want to cancel this booking?").pack(pady=10)
        
        tk.Button(confirm_window, text="Yes, Cancel", command=lambda: self.process_cancellation(confirm_window, booking[0])).pack(pady=10)
        tk.Button(confirm_window, text="No, Keep Booking", command=confirm_window.destroy).pack(pady=10)

    def process_cancellation(self, window, booking_id):
        try:
            self.cursor.execute('DELETE FROM MOVIEBOOKINGS WHERE NAME = %s', (booking_id,))
            self.db.commit()
            messagebox.showinfo("Success", "Your booking has been cancelled successfully")
            window.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"An error occurred: {err}")

    def run(self):
        self.create_main_window()

if __name__ == "__main__":
    booking_system = MovieBookingSystem()
    booking_system.run()
