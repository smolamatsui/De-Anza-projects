import csv

class Student:
    def __init__(self, last_name, first_name, student_id):
        self.first_name = first_name
        self.last_name = last_name
        self.student_id = student_id
    
    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.student_id}"
    
    def __eq__(self, other):
        return (self.first_name, self.last_name, self.student_id) == \
               (other.first_name, other.last_name, other.student_id)
    
    def __lt__(self, other):
        return (self.last_name, self.first_name) < (other.last_name, other.first_name)

class ClassroomList:
    def __init__(self):
        self.students = []
    
    def add_student(self, student):
        self.students.append(student)
    
    def __iter__(self):
        self.current = 0
        return self
    
    def __next__(self):
        if self.current < len(self.students):
            result = self.students[self.current]
            self.current += 1
            return result
        else:
            raise StopIteration
    
    def sort_students(self):
        self.students.sort()

class ClassroomDict:
    def __init__(self):
        self.students_dict = {}
    
    def add_student(self, student):
        self.students_dict[student.student_id] = student
    
    def __iter__(self):
        self.current = iter(sorted(self.students_dict.values(), key=lambda x: x.student_id))
        return self
    
    def __next__(self):
        return next(self.current)

def readfromcsv(filename):
    students = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader) 
        for row in reader:
            if row:  
                last_name, first_name, student_id = row[0], row[1], int(row[2])
                students.append(Student(first_name, last_name, student_id))
    return students

students = readfromcsv('/Users/sophia/Desktop/Programming/simple python/sample_data.csv') # put path to csv file here.


classroom_list = ClassroomList()
for student in students:
    classroom_list.add_student(student)
classroom_list.sort_students()

print("Classroom List (by Name):")
for student in classroom_list:
    print(student)


classroom_dict = ClassroomDict()
for student in students:
    classroom_dict.add_student(student)

print("\nClassroom Dict (by ID):")
for student in classroom_dict:
    print(student)
