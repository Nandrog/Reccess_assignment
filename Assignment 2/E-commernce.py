print("+"*40)
print("Welcome to the E-commerce platform")
print("+"*40)
print("\n")

print("Enter Credentials you would want to use to login to your account")

Reg_username = input("Please enter your desired username: ")
Reg_password = input("Please enter your desired password: ")
Reg_profile = input("Please enter your profile name(Admin , Customer, Cashier): ")

Customer_usernames=[]
Customer_passwords = []
Admin_usernames = []
Admin_passwords = []
Cashier_usernames = []
Cashier_passwords = []

if Reg_profile.title() == "Customer":
    Customer_usernames.append(Reg_username)
    Customer_passwords.append(Reg_password)
elif Reg_profile.title() == "Admin":
    Admin_usernames.append(Reg_username)
    Admin_passwords.append(Reg_password)
elif Reg_profile.title == "Cashier":
    Cashier_usernames.append(Reg_username)
    Cashier_passwords.append(Reg_password)


print("\n")


print("Login to your account")
print("+"*40)
print("\n")

attempts =0

while attempts < 3:
    Username = input("Please enter your username: ")
    Password = input("Please enter your password: ")
    print("\n")
    if Username in Customer_usernames and Password in Customer_passwords:
        print("Login successful!")
        break
    elif Username in Admin_usernames and Password in Admin_passwords:
        print("Login successful!")
        break
    elif Username in Cashier_usernames and Password in Cashier_passwords:
        print("Login successful!")
        break   
    else:
        print("Invalid username or password. Please try again.")
        attempts += 1

if attempts == 3:
    print("Too many failed login attempts. Please try again later.")


products = [{
"id": 1,
"name": "Laptop",
"price": 10000000, 
"quantity": 10,
"rating": 4.5
},
{
"id": 2,
"name": "Mouse",
"price": 25000,
"quantity": 50,
"rating": 4.0
},
{
"id": 3,
"name": "Keyboard",
"price": 75000,
"quantity": 20,
"rating": 4.2
},
{"id": 4, "name":"Apples",
"price": 5000, 
"quantity": 100,
"rating": 4.3},
{"id": 5, "name":"Bananas",
"price": 3000,
"quantity": 150,
"rating": 4.1}
]

customer_orders = []
paid_orders = []


if Reg_profile.title() == "Customer":
    print(f"Welcome Customer! {Reg_username} You have access to browse and purchase products.")
    print("\n")
    print("Available products:")
    print("\n")
    print("We offer Discounts of 10%, off as long as your total bill exceeds 100,000. Enjoy shopping!")
    print("\n")
    for product in products:
        print(f"Name: {product['name']}, Price: {product['price']}, Quantity: {product['quantity']}, Rating: {product['rating']}") 
        add_to_cart = input("Add to cart? (yes or no) ")
        if add_to_cart.lower() == "yes":
            quantity = int(input("Enter quantity: "))
            if quantity <= product["quantity"]:
                customer_orders.append({
                    "id": len(customer_orders) + 1,
                    "customer_name": Reg_username,
                    "products": {product["name"]: quantity}
                })
                product["quantity"] -= quantity
                print(f"{quantity} {product['name']} added to cart.")
            else:
                print(f"Sorry, only {product['quantity']} {product['name']} available.")
                print("\n")
        else:
            print(f"{product['name']} not added to cart.")
            print("\n")

    print("Your cart:")
    if customer_orders is None:
        print("You have no appending order request")
        print("\n")
    else:
        print("Order Summary:")
        print("-"*40)
        print(f"{'Product Name':<20}{'Quantity':<10}{'PAYE(1%)':<15}{'Subtotal':<15}")
        print("-"*40)

        for order in customer_orders:
            if order["customer_name"] == Reg_username:
                for product_name, quantity in order["products"].items():
                    print(f"{product_name:<20}{quantity:<10}{quantity * 0.01:<15}{quantity * next((p['price'] for p in products if p['name'] == product_name), 0):<15,}")
        print("-"*40)
        if sum(quantity * next((p['price'] for p in products if p['name'] == product_name), 0) for order in customer_orders if order["customer_name"] == Reg_username for product_name, quantity in order["products"].items()) > 100000:
            print(f"{'Total':<30}{sum(quantity * next((p['price'] for p in products if p['name'] == product_name), 0) for order in customer_orders if order['customer_name'] == Reg_username for product_name, quantity in order['products'].items()) * 0.9:<15,}")
        else:
            coupon= input("Do you have a coupon: ")
            if coupon.lower() == "yes":
                coupon_code = input("Enter coupon code for discount (if applicable): ")
                if coupon_code == "DISCOUNT10":
                    print(f"{'Total':<30}{sum(quantity * next((p['price'] for p in products if p['name'] == product_name), 0) for order in customer_orders if order['customer_name'] == Reg_username for product_name, quantity in order['products'].items()) * 0.9:<15,}")
                elif coupon_code == "DISCOUNT20":
                    print(f"{'Total':<30}{sum(quantity * next((p['price'] for p in products if p['name'] == product_name), 0) for order in customer_orders if order['customer_name'] == Reg_username for product_name, quantity in order['products'].items()) * 0.8:<15,}")
            else:
                print(f"{'Total':<30}{sum(quantity * next((p['price'] for p in products if p['name'] == product_name), 0) for order in customer_orders if order['customer_name'] == Reg_username for product_name, quantity in order['products'].items()):<15,}")
                print("\n")
    print("="*40)
    print("Only Momo pay is available for payment. Please proceed to payment.")
    print("\n")
    Affirm=input("Proceed with payment? (yes or no) ")
    if Affirm.lower() == "yes":
        momo_number = input("Enter your Momo number: ")
        if len(momo_number) == 10 and momo_number.isdigit():
            print("processing payment...")
            accept=input("Confirm payment? (yes or no) ")
            if accept.lower() == "yes":
                print("Payment successful! Thank you for your purchase.")
                print("Your order will be delivered to you soon.")
                paid_orders.append({
                    "id": len(paid_orders) + 1,
                    "customer_name": Reg_username,
                    "products": {product["name"]: quantity for order in customer_orders if order["customer_name"] == Reg_username for product["name"], quantity in order["products"].items()}
                })
            else:
                print("Payment cancelled.")
        else:
            print("Invalid Momo number. Payment failed.")

elif Reg_profile.title() == "Cashier":
    print(f"Welcome Cashier! {Reg_username} You have access to manage customer orders and process payments.")
    print("\n")
    print("Customer orders:")
    for order in customer_orders:
        print(f"Order ID: {order['id']}, Customer: {order['customer_name']}, Products: {order['products']}")
    print("\n")
    print("Processing payments for customer orders...")
    for order in customer_orders:
        print(f"Processing payment for Order ID: {order['id']}, Customer: {order['customer_name']}")
        payment_method = input("Enter payment method (Momo, Cash, Card): ")
        if payment_method.lower() == "momo":
            momo_number = input("Enter customer's Momo number: ")
            if len(momo_number) == 10 and momo_number.isdigit():
                print("Processing Momo payment...")
                confirm_payment = input("Confirm payment? (yes or no) ")
                if confirm_payment.lower() == "yes":
                    print("Payment successful! Thank you for your purchase.")
                else:
                    print("Payment cancelled.")
            else:
                print("Invalid Momo number. Payment failed.")
        elif payment_method.lower() == "cash":
            cash_received = float(input("Enter cash received from customer: "))
            total_amount = sum(quantity * next((p['price'] for p in products if p['name'] == product_name), 0) for product_name, quantity in order["products"].items())
            if cash_received >= total_amount:
                change = cash_received - total_amount
                print(f"Payment successful! Change to return: {change:.2f}")
            else:
                print("Insufficient cash. Payment failed.")
        elif payment_method.lower() == "card":
            card_number = input("Enter customer's card number: ")
            if len(card_number) == 16 and card_number.isdigit():
                print("Processing card payment...")
                confirm_payment = input("Confirm payment? (yes or no) ")
                if confirm_payment.lower() == "yes":
                    print("Payment successful! Thank you for your purchase.")
                else:
                    print("Payment cancelled.")
            else:
                print("Invalid card number. Payment failed.")
        else:
            print("Invalid payment method. Payment failed.")

elif Reg_profile.title() == "Admin":
    print(f"Welcome Admin! {Reg_username} You have access to manage products.")
    print("\n")

    print("Would you like to add a new product?")
    response = input("yes or no? ")
    print("\n")
    if response.lower() == "yes":
        print("How many products would you like to add?")
        num_products = int(input())
        for _ in range(num_products):
            new_product_id = int(input("Enter the unique ID of the new product: "))
            if any(product["id"] == new_product_id for product in products):
                print(f"Product ID {new_product_id} already exists. Please enter a unique ID.")
                continue
            new_product_name = input("Enter the name of the new product: ")
            new_product_price = float(input("Enter the price of the new product: "))
            new_product_quantity = int(input("Enter the quantity of the new product: "))
            new_product_rating = float(input("Enter the rating of the new product: "))
            new_product = {
            "id": new_product_id,
            "name": new_product_name,
            "price": new_product_price,
            "quantity": new_product_quantity,
            "rating": new_product_rating
        }
            products.append(new_product)
        print(f"Product '{new_product_name}' added successfully!")
    else:
        print("No product added.")

    print("\n")
    print("Would you like to update an existing product?")
    response = input("yes or no? ")
    print("\n")
    if response.lower() == "yes":
        print("Enter the id of the product you want to update:")
        product_id_to_update = int(input())
        for product in products:
            if product["id"] == product_id_to_update:
                print("What would you like to update?")
                print("1. Price")
                print("2. Quantity")
                print("3. Rating")
                update_choice = input("Enter the number corresponding to your choice: ")
                if update_choice == "1":
                    new_price = float(input("Enter the new price: "))
                    product["price"] = new_price
                    print(f"Price of '{product['name']}' updated successfully!")
                elif update_choice == "2":
                    new_quantity = int(input("Enter the new quantity: "))
                    product["quantity"] = new_quantity
                    print(f"Quantity of '{product['name']}' updated successfully!")
                elif update_choice == "3":
                    new_rating = float(input("Enter the new rating: "))
                    product["rating"] = new_rating
                    print(f"Rating of '{product['name']}' updated successfully!")
                else:
                    print("Invalid choice. No updates made.")
                break
        else:
            print(f"Product with ID {product_id_to_update} not found.")
    else:
        print("No product updated.")

    print("\n")
    print("Would you like to delete a product?")
    response = input("yes or no? ")
    print("\n") 
    if response.lower() == "yes":
        print("Enter the id of the product you want to delete:")
        product_id_to_delete = int(input())
        for i, product in enumerate(products):
            if product["id"] == product_id_to_delete:
                deleted_product_name = product["name"]
                del products[i]
                print(f"Product '{deleted_product_name}' deleted successfully!")
                break
        else:
            print(f"Product with ID {product_id_to_delete} not found.")
    else:
        print("No product deleted.")

    print("\n")
    print("would you like to view paid orders?")
    response = input("yes or no? ")
    print("\n")
    if response.lower() == "yes":
        if paid_orders is None :
            print("No paid orders to view")
        else:
            print("Paid orders:")
            for order in paid_orders:
                print(f"Order ID: {order['id']}, Customer: {order['customer_name']}, Products: {order['products']}")
                print("\n")
                print("please confirm paid orders delivery")
                response = input("yes or no? ")
                print("\n") 
                if response.lower() == "yes":
                    print("Choose which paid order to mark as delivered:")
                    for i, order in enumerate(paid_orders, start=1):
                        print(f"{i}. Order ID: {order['id']}, Customer: {order['customer_name']}")
                    choice = int(input("Enter the number corresponding to the order: "))
                    if 1 <= choice <= len(paid_orders):
                        print("Paid orders marked as delivered.")
                        paid_orders.clear()
                    else:
                        print("Invalid choice.")
                else:
                    print("Paid orders not marked as delivered.")
                    print("Paid orders remain in the system until delivery is confirmed.")
    else:
        print(f"As You wish {Reg_username}")   
        print("\n")       

print("\n")
print("Thank you for using the E-com")
    # Code for managing products would go here

