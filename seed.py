# seed.py
"""Seed the database with realistic random data using Faker."""

import logging
import random
from datetime import datetime, timedelta

from faker import Faker

from app.db import get_session
from app.models import Grade, Group, Student, Subject, Teacher

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Initialize Faker
fake = Faker()

# Configuration
NUM_GROUPS = 3
NUM_TEACHERS = random.randint(3, 5)
NUM_SUBJECTS = random.randint(5, 8)
NUM_STUDENTS = random.randint(30, 50)
MAX_GRADES_PER_STUDENT = 20

# Predefined group names
GROUP_NAMES = ["AD-101", "AD-102", "AD-103"]

# Predefined subject names
SUBJECT_NAMES = [
    "Mathematics",
    "Physics",
    "Chemistry",
    "Biology",
    "Computer Science",
    "English Literature",
    "History",
    "Philosophy",
    "Economics",
    "Psychology",
]


def seed_groups(session) -> list[Group]:
    """Create groups."""
    logger.info(f"Creating {NUM_GROUPS} groups...")
    groups = []
    for name in GROUP_NAMES[:NUM_GROUPS]:
        group = Group(name=name)
        session.add(group)
        groups.append(group)
    session.flush()
    logger.info(f"Created {len(groups)} groups")
    return groups


def seed_teachers(session) -> list[Teacher]:
    """Create teachers with random names."""
    logger.info(f"Creating {NUM_TEACHERS} teachers...")
    teachers = []
    for _ in range(NUM_TEACHERS):
        teacher = Teacher(full_name=fake.name())
        session.add(teacher)
        teachers.append(teacher)
    session.flush()
    logger.info(f"Created {len(teachers)} teachers")
    return teachers


def seed_subjects(session, teachers: list[Teacher]) -> list[Subject]:
    """Create subjects and assign them to random teachers."""
    logger.info(f"Creating {NUM_SUBJECTS} subjects...")
    subjects = []
    subject_names = random.sample(SUBJECT_NAMES, NUM_SUBJECTS)
    for name in subject_names:
        teacher = random.choice(teachers)
        subject = Subject(name=name, teacher_id=teacher.id)
        session.add(subject)
        subjects.append(subject)
    session.flush()
    logger.info(f"Created {len(subjects)} subjects")
    return subjects


def seed_students(session, groups: list[Group]) -> list[Student]:
    """Create students and assign them to random groups."""
    logger.info(f"Creating {NUM_STUDENTS} students...")
    students = []
    for _ in range(NUM_STUDENTS):
        group = random.choice(groups)
        student = Student(full_name=fake.name(), group_id=group.id)
        session.add(student)
        students.append(student)
    session.flush()
    logger.info(f"Created {len(students)} students")
    return students


def seed_grades(session, students: list[Student], subjects: list[Subject]) -> list[Grade]:
    """Create grades for each student across random subjects."""
    logger.info("Creating grades for students...")
    grades = []
    now = datetime.now()
    one_year_ago = now - timedelta(days=365)

    for student in students:
        # Each student gets up to MAX_GRADES_PER_STUDENT grades
        num_grades = random.randint(10, MAX_GRADES_PER_STUDENT)
        # Select random subjects for this student's grades
        selected_subjects = random.choices(subjects, k=num_grades)

        for subject in selected_subjects:
            # Random grade value between 1 and 100
            value = random.randint(1, 100)
            # Random date within the last year
            random_days = random.randint(0, 365)
            graded_at = one_year_ago + timedelta(days=random_days)

            grade = Grade(
                student_id=student.id,
                subject_id=subject.id,
                value=value,
                graded_at=graded_at,
            )
            session.add(grade)
            grades.append(grade)

    session.flush()
    logger.info(f"Created {len(grades)} grades")
    return grades


def main():
    """Main seeding function."""
    logger.info("Starting database seeding...")

    with get_session() as session:
        # Clear existing data (optional, for re-seeding)
        session.query(Grade).delete()
        session.query(Student).delete()
        session.query(Subject).delete()
        session.query(Teacher).delete()
        session.query(Group).delete()
        session.flush()
        logger.info("Cleared existing data")

        # Seed in order of dependencies
        groups = seed_groups(session)
        teachers = seed_teachers(session)
        subjects = seed_subjects(session, teachers)
        students = seed_students(session, groups)
        grades = seed_grades(session, students, subjects)

        # Summary
        logger.info("=" * 50)
        logger.info("Seeding completed successfully!")
        logger.info(f"  Groups: {len(groups)}")
        logger.info(f"  Teachers: {len(teachers)}")
        logger.info(f"  Subjects: {len(subjects)}")
        logger.info(f"  Students: {len(students)}")
        logger.info(f"  Grades: {len(grades)}")
        logger.info("=" * 50)


if __name__ == "__main__":
    main()
