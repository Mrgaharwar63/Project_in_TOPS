"""
PROJECT NAME : Car Rental System (Refactored)
Features:
- Role-based login (Owner / Customer)
- Car management (Add, View, Search, Sort)
- Booking system
- Robust input handling & Clean UI
"""

import time
from dataclasses import dataclass, field
from typing import List, Optional

# --- Data Structures ---

@dataclass
class User:
    username: str
    password: str
    role: str  # 'owner' or 'customer'

@dataclass
class Car:
    model: str
    car_type: str
    rent: int
    city: str
    owner: str
    available: bool = True

@dataclass
class Booking:
    customer: str
    car_model: str
    owner: str
    days: int
    total_cost: int

# --- System Class ---

class Urban_Wheels:
    def __init__(self):
        self.users: List[User] = []
        self.cars: List[Car] = []
        self.bookings: List[Booking] = []
        self.current_user: Optional[User] = None

    # --- Helpers ---

    def clear_screen(self):
        print("\n" * 2) # Simple spacer instead of os.system('cls') for safer portability

    def _get_valid_int(self, prompt: str) -> int:
        """Helper to ensure integer input without crashing."""
        while True:
            try:
                value = input(prompt)
                if int(value) < 0:
                    print("Please enter a positive number.")
                    continue
                return int(value)
            except ValueError:
                print("Invalid input. Please enter a number.")

    def _wait_for_enter(self):
        input("\nPress Enter to continue...")

    # --- Authentication ---

    def register(self):
        self.clear_screen()
        print("=== REGISTRATION ===")
        username = input("Enter username: ").strip()
        if any(u.username == username for u in self.users):
            print("Username already taken!")
            self._wait_for_enter()
            return

        password = input("Enter password: ").strip()
        
        print("\nSelect Role:")
        print("1. Car Owner")
        print("2. Customer")
        while True:
            choice = input("Enter choice (1 or 2): ").strip()
            if choice == '1':
                role = 'owner'
                break
            elif choice == '2':
                role = 'customer'
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")

        self.users.append(User(username, password, role))
        print(f"\nRegistration Successful! You can now login as a {role}.")
        self._wait_for_enter()

    def login(self):
        self.clear_screen()
        print("=== LOGIN ===")
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()

        for user in self.users:
            if user.username == username and user.password == password:
                self.current_user = user
                print(f"\nWelcome back, {user.username}!")
                time.sleep(1)
                return

        print("\nInvalid username or password.")
        self._wait_for_enter()

    def logout(self):
        print(f"Goodbye, {self.current_user.username}!")
        self.current_user = None
        time.sleep(1)

    # --- Owner Features ---

    def owner_menu(self):
        while True:
            self.clear_screen()
            print(f"--- OWNER DASHBOARD ({self.current_user.username}) ---")
            print("1. Add Car for Rental")
            print("2. Check Bookings")
            print("3. Logout")

            choice = input("\nEnter choice: ").strip()

            if choice == '1':
                self.add_car()
            elif choice == '2':
                self.view_owner_bookings()
            elif choice == '3':
                self.logout()
                break
            else:
                print("Invalid choice.")
                time.sleep(0.5)

    def add_car(self):
        self.clear_screen()
        print("--- ADD NEW CAR ---")
        model = input("Car Model (e.g., Toyota Camry): ").strip()
        car_type = input("Car Type (e.g., SUV, Sedan): ").strip()
        rent = self._get_valid_int("Rent per Day: ")
        city = input("City: ").strip()

        new_car = Car(model, car_type, rent, city, self.current_user.username)
        self.cars.append(new_car)
        print(f"\nCar '{model}' added successfully!")
        self._wait_for_enter()

    def view_owner_bookings(self):
        self.clear_screen()
        print("--- MY BOOKINGS ---")
        my_bookings = [b for b in self.bookings if b.owner == self.current_user.username]
        
        if not my_bookings:
            print("No bookings found yet.")
        else:
            for b in my_bookings:
                print(f"Car: {b.car_model:<15} | Customer: {b.customer:<10} | Days: {b.days} | Total: ${b.total_cost}")
        
        self._wait_for_enter()

    # --- Customer Features ---

    def customer_menu(self):
        while True:
            self.clear_screen()
            print(f"--- CUSTOMER DASHBOARD ({self.current_user.username}) ---")
            print("1. View All Cars")
            print("2. Search Cars by City")
            print("3. View Cars by Price (Low to High)")
            print("4. Book a Car")
            print("5. Logout")

            choice = input("\nEnter choice: ").strip()

            if choice == '1':
                self.view_all_cars()
            elif choice == '2':
                self.search_cars_by_city()
            elif choice == '3':
                self.view_cars_by_price()
            elif choice == '4':
                self.book_car()
            elif choice == '5':
                self.logout()
                break
            else:
                print("Invalid choice.")
                time.sleep(0.5)

    def view_all_cars(self, car_list: Optional[List[Car]] = None, title="AVAILABLE CARS"):
        self.clear_screen()
        target_list = car_list if car_list is not None else self.cars
        active_cars = [c for c in target_list if c.available]

        print(f"--- {title} ---")
        if not active_cars:
            print("No cars available at the moment.")
            if car_list is None: # Only wait if we are in the main view mode
                self._wait_for_enter()
            return

        print(f"{'No.':<4} {'Model':<20} {'Type':<10} {'City':<15} {'Rent/Day':<10}")
        print("-" * 65)
        for i, car in enumerate(active_cars, 1):
            print(f"{i:<4} {car.model:<20} {car.car_type:<10} {car.city:<15} ${car.rent:<10}")
        
        if car_list is None: # Only wait if manually viewing
            self._wait_for_enter()

    def search_cars_by_city(self):
        self.clear_screen()
        city_query = input("Enter city to search: ").strip().lower()
        # Filter cars that match city (case-insensitive)
        found_cars = [c for c in self.cars if c.city.lower() == city_query]
        
        if not found_cars:
            print(f"No cars found in '{city_query}'.")
            self._wait_for_enter()
        else:
            self.view_all_cars(found_cars, title=f"CARS IN {city_query.upper()}")

    def view_cars_by_price(self):
        # Sort a copy of the list
        sorted_cars = sorted(self.cars, key=lambda c: c.rent)
        self.view_all_cars(sorted_cars, title="CARS BY PRICE (LOW -> HIGH)")

    def book_car(self):
        # 1. Show available cars
        active_cars = [c for c in self.cars if c.available]
        if not active_cars:
            print("\nNo cars available to book.")
            self._wait_for_enter()
            return
            
        self.view_all_cars(car_list=None, title="SELECT A CAR TO BOOK") # Re-uses view logic simply

        # 2. Select Car
        print("\n(Enter 0 to cancel)")
        choice = self._get_valid_int("Enter the car No. you want to book: ")
        
        if choice == 0:
            return

        if choice < 1 or choice > len(active_cars):
            print("Invalid car number.")
            self._wait_for_enter()
            return

        selected_car = active_cars[choice - 1]

        # 3. Booking Details
        print(f"\nYou selected: {selected_car.model} (${selected_car.rent}/day)")
        days = self._get_valid_int("How many days do you want to rent? ")
        total = selected_car.rent * days

        print(f"\nTotal Bill: ${total}")
        confirm = input("Confirm booking? (yes/no): ").lower()

        if confirm in ['yes', 'y']:
            # Create booking
            booking = Booking(
                customer=self.current_user.username,
                car_model=selected_car.model,
                owner=selected_car.owner,
                days=days,
                total_cost=total
            )
            self.bookings.append(booking)
            
            # Update car availability
            # Note: We need to find the specific car in the main list to update it properly
            # Since objects are references, 'selected_car' points to the same object in self.cars
            selected_car.available = False
            
            print("Booking Successful! Enjoy your ride.")
        else:
            print("Booking Cancelled.")
        
        self._wait_for_enter()

    # --- Main Loop ---

    def run(self):
        while True:
            self.clear_screen()
            print("==============================")
            print("   Urban-Wheels   ")
            print("==============================")
            print("1. Register")
            print("2. Login")
            print("3. Exit")

            choice = input("\nEnter choice: ").strip()

            if choice == '1':
                self.register()
            elif choice == '2':
                self.login()
                if self.current_user:
                    if self.current_user.role == 'owner':
                        self.owner_menu()
                    else:
                        self.customer_menu()
            elif choice == '3':
                print("Thank you for using the system. Goodbye!")
                break
            else:
                print("Invalid input. Try again.")
                time.sleep(0.5)

if __name__ == "__main__":
    app = Urban_Wheels()
    app.run()
