import pandas as pd
from student import Student
from gcloud import SheetHandler

def main():
    gcloud = SheetHandler()
    class_data = gcloud.get_sheet_as_dataframe()

    lectures = gcloud.get_lectures_number()

    students = transform_into_students(class_data, lectures)

    Student.evaluate_students(students)

    students_status = [student.get_status() for student in students]
    students_final_marks = [student.get_marks_for_approval() for student in students]

    students_status = Student.get_students_status(students)
    students_final_marks = Student.get_students_marks_for_approval(students)

    class_data["Situação"] = students_status
    class_data["Nota para Aprovação Final"] = students_final_marks

    gcloud.update_status_column(students_status)
    gcloud.update_marks_approval_column(students_final_marks)


if (__name__ == "__main__"): main()
