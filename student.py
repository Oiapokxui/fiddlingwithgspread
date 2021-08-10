from enum import Enum

class Student:
    """ 
    Represents a Student of a certain course and processes some 
    information about them.  

    ...
    Attributes:
        name (str) : Name of student.
        registration_num (int) : Number of registration assigned to this object.
        absences (int) : Number of lectures missed by the student.
        lectures (int) : Total number of lectures of the course.
        marks (float) : List of marks obtained by the student. 
                Each mark is in range [0; 100]
        marks_for_approval (float) : Marks needed for the approval of the 
                student, in case his status is Statuses_Enum.FINAL_EXAM
        statuses_dict (str dict) : Dictionary of all status and its 
                portuguese translation 
        Statuses_Enum (enum.Enum) : A Enum of all the possible status of a student. 
        status (enum.Enum member) : This student specific current status.

    """
    name = ""
    registration_num = 0
    absences = 0
    lectures = 0
    marks = [0, 0, 0]
    marks_for_approval = 0
    statuses_dict = { 
            "FAILED_ABSENCE" : "Reprovado por Falta", 
            "FAILED_MARKS"   : "Reprovado por Nota", 
            "FINAL_EXAM"     : "Exame Final", 
            "PASSED"         : "Aprovado", 
            "TO_EVALUATE"    : "Nao Avaliado"
            }
    Statuses_Enum = Enum("Final Status", statuses_dict)
    status = Statuses_Enum.TO_EVALUATE


    @staticmethod
    def are_all_student_type(students):
        """ Checks if all elements of list students are instances of Student
        """
        return all([isinstance(obj, Student) for obj in students])


    @staticmethod
    def evaluate_students(students):
        """ Calls self.evaluate() for every student in students list.
        """
        print("Evaluating all students")
        if(Student.are_all_student_type(students)):
            for student in students : student.evaluate()
        else:
            print("Not all objects in students list are of type Student")


    @staticmethod
    def get_students_marks_for_approval(students):
        """ Save each student's marks_for_approval field in a list.
        """
        print("Grouping all students' marks for approval")
        if(Student.are_all_student_type(students)):
            return [student.get_marks_for_approval() for student in students]
        else:
            print("Not all objects in students list are of type Student")


    @staticmethod
    def get_students_status(students):
        """ Save each student's status field in a list.
        """
        print("Grouping all students' status")
        if(Student.are_all_student_type(students)):
            return [student.get_status() for student in students]
        else:
            print("Not all objects in students list are of type Student")
            


    def __init__(self, lectures, registration_num, name, absences=0, *marks):
        """
        Constructs a student if name is not None and registration_num 
        and absences are positive.
        """
        if (not name or registration_num < 0 or absences < 0): return
        self.name = name
        self.registration_num = registration_num
        self.lectures = lectures
        self.absences = absences
        self.marks = marks


    def average(self):
        """ Calculates the average of all marks then normalizes it to range [0; 10]
        """
        if (self.marks == []) :
            print("Marks were not added yet", stderr)
            return None
        return sum(self.marks)/(len(self.marks) * 10)


    def calculate_marks_for_approval(self):
        """ This is obtained by the inequation 5 <= 0.5(self.average() - x) 
        """
        from math import ceil
        return ceil(10 - self.average())


    def failed_due_absence(self):
        """ Checks if student has skipped more lectures than allowed. 
        """
        failed = self.absences > (0.25 * float(self.lectures))
        return failed


    def evaluate(self):
        """ Given this student current fields, assigns a status to the student. 
        """
        if (self.failed_due_absence()) : 
            self.status = self.Statuses_Enum.FAILED_ABSENCE
            return

        avg = self.average()

        if(avg is None): return 

        if (avg >= 7) : 
            self.status = self.Statuses_Enum.PASSED
        elif (5 <= avg and avg < 7) :
            self.status = self.Statuses_Enum.FINAL_EXAM
            self.marks_for_approval = self.calculate_marks_for_approval()
        else :
            self.status = self.Statuses_Enum.FAILED_MARKS


    def get_marks_for_approval(self):
        return self.marks_for_approval


    def get_status(self):
        return self.status.value
