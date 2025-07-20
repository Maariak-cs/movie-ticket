# 🎟️ NEWERA Movie Booking System

A GUI-based movie ticket booking system built using Python and Tkinter, integrated with a MySQL database for storing and managing bookings.

---

## ✨ Features
* Book movie tickets across major Indian cities.
* Choose from various cinemas, movies, dates, and showtimes.
* Select seat types: Classic, Prime, Recliner.
* Payment simulation with validation for user details.
* Modify existing bookings (add tickets or change date/time).
* Cancel existing bookings with confirmation.

---

## 🛠️ Technologies Used
* **Python** (Tkinter for GUI)
* **MySQL** (for storing bookings)
* **Regex** (for input validation)

---

## 💾 Database Setup
Ensure you have MySQL installed and running.
1. Create a user with appropriate privileges, or use `root` (default in code).
2. The database `MOVIEBOOKING` and required table `MOVIEBOOKINGS` will be created automatically when the app starts.

The GUI window will launch with options to:
Book Tickets
Add Tickets to Existing Booking
Cancel Booking

---

## 📋 Input Validations
Name: Alphabetical characters and spaces only.
Mobile Number: Must be exactly 10 digits.
Credit Card Number: Must be exactly 16 digits (no real payment processing is done).

---

## 📸 GUI Preview
The app provides a multi-window interface to guide the user through:
City ➝ Cinema ➝ Movie ➝ Date ➝ Time ➝ Seat Type ➝ Seat Selection ➝ Payment

---

## ❗ Notes
This project simulates a booking environment. No actual payment gateway is used.
All bookings are stored in a local MySQL database.
Error messages and confirmations are shown via tkinter.messagebox.

---

## 📦 Future Improvements
Store individual seat numbers in the database.
Add email confirmations.
Integrate real payment gateway APIs.
Include seat availability tracking.

---

## 🙋‍♀️ Author
Maaria Khan
Final Year Computer Science Engineering Student
🔗www.linkedin.com/in/maariak-cs



