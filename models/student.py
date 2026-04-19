class Student:
    def __init__(self, id: int, first_name: str, last_name: str, age: int, email: str):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.email = email

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
        }