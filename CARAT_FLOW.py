"""
CARATFLOW JEWELRY BILLING SYSTEM

Discount Structure:
- Male >= 65: 20% (2L-3L), 30% (3L-5L), 35% (>5L)
- Male < 65:  10% (2L-3L), 20% (3L-5L), 25% (>5L)
- Female >= 65: 25% (2L-3L), 35% (3L-5L), 40% (>5L)
- Female < 65:  15% (2L-3L), 25% (3L-5L), 35% (>5L)
"""

from dataclasses import dataclass
from typing import List
from enum import Enum


class Gender(Enum):
    """Enum for gender types"""
    MALE = 'm'
    FEMALE = 'f'


@dataclass
class Product:
    """Represents a jewelry product"""
    name: str
    weight_grams: float
    
    def calculate_gold_price(self, price_per_gram: float) -> float:
        """Calculate total gold price for this product"""
        return self.weight_grams * price_per_gram
    
    def calculate_making_charges(self, charges_per_gram: float) -> float:
        """Calculate total making charges for this product"""
        return self.weight_grams * charges_per_gram


@dataclass
class Customer:
    """Represents a customer"""
    name: str
    gender: Gender
    age: int
    
    def is_senior(self) -> bool:
        """Check if customer is a senior citizen (>= 65)"""
        return self.age >= 65


class DiscountCalculator:
    """Handles discount calculation based on customer profile and purchase amount"""
    
    # Discount structure: {gender: {is_senior: [(min_amount, max_amount, discount_percent)]}}
    DISCOUNT_RULES = {
        Gender.MALE: {
            True: [  # Senior Male
                (200000, 300000, 20),
                (300000, 500000, 30),
                (500000, float('inf'), 35)
            ],
            False: [  # Non-senior Male
                (200000, 300000, 10),
                (300000, 500000, 20),
                (500000, float('inf'), 25)
            ]
        },
        Gender.FEMALE: {
            True: [  # Senior Female
                (200000, 300000, 25),
                (300000, 500000, 35),
                (500000, float('inf'), 40)
            ],
            False: [  # Non-senior Female
                (200000, 300000, 15),
                (300000, 500000, 25),
                (500000, float('inf'), 35)
            ]
        }
    }
    
    @classmethod
    def calculate_discount(cls, customer: Customer, total_amount: float) -> float:
        """Calculate discount percentage based on customer and amount"""
        rules = cls.DISCOUNT_RULES[customer.gender][customer.is_senior()]
        
        for min_amt, max_amt, discount in rules:
            if min_amt <= total_amount <= max_amt:
                return discount
        return 0


class Bill:
    """Represents a jewelry bill"""
    
    def __init__(self, customer: Customer, products: List[Product], 
                 gold_price_per_gram: float, making_charges_per_gram: float):
        self.customer = customer
        self.products = products
        self.gold_price_per_gram = gold_price_per_gram
        self.making_charges_per_gram = making_charges_per_gram
        
    @property
    def total_gold_price(self) -> float:
        """Calculate total gold price for all products"""
        return sum(p.calculate_gold_price(self.gold_price_per_gram) 
                   for p in self.products)
    
    @property
    def total_making_charges(self) -> float:
        """Calculate total making charges for all products"""
        return sum(p.calculate_making_charges(self.making_charges_per_gram) 
                   for p in self.products)
    
    @property
    def subtotal(self) -> float:
        """Calculate subtotal (gold + making charges)"""
        return self.total_gold_price + self.total_making_charges
    
    @property
    def discount_percentage(self) -> float:
        """Get applicable discount percentage"""
        return DiscountCalculator.calculate_discount(self.customer, self.subtotal)
    
    @property
    def discount_amount(self) -> float:
        """Calculate discount amount"""
        return (self.subtotal * self.discount_percentage) / 100
    
    @property
    def net_payable(self) -> float:
        """Calculate final payable amount"""
        return self.subtotal - self.discount_amount
    
    def print_bill(self):
        """Print formatted bill"""
        print("\n" + "=" * 50)
        print("          CARATFLOW JEWELRY BILL")
        print("=" * 50)
        print(f"Customer Name        : {self.customer.name}")
        print(f"Gender               : {'Male' if self.customer.gender == Gender.MALE else 'Female'}")
        print(f"Age                  : {self.customer.age}")
        print("-" * 50)
        print(f"Total Gold Price     : ₹{self.total_gold_price:,.2f}")
        print(f"Total Making Charges : ₹{self.total_making_charges:,.2f}")
        print("-" * 50)
        print(f"Total Amount         : ₹{self.subtotal:,.2f}")
        print(f"Discount Applied     : {self.discount_percentage}%")
        print(f"Discount Amount      : ₹{self.discount_amount:,.2f}")
        print("-" * 50)
        print(f"Net Payable Amount   : ₹{self.net_payable:,.2f}")
        print("=" * 50)
        print("      Thank You for Shopping With CaratFlow!")
        print("=" * 50)


class JewelryBillingSystem:
    """Main billing system application"""
    
    def __init__(self, gold_price: float = 12000, making_charges: float = 1000):
        self.gold_price_per_gram = gold_price
        self.making_charges_per_gram = making_charges
    
    def get_customer_details(self) -> Customer:
        """Get customer information from user input"""
        print("\n" + "=" * 50)
        print("    CARATFLOW JEWELRY BILLING SYSTEM")
        print("=" * 50)
        
        name = input("Enter Customer Name : ").strip()
        
        while True:
            gender_input = input("Enter Gender (M/F) : ").strip().lower()
            if gender_input in ['m', 'f']:
                gender = Gender.MALE if gender_input == 'm' else Gender.FEMALE
                break
            print("Invalid input! Please enter 'M' or 'F'.")
        
        while True:
            try:
                age = int(input("Enter Customer Age : "))
                if age > 0:
                    break
                print("Age must be positive!")
            except ValueError:
                print("Invalid input! Please enter a valid number.")
        
        return Customer(name, gender, age)
    
    def get_products(self) -> List[Product]:
        """Get product details from user input"""
        products = []
        
        while True:
            print("\n--- Add Product ---")
            product_name = input("Enter Product Name : ").strip()
            
            while True:
                try:
                    weight = float(input("Enter Gold Weight (grams) : "))
                    if weight > 0:
                        break
                    print("Weight must be positive!")
                except ValueError:
                    print("Invalid input! Please enter a valid number.")
            
            products.append(Product(product_name, weight))
            
            add_more = input("Add another product? (yes/no) : ").strip().lower()
            if add_more != 'yes':
                break
        
        return products
    
    def run(self):
        """Run the billing system"""
        customer = self.get_customer_details()
        products = self.get_products()
        
        bill = Bill(customer, products, self.gold_price_per_gram, 
                    self.making_charges_per_gram)
        bill.print_bill()


def main():
    """Main entry point"""
    system = JewelryBillingSystem()
    system.run()


if __name__ == "__main__":
    main()
