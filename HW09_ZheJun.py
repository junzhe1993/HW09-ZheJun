import sys
from collections import defaultdict
from prettytable import PrettyTable
try:
    b=open('grades.txt')
    x=open('students.txt')
    o=open('instructors.txt')
except:
    print('File could not open:')
    sys.exit()
else:
    c=defaultdict(list)
    people=defaultdict(int)
    instructor=defaultdict(set)
    instructors_in=defaultdict(list)
    y=list()
    m=list()
    for i in b:
        a=i.strip().split('\t')
        c[a[0]] += [a[1]]
        people[a[1]] += 1
        instructor[a[1]].add(a[3])
    for j in x:
        student=j.strip().split('\t')
        cwid=student[0]
        name=student[1]
        y.append([cwid, name, c[cwid]])
    for os in o:
        instructors= os.strip().split('\t')
        instructors_in[instructors[0]] += [instructors[1],instructors[2]]
    for nb in instructor:
        m.append([list(instructor[nb])[0], instructors_in[list(instructor[nb])[0]][0], instructors_in[list(instructor[nb])[0]][1], nb, people[nb]])
    def pt1(x):
        """define a function return prettytable"""
    
        pt= PrettyTable(field_names=['Cwid', 'Name', 'Completed Courses'])
        for Cwid, Name, CompletedCourses in x:
            pt.add_row([Cwid, Name, CompletedCourses])
        return pt
    def pt2(x):
        """define a function return prettytable"""
    
        pt= PrettyTable(field_names=['Cwid', 'Name', 'Dept', 'Course', 'student'])
        for Cwid, Name, Dept, Course, Student in x:
            pt.add_row([Cwid, Name, Dept, Course, Student])
        return pt
    print(pt2(m))
    print(pt1(y))
        
        
        
        
        