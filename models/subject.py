class Subject:
    def __init__(self, id: int, name: str, code: str, teacher: str):
        self.id = id
        self.name = name
        self.code = code
        self.teacher = teacher

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "teacher": self.teacher,
        }