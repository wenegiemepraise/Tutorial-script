# Import required libraries

import sqlite3 # # for database operations
import tkinter as tk # For creating the GUI
from tkinter import ttk, messagebox # ttk is a modern GUI widget library (for more modern-looking widgets)

# Define Car class

class Car:
    # initialising  a new instance of the car class (declaring attributes of car)
    def __init__(self, id, make, model, engine_capacity, top_speed, price):
        self.id = id
        self.make = make
        self.model = model
        self.engine_capacity = engine_capacity
        self.top_speed = top_speed
        self.price = price

    # String representation of the car
    def __str__(self):
        return f"ID: {self.id}, Make: {self.make}, Model: {self.model}, Engine Capacity: {self.engine_capacity}, Top Speed: {self.top_speed} km/h, Price: €{self.price}"

    # calls the string representation above
    def __repr__(self):
        return str(self)


# Define the DAO class (Data Access Object)
class CarDao:

    # Constructor and destructor
    # (This is our CONSTRUCTOR)
    def __init__(self):
        self.connection = sqlite3.connect("cars.db") # Connect to SQLite database
        # The cursor is necessary to execute SQL statements and handle the results of queries.
        self.cursor = self.connection.cursor() # Create a cursor for executing SQL commands
        # Three quotation marks is for multi-line strings
        # here we create the car database table, if it does not already exist
        # we also give the table its column names and data types
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS car (
            id INTEGER PRIMARY KEY,
            make TEXT,
            model TEXT,
            engine_capacity FLOAT,
            top_speed INTEGER,
            price INTEGER
            )""")

    # we need to close the connection when an instance is destroyed so that the database does not remain locked
    # When the database is locked no other instances can access it until it is unlocked
    # (This is our DESTRUCTOR)
    def __del__(self):
        self.connection.close()

    # CRUD operations

    # CREATE operation - adds a car to the database
    def addCar(self, car):
        # SQL insert statement (question marks represent unknown variables -
        # placeholders, id is NULL because the ID will be Auto-Incremented)
        sql = ("INSERT INTO car VALUES(NULL, ?, ?, ?, ?, ?)")
        # Arguments for SQL statement
        args = (car.make, car.model, car.engine_capacity, car.top_speed, car.price)
        self.cursor.execute(sql, args)  # Execute SQL with arguments
        self.connection.commit()  # Commit the transaction to save changes

        # Retrieve the last inserted ID and update the car's ID
        car.id = self.cursor.lastrowid

        # READ operation - retrieves a specific car by id

    def getCar(self, id):
        sql = "SELECT * FROM car WHERE id = ?"
        args = (str(id),)  # ID of the car to retrieve
        row = self.cursor.execute(sql, args).fetchall()[0]  # Fetch the first matching result
        # Return Car object with data
        return Car(row[0], row[1], row[2], row[3], row[4], row[5])

        # Retrieves all cars from the database

    def getAllCars(self):
        cars = []  # List to store Car objects
        rows = self.cursor.execute("SELECT * FROM car").fetchall()  # Fetch all rows from car table
        for row in rows:
            cars.append(Car(row[0], row[1], row[2], row[3], row[4], row[5]))  # Append each row as a Car object
        return cars

        # UPDATE operation - updates a car’s data in the database

    def updateCar(self, car):
        sql = """UPDATE car
        SET make = ?, model = ?, engine_capacity = ?, top_speed = ?, price = ?
        WHERE id = ?"""
        args = (car.make, car.model, car.engine_capacity, car.top_speed, car.price, car.id)
        self.cursor.execute(sql, args)  # Execute SQL with arguments
        self.connection.commit()  # Commit the transaction

        # DELETE operation - deletes a car from the database by id

    def deleteCar(self, id):
        sql = "DELETE FROM car WHERE id = ?"
        args = (str(id),)  # ID of the car to delete
        self.cursor.execute(sql, args)  # Execute SQL with arguments
        self.connection.commit()  # Commit the transaction

    # Define the Tkinter application
class CarShowRoom(tk.Tk):
    # Constructor - initializes the application window and populates the listbox with cars
    def __init__(self):
        super().__init__()
        self.title("Car Showroom App")  # Set window title
        self.geometry("680x400")  # Set window size
        self.myCarDao = CarDao()  # Instantiate CarDao for database operations
        self.buildWidgets()  # Build all the GUI components
        self.allCars = self.myCarDao.getAllCars()  # Retrieve all cars from database
        for car in self.allCars:
            self.listbox.insert(tk.END, str(car))  # Insert each car into the listbox

    # Destructor - deletes the CarDao instance when the window is closed
    def __del__(self):
        del self.myCarDao

    # Method to build the widgets (GUI elements) This method is called in the CarShowRoom constructor method.
    def buildWidgets(self):
        # Entry fields for car details

        # Make entry
        self.make_label = ttk.Label(self, text="Make:")
        self.make_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.make_entry = ttk.Entry(self)
        self.make_entry.grid(row=0, column=1, padx=10, pady=5)

        # Model entry
        self.model_label = ttk.Label(self, text="Model:")
        self.model_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.model_entry = ttk.Entry(self)
        self.model_entry.grid(row=1, column=1, padx=10, pady=5)

        # Engine capacity entry
        self.capacity_label = ttk.Label(self, text="Capacity:")
        self.capacity_label.grid(row=0, column=2, sticky="w", padx=10, pady=5)
        self.capacity_entry = ttk.Entry(self)
        self.capacity_entry.grid(row=0, column=3, padx=10, pady=5)

        # Top speed entry
        self.speed_label = ttk.Label(self, text="Top Speed:")
        self.speed_label.grid(row=1, column=2, sticky="w", padx=10, pady=5)
        self.speed_entry = ttk.Entry(self)
        self.speed_entry.grid(row=1, column=3, padx=10, pady=5)

        # Price entry
        self.price_label = ttk.Label(self, text="Price:")
        self.price_label.grid(row=0, column=4, sticky="w", padx=10, pady=5)
        self.price_entry = ttk.Entry(self)
        self.price_entry.grid(row=0, column=5, padx=10, pady=5)

        # Action buttons

        # Add car button
        self.add_button = ttk.Button(self, text="Add", command=self.add_item)
        self.add_button.grid(row=2, column=0, pady=10)

        # Update car button
        self.update_button = ttk.Button(self, text="Update", command=self.update_item)
        self.update_button.grid(row=2, column=1, pady=10)

        # Delete car button
        self.delete_button = ttk.Button(self, text="Delete", command=self.delete_item)
        self.delete_button.grid(row=2, column=2, pady=10)

        # Listbox to display cars
        self.listbox = tk.Listbox(self, height=15, width=100)
        self.listbox.grid(row=3, column=0, columnspan=6, padx=10, pady=5)
        self.listbox.bind('<<ListboxSelect>>', self.on_listbox_select)  # Bind listbox selection event

    # Actions

    # Add a new car to the database and listbox
    def add_item(self):
        #I added this validation
        # Checl if any netry field is empty
        if not(self.make_entry.get() and self.model_entry.get() and self.capacity_entry.get() and self.speed_entry.get() and self.price_entry.get()):
            messagebox.showerror("Input Error", "All fields are required")
            return #Exit the function if validation fails
        
        car = Car(0, self.make_entry.get(), self.model_entry.get(), float(self.capacity_entry.get()), int(self.speed_entry.get()), int(self.price_entry.get()))

        self.myCarDao.addCar(car)  # Add car to database    
        self.listbox.insert(0, tk.END)
        for car in self.allCars:
            self.listbox.insert(tk.END, str(car))  # Insert each car into the listbox


    def update_item(self):
        selected_index = self.listbox.curselection()  # Get the selected index from the listbox

        if not selected_index:
            messagebox.showerror("Update Error", "Please select a car to update")
            return #Exit the function if validation fails
        
        car.make = self.make_entry.get()
        car.model = self.model_entry.get()
        car.engine_capacity = float(self.capacity_entry.get())
        car.top_speed = int(self.speed_entry.get())
        car.price = int(self.price_entry.get())

        self.myCarDao.updateCar(car)  # Update car in database

        self.allCars = self.myCarDao.getAllCars()  # Retrieve all cars from database

        self.listbox.delete(0, tk.END)  # Clear the listbox
        for car in self.allCars:
            self.listbox.insert(tk.END, str(car))
            
        self.clear_entries()  # Clear the entry fields


    # We need to add functionality to the delete function
    def delete_item(self):
        selected_index = self.listbox.curselection()
        if not selected_index:
            messagebox.showerror("Delete Error", "Please select a car to delete")
            return # Exit the function if validation fails

        car = self.allCars[selected_index[0]]
        self.myCarDao.deleteCar(car.id)  # Delete car from database

        self.allCars = self.myCarDao.getAllCars()  # Retrieve all cars from database

        self.listbox.delete(0, tk.END)  # Clear the listbox
        for car in self.allCars:
            self.listbox.insert(tk.END, str(car))  # Insert each car into the listbox

        self.clear_entries()  # Clear the entry fields

    # Event handler for listbox selection, fills entries with selected car's details
    def on_listbox_select(self, event):
        selected_index = self.listbox.curselection()
        if not selected_index:
            return # Exit the function if no selection

        car = self.allCars[selected_index[0]]
        self.make_entry.delete(0, tk.END)
        self.make_entry.insert(0, car.make)
        self.model_entry.delete(0, tk.END)
        self.model_entry.insert(0, car.model)
        self.capacity_entry.delete(0, tk.END)
        self.capacity_entry.insert(0, car.engine_capacity)
        self.speed_entry.delete(0, tk.END)
        self.speed_entry.insert(0, car.top_speed)
        self.price_entry.delete(0, tk.END)
        self.price_entry.insert(0, car.price)


     # Each delete method call removes the text from the entry field,
    # starting from the first character (index 0) to the end (tk.END)
    def clear_entries(self):
        self.make_entry.delete(0, tk.END)
        self.model_entry.delete(0, tk.END)
        self.capacity_entry.delete(0, tk.END)
        self.speed_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)

# Define main program
if __name__ == "__main__":
    app = CarShowRoom()  # Instantiate and run the app
    app.mainloop()  # Start the main event loop
    del app  # Explicitly delete the app instance when it’s closed