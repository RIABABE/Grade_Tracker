import database
from models.grade import Grade


class GradesService:

    def get_all_grades(self):
        return list(database.grades_db.values())

    def get_grade_by_id(self, grade_id: int):
        return database.grades_db.get(grade_id)

    def get_grades_by_student(self, student_id: int):
        return [g for g in database.grades_db.values() if g.student_id == student_id]

    def get_grades_by_subject(self, subject_id: int):
        return [g for g in database.grades_db.values() if g.subject_id == subject_id]

    def create_grade(self, student_id: int, subject_id: int, score: float, term: str):
        global_id = self._next_id()
        grade = Grade(
            id=global_id,
            student_id=student_id,
            subject_id=subject_id,
            score=score,
            term=term,
        )
        database.grades_db[global_id] = grade
        return grade

    def update_grade(self, grade_id: int, score=None, term=None):
        grade = database.grades_db.get(grade_id)
        if not grade:
            return None
        if score is not None:
            grade.score = score
            grade.letter_grade = grade._compute_letter_grade(score)
        if term is not None:
            grade.term = term
        return grade

    def delete_grade(self, grade_id: int):
        return database.grades_db.pop(grade_id, None)

    def get_student_gpa(self, student_id: int):
        grades = self.get_grades_by_student(student_id)
        if not grades:
            return None
        return round(sum(g.score for g in grades) / len(grades), 2)

    def _next_id(self):
        database.grade_id_counter += 1
        return database.grade_id_counter