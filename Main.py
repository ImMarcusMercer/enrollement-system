#Imports
from Programs import programs
from Logic import *

programs=programs

def paginatePrograms():
    """Show all programs with pagination of 10 programs per page"""
    index = 0
    cap = 10

    while True:
        header("Choose Program")
        end = min(index + cap, len(programs))
        for i in range(index, end):
            print(f"{i+1}: {programs[i]}")
        print("\nOptions: [N]ext | [P]revious | [E]xit")
        choice = input("Choose an option: ").strip().lower()

        if choice == 'n' and end < len(programs):
            index += cap
        elif choice == 'p' and index - cap >= 0:
            index -= cap
        elif choice == 'e':
            break
        else:
            print("Invalid option or no more pages.")

def header(text):
    print(f"====={text}=====")


def main():
    data = load_data()

    while True:
        header("CMU Enrollment System")
        print("1. View Programs")
        print("2. Enroll Student")
        print("3. View Class List")
        print("4. Exit")
        choice = input("Select option: ")

        if choice == "1":
            # showPrograms(data)
            paginatePrograms()

        elif choice == "2":
            header("Enrollment")
            paginatePrograms()
            program = input("Enter Program: ")
            year = input("Enter Year: ")
            section = input("Enter Section: ")
            studentID = input("Enter Student ID: ")
            fname = input("Enter First name: ")
            lname = input("Enter Last name: ")
            enroll(data, program, year, section, studentID, fname, lname)

        elif choice == "3":
            header("View Class")
            showPrograms(data)
            program = input("Enter Program: ")
            year = input("Enter Year: ")
            section = input("Enter Section: ")
            viewclass(data, program, year, section)

        elif choice == "4":
            save_data(data)
            print("Exiting program...")
            break

        elif choice == "5":
            #Login as Admin
            #Complete this option
            pass

        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()