#Imports
import json

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

class Student:
    def __init__(self, ID, fname, lname):
        self.ID = ID
        self.fname = fname
        self.lname = lname

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

def addStudent(data, program, year, section, studentID, firstname, lastname):
    if program in data and year in data[program] and section in data[program][year]:
        for student in data[program][year][section]:
            if student["studentID"] == studentID:
                print(f"Student {studentID} already exists in {program} {year}{section}")
                return
        
        student = {
            "studentID": studentID,"details": 
            {
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
        print("⚠️ Invalid program/year.")

def enroll(data, program, year, section, studentID, fname, lname):
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
    new_student = {
        "studentID": studentID,
        "details": {"firstname": fname, "lastname": lname}
    }
    data[program][year][section].append(new_student)
    print(f"{fname} {lname} enrolled in {program} {year}{section}")

def viewclass(data, program, year, section):
    if program in data and year in data[program] and section in data[program][year]:
        print(f"\nClass List: {program} {year}{section}")
        students = data[program][year][section]
        class_obj = Class(program, year, section)
        for s in students:
            student = Student(s["studentID"], s["details"]["firstname"], s["details"]["lastname"])
            class_obj.addStudent(student)
        class_obj.showClassList()
    else:
        print("Class not found.")