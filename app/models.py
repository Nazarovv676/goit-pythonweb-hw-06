# app/models.py
"""SQLAlchemy 2.0 ORM models for the university database."""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Group(Base):
    """Represents a student group (e.g., AD-101)."""

    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    # Relationships
    students: Mapped[List["Student"]] = relationship("Student", back_populates="group")

    def __repr__(self) -> str:
        return f"<Group(id={self.id}, name='{self.name}')>"


class Student(Base):
    """Represents a student enrolled in a group."""

    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey("groups.id"), nullable=False)

    # Relationships
    group: Mapped["Group"] = relationship("Group", back_populates="students")
    grades: Mapped[List["Grade"]] = relationship("Grade", back_populates="student")

    def __repr__(self) -> str:
        return f"<Student(id={self.id}, full_name='{self.full_name}', group_id={self.group_id})>"


class Teacher(Base):
    """Represents a teacher who teaches subjects."""

    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)

    # Relationships
    subjects: Mapped[List["Subject"]] = relationship("Subject", back_populates="teacher")

    def __repr__(self) -> str:
        return f"<Teacher(id={self.id}, full_name='{self.full_name}')>"


class Subject(Base):
    """Represents a subject taught by a teacher."""

    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    teacher_id: Mapped[int] = mapped_column(Integer, ForeignKey("teachers.id"), nullable=False)

    # Relationships
    teacher: Mapped["Teacher"] = relationship("Teacher", back_populates="subjects")
    grades: Mapped[List["Grade"]] = relationship("Grade", back_populates="subject")

    def __repr__(self) -> str:
        return f"<Subject(id={self.id}, name='{self.name}', teacher_id={self.teacher_id})>"


class Grade(Base):
    """Represents a grade given to a student for a subject."""

    __tablename__ = "grades"
    __table_args__ = (
        CheckConstraint("value >= 1 AND value <= 100", name="check_grade_value_range"),
        Index("ix_grades_student_id", "student_id"),
        Index("ix_grades_subject_id", "subject_id"),
        Index("ix_grades_graded_at", "graded_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id"), nullable=False)
    subject_id: Mapped[int] = mapped_column(Integer, ForeignKey("subjects.id"), nullable=False)
    value: Mapped[int] = mapped_column(Integer, nullable=False)
    graded_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    # Relationships
    student: Mapped["Student"] = relationship("Student", back_populates="grades")
    subject: Mapped["Subject"] = relationship("Subject", back_populates="grades")

    def __repr__(self) -> str:
        return (
            f"<Grade(id={self.id}, student_id={self.student_id}, "
            f"subject_id={self.subject_id}, value={self.value}, graded_at={self.graded_at})>"
        )
