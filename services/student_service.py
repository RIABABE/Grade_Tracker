import database
from models.student import Student


class StudentsService:

    def get_all_students(self):
        return list(database.students_db.values())

    def get_student_by_id(self, student_id: int):
        return database.students_db.get(student_id)

    def create_student(self, first_name: str, last_name: str, age: int, email: str):
        global_id = self._next_id()
        student = Student(
            id=global_id,
            first_name=first_name,
            last_name=last_name,
            age=age,
            email=email,
        )
        database.students_db[global_id] = student
        return student

    def update_student(self, student_id: int, first_name=None, last_name=None, age=None, email=None):
        student = database.students_db.get(student_id)
        if not student:
            return None
        if first_name is not None:
            student.first_name = first_name
        if last_name is not None:
            student.last_name = last_name
        if age is not None:
            student.age = age
        if email is not None:
            student.email = email
        return student

    def delete_student(self, student_id: int):
        return database.students_db.pop(student_id, None)

    def _next_id(self):
        database.student_id_counter += 1
        return database.student_id_counter