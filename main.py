from fastapi import FastAPI, status, HTTPException, Body
from services.student_service import StudentsService
from services.subject_service import SubjectsService
from services.grade_service import GradesService

student_service = StudentsService()
subject_service = SubjectsService()
grade_service = GradesService()

app = FastAPI(title="Student Grade Tracker API")


# ──────────────────────────────────────────────
# ROOT
# ──────────────────────────────────────────────

@app.get("/")
def home():
    return {"message": "Welcome to the Student Grade Tracker API"}


# ──────────────────────────────────────────────
# STUDENTS
# ──────────────────────────────────────────────

@app.get("/students", status_code=status.HTTP_200_OK)
def fetch_students():
    students = student_service.get_all_students()
    if not students:
        raise HTTPException(status_code=404, detail="No students found")
    return [s.to_dict() for s in students]


@app.get("/students/{student_id}", status_code=status.HTTP_200_OK)
def fetch_student(student_id: int):
    student = student_service.get_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail=f"Student {student_id} not found")
    return student.to_dict()


@app.post("/students", status_code=status.HTTP_201_CREATED)
def create_student(body: dict = Body(...)):
    first_name = body.get("first_name")
    last_name  = body.get("last_name")
    age        = body.get("age")
    email      = body.get("email")

    if not all([first_name, last_name, age, email]):
        raise HTTPException(status_code=400, detail="first_name, last_name, age, and email are required")

    new_student = student_service.create_student(
        first_name=first_name,
        last_name=last_name,
        age=age,
        email=email,
    )
    return new_student.to_dict()


@app.put("/students/{student_id}", status_code=status.HTTP_200_OK)
def update_student(student_id: int, body: dict = Body(...)):
    updated = student_service.update_student(
        student_id=student_id,
        first_name=body.get("first_name"),
        last_name=body.get("last_name"),
        age=body.get("age"),
        email=body.get("email"),
    )
    if not updated:
        raise HTTPException(status_code=404, detail=f"Student {student_id} not found")
    return updated.to_dict()


@app.delete("/students/{student_id}", status_code=status.HTTP_200_OK)
def delete_student(student_id: int):
    deleted = student_service.delete_student(student_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Student {student_id} not found")
    return {"message": f"Student {student_id} deleted successfully"}


# ──────────────────────────────────────────────
# SUBJECTS
# ──────────────────────────────────────────────

@app.get("/subjects", status_code=status.HTTP_200_OK)
def fetch_subjects():
    subjects = subject_service.get_all_subjects()
    if not subjects:
        raise HTTPException(status_code=404, detail="No subjects found")
    return [s.to_dict() for s in subjects]


@app.get("/subjects/{subject_id}", status_code=status.HTTP_200_OK)
def fetch_subject(subject_id: int):
    subject = subject_service.get_subject_by_id(subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail=f"Subject {subject_id} not found")
    return subject.to_dict()


@app.post("/subjects", status_code=status.HTTP_201_CREATED)
def create_subject(body: dict = Body(...)):
    name    = body.get("name")
    code    = body.get("code")
    teacher = body.get("teacher")

    if not all([name, code, teacher]):
        raise HTTPException(status_code=400, detail="name, code, and teacher are required")

    new_subject = subject_service.create_subject(name=name, code=code, teacher=teacher)
    return new_subject.to_dict()


@app.put("/subjects/{subject_id}", status_code=status.HTTP_200_OK)
def update_subject(subject_id: int, body: dict = Body(...)):
    updated = subject_service.update_subject(
        subject_id=subject_id,
        name=body.get("name"),
        code=body.get("code"),
        teacher=body.get("teacher"),
    )
    if not updated:
        raise HTTPException(status_code=404, detail=f"Subject {subject_id} not found")
    return updated.to_dict()


@app.delete("/subjects/{subject_id}", status_code=status.HTTP_200_OK)
def delete_subject(subject_id: int):
    deleted = subject_service.delete_subject(subject_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Subject {subject_id} not found")
    return {"message": f"Subject {subject_id} deleted successfully"}


# ──────────────────────────────────────────────
# GRADES
# ──────────────────────────────────────────────

@app.get("/grades", status_code=status.HTTP_200_OK)
def fetch_grades():
    grades = grade_service.get_all_grades()
    if not grades:
        raise HTTPException(status_code=404, detail="No grades found")
    return [g.to_dict() for g in grades]


@app.get("/grades/{grade_id}", status_code=status.HTTP_200_OK)
def fetch_grade(grade_id: int):
    grade = grade_service.get_grade_by_id(grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail=f"Grade {grade_id} not found")
    return grade.to_dict()


@app.get("/students/{student_id}/grades", status_code=status.HTTP_200_OK)
def fetch_student_grades(student_id: int):
    student = student_service.get_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail=f"Student {student_id} not found")

    grades = grade_service.get_grades_by_student(student_id)
    if not grades:
        raise HTTPException(status_code=404, detail=f"No grades found for student {student_id}")
    return [g.to_dict() for g in grades]


@app.get("/students/{student_id}/gpa", status_code=status.HTTP_200_OK)
def fetch_student_gpa(student_id: int):
    student = student_service.get_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail=f"Student {student_id} not found")

    gpa = grade_service.get_student_gpa(student_id)
    if gpa is None:
        raise HTTPException(status_code=404, detail=f"No grades recorded for student {student_id}")

    return {
        "student_id": student_id,
        "student_name": f"{student.first_name} {student.last_name}",
        "average_score": gpa,
    }


@app.get("/subjects/{subject_id}/grades", status_code=status.HTTP_200_OK)
def fetch_subject_grades(subject_id: int):
    subject = subject_service.get_subject_by_id(subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail=f"Subject {subject_id} not found")

    grades = grade_service.get_grades_by_subject(subject_id)
    if not grades:
        raise HTTPException(status_code=404, detail=f"No grades found for subject {subject_id}")
    return [g.to_dict() for g in grades]


@app.post("/grades", status_code=status.HTTP_201_CREATED)
def create_grade(body: dict = Body(...)):
    student_id = body.get("student_id")
    subject_id = body.get("subject_id")
    score      = body.get("score")
    term       = body.get("term")

    if not all([student_id, subject_id, score is not None, term]):
        raise HTTPException(status_code=400, detail="student_id, subject_id, score, and term are required")

    if not (0 <= score <= 100):
        raise HTTPException(status_code=400, detail="Score must be between 0 and 100")

    if not student_service.get_student_by_id(student_id):
        raise HTTPException(status_code=404, detail=f"Student {student_id} not found")

    if not subject_service.get_subject_by_id(subject_id):
        raise HTTPException(status_code=404, detail=f"Subject {subject_id} not found")

    new_grade = grade_service.create_grade(
        student_id=student_id,
        subject_id=subject_id,
        score=score,
        term=term,
    )
    return new_grade.to_dict()


@app.put("/grades/{grade_id}", status_code=status.HTTP_200_OK)
def update_grade(grade_id: int, body: dict = Body(...)):
    score = body.get("score")
    if score is not None and not (0 <= score <= 100):
        raise HTTPException(status_code=400, detail="Score must be between 0 and 100")

    updated = grade_service.update_grade(
        grade_id=grade_id,
        score=score,
        term=body.get("term"),
    )
    if not updated:
        raise HTTPException(status_code=404, detail=f"Grade {grade_id} not found")
    return updated.to_dict()


@app.delete("/grades/{grade_id}", status_code=status.HTTP_200_OK)
def delete_grade(grade_id: int):
    deleted = grade_service.delete_grade(grade_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Grade {grade_id} not found")
    return {"message": f"Grade {grade_id} deleted successfully"}