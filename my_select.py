# my_select.py
"""Analytical queries for the university database."""

from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Grade, Group, Student, Subject, Teacher


def select_1(session: Session) -> list[tuple[str, float]]:
    """
    Top 5 students by highest average grade across all subjects.

    Returns:
        List of tuples: [(student_name, avg_score), ...]
    """
    stmt = (
        select(Student.full_name, func.avg(Grade.value).label("avg_score"))
        .join(Grade, Student.id == Grade.student_id)
        .group_by(Student.id, Student.full_name)
        .order_by(func.avg(Grade.value).desc())
        .limit(5)
    )
    result = session.execute(stmt).all()
    return [(row.full_name, float(row.avg_score)) for row in result]


def select_2(session: Session, subject_name: str) -> tuple[str, float] | None:
    """
    Student with the highest average in a given subject.

    Args:
        subject_name: Name of the subject.

    Returns:
        Tuple (student_name, avg_score) or None if not found.
    """
    stmt = (
        select(Student.full_name, func.avg(Grade.value).label("avg_score"))
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Grade.subject_id == Subject.id)
        .where(Subject.name == subject_name)
        .group_by(Student.id, Student.full_name)
        .order_by(func.avg(Grade.value).desc())
        .limit(1)
    )
    result = session.execute(stmt).first()
    if result:
        return (result.full_name, float(result.avg_score))
    return None


def select_3(session: Session, subject_name: str) -> list[tuple[str, float]]:
    """
    Average grade per group for a given subject.

    Args:
        subject_name: Name of the subject.

    Returns:
        List of tuples: [(group_name, avg_score), ...]
    """
    stmt = (
        select(Group.name, func.avg(Grade.value).label("avg_score"))
        .join(Student, Group.id == Student.group_id)
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Grade.subject_id == Subject.id)
        .where(Subject.name == subject_name)
        .group_by(Group.id, Group.name)
        .order_by(Group.name)
    )
    result = session.execute(stmt).all()
    return [(row.name, float(row.avg_score)) for row in result]


def select_4(session: Session) -> float:
    """
    Average grade across the entire stream (all grades).

    Returns:
        Average grade as float.
    """
    stmt = select(func.avg(Grade.value))
    result = session.execute(stmt).scalar()
    return float(result) if result else 0.0


def select_5(session: Session, teacher_name: str) -> list[str]:
    """
    Which subjects a given teacher teaches.

    Args:
        teacher_name: Full name of the teacher.

    Returns:
        List of subject names.
    """
    stmt = (
        select(Subject.name)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .where(Teacher.full_name == teacher_name)
        .order_by(Subject.name)
    )
    result = session.execute(stmt).scalars().all()
    return list(result)


def select_6(session: Session, group_name: str) -> list[str]:
    """
    List of students in a given group.

    Args:
        group_name: Name of the group.

    Returns:
        List of student full names.
    """
    stmt = (
        select(Student.full_name)
        .join(Group, Student.group_id == Group.id)
        .where(Group.name == group_name)
        .order_by(Student.full_name)
    )
    result = session.execute(stmt).scalars().all()
    return list(result)


def select_7(session: Session, group_name: str, subject_name: str) -> list[tuple[str, int]]:
    """
    Grades of students in a given group for a given subject (all records).

    Args:
        group_name: Name of the group.
        subject_name: Name of the subject.

    Returns:
        List of tuples: [(student_name, grade_value), ...]
    """
    stmt = (
        select(Student.full_name, Grade.value)
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Grade.subject_id == Subject.id)
        .join(Group, Student.group_id == Group.id)
        .where(Group.name == group_name, Subject.name == subject_name)
        .order_by(Student.full_name, Grade.value)
    )
    result = session.execute(stmt).all()
    return [(row.full_name, row.value) for row in result]


def select_8(session: Session, teacher_name: str) -> float:
    """
    Average grade that a given teacher assigns across their subjects.

    Args:
        teacher_name: Full name of the teacher.

    Returns:
        Average grade as float.
    """
    stmt = (
        select(func.avg(Grade.value))
        .join(Subject, Grade.subject_id == Subject.id)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .where(Teacher.full_name == teacher_name)
    )
    result = session.execute(stmt).scalar()
    return float(result) if result else 0.0


def select_9(session: Session, student_name: str) -> list[str]:
    """
    List of subjects a given student attends.

    Args:
        student_name: Full name of the student.

    Returns:
        List of subject names (unique, based on grades).
    """
    stmt = (
        select(Subject.name)
        .distinct()
        .join(Grade, Subject.id == Grade.subject_id)
        .join(Student, Grade.student_id == Student.id)
        .where(Student.full_name == student_name)
        .order_by(Subject.name)
    )
    result = session.execute(stmt).scalars().all()
    return list(result)


def select_10(session: Session, student_name: str, teacher_name: str) -> list[str]:
    """
    List of subjects taught to a given student by a given teacher.

    Args:
        student_name: Full name of the student.
        teacher_name: Full name of the teacher.

    Returns:
        List of subject names.
    """
    stmt = (
        select(Subject.name)
        .distinct()
        .join(Grade, Subject.id == Grade.subject_id)
        .join(Student, Grade.student_id == Student.id)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .where(Student.full_name == student_name, Teacher.full_name == teacher_name)
        .order_by(Subject.name)
    )
    result = session.execute(stmt).scalars().all()
    return list(result)


# ============================================================================
# Optional Advanced Queries
# ============================================================================


def select_extra_1(session: Session, teacher_name: str, student_name: str) -> float | None:
    """
    Average grade a given teacher assigns to a given student.

    Args:
        teacher_name: Full name of the teacher.
        student_name: Full name of the student.

    Returns:
        Average grade as float, or None if no grades found.
    """
    stmt = (
        select(func.avg(Grade.value))
        .join(Subject, Grade.subject_id == Subject.id)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .join(Student, Grade.student_id == Student.id)
        .where(Teacher.full_name == teacher_name, Student.full_name == student_name)
    )
    result = session.execute(stmt).scalar()
    return float(result) if result else None


def select_extra_2(
    session: Session, group_name: str, subject_name: str
) -> list[tuple[str, int, datetime]]:
    """
    Grades of students in a given group for a given subject on the latest lesson date.

    The "latest lesson date" is the most recent graded_at date for that subject & group.

    Args:
        group_name: Name of the group.
        subject_name: Name of the subject.

    Returns:
        List of tuples: [(student_name, grade_value, graded_at), ...]
    """
    # First, find the latest date for grades in this group & subject
    subquery = (
        select(func.max(Grade.graded_at).label("max_date"))
        .join(Student, Grade.student_id == Student.id)
        .join(Group, Student.group_id == Group.id)
        .join(Subject, Grade.subject_id == Subject.id)
        .where(Group.name == group_name, Subject.name == subject_name)
    ).scalar_subquery()

    # Then, fetch all grades on that date
    stmt = (
        select(Student.full_name, Grade.value, Grade.graded_at)
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Grade.subject_id == Subject.id)
        .join(Group, Student.group_id == Group.id)
        .where(
            Group.name == group_name,
            Subject.name == subject_name,
            func.date(Grade.graded_at) == func.date(subquery),
        )
        .order_by(Student.full_name)
    )
    result = session.execute(stmt).all()
    return [(row.full_name, row.value, row.graded_at) for row in result]
