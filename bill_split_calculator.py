print("Bill split calculator")
print("+"*40)
print ("Welcome to the bill split calculator!")
print("\n")

def prompt_int(prompt, min_value=None):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Please enter a whole number.")
            continue
        if min_value is not None and value < min_value:
            print(f"Please enter a number greater than or equal to {min_value}.")
            continue
        return value


def prompt_float(prompt, min_value=None):
    while True:
        try:
            value = float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")
            continue
        if min_value is not None and value < min_value:
            print(f"Please enter a value greater than or equal to {min_value}.")
            continue
        return value


def prompt_choice(prompt, choices):
    choices_lower = [choice.lower() for choice in choices]
    while True:
        value = input(prompt).strip().lower()
        if value in choices_lower:
            return value
        print(f"Please enter one of: {', '.join(choices)}.")


def prompt_nonempty_string(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Please enter a non-empty name.")


print("How many people are in your group?")
num_people = prompt_int("", min_value=1)
print("\n")

print("What is the total bill amount?")
total_bill = prompt_float("", min_value=0.0)
print("\n")

print("DEFAULT TIP:")
print ("This implies a default tip of 15% that will be eequally split among all members of the group.")
print("\n")
print("CUSTOM TIP:")
print("This means every individual will have there own tip personal tip.")
print("\n")

print("Would you what to include a default tip?")
response = prompt_choice("yes or no?", ["yes", "no"])
print("\n")

if response == "yes":
    
    tip_percentage = 15
    print(f"Entered tip percentage is {tip_percentage} for {tip_percentage}%")

    print("Enter the names for each person in the group:")
    arr_names = [None]*num_people
    for i in range(num_people):
        print("Person", i+1)
        arr_names[i] = input("Name: ")
        print("\n")


    tip_amount = total_bill * (tip_percentage / 100)
    total_bill= total_bill + tip_amount
    Amount_per_person = total_bill / num_people

    print("*"*40)
    print("bill split Receipt")
    print("*"*40)
    print("bill breakdown:")
    print("\n")
    print("-"*40)
    print(f"{'Customer Name':<20}{'tip(%)':<10}{'total amount':<15}")
    print("-"*40)

    for i in range(num_people):
        print(f"{arr_names[i]:<20}{tip_percentage:<10}{Amount_per_person:<15,}")
    
    print("-"*40)
    print(f"{'Total':<30}{total_bill:,}")
    print("="*40)

else:
    print("Customise your tip percentage for each person:")
    print("\n")
    arr_tip_percentages = [None]*num_people
    total_tip_amount = 0
    for i in range(num_people):
        print("Enter name and tip percentage for person", i+1)
        arr_tip_percentages[i] = {"Name": prompt_nonempty_string("Name: "), "Tip Percentage": prompt_float("Tip Percentage: ", min_value=0.0)}
        print("\n")


    print("*"*40)
    print("bill split Receipt")
    print("*"*40)
    print("bill breakdown:")
    print("\n")
    print("-"*40)
    print(f"{'Customer Name':<20}{'tip(%)':<10}{'total amount':<15}")
    print("-"*40)

    for i in range(num_people):
        tip_amount = total_bill * (arr_tip_percentages[i]["Tip Percentage"] / 100)
        amount_per_person = (total_bill/num_people) + tip_amount
        total_tip_amount+=tip_amount
        print(f"{arr_tip_percentages[i]['Name']:<20}{arr_tip_percentages[i]['Tip Percentage']:<10}{amount_per_person:<15,}")

    total_bill= total_bill + total_tip_amount
    print("-"*40)
    print(f"{'Total':<30}{total_bill:,}")
    print("="*40)



    
print("Thank you for using the bill split calculator!")
