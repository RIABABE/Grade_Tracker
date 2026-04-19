import database
from models.subject import Subject


class SubjectsService:

    def get_all_subjects(self):
        return list(database.subjects_db.values())

    def get_subject_by_id(self, subject_id: int):
        return database.subjects_db.get(subject_id)

    def create_subject(self, name: str, code: str, teacher: str):
        global_id = self._next_id()
        subject = Subject(id=global_id, name=name, code=code, teacher=teacher)
        database.subjects_db[global_id] = subject
        return subject

    def update_subject(self, subject_id: int, name=None, code=None, teacher=None):
        subject = database.subjects_db.get(subject_id)
        if not subject:
            return None
        if name is not None:
            subject.name = name
        if code is not None:
            subject.code = code
        if teacher is not None:
            subject.teacher = teacher
        return subject

    def delete_subject(self, subject_id: int):
        return database.subjects_db.pop(subject_id, None)

    def _next_id(self):
        database.subject_id_counter += 1
        return database.subject_id_counter