#Imports
import json
from SharedPreferences import *
import datetime

#Classes
class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = Node()

    def add(self, newVal):
        curr = self.head
        while curr.next and curr.next.data.ID < newVal.ID:
            curr = curr.next
        new_node = Node(newVal)
        new_node.next = curr.next
        curr.next = new_node

    def remove(self, value):
        prev = self.head
        current = prev.next
        while current:
            if current.data == value:
                prev.next = current.next
                return True
            prev = current
            current = current.next
        return False
    def getSize(self):
        count = 0
        current = self.head.next
        while current:
            count += 1
            current = current.next
        return count


    def showList(self):
        current = self.head.next
        while current:
            print(current.data)
            current = current.next
class Subject:
    def __init__(self, code, description):
        self.__code = code
        self.__description= description

    def getCode(self):
        return self.__code
    def getDesciption(self):
        return self.__description
    
    def __str__(self):
        return f"|Code: {self.getCode()} \t| {self.getDesciption()}"
    
def getSubjects(year:str):
        id=year
        with open('subjects.json', 'r') as file:
            data = json.load(file)
        subjects=[]
        for year, subject in data.items():
            if year == id:
                for items, desc in subject.items():
                    subjects.append(Subject(items, desc))
        for items in subjects:
            print(items)

class Student:
    def __init__(self, ID,email, password, fname, lname):
        self.ID = ID
        self.email= email
        self.__password=password
        self.fname = fname
        self.lname = lname

    def getPass(self):
        return self.__password
    
    def getFullName(self):
        return f"{self.lname}, {self.fname}"

    def __str__(self):
        return f"ID: {self.ID} Name: {self.getFullName()}"

class Class:
    def __init__(self, program, year, section):
        self.program = program
        self.year = year
        self.section = section
        self.capacity = 30
        self.attendance = LinkedList()
        

    def addStudent(self, newStudent):
        if self.attendance.getSize()>= self.capacity:
            print("Class is Full!")
            return
        self.attendance.add(newStudent)

    def showClassList(self):
        print(f"\nClass List: {self.program} {self.year}{self.section}")
        self.attendance.showList()

class Section:
    def __init__(self, program, year, section):
        self.program = program
        self.year = year
        self.section = section
        self.students = LinkedList() 
        self.load_students()

    def load_students(self):
        
        with open('studentsdatabase.json', 'r') as f:
            data = json.load(f)

        if (self.program in data and self.year in data[self.program] and self.section in data[self.program][self.year]):
            
            for s in data[self.program][self.year][self.section]:
                stud = Student(
                    s["studentID"],
                    s["details"]["email"],
                    s["details"]["password"],
                    s["details"]["firstname"],
                    s["details"]["lastname"]
                )
                self.students.add(stud)
        else:
            print(f"Section {self.program} {self.year}{self.section} not found in database.")
    

    def display_students(self):
        print(f"\n=== Section: {self.program} {self.year}{self.section} ===")
        self.students.showList()

    def add_student(self, student: Student):
        if self.students.getSize() >= 30:
            print("Section is full!")
            return False
        self.students.add(student)
        print(f"Added {student.getFullName()} to {self.program} {self.year}{self.section}")
        return True

#Database manager
def getData():
    with open('studentsdatabase.json', 'r') as file:
        data = json.load(file)

    students = []
    for program, years in data.items():
        for year, sections in years.items():
            for section, studentList in sections.items():
                for stud in studentList:
                    student = Student(stud["studentID"],stud["details"]["firstname"],stud["details"]["lastname"])
                    students.append({"program": program,"year": year,"section": section,"student": student})
    return students

def addProgram(data, program):
    if program not in data:
        data[program] = {}
        print(f"Added program: {program}")
    else:
        print(f"Program \"{program}\" already exists.")

def addYear(data, program, year):
    if program in data:
        if year not in data[program]:
            data[program][year] = {}
            print(f"Added year {year} to {program}")
        else:
            print(f"Year \"{year}\" already exists in {program}")
    else:
        print(f"Program {program} does not exist.")

def addSection(data, program, year, section):
    if program in data and year in data[program]:
        if section not in data[program][year]:
            data[program][year][section] = []
            print(f"Added section {section} to {program} {year}")
        else:
            print(f"Section {section} already exists in {program} {year}")
    else:
        print(f"Cannot add section — program/year not found.")

def addStudent(data, program, year, section, studentID,email,password, firstname, lastname):
    if program in data and year in data[program] and section in data[program][year]:
        for student in data[program][year][section]:
            if student["studentID"] == studentID:
                print(f"Student {studentID} already exists in {program} {year}{section}")
                return
        
        student = {
            "studentID": studentID,"details": 
            {
                "email":email,
                "password":password,
                "firstname": firstname,
                "lastname": lastname
            }
        }
        data[program][year][section].append(student)
        print(f"Added student {studentID} to {program} {year}{section}")
    else:
        print(f"Cannot add student — location not found.")

#Test Section
# if __name__ == '__main__':
#     studentRecords = getData()
#     with open('studentsdatabase.json') as f:
#         data = json.load(f)
#     addProgram(data, "BSCS")
#     addYear(data, "BSCS", "1")
#     addSection(data, "BSCS", "1", "A")
#     addStudent(data, "BSCS", "1", "A", "2025310607", "Alice", "Anderson")
#     with open('studentsdatabase.json', 'w') as f:
#         json.dump(data, f, indent=2)

#Test run
def load_data(filename="studentsdatabase.json"):
    with open(filename, 'r') as file:
        return json.load(file)

def save_data(data, filename="studentsdatabase.json"):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)


def showPrograms(data):
    print("\nAvailable Programs:")
    for prog in data:
        print(f" - {prog}")

def displaySections(data, program, year):
    if program in data and year in data[program]:
        print(f"\nSections in {program} {year}:")
        for section in data[program][year]:
            print(f" - {section}")
    else:
        print("Invalid program/year.")

def enroll(data: list, program, year, section, studentID,email,password, fname, lname):
    if program not in data:
        data[program] = {}
    if year not in data[program]:
        data[program][year] = {}
    if section not in data[program][year]:
        data[program][year][section] = []

    for student in data[program][year][section]:
        if student["studentID"] == studentID:
            print("Student already enrolled.")
            return
        
    for student in data[program][year][section]:
        student_fname = student["details"]["firstname"].lower()
        student_lname = student["details"]["lastname"].lower()
        if student_fname == fname.lower() and student_lname == lname.lower():
            print("A student with the same first and last name already exists in this section.")
            return False
    newStudent = {
        "studentID": studentID,
        "details": {
            "email":email,
            "password":password,
            "firstname": fname,
            "lastname": lname
        }
    }
    data[program][year][section].append(newStudent)
    print(f"{fname} {lname} enrolled in {program} {year}{section}")
    with open('studentsdatabase.json', 'w') as f:
        json.dump(data, f, indent=2)
    return True

#Enroll process
def fillUpForm():
    try:
        fname=str(input("Enter First Name: "))
        lname=str(input("Enter Last Name: "))
        if fname.isdigit() and lname.isdigit():
            print("Please enter correct information!")
    except:
        print("invalid input! Try Again")
    return fname,lname

    
def Enroll(data: list):
    while True:
        chosenProgram = paginatePrograms()
        if chosenProgram is None:
            print("\nYou have not chosen a program!")
            loading("Cancelling Enrollment")
            break

        year = "1" 
        section = "A" #default A, need checker for available slots in sections
        id = generateID()
        fname, lname = fillUpForm()
        email = generateStudentEmail(lname, fname)

        while True:
            password = input(f"Enter password for {email}: ")
            confirmPass = input("Confirm password: ")
            if password != confirmPass:
                print("Passwords do not match! Try again.")
                continue
            while True:
                print(f"\nDetails:\nID: {id}\nEmail: {email}\nFull Name: {fname} {lname}")
                print(f"Enrolling to: {chosenProgram} {year}A")
                enrollChoice = input("Confirm enrollment [Y/N]: ").strip().lower()
                if enrollChoice == "y":
                    # def enroll(data: list, program, year, section, studentID,email,password, fname, lname):
                    # set_pref("enrollee",{data,programs[chosenProgram],year,section,id,email, password, fname,lname})
                    # set_pref("enrolleeStatus","pending")
                    enrolled=enroll(data,programs[chosenProgram],year,section,id,email, password, fname,lname)
                    # enrollmentStatus=get_pref("enrolleeStatus")
                    
                    # if enrollmentStatus=="pending":
                    #     print("Enrollment is pending")
                    # elif enrollmentStatus=="accepted":
                    #     print("Enrollment is accepted. Please sign-in using your IE")
                    # elif enrollmentStatus=="declined":
                    #     print("We are sorry to inform you that your enrollment was declined.\nSee you next year!")
                    
                    if not enrolled:
                        print("Enrollment Unsuccessful!")
                        set_pref("currentIDNumber",id-1)
                        return
                    print("Enrollment successful!")
                    return  
                elif enrollChoice == "n":
                    set_pref("currentIDNumber",id-1)
                    loading("Cancelling enrollment")
                    return
                else:
                    print("Invalid input! Please enter Y or N.")




def viewclass(data, program, year, section):
    if program in data and year in data[program] and section in data[program][year]:
        print(f"\nClass List: {program} {year}{section}")
        students = data[program][year][section]
        classObj = Class(program, year, section)
        for s in students:
            student = Student(s["studentID"], s["details"]["firstname"], s["details"]["lastname"])
            classObj.addStudent(student)
        classObj.showClassList()
    else:
        print("Class not found.")

import sys
import time
def loading(string):
    sys.stdout.write(string)
    sys.stdout.flush()
    for _ in range(5):
        time.sleep(0.3)
        sys.stdout.write(".")
        sys.stdout.flush()
    print()


def header(text):
    print(f"====={text}=====")


from Programs import programs
programs = programs

def paginatePrograms():
    """Show all programs with pagination of 10 programs per page and return selected index"""
    index = 0
    cap = 10

    while True:
        header("Choose Program")
        end = min(index + cap, len(programs))
        for i in range(index, end):
            print(f"{i + 1}: {programs[i]}")
        
        print("Options:")
        print("[N]ext page | [P]revious page | [E]xit")
        print("[Or enter the number of the program to select it]")

        choice = input("Choose an option: ").strip().lower()

        if choice == 'n' and end < len(programs):
            index += cap
        elif choice == 'p' and index - cap >= 0:
            index -= cap
        elif choice == 'e':
            return None
        elif choice.isdigit():
            selected = int(choice) - 1
            if 0 <= selected < len(programs):
                return selected
            else:
                print("Invalid program number.")
        else:
            print("Invalid option.")



# def main():
#     data = load_data()

#     while True:
#         header("CMU Enrollment System")
#         print("1. View Programs")
#         print("2. Enroll Student")
#         print("3. View Class List")
#         print("4. Exit")
#         choice = input("Select option: ")

#         if choice == "1":
#             paginatePrograms()

#         elif choice == "2":
#             header("Enrollment")
#             paginatePrograms()
#             program = input("Enter Program: ")
#             year = input("Enter Year: ")
#             section = input("Enter Section: ")
#             studentID = input("Enter Student ID: ")
#             fname = input("Enter First name: ")
#             lname = input("Enter Last name: ")
#             enroll(data, program, year, section, studentID, fname, lname)

#         elif choice == "3":
#             header("View Class")
#             showPrograms(data)
#             program = input("Enter Program: ")
#             year = input("Enter Year: ")
#             section = input("Enter Section: ")
#             viewclass(data, program, year, section)

#         elif choice == "4":
#             save_data(data)
#             print("Exiting program...")
#             break

#         elif choice == "5":
#             pass

#         else:
            # print("Invalid option. Try again.")
def evaluateEmail(email:str):
    """Check email type: s=Student, f=Faculty"""
    if not email:
        return -1  # Handle empty input

    first_char = email[0].lower()
    
    if first_char == 's':
        return 1
    elif first_char == 'f':
        return 0
    else:
        return -1

def generateStudentEmail(lname:str,fname:str):
    return f"s.{lname.lower()}.{fname.lower()}@cmu.edu.ph"

def generateFacultyEmail(lname:str,fname:str):
    return f"f.{lname.lower()}.{fname.lower()}@cmu.edu.ph"

def generateID()->int:
    """Generate student ID: start 2025000000"""
    currentID= get_pref("currentIDNumber")
    newIdNumber = currentID+1
    set_pref("currentIDNumber",newIdNumber)
    return newIdNumber

# print(generateID())

# print(generateFacultyEmail("Pulmones", "JanmArc"))

def signIn(data,email,password):
    found = False
    typeCheck=evaluateEmail(email)
    if typeCheck==1: #Student sign n
        for program in data:
            for year in data[program]:
                for section in data[program][year]:
                    students = data[program][year][section]
                    for student in students:
                        details = student["details"]
                        if details["email"] == email and details["password"] == password:
                            print(f"\nWelcome, {details['firstname']} {details['lastname']}!")
                            user_data = {
                                "studentID": student["studentID"],
                                "email": details["email"],
                                "firstname": details["firstname"],
                                "lastname": details["lastname"],
                                "program": program,
                                "year": year,
                                "section": section
                            }
                            set_pref("is_logged_in", True)
                            set_pref("email", details["email"])
                            set_pref("password",details["password"])
                            found = True

                            #Student Dash boiard
                            showStudentDashboard(user_data)
                            break
                        # elif emailType==0:
                        #     print("Faculty Dashboard is still in production!")
                        #     break
                    if found: break
                if found: break
            if found: break

        if not found:
            print("\nInvalid email or password.")
    elif typeCheck==0:#Faculty sign in
        pass 

def showCOR(data:dict):
    print(f"\nCollege: {data["program"]}\nID: {data["studentID"]}\t\tName: {data["firstname"]} {data["lastname"]}\n\nSubjects")
    getSubjects(data["year"])
    now = datetime.datetime.now()
    print(f"\nDate Printed: {now.strftime('%Y-%m-%d %I:%M:%S %p')}")

def showStudentDashboard(data:dict):
    while True:
        header("Student Dashboard")
        print("1. Show C.O.R.\n2. Show Subjects\n3. Logout")

        dash_choice = input("Select an option: ")
        if dash_choice == "3":
            set_pref("is_logged_in", False)
            set_pref("email", "")
            set_pref("password", "")
            print("Logged out successfully.")
            break
        elif dash_choice == "1":
            #show COR of student
            showCOR(data)
        elif dash_choice == "2":
            getSubjects(data["year"])
        else:
            print("Invalid choice. Try again.")