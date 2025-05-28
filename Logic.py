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
                print(f"Enrolling to: {programs[chosenProgram]} {year}A")
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
        # Load faculty data
        try:
            with open('faculty.json', 'r') as f:
                faculty_data = json.load(f)
                
            for faculty in faculty_data['faculty']:
                details = faculty['details']
                if details['email'] == email and details['password'] == password:
                    print(f"\nWelcome, Professor {details['firstname']} {details['lastname']}!")
                    user_data = {
                        "facultyID": faculty['facultyID'],
                        "email": details['email'],
                        "firstname": details['firstname'],
                        "lastname": details['lastname'],
                        "department": details['department'],
                        "assignedSubjects": faculty['assignedSubjects']
                    }
                    set_pref("is_logged_in", True)
                    set_pref("email", details['email'])
                    set_pref("password", details['password'])
                    found = True
                    
                    # Show Faculty Dashboard
                    showFacultyDashboard(user_data)
                    break
            
            if not found:
                print("\nInvalid email or password.")
        except FileNotFoundError:
            print("\nFaculty database not found. Please contact system administrator.")
        except Exception as e:
            print(f"\nAn error occurred: {e}")

def showFacultyDashboard(user_data):
    while True:
        header("Faculty Dashboard")
        print(f"ID: {user_data['facultyID']} | Name: {user_data['firstname']} {user_data['lastname']} | Department: {user_data['department']}")
        print("1. View Assigned Classes")
        print("2. View Students in Class")
        print("3. Manage Grades")
        print("4. Assign Subjects to Students")
        print("5. Assign Sections to Students")
        print("6. Logout")

        dash_choice = input("Select an option: ")
        if dash_choice == "6":
            set_pref("is_logged_in", False)
            set_pref("email", "")
            set_pref("password", "")
            print("Logged out successfully.")
            break
        elif dash_choice == "1":
            viewAssignedClasses(user_data)
        elif dash_choice == "2":
            viewStudentsInClass(user_data)
        elif dash_choice == "3":
            manageGrades(user_data)
        elif dash_choice == "4":
            assignSubjectsToStudents(user_data)
        elif dash_choice == "5":
            assignSectionsToStudents(user_data)
        else:
            print("Invalid choice. Try again.")

def assignSubjectsToStudents(faculty_data):
    header("Assign Subjects to Students")
    assigned = faculty_data["assignedSubjects"]
    
    if not assigned:
        print("No classes assigned to you.")
        return
    
    # List all classes where faculty teaches
    print("Select a class:")
    classes = []
    for program in assigned:
        for year in assigned[program]:
            for section in assigned[program][year]:
                class_info = {"program": program, "year": year, "section": section}
                classes.append(class_info)
    
    # Remove duplicates (faculty might teach multiple subjects in same class)
    unique_classes = []
    for c in classes:
        if c not in unique_classes:
            unique_classes.append(c)
    
    for i, class_info in enumerate(unique_classes):
        print(f"{i+1}. {class_info['program']} {class_info['year']}{class_info['section']}")
    
    try:
        choice = int(input("Enter class number (0 to cancel): "))
        if choice == 0:
            return
        
        selected_class = unique_classes[choice-1]
        program = selected_class['program']
        year = selected_class['year']
        section = selected_class['section']
        
        # Load student data
        student_data = load_data()
        
        if (program in student_data and 
            year in student_data[program] and 
            section in student_data[program][year]):
            
            # Get available subjects for this faculty in this class
            available_subjects = []
            for subject in assigned[program][year][section]:
                available_subjects.append(subject)
            
            # Load subject descriptions
            try:
                with open('subjects.json', 'r') as f:
                    subjects_data = json.load(f)
            except FileNotFoundError:
                subjects_data = {}
            
            # Display available subjects
            print(f"\nAvailable subjects for {program} {year}{section}:")
            for i, subject_code in enumerate(available_subjects):
                description = ""
                if year in subjects_data and subject_code in subjects_data[year]:
                    description = subjects_data[year][subject_code]
                print(f"{i+1}. {subject_code}: {description}")
            
            subject_choice = int(input("Select subject to assign (0 to cancel): "))
            if subject_choice == 0:
                return
            
            selected_subject = available_subjects[subject_choice-1]
            
            # Display students in the class
            print(f"\nStudents in {program} {year}{section}:")
            students = student_data[program][year][section]
            
            for i, student in enumerate(students):
                details = student["details"]
                print(f"{i+1}. ID: {student['studentID']} | Name: {details['firstname']} {details['lastname']}")
            
            # Choose students to assign the subject to
            print("\nEnter student numbers to assign this subject to (comma-separated, e.g., 1,3,5)")
            print("Enter 'all' to assign to all students")
            student_choices = input("> ").strip()
            
            # Load student subjects data
            try:
                with open('student_subjects.json', 'r') as f:
                    student_subjects = json.load(f)
            except FileNotFoundError:
                student_subjects = {}
            
            # Initialize structure if needed
            if program not in student_subjects:
                student_subjects[program] = {}
            if year not in student_subjects[program]:
                student_subjects[program][year] = {}
            if section not in student_subjects[program][year]:
                student_subjects[program][year][section] = {}
            
            # Process student choices
            if student_choices.lower() == 'all':
                # Assign to all students
                for student in students:
                    student_id = student['studentID']
                    if student_id not in student_subjects[program][year][section]:
                        student_subjects[program][year][section][student_id] = []
                    
                    if selected_subject not in student_subjects[program][year][section][student_id]:
                        student_subjects[program][year][section][student_id].append(selected_subject)
                
                print(f"\nAssigned {selected_subject} to all students in {program} {year}{section}")
            else:
                try:
                    # Parse comma-separated numbers
                    selected_indices = [int(idx.strip()) - 1 for idx in student_choices.split(',')]
                    
                    # Validate indices
                    valid_indices = [idx for idx in selected_indices if 0 <= idx < len(students)]
                    
                    # Assign subject to selected students
                    for idx in valid_indices:
                        student = students[idx]
                        student_id = student['studentID']
                        
                        if student_id not in student_subjects[program][year][section]:
                            student_subjects[program][year][section][student_id] = []
                        
                        if selected_subject not in student_subjects[program][year][section][student_id]:
                            student_subjects[program][year][section][student_id].append(selected_subject)
                    
                    print(f"\nAssigned {selected_subject} to selected students")
                except ValueError:
                    print("Invalid input format. Please use comma-separated numbers.")
            
            # Save updated student subjects data
            with open('student_subjects.json', 'w') as f:
                json.dump(student_subjects, f, indent=4)
        else:
            print("No students found in this class.")
    except (ValueError, IndexError):
        print("Invalid selection.")
    
    input("\nPress Enter to continue...")


def viewAssignedClasses(faculty_data):
    header("Assigned Classes")
    assigned = faculty_data["assignedSubjects"]
    
    if not assigned:
        print("No classes assigned.")
        return
    
    # Load subject descriptions
    try:
        with open('subjects.json', 'r') as f:
            subjects_data = json.load(f)
    except FileNotFoundError:
        subjects_data = {}
    
    # Display assigned classes by program, year, and section
    for program in assigned:
        print(f"\nProgram: {program}")
        for year in assigned[program]:
            print(f"Year: {year}")
            for section in assigned[program][year]:
                print(f"Section: {section}")
                print("Subjects:")
                for subject_code in assigned[program][year][section]:
                    description = ""
                    if year in subjects_data and subject_code in subjects_data[year]:
                        description = subjects_data[year][subject_code]
                    print(f"  - {subject_code}: {description}")
    
    input("\nPress Enter to continue...")

def viewStudentsInClass(faculty_data):
    header("View Students in Class")
    assigned = faculty_data["assignedSubjects"]
    
    if not assigned:
        print("No classes assigned.")
        return
    
    # List all programs, years, sections where faculty teaches
    print("Select a class:")
    classes = []
    for program in assigned:
        for year in assigned[program]:
            for section in assigned[program][year]:
                for subject in assigned[program][year][section]:
                    class_info = {"program": program, "year": year, "section": section, "subject": subject}
                    classes.append(class_info)
    
    for i, class_info in enumerate(classes):
        print(f"{i+1}. {class_info['program']} {class_info['year']}{class_info['section']} - {class_info['subject']}")
    
    try:
        choice = int(input("Enter class number (0 to cancel): "))
        if choice == 0:
            return
        
        selected_class = classes[choice-1]
        
        # Load student data
        student_data = load_data()
        
        if (selected_class['program'] in student_data and 
            selected_class['year'] in student_data[selected_class['program']] and 
            selected_class['section'] in student_data[selected_class['program']][selected_class['year']]):
            
            print(f"\nStudents in {selected_class['program']} {selected_class['year']}{selected_class['section']} - {selected_class['subject']}:")
            students = student_data[selected_class['program']][selected_class['year']][selected_class['section']]
            
            for i, student in enumerate(students):
                details = student["details"]
                print(f"{i+1}. ID: {student['studentID']} | Name: {details['firstname']} {details['lastname']}")
        else:
            print("No students found in this class.")
    except (ValueError, IndexError):
        print("Invalid selection.")
    
    input("\nPress Enter to continue...")

def assignSectionsToStudents(faculty_data):
    header("Assign Sections to Students")
    assigned = faculty_data["assignedSubjects"]
    
    if not assigned:
        print("No classes assigned to you.")
        return
    
    # List all classes where faculty teaches
    print("Select a class:")
    classes = []
    for program in assigned:
        for year in assigned[program]:
            for section in assigned[program][year]:
                class_info = {"program": program, "year": year, "section": section}
                classes.append(class_info)
    
    # Remove duplicates (faculty might teach multiple subjects in same class)
    unique_classes = []
    for c in classes:
        if c not in unique_classes:
            unique_classes.append(c)
    
    for i, class_info in enumerate(unique_classes):
        print(f"{i+1}. {class_info['program']} {class_info['year']}{class_info['section']}")
    
    try:
        choice = int(input("Enter class number (0 to cancel): "))
        if choice == 0:
            return
        
        selected_class = unique_classes[choice-1]
        program = selected_class['program']
        year = selected_class['year']
        section = selected_class['section']
        
        # Load student data
        student_data = load_data()
        
        if (program in student_data and 
            year in student_data[program] and 
            section in student_data[program][year]):
            
            # Display students in the class
            print(f"\nStudents in {program} {year}{section}:")
            students = student_data[program][year][section]
            
            for i, student in enumerate(students):
                details = student["details"]
                print(f"{i+1}. ID: {student['studentID']} | Name: {details['firstname']} {details['lastname']}")
            
            # Choose students to reassign
            print("\nEnter student numbers to reassign to a different section (comma-separated, e.g., 1,3,5)")
            student_choices = input("> ").strip()
            
            try:
                # Parse comma-separated numbers
                selected_indices = [int(idx.strip()) - 1 for idx in student_choices.split(',')]
                
                # Validate indices
                valid_indices = [idx for idx in selected_indices if 0 <= idx < len(students)]
                
                if not valid_indices:
                    print("No valid student selections.")
                    input("\nPress Enter to continue...")
                    return
                
                # Get available sections for this program and year
                available_sections = []
                if program in student_data and year in student_data[program]:
                    available_sections = list(student_data[program][year].keys())
                
                if not available_sections:
                    print(f"No sections found for {program} {year}.")
                    input("\nPress Enter to continue...")
                    return
                
                # Display available sections
                print(f"\nAvailable sections for {program} {year}:")
                for i, sec in enumerate(available_sections):
                    print(f"{i+1}. Section {sec}")
                
                # Select target section
                target_section_idx = int(input("\nSelect target section (0 to cancel): "))
                if target_section_idx == 0:
                    return
                
                target_section = available_sections[target_section_idx-1]
                
                # Confirm if target section is different from current section
                if target_section == section:
                    print("Cannot reassign to the same section.")
                    input("\nPress Enter to continue...")
                    return
                
                # Move selected students to the target section
                students_moved = []
                for idx in valid_indices:
                    student = students[idx]
                    student_id = student['studentID']
                    student_name = f"{student['details']['firstname']} {student['details']['lastname']}"
                    
                    # Add student to target section
                    if student not in student_data[program][year][target_section]:
                        student_data[program][year][target_section].append(student)
                        students_moved.append(f"ID: {student_id} | Name: {student_name}")
                
                # Remove moved students from original section
                for idx in sorted(valid_indices, reverse=True):
                    del student_data[program][year][section][idx]
                
                # Save updated student data
                save_data(student_data)
                
                # Display results
                print(f"\nSuccessfully moved {len(students_moved)} student(s) from Section {section} to Section {target_section}:")
                for student_info in students_moved:
                    print(f"- {student_info}")
                
                # Update student_subjects.json if it exists
                try:
                    with open('student_subjects.json', 'r') as f:
                        student_subjects = json.load(f)
                    
                    # Move subject assignments for transferred students
                    if (program in student_subjects and 
                        year in student_subjects[program] and 
                        section in student_subjects[program][year]):
                        
                        # Initialize target section if needed
                        if target_section not in student_subjects[program][year]:
                            student_subjects[program][year][target_section] = {}
                        
                        # Move each student's subject assignments
                        for student_info in students_moved:
                            student_id = student_info.split("|")[0].strip().replace("ID: ", "")
                            
                            if student_id in student_subjects[program][year][section]:
                                # Copy assignments to new section
                                student_subjects[program][year][target_section][student_id] = \
                                    student_subjects[program][year][section][student_id]
                                
                                # Remove from old section
                                del student_subjects[program][year][section][student_id]
                        
                        # Save updated student subjects data
                        with open('student_subjects.json', 'w') as f:
                            json.dump(student_subjects, f, indent=4)
                except FileNotFoundError:
                    pass
                
                # Update grades.json if it exists
                try:
                    with open('grades.json', 'r') as f:
                        grades_data = json.load(f)
                    
                    # Move grade records for transferred students
                    if (program in grades_data and 
                        year in grades_data[program] and 
                        section in grades_data[program][year]):
                        
                        # Initialize target section if needed
                        if target_section not in grades_data[program][year]:
                            grades_data[program][year][target_section] = {}
                        
                        # For each subject in the original section
                        for subject_code in grades_data[program][year][section]:
                            # Initialize subject in target section if needed
                            if subject_code not in grades_data[program][year][target_section]:
                                grades_data[program][year][target_section][subject_code] = {}
                            
                            # Move each student's grades
                            for student_info in students_moved:
                                student_id = student_info.split("|")[0].strip().replace("ID: ", "")
                                
                                if student_id in grades_data[program][year][section][subject_code]:
                                    # Copy grades to new section
                                    grades_data[program][year][target_section][subject_code][student_id] = \
                                        grades_data[program][year][section][subject_code][student_id]
                                    
                                    # Remove from old section
                                    del grades_data[program][year][section][subject_code][student_id]
                        
                        # Save updated grades data
                        with open('grades.json', 'w') as f:
                            json.dump(grades_data, f, indent=4)
                except FileNotFoundError:
                    pass
                
            except ValueError:
                print("Invalid input format. Please use comma-separated numbers.")
        else:
            print("No students found in this class.")
    except (ValueError, IndexError):
        print("Invalid selection.")
    
    input("\nPress Enter to continue...")

def manageGrades(faculty_data):
    header("Manage Student Grades")
    assigned = faculty_data["assignedSubjects"]
    
    if not assigned:
        print("No classes assigned to you.")
        return
    
    # List all classes where faculty teaches
    print("Select a class to manage grades:")
    classes = []
    for program in assigned:
        for year in assigned[program]:
            for section in assigned[program][year]:
                for subject in assigned[program][year][section]:
                    class_info = {"program": program, "year": year, "section": section, "subject": subject}
                    classes.append(class_info)
    
    for i, class_info in enumerate(classes):
        print(f"{i+1}. {class_info['program']} {class_info['year']}{class_info['section']} - {class_info['subject']}")
    
    try:
        choice = int(input("Enter class number (0 to cancel): "))
        if choice == 0:
            return
        
        selected_class = classes[choice-1]
        
        # Load student data
        student_data = load_data()
        
        # Load grades data
        try:
            with open('grades.json', 'r') as f:
                grades_data = json.load(f)
        except FileNotFoundError:
            grades_data = {}
        
        # Initialize grades structure if needed
        program = selected_class['program']
        year = selected_class['year']
        section = selected_class['section']
        subject = selected_class['subject']
        
        if program not in grades_data:
            grades_data[program] = {}
        if year not in grades_data[program]:
            grades_data[program][year] = {}
        if section not in grades_data[program][year]:
            grades_data[program][year][section] = {}
        if subject not in grades_data[program][year][section]:
            grades_data[program][year][section][subject] = {}
        
        # Get students in this class
        if (program in student_data and year in student_data[program] and section in student_data[program][year]):
            students = student_data[program][year][section]
            
            while True:
                header(f"Grades for {program} {year}{section} - {subject}")
                print("\nStudent List:")
                
                for i, student in enumerate(students):
                    student_id = student['studentID']
                    details = student["details"]
                    
                    # Initialize student grades if not exists
                    if student_id not in grades_data[program][year][section][subject]:
                        grades_data[program][year][section][subject][student_id] = {
                            "midterm": 0,
                            "finals": 0,
                            "average": 0,
                            "remarks": "Not yet graded"
                        }
                    
                    grade_info = grades_data[program][year][section][subject][student_id]
                    print(f"{i+1}. ID: {student_id} | Name: {details['firstname']} {details['lastname']} | "
                          f"Midterm: {grade_info['midterm']} | Finals: {grade_info['finals']} | "
                          f"Average: {grade_info['average']} | Remarks: {grade_info['remarks']}")
                
                print("\nOptions:")
                print("1. Update student grade")
                print("2. Back to Faculty Dashboard")
                
                grade_choice = input("Select option: ")
                
                if grade_choice == "1":
                    try:
                        student_num = int(input("Enter student number: "))
                        if 1 <= student_num <= len(students):
                            student = students[student_num-1]
                            student_id = student['studentID']
                            
                            print(f"\nUpdating grades for {student['details']['firstname']} {student['details']['lastname']}")
                            
                            try:
                                print("\nEnter grades using the 1.0-5.0 scale:")
                                print("1.0-3.0 (1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0) = Pass")
                                print("4.0 = INC, 5.0 and others = Failed")
                                midterm = float(input("Enter midterm grade (1.0-5.0): "))
                                finals = float(input("Enter finals grade (1.0-5.0): "))
                                
                                if 1.0 <= midterm <= 5.0 and 1.0 <= finals <= 5.0:
                                    # Calculate average of the grade points
                                    average = (midterm + finals) / 2
                                    grade_point = round(average, 1)  # Round to 1 decimal place
                                    remarks="Not yet graded"
                                    # Determine remarks based on the new grading system
                                    # Passing grades: 1.0, 1.25, 1.50, 1.75, 2.0, 2.25, 2.50, 2.75, 3.0
                                    passing_grades = [1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0]
                                    if 1.0 <= grade_point <= 3.0:
                                        remarks = "Passed"
                                    elif 5> grade_point >= 4.0:
                                        remarks = "Removal"
                                    else:
                                        remarks = "Failed"
                                    
                                    # Update grades
                                    grades_data[program][year][section][subject][student_id] = {
                                        "midterm": midterm,
                                        "finals": finals,
                                        "average": round(average, 1),  # Round to 1 decimal place
                                        "grade_point": grade_point,
                                        "remarks": remarks
                                    }
                                    
                                    # Save grades to file
                                    with open('grades.json', 'w') as f:
                                        json.dump(grades_data, f, indent=4)
                                    
                                    print("Grades updated successfully.")
                                else:
                                    print("Invalid grade range. Grades must be between 1.0 and 5.0.")
                            except ValueError:
                                print("Invalid input. Please enter numeric grades.")
                        else:
                            print("Invalid student number.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                
                elif grade_choice == "2":
                    break
                
                else:
                    print("Invalid choice.")
        else:
            print("No students found in this class.")
    
    except (ValueError, IndexError):
        print("Invalid selection.")
    
    input("\nPress Enter to continue...")


def showCOR(data:dict):
    print(f"\nCollege: {data['program']}\nID: {data['studentID']}\t\tName: {data['firstname']} {data['lastname']}\n\nSubjects")
    
    # Check if student has individually assigned subjects
    has_individual_subjects = False
    try:
        with open('student_subjects.json', 'r') as f:
            student_subjects = json.load(f)
            
        program = data['program']
        year = data['year']
        section = data['section']
        student_id = data['studentID']
        
        if (program in student_subjects and 
            year in student_subjects[program] and 
            section in student_subjects[program][year] and 
            student_id in student_subjects[program][year][section]):
            
            # Load subject descriptions
            with open('subjects.json', 'r') as f:
                subjects_data = json.load(f)
            
            # Display individually assigned subjects
            assigned_subjects = student_subjects[program][year][section][student_id]
            print("Assigned Subjects:")
            for subject_code in assigned_subjects:
                description = ""
                if year in subjects_data and subject_code in subjects_data[year]:
                    description = subjects_data[year][subject_code]
                print(f"|Code: {subject_code}\t| {description}")
            
            has_individual_subjects = True
    except (FileNotFoundError, KeyError):
        pass
    
    # If no individually assigned subjects, show all subjects for the year
    if not has_individual_subjects:
        print("Default Year Subjects:")
        getSubjects(data["year"])
    
    now = datetime.datetime.now()
    print(f"\nDate Printed: {now.strftime('%Y-%m-%d %I:%M:%S %p')}")
    
    # Add note about subject assignment
    if not has_individual_subjects:
        print("\nNote: Forgery of grades is a violation of the University's Code of Conduct.")
    else:
        # Check for grades
        try:
            with open('grades.json', 'r') as f:
                grades_data = json.load(f)
                
            program = data['program']
            year = data['year']
            section = data['section']
            student_id = data['studentID']
            
            has_grades = False
            print("\nGrades:")
            for subject_code in assigned_subjects:
                if (program in grades_data and 
                    year in grades_data[program] and 
                    section in grades_data[program][year] and 
                    subject_code in grades_data[program][year][section] and 
                    student_id in grades_data[program][year][section][subject_code]):
                    
                    grade_info = grades_data[program][year][section][subject_code][student_id]
                    print(f"{subject_code}: Midterm: {grade_info['midterm']}, Finals: {grade_info['finals']}, Average: {grade_info['average']}, Remarks: {grade_info['remarks']}")
                    has_grades = True
            
            if not has_grades:
                print("No grades recorded yet.")
        except (FileNotFoundError, KeyError):
            print("No grades recorded yet.")


def showStudentGrades(data:dict):
    header("Student Grades")
    
    program = data['program']
    year = data['year']
    section = data['section']
    student_id = str(data['studentID'])
    
    # First, try to get subjects from student_subjects.json
    try:
        with open('student_subjects.json', 'r') as f:
            student_subjects = json.load(f)
            
        if (program in student_subjects and 
            year in student_subjects[program] and 
            section in student_subjects[program][year] and 
            student_id in student_subjects[program][year][section]):
            
            assigned_subjects = student_subjects[program][year][section][student_id]
            has_assigned_subjects = True
        else:
            has_assigned_subjects = False
    except FileNotFoundError:
        has_assigned_subjects = False
    
    # If no individually assigned subjects, get all subjects for the year
    if not has_assigned_subjects:
        try:
            with open('subjects.json', 'r') as f:
                subjects_data = json.load(f)
            
            if year in subjects_data:
                assigned_subjects = list(subjects_data[year].keys())
            else:
                assigned_subjects = []
        except FileNotFoundError:
            assigned_subjects = []
    
    # Load grades data
    try:
        with open('grades.json', 'r') as f:
            grades_data = json.load(f)
        
        has_grades = False
        print(f"\nGrades for {data['firstname']} {data['lastname']} (ID: {student_id}):\n")
        print("-" * 90)
        print(f"{'Subject':<10} | {'Description':<30} | {'Midterm':<7} | {'Finals':<7} | {'Average':<7} | {'Remarks':<10}")
        print("-" * 90)
        
        # Try to load subject descriptions
        try:
            with open('subjects.json', 'r') as f:
                subjects_data = json.load(f)
        except FileNotFoundError:
            subjects_data = {}
        
        for subject_code in assigned_subjects:
            # Get subject description
            description = ""
            if year in subjects_data and subject_code in subjects_data[year]:
                description = subjects_data[year][subject_code]
            
            # Check if grade exists
            if (program in grades_data and 
                year in grades_data[program] and 
                section in grades_data[program][year] and 
                subject_code in grades_data[program][year][section] and 
                student_id in grades_data[program][year][section][subject_code]):
                
                grade_info = grades_data[program][year][section][subject_code][student_id]
                midterm = grade_info.get('midterm', 0)
                finals = grade_info.get('finals', 0)
                average = grade_info.get('average', 0)
                remarks = grade_info.get('remarks', 'Not yet graded')
                
                print(f"{subject_code:<10} | {description[:30]:<30} | {midterm:<7} | {finals:<7} | {average:<7} | {remarks:<10}")
                has_grades = True
            else:
                print(f"{subject_code:<10} | {description[:30]:<30} | {'-':<7} | {'-':<7} | {'-':<7} | {'Not graded':<10}")
        
        print("-" * 90)
        
        # Show summary of passed/failed subjects
        if has_grades:
            passed_count = 0
            failed_count = 0
            inc_count = 0
            not_graded_count = 0
            
            for subject_code in assigned_subjects:
                if (program in grades_data and 
                    year in grades_data[program] and 
                    section in grades_data[program][year] and 
                    subject_code in grades_data[program][year][section] and 
                    student_id in grades_data[program][year][section][subject_code]):
                    
                    remarks = grades_data[program][year][section][subject_code][student_id].get('remarks', 'Not yet graded')
                    if remarks == 'Passed':
                        passed_count += 1
                    elif remarks == 'Failed':
                        failed_count += 1
                    elif remarks == 'Removal':
                        inc_count += 1
                    else:
                        not_graded_count += 1
            
            print(f"\nSummary: {passed_count} Passed, {failed_count} Failed, {inc_count} Removal, {not_graded_count} Not Graded")
        else:
            print("\nNo grades have been recorded for your subjects yet.")
    except FileNotFoundError:
        print("\nNo grades have been recorded in the system yet.")
    
    input("\nPress Enter to continue...")

def showStudentDashboard(data:dict):
    while True:
        header("Student Dashboard")
        print("1. Show C.O.R.\n2. Show Subjects\n3. Show Grades\n4. Logout")

        dash_choice = input("Select an option: ")
        if dash_choice == "4":
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
        elif dash_choice == "3":
            # Show student grades
            showStudentGrades(data)
        elif dash_choice == "4":
            # Account option - placeholder for now
            print("\nAccount management features coming soon!")
            input("\nPress Enter to continue...")
        else:
            print("Invalid choice. Try again.")