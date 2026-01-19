"""
TASK 3 : mini project : 

KALYAN JEWELLERS : 

M >= 65
purchase > 2lk - 3lk    20% 
purchase > 3lk - 5lk 	30% 
purchase > 5lk  	    35% 

<65
purchase > 2lk - 3lk    10% 
purchase > 3lk - 5lk 	20% 
purchase > 5lk  	    25% 

F >= 65
purchase > 2lk - 3lk    25% 
purchase > 3lk - 5lk 	35% 
purchase > 5lk  	    40% 

<65
purchase > 2lk - 3lk    15% 
purchase > 3lk - 5lk 	25% 
purchase > 5lk  	    30% 
------------------------------------------------------------
Enter your name : 
Enter gender : 
Enter age : 
Enter product : Ring 
Enter product gram : 20  
current gold price (1 grm) : 5752
-------------------------------------
TOTAL GOLD RATE :  XXXXX 
Making charges (1 gram)  : 845
Total Making CHarges :    TOTAL GOLD  X  MAKING CHARGES 
---------------------------------------
TOTAL AMOUNT : GOLD PRICE + TOTAL MAKING CHARGE
DISCOUNT :   25 (AUTOMATIC) 
DIS- AMOUNT : except (making charges) 
-----------------------------------------
total net amount : 
--------------------------------------------
HINT : variables , input , conditional statements 
======================================================================================================================================================
"""
print("\n========== CARATFLOW JEWELRY BILLING SYSTEM ==========")

# ------------------ CUSTOMER DETAILS ------------------
name = input("Enter Customer Name : ")
gender = input("Enter Gender (M/F) : ").lower()
age = int(input("Enter Customer Age : "))

# ------------------ PRICE SETUP ------------------
gold_price = 12000
making_charges_per_gram = 1000

grand_gold_price = 0
grand_making_charges = 0

product_status = "yes"

# ------------------ PRODUCT LOOP ------------------
while product_status == "yes":

    print("\n--- Add Product ---")
    product = input("Enter Product Name : ")
    gram = float(input("Enter Gold Weight (grams) : "))

    total_gold_price = gold_price * gram
    total_making_charges = making_charges_per_gram * gram

    grand_gold_price += total_gold_price
    grand_making_charges += total_making_charges

    choice = input("Add another product? (yes/no) : ").lower()
    if choice != "yes":
        product_status = "no"

# ------------------ FINAL AMOUNT ------------------
total_amount = grand_gold_price + grand_making_charges
discount = 0

# ------------------ DISCOUNT LOGIC ------------------
if gender == "m":
    if age >= 65:
        if 200000 <= total_amount <= 300000:
            discount = 20
        elif 300000 < total_amount <= 500000:
            discount = 30
        elif total_amount > 500000:
            discount = 35
    else:
        if 200000 <= total_amount <= 300000:
            discount = 10
        elif 300000 < total_amount <= 500000:
            discount = 20
        elif total_amount > 500000:
            discount = 25

elif gender == "f":
    if age >= 65:
        if 200000 <= total_amount <= 300000:
            discount = 25
        elif 300000 < total_amount <= 500000:
            discount = 35
        elif total_amount > 500000:
            discount = 40
    else:
        if 200000 <= total_amount <= 300000:
            discount = 15
        elif 300000 < total_amount <= 500000:
            discount = 25
        elif total_amount > 500000:
            discount = 35
            
# ------------------ DISCOUNT CALCULATION ------------------
discount_amount = (total_amount * discount) / 100
net_payable = total_amount - discount_amount

# ------------------ BILL OUTPUT ------------------
print("\n==============================================")
print("          CARATFLOW JEWELRY BILL                    ")
print("==============================================")
print(f"Customer Name        : {name}")
print(f"Gender               : {'Male' if gender == 'm' else 'Female'}")
print(f"Age                  : {age}")
print("----------------------------------------------")
print(f"Total Gold Price     : ₹{grand_gold_price:,.2f}")
print(f"Total Making Charges : ₹{grand_making_charges:,.2f}")
print("----------------------------------------------")
print(f"Total Amount         : ₹{total_amount:,.2f}")
print(f"Discount Applied     : {discount}%")
print(f"Discount Amount      : ₹{discount_amount:,.2f}")
print("----------------------------------------------")
print(f"Net Payable Amount   : ₹{net_payable:,.2f}")
print("==============================================")
print("      Thank You for Shopping With CaratFlow!")
print("==============================================")
