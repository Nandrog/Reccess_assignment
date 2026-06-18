"""Contact Manager CLI

Simple function-based contact management system with validation,
search by name/phone/email, and an interactive menu.
"""

contacts = []


def is_valid_phone(phone: str) -> bool:
    """Return True if phone contains only digits, hyphens, or an optional leading plus."""
    if not phone:
        return False
    allowed = set("0123456789-+")
    return all(ch in allowed for ch in phone)


def is_valid_email(email: str) -> bool:
    """Return True if email contains an @ symbol and a period."""
    if not email:
        return False
    return "@" in email and "." in email


def format_contact(contact: dict) -> str:
    return f"Name: {contact['Name']}, Tel: {contact['Tel']}, Email: {contact['Email'] or 'N/A'}"


def print_contacts(contact_list: list[dict]) -> None:
    if not contact_list:
        print("No matching contacts found.")
        return
    print("\n=== Contacts ===")
    for index, contact in enumerate(contact_list, start=1):
        print(f"{index}. {format_contact(contact)}")
    print("================\n")


def find_contacts(query: str) -> list[dict]:
    normalized = query.strip().lower()
    if not normalized:
        return []

    matcher = lambda contact: (
        normalized in contact["Name"].lower()
        or normalized in contact["Tel"].lower()
        or (contact["Email"] and normalized in contact["Email"].lower())
    )

    return [contact for contact in contacts if contact and matcher(contact)]


def add_contact() -> None:
    name = input("Name: ").strip()
    if not name:
        print("Error: Name cannot be empty.")
        return

    tel = input("Tel: ").strip()
    if not is_valid_phone(tel):
        print("Error: Phone must contain only digits, hyphens, or a leading plus.")
        return

    email = input("Email (optional): ").strip()
    if email and not is_valid_email(email):
        print("Error: Email must contain an '@' symbol and a period.")
        return

    contacts.append({
        "Name": name,
        "Tel": tel,
        "Email": email or None,
    })
    print("Contact added successfully.")


def view_contact() -> None:
    if not contacts:
        print("No contacts have been added yet.")
        return
    query = input("Enter name, phone, or email to view (leave blank to show all): ").strip()
    if not query:
        print_contacts(contacts)
        return
    matches = find_contacts(query)
    print_contacts(matches)


def update_contact() -> None:
    if not contacts:
        print("No contacts available to update.")
        return
    query = input("Enter name, phone, or email of the contact to update: ").strip()
    matches = find_contacts(query)
    if not matches:
        print("No contacts matched that search.")
        return
    if len(matches) > 1:
        print("Multiple contacts found. Please refine your search.")
        print_contacts(matches)
        return

    contact = matches[0]
    print(f"Updating contact: {format_contact(contact)}")

    new_name = input(f"New name [{contact['Name']}]: ").strip()
    new_tel = input(f"New phone [{contact['Tel']}]: ").strip()
    new_email = input(f"New email [{contact['Email'] or 'None'}]: ").strip()

    if new_name:
        contact["Name"] = new_name

    if new_tel:
        if not is_valid_phone(new_tel):
            print("Error: Phone must contain only digits, hyphens, or a leading plus. Update canceled.")
            return
        contact["Tel"] = new_tel

    if new_email:
        if not is_valid_email(new_email):
            print("Error: Email must contain an '@' symbol and a period. Update canceled.")
            return
        contact["Email"] = new_email
    elif new_email == "":
        contact["Email"] = None

    print("Contact updated successfully.")


def delete_contact() -> None:
    if not contacts:
        print("No contacts available to delete.")
        return
    query = input("Enter name, phone, or email of the contact to delete: ").strip()
    matches = find_contacts(query)
    if not matches:
        print("No contacts matched that search.")
        return
    if len(matches) > 1:
        print("Multiple contacts found. Please refine your search.")
        print_contacts(matches)
        return

    contact = matches[0]
    confirm = input(f"Delete {format_contact(contact)}? (yes/no): ").strip().lower()
    if confirm == "yes":
        contacts.remove(contact)
        print("Contact deleted.")
    else:
        print("Delete canceled.")


def search_contacts() -> None:
    if not contacts:
        print("No contacts available to search.")
        return
    query = input("Search by name, phone, or email: ").strip()
    matches = find_contacts(query)
    print_contacts(matches)


def list_all_contacts() -> None:
    print_contacts(contacts)


def main() -> None:
    while True:
        print("=== Contact Manager Menu ===")
        print("1. Add Contact")
        print("2. View Contact")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. Search Contacts")
        print("6. List All Contacts")
        print("7. Exit")

        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            add_contact()
        elif choice == "2":
            view_contact()
        elif choice == "3":
            update_contact()
        elif choice == "4":
            delete_contact()
        elif choice == "5":
            search_contacts()
        elif choice == "6":
            list_all_contacts()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid menu option. Please enter a number from 1 to 7.")
        print()


if __name__ == "__main__":
    main()


            
