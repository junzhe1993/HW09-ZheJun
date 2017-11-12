import sys
from collections import defaultdict
from prettytable import PrettyTable
import unittest

class Repository:
    """Read the student,instructor, grade and major files"""
    
    directory_student = 'students.txt'
    directory_instructor = 'instructors.txt'
    directory_grade = 'grades.txt'
    directory_major = 'majors.txt'
    count = 0
    
    for i in [directory_student, directory_instructor, directory_grade, directory_major]:
        try:
            count += 1
            a = open(i)
        except:
            print('FIle could not open:', i)
            sys.exit()
        else:
            with a:
                if count == 1:
                    student_rows = a.readlines()
                elif count == 2:
                    instructor_rows = a.readlines()
                elif count==3:
                    grade_rows = a.readlines()
                else:
                    major_rows = a.readlines()  

class major:
    """store the data of the major"""
    
    def __init__(self, Dept):
        
        major_course = defaultdict(list)
        
        for i in Repository.major_rows:
            a=i.strip().split('\t')
            if Dept == a[0]:
                    major_course[a[1]] += [a[2]]
        
        self.major_course = major_course


class student:
    """store the data of the student"""
    
    def __init__(self, student_id):
        
        completed_courses = defaultdict(list)
        course_grade = defaultdict(str)
        Remaining_required = list()
        Remaining_electives = list()
        count = 0

        
        for i in Repository.grade_rows:
            a = i.split('\t')
            completed_courses[a[0]] += [a[1]]
            if student_id == a[0]:
                course_grade[a[1]] += a[2]
            
        self.course = completed_courses[(student_id)]
        
        for j in Repository.student_rows:
            b = j.strip().split('\t')
            if student_id == b[0]:
                self.cwid = b[0]
                self.name = b[1]
                self.Dept = b[2]
                for o in Repository.major_rows:
                    k= o.strip().split('\t')
                    if b[2] == k[0]:
                        if k[1] == 'R':
                            if course_grade[k[2]] not in ['A','A-','B+','B','B-','C+','C']:
                                Remaining_required.append(k[2])
                        elif k[1] == 'E':
                            if course_grade[k[2]] not in ['A','A-','B+','B','B-','C+','C']:
                                Remaining_electives.append(k[2])
                            else:
                                count += 1 
        
        if count >= 1:
             Remaining_electives = list() 
                            
        
        self.Remaining_required = sorted(Remaining_required)
        self.Remaining_electives = sorted(Remaining_electives)
            
                

class instructor:
    """store the data of instructor"""
    
    def __init__(self, instructor_id):
        
        course_people = defaultdict(int)
        
        for i in Repository.instructor_rows:
            a = i.strip().split('\t')
            if instructor_id == a[0]:
                self.cwid = a[0]
                self.name = a[1]
                self.Dept = a[2]
        
        for j in Repository.grade_rows:
            b = j.strip().split('\t')
            if instructor_id == b[3]:
                course_people[b[1]] += 1
        
        self.course_people = course_people
        
        
def main():
    """prettytable"""
    
    pt_student = PrettyTable(field_names=['Cwid', 'Name', 'Completed Courses', 'Remaining Required', 'Remaining Electives'])
    pt_instructor = PrettyTable(field_names=['Cwid', 'Name', 'Dept', 'Course', 'student'])
    pt_major = PrettyTable(field_names = ['Dept', 'Required', 'Electives'])
    st = list()
    ins = list()
    cnt = list()
    
    for i in Repository.student_rows:
        a = i.strip().split('\t')
        st.append([student(a[0]).cwid, student(a[0]).name, student(a[0]).course, student(a[0]).Remaining_required, student(a[0]).Remaining_electives])
    
    for Cwid, Name, CompletedCourses, RemainingRequired, RemainingElectives in st:
        pt_student.add_row([Cwid, Name, CompletedCourses, RemainingRequired, RemainingElectives])
    
    for j in Repository.grade_rows:
        b = j.strip().split('\t')
        if b[1] not in cnt:
            cnt.append(b[1])
            ins.append([b[3], instructor(b[3]).name, instructor(b[3]).Dept, b[1], instructor(b[3]).course_people[b[1]]])
    
    for Cwid, Name, Dept, Course, Student in ins:
        pt_instructor.add_row([Cwid, Name, Dept, Course, Student])
        
    for Dept, Required, Electives in [['SFEN', major('SFEN').major_course['R'], major('SFEN').major_course['E']], ['SYEN', major('SYEN').major_course['R'], major('SYEN').major_course['E']]]:
        pt_major.add_row([ Dept, Required, Electives])
        
    print(pt_student)
    print(pt_instructor)
    print(pt_major)

class Data_Test(unittest.TestCase):

    def test_repository(self):
        """test repository """
        self.assertEqual( Repository.student_rows[0].strip().split('\t')[0], '10103')

    def test_student(self):
        """test Students """
        Student = student('10103')
        self.assertEqual(Student.name, 'Baldwin, C')
        self.assertEqual(Student.Dept, 'SFEN')
        self.assertEqual(Student.course, ['SSW 567', 'SSW 564', 'SSW 687', 'CS 501'])
        self.assertEqual(Student.Remaining_required, ['SSW 533', 'SSW 540', 'SSW 555', 'SSW 565', 'SSW 690', 'SSW 695'])
        self.assertEqual(Student.Remaining_electives, [])

    def test_instructors(self):
        """test Instructors """
        Instructor = instructor('98763')
        self.assertEqual(Instructor.name, 'Newton, I')
        self.assertEqual(Instructor.Dept, 'SFEN')
        self.assertEqual(Instructor.course_people, {'SSW 555': 1, 'SSW 689': 1})
        
    def test_major(self):
        """test major"""
        
        Major = major('SFEN')
        self.assertEqual(Major.major_course, {'E': ['CS 501', 'CS 513', 'CS 545'], 'R': ['SSW 540', 'SSW 564', 'SSW 565', 'SSW 555', 'SSW 567', 'SSW 533', 'SSW 690', 'SSW 695']})

if __name__=='__main__':
    main()
    unittest.main(exit=False, verbosity=2)

    
      
                
           
                
        
        
        
        
        


            