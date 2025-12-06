# main.py
"""CRUD CLI for managing Teachers, Groups, Students, and Subjects."""

import argparse
import logging
import sys

from sqlalchemy.orm import Session

from app.db import get_session
from app.models import Group, Student, Subject, Teacher

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


# ============================================================================
# Service Layer
# ============================================================================


def create_teacher(session: Session, name: str) -> Teacher:
    """Create a new teacher."""
    teacher = Teacher(full_name=name)
    session.add(teacher)
    session.flush()
    logger.info(f"Created teacher: {teacher}")
    return teacher


def list_teachers(session: Session) -> list[Teacher]:
    """List all teachers."""
    return session.query(Teacher).order_by(Teacher.full_name).all()


def update_teacher(session: Session, teacher_id: int, name: str) -> Teacher | None:
    """Update a teacher by ID."""
    teacher = session.query(Teacher).filter(Teacher.id == teacher_id).first()
    if teacher:
        teacher.full_name = name
        session.flush()
        logger.info(f"Updated teacher: {teacher}")
    return teacher


def remove_teacher(session: Session, teacher_id: int) -> bool:
    """Remove a teacher by ID."""
    teacher = session.query(Teacher).filter(Teacher.id == teacher_id).first()
    if teacher:
        # Check for related subjects
        subject_count = session.query(Subject).filter(Subject.teacher_id == teacher_id).count()
        if subject_count > 0:
            logger.error(f"Cannot delete teacher with {subject_count} assigned subjects")
            return False
        session.delete(teacher)
        logger.info(f"Removed teacher: {teacher}")
        return True
    return False


def create_group(session: Session, name: str) -> Group:
    """Create a new group."""
    group = Group(name=name)
    session.add(group)
    session.flush()
    logger.info(f"Created group: {group}")
    return group


def list_groups(session: Session) -> list[Group]:
    """List all groups."""
    return session.query(Group).order_by(Group.name).all()


def update_group(session: Session, group_id: int, name: str) -> Group | None:
    """Update a group by ID."""
    group = session.query(Group).filter(Group.id == group_id).first()
    if group:
        group.name = name
        session.flush()
        logger.info(f"Updated group: {group}")
    return group


def remove_group(session: Session, group_id: int) -> bool:
    """Remove a group by ID."""
    group = session.query(Group).filter(Group.id == group_id).first()
    if group:
        # Check for related students
        student_count = session.query(Student).filter(Student.group_id == group_id).count()
        if student_count > 0:
            logger.error(f"Cannot delete group with {student_count} students")
            return False
        session.delete(group)
        logger.info(f"Removed group: {group}")
        return True
    return False


def create_student(session: Session, full_name: str, group_id: int) -> Student:
    """Create a new student."""
    student = Student(full_name=full_name, group_id=group_id)
    session.add(student)
    session.flush()
    logger.info(f"Created student: {student}")
    return student


def list_students(session: Session) -> list[Student]:
    """List all students."""
    return session.query(Student).order_by(Student.full_name).all()


def update_student(
    session: Session, student_id: int, full_name: str | None = None, group_id: int | None = None
) -> Student | None:
    """Update a student by ID."""
    student = session.query(Student).filter(Student.id == student_id).first()
    if student:
        if full_name:
            student.full_name = full_name
        if group_id:
            student.group_id = group_id
        session.flush()
        logger.info(f"Updated student: {student}")
    return student


def remove_student(session: Session, student_id: int) -> bool:
    """Remove a student by ID."""
    student = session.query(Student).filter(Student.id == student_id).first()
    if student:
        # Grades will be orphaned, but we allow deletion
        session.delete(student)
        logger.info(f"Removed student: {student}")
        return True
    return False


def create_subject(session: Session, name: str, teacher_id: int) -> Subject:
    """Create a new subject."""
    subject = Subject(name=name, teacher_id=teacher_id)
    session.add(subject)
    session.flush()
    logger.info(f"Created subject: {subject}")
    return subject


def list_subjects(session: Session) -> list[Subject]:
    """List all subjects."""
    return session.query(Subject).order_by(Subject.name).all()


def update_subject(
    session: Session, subject_id: int, name: str | None = None, teacher_id: int | None = None
) -> Subject | None:
    """Update a subject by ID."""
    subject = session.query(Subject).filter(Subject.id == subject_id).first()
    if subject:
        if name:
            subject.name = name
        if teacher_id:
            subject.teacher_id = teacher_id
        session.flush()
        logger.info(f"Updated subject: {subject}")
    return subject


def remove_subject(session: Session, subject_id: int) -> bool:
    """Remove a subject by ID."""
    subject = session.query(Subject).filter(Subject.id == subject_id).first()
    if subject:
        session.delete(subject)
        logger.info(f"Removed subject: {subject}")
        return True
    return False


# ============================================================================
# CLI Handlers
# ============================================================================


def handle_teacher(args, session: Session) -> None:
    """Handle Teacher model operations."""
    if args.action == "create":
        if not args.name:
            print("Error: --name is required for creating a teacher")
            return
        teacher = create_teacher(session, args.name)
        print(f"Created: {teacher}")

    elif args.action == "list":
        teachers = list_teachers(session)
        if teachers:
            print("Teachers:")
            for t in teachers:
                print(f"  [{t.id}] {t.full_name}")
        else:
            print("No teachers found.")

    elif args.action == "update":
        if not args.id or not args.name:
            print("Error: --id and --name are required for updating a teacher")
            return
        teacher = update_teacher(session, args.id, args.name)
        if teacher:
            print(f"Updated: {teacher}")
        else:
            print(f"Teacher with id={args.id} not found.")

    elif args.action == "remove":
        if not args.id:
            print("Error: --id is required for removing a teacher")
            return
        if remove_teacher(session, args.id):
            print(f"Teacher with id={args.id} removed.")
        else:
            print(f"Could not remove teacher with id={args.id}.")


def handle_group(args, session: Session) -> None:
    """Handle Group model operations."""
    if args.action == "create":
        if not args.name:
            print("Error: --name is required for creating a group")
            return
        group = create_group(session, args.name)
        print(f"Created: {group}")

    elif args.action == "list":
        groups = list_groups(session)
        if groups:
            print("Groups:")
            for g in groups:
                print(f"  [{g.id}] {g.name}")
        else:
            print("No groups found.")

    elif args.action == "update":
        if not args.id or not args.name:
            print("Error: --id and --name are required for updating a group")
            return
        group = update_group(session, args.id, args.name)
        if group:
            print(f"Updated: {group}")
        else:
            print(f"Group with id={args.id} not found.")

    elif args.action == "remove":
        if not args.id:
            print("Error: --id is required for removing a group")
            return
        if remove_group(session, args.id):
            print(f"Group with id={args.id} removed.")
        else:
            print(f"Could not remove group with id={args.id}.")


def handle_student(args, session: Session) -> None:
    """Handle Student model operations."""
    if args.action == "create":
        if not args.full_name or not args.group_id:
            print("Error: --full-name and --group-id are required for creating a student")
            return
        student = create_student(session, args.full_name, args.group_id)
        print(f"Created: {student}")

    elif args.action == "list":
        students = list_students(session)
        if students:
            print("Students:")
            for s in students:
                print(f"  [{s.id}] {s.full_name} (group_id={s.group_id})")
        else:
            print("No students found.")

    elif args.action == "update":
        if not args.id:
            print("Error: --id is required for updating a student")
            return
        if not args.full_name and not args.group_id:
            print("Error: --full-name or --group-id is required for updating")
            return
        student = update_student(session, args.id, args.full_name, args.group_id)
        if student:
            print(f"Updated: {student}")
        else:
            print(f"Student with id={args.id} not found.")

    elif args.action == "remove":
        if not args.id:
            print("Error: --id is required for removing a student")
            return
        if remove_student(session, args.id):
            print(f"Student with id={args.id} removed.")
        else:
            print(f"Could not remove student with id={args.id}.")


def handle_subject(args, session: Session) -> None:
    """Handle Subject model operations."""
    if args.action == "create":
        if not args.name or not args.teacher_id:
            print("Error: --name and --teacher-id are required for creating a subject")
            return
        subject = create_subject(session, args.name, args.teacher_id)
        print(f"Created: {subject}")

    elif args.action == "list":
        subjects = list_subjects(session)
        if subjects:
            print("Subjects:")
            for s in subjects:
                print(f"  [{s.id}] {s.name} (teacher_id={s.teacher_id})")
        else:
            print("No subjects found.")

    elif args.action == "update":
        if not args.id:
            print("Error: --id is required for updating a subject")
            return
        if not args.name and not args.teacher_id:
            print("Error: --name or --teacher-id is required for updating")
            return
        subject = update_subject(session, args.id, args.name, args.teacher_id)
        if subject:
            print(f"Updated: {subject}")
        else:
            print(f"Subject with id={args.id} not found.")

    elif args.action == "remove":
        if not args.id:
            print("Error: --id is required for removing a subject")
            return
        if remove_subject(session, args.id):
            print(f"Subject with id={args.id} removed.")
        else:
            print(f"Could not remove subject with id={args.id}.")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="CRUD CLI for university database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py -a list -m Teacher
  python main.py -a create -m Teacher --name "John Smith"
  python main.py -a update -m Teacher --id 1 --name "Jane Smith"
  python main.py -a remove -m Teacher --id 1
  python main.py -a create -m Student --full-name "Alice" --group-id 1
  python main.py -a create -m Subject --name "Physics" --teacher-id 1
        """,
    )

    parser.add_argument(
        "-a",
        "--action",
        required=True,
        choices=["create", "list", "update", "remove"],
        help="Action to perform",
    )
    parser.add_argument(
        "-m",
        "--model",
        required=True,
        choices=["Teacher", "Group", "Student", "Subject"],
        help="Model to operate on",
    )
    parser.add_argument("--id", type=int, help="ID for update/remove operations")
    parser.add_argument("--name", type=str, help="Name for Teacher/Group/Subject")
    parser.add_argument("--full-name", type=str, dest="full_name", help="Full name for Student")
    parser.add_argument("--group-id", type=int, dest="group_id", help="Group ID for Student")
    parser.add_argument("--teacher-id", type=int, dest="teacher_id", help="Teacher ID for Subject")

    args = parser.parse_args()

    # Route to appropriate handler
    handlers = {
        "Teacher": handle_teacher,
        "Group": handle_group,
        "Student": handle_student,
        "Subject": handle_subject,
    }

    try:
        with get_session() as session:
            handler = handlers.get(args.model)
            if handler:
                handler(args, session)
            else:
                print(f"Unknown model: {args.model}")
                sys.exit(1)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
