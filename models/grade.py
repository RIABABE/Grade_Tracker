class Grade:
    def __init__(self, id: int, student_id: int, subject_id: int, score: float, term: str):
        self.id = id
        self.student_id = student_id
        self.subject_id = subject_id
        self.score = score
        self.term = term
        self.letter_grade = self._compute_letter_grade(score)

    def _compute_letter_grade(self, score: float) -> str:
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "subject_id": self.subject_id,
            "score": self.score,
            "letter_grade": self.letter_grade,
            "term": self.term,
        }