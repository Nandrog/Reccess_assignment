"""Student Record Management System

This application stores student records in a CSV file and saves additional
student details in a JSON file. It supports adding, viewing, searching,
updating, and deleting student records, while logging user actions and errors.
"""

import csv
import json
import logging
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STUDENT_CSV = os.path.join(SCRIPT_DIR, "students.csv")
STUDENT_JSON = os.path.join(SCRIPT_DIR, "students.json")
LOG_FILE = os.path.join(SCRIPT_DIR, "student_system.log")

logger = logging.getLogger("student_management")
logger.setLevel(logging.INFO)
logger.propagate = False

if not logger.handlers:
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


class StudentError(Exception):
    """Base exception for student record errors."""


class StudentNotFoundError(StudentError):
    """Raised when a student registration number cannot be found."""


class DuplicateStudentError(StudentError):
    """Raised when a student with the same registration number already exists."""


def initialize_storage() -> None:
    """Create storage files if they do not exist."""
    try:
        if not os.path.exists(STUDENT_CSV):
            with open(STUDENT_CSV, mode="w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=["registration_number", "name", "age", "email", "university"])
                writer.writeheader()
        if not os.path.exists(STUDENT_JSON):
            with open(STUDENT_JSON, mode="w", encoding="utf-8") as jsonfile:
                json.dump({}, jsonfile, indent=4)
        logger.info("Storage initialized: CSV=%s JSON=%s", STUDENT_CSV, STUDENT_JSON)
    except OSError as error:
        logger.exception("Failed to initialize storage files")
        raise StudentError("Could not initialize storage files.") from error
    finally:
        pass


def load_students_csv() -> list[dict]:
    """Load student records from the CSV file."""
    try:
        with open(STUDENT_CSV, mode="r", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            students = [row for row in reader]
        logger.info("Loaded %d student records from CSV.", len(students))
        return students
    except FileNotFoundError:
        logger.warning("CSV file not found, returning empty student list.")
        return []
    except csv.Error as error:
        logger.exception("CSV parsing failed.")
        raise StudentError("Could not read student records from CSV.") from error
    finally:
        pass


def save_students_csv(students: list[dict]) -> None:
    """Save student records to the CSV file."""
    try:
        with open(STUDENT_CSV, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["registration_number", "name", "age", "email", "university"])
            writer.writeheader()
            writer.writerows(students)
        logger.info("Saved %d student records to CSV.", len(students))
    except OSError as error:
        logger.exception("Failed to write student CSV.")
        raise StudentError("Could not save student records to CSV.") from error
    finally:
        pass


def load_student_details() -> dict:
    """Load additional student details from the JSON file."""
    try:
        with open(STUDENT_JSON, mode="r", encoding="utf-8") as jsonfile:
            details = json.load(jsonfile)
        logger.info("Loaded %d student detail records from JSON.", len(details))
        return details
    except FileNotFoundError:
        logger.warning("JSON file not found, returning empty details dictionary.")
        return {}
    except json.JSONDecodeError as error:
        logger.exception("JSON parsing failed.")
        raise StudentError("Could not read additional student details from JSON.") from error
    finally:
        pass


def save_student_details(details: dict) -> None:
    """Save additional student details to the JSON file."""
    try:
        with open(STUDENT_JSON, mode="w", encoding="utf-8") as jsonfile:
            json.dump(details, jsonfile, indent=4)
        logger.info("Saved additional details for %d students.", len(details))
    except OSError as error:
        logger.exception("Failed to write student JSON.")
        raise StudentError("Could not save additional student details to JSON.") from error
    finally:
        pass


def validate_nonempty(prompt_text: str) -> str:
    """Prompt until the user enters a non-empty string."""
    while True:
        value = input(prompt_text).strip()
        if value:
            return value
        print("This field cannot be blank. Please enter a value.")


def validate_registration_number(existing_ids: set[str] | None = None) -> str:
    """Prompt for a registration number and ensure it is valid and unique."""
    while True:
        registration_number = input("Registration number (e.g. REG001): ").strip().upper()
        if not registration_number:
            print("Registration number cannot be empty.")
            continue
        if not re.fullmatch(r"[A-Z0-9]+", registration_number):
            print("Registration number must contain only letters and digits.")
            continue
        if existing_ids and registration_number in existing_ids:
            print("A student with that registration number already exists.")
            continue
        return registration_number


def validate_age() -> str:
    """Prompt for age and validate it is a positive integer."""
    while True:
        value = input("Age: ").strip()
        if not value.isdigit():
            print("Age must be a number.")
            continue
        age = int(value)
        if age < 5 or age > 120:
            print("Age must be between 5 and 120.")
            continue
        return str(age)


def validate_email() -> str:
    """Prompt for an email address and validate its format."""
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$"
    while True:
        email = input("Email: ").strip()
        if not email:
            print("Email cannot be blank.")
            continue
        if re.fullmatch(email_pattern, email):
            return email
        print("Please enter a valid email address.")


def validate_contact() -> str:
    """Prompt for a contact number and validate digits, spaces, or hyphens."""
    while True:
        contact = input("Contact number: ").strip()
        if not contact:
            print("Contact number cannot be blank.")
            continue
        if re.fullmatch(r"[\d\-\s\+]{7,20}", contact):
            return contact
        print("Please enter a valid contact number with digits, spaces, or dashes.")


def validate_university() -> str:
    """Prompt for a university name."""
    while True:
        university = input("University: ").strip()
        if university:
            return university
        print("University cannot be empty.")


def display_student_record(student: dict, details: dict) -> None:
    """Print a combined student record to the console."""
    print("----------------------------------------")
    print(f"Registration Number: {student['registration_number']}")
    print(f"Name: {student['name']}")
    print(f"Age: {student['age']}")
    print(f"Email: {student['email']}")
    print(f"University: {student['university']}")
    if details:
        print(f"Program: {details.get('program', 'N/A')}")
        print(f"Address: {details.get('address', 'N/A')}")
        print(f"Contact: {details.get('contact', 'N/A')}")
    print("----------------------------------------")


def view_all_students() -> None:
    """Show all student records, combining CSV and JSON data."""
    students = load_students_csv()
    details = load_student_details()
    if not students:
        print("No students are registered yet.")
        return
    print("\nAll registered students:")
    for student in students:
        display_student_record(student, details.get(student["registration_number"], {}))
    logger.info("Displayed all student records.")


def add_student() -> None:
    """Add a new student to the system."""
    students = load_students_csv()
    details = load_student_details()
    existing_ids = {student["registration_number"] for student in students}
    try:
        registration_number = validate_registration_number(existing_ids)
        new_student = {
            "registration_number": registration_number,
            "name": validate_nonempty("Student name: "),
            "age": validate_age(),
            "email": validate_email(),
            "university": validate_university(),
        }
        new_details = {
            "program": validate_nonempty("Program: "),
            "address": validate_nonempty("Address: "),
            "contact": validate_contact(),
        }
        students.append(new_student)
        details[registration_number] = new_details
        save_students_csv(students)
        save_student_details(details)
        print(f"Student {registration_number} has been added successfully.")
        logger.info("Added student %s.", registration_number)
    except DuplicateStudentError as error:
        logger.error("Duplicate student detected: %s", error)
        raise
    except Exception:
        logger.exception("Failed to add a new student.")
        raise StudentError("Unable to add the student at this time.")
    finally:
        pass


def find_student_by_registration(registration_number: str, students: list[dict]) -> dict:
    """Find a student record by registration number."""
    for student in students:
        if student["registration_number"] == registration_number:
            return student
    raise StudentNotFoundError(f"Student {registration_number} was not found.")


def search_student() -> None:
    """Search for a student and display their full record."""
    registration_number = input("Enter registration number to search: ").strip().upper()
    if not registration_number:
        print("Registration number is required for search.")
        return
    students = load_students_csv()
    details = load_student_details()
    try:
        student = find_student_by_registration(registration_number, students)
        display_student_record(student, details.get(registration_number, {}))
        logger.info("Searched for student %s.", registration_number)
    except StudentNotFoundError as error:
        logger.warning("Search failed: %s", error)
        print(error)


def update_student() -> None:
    """Update an existing student's information."""
    registration_number = input("Enter registration number to update: ").strip().upper()
    if not registration_number:
        print("Registration number is required for update.")
        return
    students = load_students_csv()
    details = load_student_details()
    try:
        student = find_student_by_registration(registration_number, students)
        current_details = details.get(registration_number, {})
        print("Enter new values or press Enter to keep the current value.")
        student["name"] = input(f"Name [{student['name']}]: ").strip() or student["name"]
        age_input = input(f"Age [{student['age']}]: ").strip()
        if age_input:
            if age_input.isdigit() and 5 <= int(age_input) <= 120:
                student["age"] = age_input
            else:
                print("Invalid age entered. Keeping the current age.")
        email_input = input(f"Email [{student['email']}]: ").strip()
        if email_input:
            if re.fullmatch(r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$", email_input):
                student["email"] = email_input
            else:
                print("Invalid email entered. Keeping the current email.")
        university_input = input(f"University [{student['university']}]: ").strip()
        if university_input:
            student["university"] = university_input
        current_program = current_details.get("program", "")
        current_address = current_details.get("address", "")
        current_contact = current_details.get("contact", "")
        program_input = input(f"Program [{current_program}]: ").strip()
        if program_input:
            current_details["program"] = program_input
        address_input = input(f"Address [{current_address}]: ").strip()
        if address_input:
            current_details["address"] = address_input
        contact_input = input(f"Contact [{current_contact}]: ").strip()
        if contact_input:
            if re.fullmatch(r"[\d\-\s\+]{7,20}", contact_input):
                current_details["contact"] = contact_input
            else:
                print("Invalid contact entered. Keeping the current contact.")
        details[registration_number] = current_details
        save_students_csv(students)
        save_student_details(details)
        print(f"Student {registration_number} has been updated.")
        logger.info("Updated student %s.", registration_number)
    except StudentNotFoundError as error:
        logger.warning("Update failed: %s", error)
        print(error)
    except Exception:
        logger.exception("Failed to update student %s.", registration_number)
        raise StudentError("Unable to complete the update.")
    finally:
        pass


def delete_student() -> None:
    """Remove a student record from both CSV and JSON storage."""
    registration_number = input("Enter registration number to delete: ").strip().upper()
    if not registration_number:
        print("Registration number is required for delete.")
        return
    students = load_students_csv()
    details = load_student_details()
    try:
        student = find_student_by_registration(registration_number, students)
        students = [item for item in students if item["registration_number"] != registration_number]
        if registration_number in details:
            del details[registration_number]
        save_students_csv(students)
        save_student_details(details)
        print(f"Student {registration_number} has been deleted.")
        logger.info("Deleted student %s.", registration_number)
    except StudentNotFoundError as error:
        logger.warning("Delete failed: %s", error)
        print(error)
    except Exception:
        logger.exception("Failed to delete student %s.", registration_number)
        raise StudentError("Unable to delete the student record.")
    finally:
        pass


def display_menu() -> None:
    """Print the main menu options for the user."""
    print("\nStudent Record Management System")
    print("1. Add a new student")
    print("2. View all students")
    print("3. Search by registration number")
    print("4. Update student details")
    print("5. Delete a student")
    print("6. Exit")


def get_menu_choice() -> int:
    """Prompt the user to select a valid menu option."""
    while True:
        choice = input("Please choose an option (1-6): ").strip()
        if choice in {"1", "2", "3", "4", "5", "6"}:
            return int(choice)
        print("Invalid choice. Enter a number between 1 and 6.")


def main() -> None:
    """Entry point for the application."""
    initialize_storage()
    while True:
        display_menu()
        choice = get_menu_choice()
        try:
            if choice == 1:
                add_student()
            elif choice == 2:
                view_all_students()
            elif choice == 3:
                search_student()
            elif choice == 4:
                update_student()
            elif choice == 5:
                delete_student()
            elif choice == 6:
                print("Goodbye! Thank you for using the student system.")
                logger.info("User exited the student management system.")
                break
        except StudentError as error:
            print(f"Error: {error}")
        except Exception:
            logger.exception("Unhandled exception in main loop.")
            print("An unexpected error occurred. Please try again.")
        finally:
            print()


if __name__ == "__main__":
    main()
