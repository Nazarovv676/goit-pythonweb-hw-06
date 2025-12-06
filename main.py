# main.py
"""Beautiful CRUD CLI for university database using Typer and Rich."""

from datetime import datetime
from typing import Optional

import typer
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from sqlalchemy.orm import Session

from app.db import get_session
from app.models import Grade, Group, Student, Subject, Teacher
from my_select import (
    select_1,
    select_2,
    select_3,
    select_4,
    select_5,
    select_6,
    select_7,
    select_8,
    select_9,
    select_10,
    select_extra_1,
    select_extra_2,
)

# Initialize Typer app and Rich console
app = typer.Typer(
    name="university-db",
    help="🎓 University Database CLI - Manage students, teachers, groups, and subjects",
    add_completion=False,
    rich_markup_mode="rich",
)
console = Console()

# Sub-apps for each model
teacher_app = typer.Typer(help="👨‍🏫 Manage teachers")
group_app = typer.Typer(help="👥 Manage groups")
student_app = typer.Typer(help="🎒 Manage students")
subject_app = typer.Typer(help="📚 Manage subjects")
grade_app = typer.Typer(help="📝 Manage grades")
query_app = typer.Typer(help="🔍 Run analytical queries")

app.add_typer(teacher_app, name="teacher")
app.add_typer(group_app, name="group")
app.add_typer(student_app, name="student")
app.add_typer(subject_app, name="subject")
app.add_typer(grade_app, name="grade")
app.add_typer(query_app, name="query")


# ============================================================================
# Helper Functions
# ============================================================================


def success(message: str) -> None:
    """Print success message."""
    console.print(f"[bold green]✓[/] {message}")


def error(message: str) -> None:
    """Print error message."""
    console.print(f"[bold red]✗[/] {message}")


def warning(message: str) -> None:
    """Print warning message."""
    console.print(f"[bold yellow]![/] {message}")


def info(message: str) -> None:
    """Print info message."""
    console.print(f"[bold blue]ℹ[/] {message}")


# ============================================================================
# Teacher Commands
# ============================================================================


@teacher_app.command("list")
def teacher_list():
    """📋 List all teachers."""
    with get_session() as session:
        teachers = session.query(Teacher).order_by(Teacher.full_name).all()

        if not teachers:
            warning("No teachers found.")
            return

        table = Table(
            title="👨‍🏫 Teachers",
            box=box.ROUNDED,
            header_style="bold magenta",
            show_lines=True,
        )
        table.add_column("ID", justify="right", style="cyan", width=6)
        table.add_column("Full Name", style="white")
        table.add_column("Subjects", style="yellow")

        for t in teachers:
            subjects = ", ".join([s.name for s in t.subjects]) or "[dim]None[/dim]"
            table.add_row(str(t.id), t.full_name, subjects)

        console.print(table)
        info(f"Total: {len(teachers)} teacher(s)")


@teacher_app.command("create")
def teacher_create(
    name: str = typer.Option(..., "--name", "-n", help="Full name of the teacher"),
):
    """➕ Create a new teacher."""
    with get_session() as session:
        teacher = Teacher(full_name=name)
        session.add(teacher)
        session.flush()
        success(f"Created teacher: [bold]{teacher.full_name}[/] (ID: {teacher.id})")


@teacher_app.command("update")
def teacher_update(
    id: int = typer.Option(..., "--id", "-i", help="Teacher ID"),
    name: str = typer.Option(..., "--name", "-n", help="New full name"),
):
    """✏️ Update a teacher."""
    with get_session() as session:
        teacher = session.query(Teacher).filter(Teacher.id == id).first()
        if not teacher:
            error(f"Teacher with ID {id} not found.")
            raise typer.Exit(1)

        old_name = teacher.full_name
        teacher.full_name = name
        success(f"Updated teacher: [dim]{old_name}[/] → [bold]{name}[/]")


@teacher_app.command("delete")
def teacher_delete(
    id: int = typer.Option(..., "--id", "-i", help="Teacher ID"),
    force: bool = typer.Option(False, "--force", "-f", help="Force delete"),
):
    """🗑️ Delete a teacher."""
    with get_session() as session:
        teacher = session.query(Teacher).filter(Teacher.id == id).first()
        if not teacher:
            error(f"Teacher with ID {id} not found.")
            raise typer.Exit(1)

        # Check for related subjects
        if teacher.subjects and not force:
            error(f"Teacher has {len(teacher.subjects)} subject(s). Use --force to delete anyway.")
            raise typer.Exit(1)

        name = teacher.full_name
        session.delete(teacher)
        success(f"Deleted teacher: [bold]{name}[/]")


@teacher_app.command("show")
def teacher_show(
    id: int = typer.Option(..., "--id", "-i", help="Teacher ID"),
):
    """👁️ Show teacher details."""
    with get_session() as session:
        teacher = session.query(Teacher).filter(Teacher.id == id).first()
        if not teacher:
            error(f"Teacher with ID {id} not found.")
            raise typer.Exit(1)

        # Create a panel with teacher info
        content = Text()
        content.append(f"ID: ", style="dim")
        content.append(f"{teacher.id}\n", style="cyan")
        content.append(f"Name: ", style="dim")
        content.append(f"{teacher.full_name}\n", style="bold white")
        content.append(f"Subjects: ", style="dim")
        if teacher.subjects:
            content.append(", ".join([s.name for s in teacher.subjects]), style="yellow")
        else:
            content.append("None", style="dim italic")

        console.print(Panel(content, title="👨‍🏫 Teacher Details", border_style="magenta"))


# ============================================================================
# Group Commands
# ============================================================================


@group_app.command("list")
def group_list():
    """📋 List all groups."""
    with get_session() as session:
        groups = session.query(Group).order_by(Group.name).all()

        if not groups:
            warning("No groups found.")
            return

        table = Table(
            title="👥 Groups",
            box=box.ROUNDED,
            header_style="bold cyan",
            show_lines=True,
        )
        table.add_column("ID", justify="right", style="cyan", width=6)
        table.add_column("Name", style="bold white")
        table.add_column("Students", justify="right", style="green")

        for g in groups:
            table.add_row(str(g.id), g.name, str(len(g.students)))

        console.print(table)
        info(f"Total: {len(groups)} group(s)")


@group_app.command("create")
def group_create(
    name: str = typer.Option(..., "--name", "-n", help="Group name (e.g., AD-104)"),
):
    """➕ Create a new group."""
    with get_session() as session:
        group = Group(name=name)
        session.add(group)
        session.flush()
        success(f"Created group: [bold]{group.name}[/] (ID: {group.id})")


@group_app.command("update")
def group_update(
    id: int = typer.Option(..., "--id", "-i", help="Group ID"),
    name: str = typer.Option(..., "--name", "-n", help="New group name"),
):
    """✏️ Update a group."""
    with get_session() as session:
        group = session.query(Group).filter(Group.id == id).first()
        if not group:
            error(f"Group with ID {id} not found.")
            raise typer.Exit(1)

        old_name = group.name
        group.name = name
        success(f"Updated group: [dim]{old_name}[/] → [bold]{name}[/]")


@group_app.command("delete")
def group_delete(
    id: int = typer.Option(..., "--id", "-i", help="Group ID"),
    force: bool = typer.Option(False, "--force", "-f", help="Force delete"),
):
    """🗑️ Delete a group."""
    with get_session() as session:
        group = session.query(Group).filter(Group.id == id).first()
        if not group:
            error(f"Group with ID {id} not found.")
            raise typer.Exit(1)

        if group.students and not force:
            error(f"Group has {len(group.students)} student(s). Use --force to delete anyway.")
            raise typer.Exit(1)

        name = group.name
        session.delete(group)
        success(f"Deleted group: [bold]{name}[/]")


@group_app.command("show")
def group_show(
    id: int = typer.Option(..., "--id", "-i", help="Group ID"),
):
    """👁️ Show group details with students."""
    with get_session() as session:
        group = session.query(Group).filter(Group.id == id).first()
        if not group:
            error(f"Group with ID {id} not found.")
            raise typer.Exit(1)

        console.print(
            Panel(
                f"[cyan]ID:[/] {group.id}\n[cyan]Name:[/] [bold]{group.name}[/]",
                title="👥 Group Details",
                border_style="cyan",
            )
        )

        if group.students:
            table = Table(box=box.SIMPLE, header_style="bold")
            table.add_column("ID", style="dim")
            table.add_column("Student Name")

            for s in sorted(group.students, key=lambda x: x.full_name):
                table.add_row(str(s.id), s.full_name)

            console.print(table)
            info(f"Total students: {len(group.students)}")
        else:
            warning("No students in this group.")


# ============================================================================
# Student Commands
# ============================================================================


@student_app.command("list")
def student_list(
    group_id: Optional[int] = typer.Option(None, "--group", "-g", help="Filter by group ID"),
    limit: int = typer.Option(50, "--limit", "-l", help="Limit results"),
):
    """📋 List all students."""
    with get_session() as session:
        query = session.query(Student).order_by(Student.full_name)
        if group_id:
            query = query.filter(Student.group_id == group_id)
        students = query.limit(limit).all()

        if not students:
            warning("No students found.")
            return

        table = Table(
            title="🎒 Students",
            box=box.ROUNDED,
            header_style="bold green",
            show_lines=False,
        )
        table.add_column("ID", justify="right", style="cyan", width=6)
        table.add_column("Full Name", style="white")
        table.add_column("Group", style="yellow")
        table.add_column("Grades", justify="right", style="magenta")

        for s in students:
            table.add_row(str(s.id), s.full_name, s.group.name, str(len(s.grades)))

        console.print(table)
        total = session.query(Student).count()
        info(f"Showing {len(students)} of {total} student(s)")


@student_app.command("create")
def student_create(
    name: str = typer.Option(..., "--name", "-n", help="Full name of the student"),
    group_id: int = typer.Option(..., "--group", "-g", help="Group ID"),
):
    """➕ Create a new student."""
    with get_session() as session:
        # Verify group exists
        group = session.query(Group).filter(Group.id == group_id).first()
        if not group:
            error(f"Group with ID {group_id} not found.")
            raise typer.Exit(1)

        student = Student(full_name=name, group_id=group_id)
        session.add(student)
        session.flush()
        success(f"Created student: [bold]{student.full_name}[/] in group [yellow]{group.name}[/]")


@student_app.command("update")
def student_update(
    id: int = typer.Option(..., "--id", "-i", help="Student ID"),
    name: Optional[str] = typer.Option(None, "--name", "-n", help="New full name"),
    group_id: Optional[int] = typer.Option(None, "--group", "-g", help="New group ID"),
):
    """✏️ Update a student."""
    if not name and not group_id:
        error("Provide at least --name or --group to update.")
        raise typer.Exit(1)

    with get_session() as session:
        student = session.query(Student).filter(Student.id == id).first()
        if not student:
            error(f"Student with ID {id} not found.")
            raise typer.Exit(1)

        changes = []
        if name:
            old = student.full_name
            student.full_name = name
            changes.append(f"name: {old} → {name}")
        if group_id:
            group = session.query(Group).filter(Group.id == group_id).first()
            if not group:
                error(f"Group with ID {group_id} not found.")
                raise typer.Exit(1)
            old_group = student.group.name
            student.group_id = group_id
            changes.append(f"group: {old_group} → {group.name}")

        success(f"Updated student: {', '.join(changes)}")


@student_app.command("delete")
def student_delete(
    id: int = typer.Option(..., "--id", "-i", help="Student ID"),
):
    """🗑️ Delete a student."""
    with get_session() as session:
        student = session.query(Student).filter(Student.id == id).first()
        if not student:
            error(f"Student with ID {id} not found.")
            raise typer.Exit(1)

        name = student.full_name
        session.delete(student)
        success(f"Deleted student: [bold]{name}[/]")


@student_app.command("show")
def student_show(
    id: int = typer.Option(..., "--id", "-i", help="Student ID"),
):
    """👁️ Show student details with grades."""
    with get_session() as session:
        student = session.query(Student).filter(Student.id == id).first()
        if not student:
            error(f"Student with ID {id} not found.")
            raise typer.Exit(1)

        # Calculate average grade
        avg_grade = (
            sum(g.value for g in student.grades) / len(student.grades) if student.grades else 0
        )

        content = Text()
        content.append(f"ID: ", style="dim")
        content.append(f"{student.id}\n", style="cyan")
        content.append(f"Name: ", style="dim")
        content.append(f"{student.full_name}\n", style="bold white")
        content.append(f"Group: ", style="dim")
        content.append(f"{student.group.name}\n", style="yellow")
        content.append(f"Average Grade: ", style="dim")
        content.append(f"{avg_grade:.1f}", style="bold green" if avg_grade >= 50 else "bold red")

        console.print(Panel(content, title="🎒 Student Details", border_style="green"))

        if student.grades:
            # Group grades by subject
            grades_by_subject: dict[str, list[int]] = {}
            for g in student.grades:
                if g.subject.name not in grades_by_subject:
                    grades_by_subject[g.subject.name] = []
                grades_by_subject[g.subject.name].append(g.value)

            table = Table(title="📝 Grades by Subject", box=box.SIMPLE)
            table.add_column("Subject", style="cyan")
            table.add_column("Grades", style="white")
            table.add_column("Average", justify="right", style="green")

            for subject, grades in sorted(grades_by_subject.items()):
                avg = sum(grades) / len(grades)
                grades_str = ", ".join(str(g) for g in sorted(grades)[-5:])
                if len(grades) > 5:
                    grades_str = "..." + grades_str
                table.add_row(subject, grades_str, f"{avg:.1f}")

            console.print(table)


# ============================================================================
# Subject Commands
# ============================================================================


@subject_app.command("list")
def subject_list():
    """📋 List all subjects."""
    with get_session() as session:
        subjects = session.query(Subject).order_by(Subject.name).all()

        if not subjects:
            warning("No subjects found.")
            return

        table = Table(
            title="📚 Subjects",
            box=box.ROUNDED,
            header_style="bold yellow",
            show_lines=True,
        )
        table.add_column("ID", justify="right", style="cyan", width=6)
        table.add_column("Name", style="bold white")
        table.add_column("Teacher", style="magenta")
        table.add_column("Grades", justify="right", style="green")

        for s in subjects:
            table.add_row(str(s.id), s.name, s.teacher.full_name, str(len(s.grades)))

        console.print(table)
        info(f"Total: {len(subjects)} subject(s)")


@subject_app.command("create")
def subject_create(
    name: str = typer.Option(..., "--name", "-n", help="Subject name"),
    teacher_id: int = typer.Option(..., "--teacher", "-t", help="Teacher ID"),
):
    """➕ Create a new subject."""
    with get_session() as session:
        teacher = session.query(Teacher).filter(Teacher.id == teacher_id).first()
        if not teacher:
            error(f"Teacher with ID {teacher_id} not found.")
            raise typer.Exit(1)

        subject = Subject(name=name, teacher_id=teacher_id)
        session.add(subject)
        session.flush()
        success(
            f"Created subject: [bold]{subject.name}[/] taught by [magenta]{teacher.full_name}[/]"
        )


@subject_app.command("update")
def subject_update(
    id: int = typer.Option(..., "--id", "-i", help="Subject ID"),
    name: Optional[str] = typer.Option(None, "--name", "-n", help="New name"),
    teacher_id: Optional[int] = typer.Option(None, "--teacher", "-t", help="New teacher ID"),
):
    """✏️ Update a subject."""
    if not name and not teacher_id:
        error("Provide at least --name or --teacher to update.")
        raise typer.Exit(1)

    with get_session() as session:
        subject = session.query(Subject).filter(Subject.id == id).first()
        if not subject:
            error(f"Subject with ID {id} not found.")
            raise typer.Exit(1)

        changes = []
        if name:
            old = subject.name
            subject.name = name
            changes.append(f"name: {old} → {name}")
        if teacher_id:
            teacher = session.query(Teacher).filter(Teacher.id == teacher_id).first()
            if not teacher:
                error(f"Teacher with ID {teacher_id} not found.")
                raise typer.Exit(1)
            old_teacher = subject.teacher.full_name
            subject.teacher_id = teacher_id
            changes.append(f"teacher: {old_teacher} → {teacher.full_name}")

        success(f"Updated subject: {', '.join(changes)}")


@subject_app.command("delete")
def subject_delete(
    id: int = typer.Option(..., "--id", "-i", help="Subject ID"),
):
    """🗑️ Delete a subject."""
    with get_session() as session:
        subject = session.query(Subject).filter(Subject.id == id).first()
        if not subject:
            error(f"Subject with ID {id} not found.")
            raise typer.Exit(1)

        name = subject.name
        session.delete(subject)
        success(f"Deleted subject: [bold]{name}[/]")


# ============================================================================
# Grade Commands
# ============================================================================


@grade_app.command("add")
def grade_add(
    student_id: int = typer.Option(..., "--student", "-s", help="Student ID"),
    subject_id: int = typer.Option(..., "--subject", "-j", help="Subject ID"),
    value: int = typer.Option(..., "--value", "-v", help="Grade value (1-100)"),
):
    """➕ Add a grade for a student."""
    if not 1 <= value <= 100:
        error("Grade value must be between 1 and 100.")
        raise typer.Exit(1)

    with get_session() as session:
        student = session.query(Student).filter(Student.id == student_id).first()
        subject = session.query(Subject).filter(Subject.id == subject_id).first()

        if not student:
            error(f"Student with ID {student_id} not found.")
            raise typer.Exit(1)
        if not subject:
            error(f"Subject with ID {subject_id} not found.")
            raise typer.Exit(1)

        grade = Grade(
            student_id=student_id,
            subject_id=subject_id,
            value=value,
            graded_at=datetime.now(),
        )
        session.add(grade)
        session.flush()
        success(
            f"Added grade [bold]{value}[/] for [cyan]{student.full_name}[/] "
            f"in [yellow]{subject.name}[/]"
        )


@grade_app.command("list")
def grade_list(
    student_id: Optional[int] = typer.Option(None, "--student", "-s", help="Filter by student"),
    subject_id: Optional[int] = typer.Option(None, "--subject", "-j", help="Filter by subject"),
    limit: int = typer.Option(20, "--limit", "-l", help="Limit results"),
):
    """📋 List grades."""
    with get_session() as session:
        query = session.query(Grade).order_by(Grade.graded_at.desc())
        if student_id:
            query = query.filter(Grade.student_id == student_id)
        if subject_id:
            query = query.filter(Grade.subject_id == subject_id)

        grades = query.limit(limit).all()

        if not grades:
            warning("No grades found.")
            return

        table = Table(
            title="📝 Grades",
            box=box.ROUNDED,
            header_style="bold blue",
        )
        table.add_column("ID", justify="right", style="dim", width=6)
        table.add_column("Student", style="cyan")
        table.add_column("Subject", style="yellow")
        table.add_column("Grade", justify="center", style="bold")
        table.add_column("Date", style="dim")

        for g in grades:
            grade_style = "green" if g.value >= 50 else "red"
            table.add_row(
                str(g.id),
                g.student.full_name,
                g.subject.name,
                f"[{grade_style}]{g.value}[/{grade_style}]",
                g.graded_at.strftime("%Y-%m-%d"),
            )

        console.print(table)
        info(f"Showing {len(grades)} grade(s)")


# ============================================================================
# Query Commands
# ============================================================================

QUERY_INFO = {
    1: ("Top 5 students by average grade", "Знайти 5 студентів із найбільшим середнім балом"),
    2: ("Best student in a subject", "Знайти студента із найвищим середнім балом з предмета"),
    3: ("Average grade per group for subject", "Знайти середній бал у групах з предмета"),
    4: ("Overall average grade", "Знайти середній бал на потоці"),
    5: ("Subjects taught by teacher", "Знайти які курси читає викладач"),
    6: ("Students in a group", "Знайти список студентів у групі"),
    7: ("Grades in group for subject", "Знайти оцінки студентів у групі з предмета"),
    8: ("Average grade by teacher", "Знайти середній бал, який ставить викладач"),
    9: ("Subjects attended by student", "Знайти список курсів, які відвідує студент"),
    10: ("Subjects by teacher for student", "Список курсів, які студенту читає викладач"),
    11: ("Avg grade teacher→student", "Середній бал, який викладач ставить студенту"),
    12: ("Last lesson grades", "Оцінки на останньому занятті"),
}


@query_app.command("list")
def query_list():
    """📋 List all available queries."""
    table = Table(
        title="🔍 Available Queries",
        box=box.ROUNDED,
        header_style="bold cyan",
    )
    table.add_column("#", justify="right", style="cyan", width=4)
    table.add_column("Description (EN)", style="white")
    table.add_column("Опис (UA)", style="yellow")

    for num, (en, ua) in QUERY_INFO.items():
        table.add_row(str(num), en, ua)

    console.print(table)
    console.print("\n[dim]Run a query with:[/] [bold]python main.py query run --num N[/]")


@query_app.command("run")
def query_run(
    num: int = typer.Option(..., "--num", "-n", help="Query number (1-12)"),
    subject: Optional[str] = typer.Option(None, "--subject", "-s", help="Subject name"),
    teacher: Optional[str] = typer.Option(None, "--teacher", "-t", help="Teacher name"),
    student: Optional[str] = typer.Option(None, "--student", "-u", help="Student name"),
    group: Optional[str] = typer.Option(None, "--group", "-g", help="Group name"),
):
    """▶️ Run a specific query."""
    if num not in QUERY_INFO:
        error(f"Invalid query number. Use 1-12.")
        raise typer.Exit(1)

    en_desc, ua_desc = QUERY_INFO[num]

    with get_session() as session:
        # Get default values if not provided
        if not teacher:
            t = session.query(Teacher).first()
            teacher = t.full_name if t else ""
        if not student:
            s = session.query(Student).first()
            student = s.full_name if s else ""
        if not group:
            g = session.query(Group).first()
            group = g.name if g else ""
        if not subject:
            subj = session.query(Subject).first()
            subject = subj.name if subj else ""

        console.print(
            Panel(
                f"[bold]{en_desc}[/]\n[dim]{ua_desc}[/]",
                title=f"🔍 Query #{num}",
                border_style="cyan",
            )
        )

        try:
            if num == 1:
                result = select_1(session)
                table = Table(box=box.SIMPLE)
                table.add_column("Student", style="cyan")
                table.add_column("Average", justify="right", style="green")
                for name, avg in result:
                    table.add_row(name, f"{avg:.2f}")
                console.print(table)

            elif num == 2:
                info(f"Subject: [yellow]{subject}[/]")
                result = select_2(session, subject)
                if result:
                    console.print(f"🏆 [bold]{result[0]}[/] with average [green]{result[1]:.2f}[/]")
                else:
                    warning("No results found.")

            elif num == 3:
                info(f"Subject: [yellow]{subject}[/]")
                result = select_3(session, subject)
                table = Table(box=box.SIMPLE)
                table.add_column("Group", style="yellow")
                table.add_column("Average", justify="right", style="green")
                for name, avg in result:
                    table.add_row(name, f"{avg:.2f}")
                console.print(table)

            elif num == 4:
                result = select_4(session)
                console.print(f"📊 Overall average grade: [bold green]{result:.2f}[/]")

            elif num == 5:
                info(f"Teacher: [magenta]{teacher}[/]")
                result = select_5(session, teacher)
                if result:
                    for subj in result:
                        console.print(f"  • [yellow]{subj}[/]")
                else:
                    warning("No subjects found.")

            elif num == 6:
                info(f"Group: [yellow]{group}[/]")
                result = select_6(session, group)
                if result:
                    for name in result:
                        console.print(f"  • [cyan]{name}[/]")
                    info(f"Total: {len(result)} student(s)")
                else:
                    warning("No students found.")

            elif num == 7:
                info(f"Group: [yellow]{group}[/], Subject: [yellow]{subject}[/]")
                result = select_7(session, group, subject)
                table = Table(box=box.SIMPLE)
                table.add_column("Student", style="cyan")
                table.add_column("Grade", justify="right")
                for name, grade in result:
                    style = "green" if grade >= 50 else "red"
                    table.add_row(name, f"[{style}]{grade}[/{style}]")
                console.print(table)

            elif num == 8:
                info(f"Teacher: [magenta]{teacher}[/]")
                result = select_8(session, teacher)
                console.print(f"📊 Average grade: [bold green]{result:.2f}[/]")

            elif num == 9:
                info(f"Student: [cyan]{student}[/]")
                result = select_9(session, student)
                if result:
                    for subj in result:
                        console.print(f"  • [yellow]{subj}[/]")
                else:
                    warning("No subjects found.")

            elif num == 10:
                info(f"Student: [cyan]{student}[/], Teacher: [magenta]{teacher}[/]")
                result = select_10(session, student, teacher)
                if result:
                    for subj in result:
                        console.print(f"  • [yellow]{subj}[/]")
                else:
                    warning("No subjects found.")

            elif num == 11:
                info(f"Teacher: [magenta]{teacher}[/], Student: [cyan]{student}[/]")
                result = select_extra_1(session, teacher, student)
                if result:
                    console.print(f"📊 Average grade: [bold green]{result:.2f}[/]")
                else:
                    warning("No grades found.")

            elif num == 12:
                info(f"Group: [yellow]{group}[/], Subject: [yellow]{subject}[/]")
                result = select_extra_2(session, group, subject)
                table = Table(box=box.SIMPLE)
                table.add_column("Student", style="cyan")
                table.add_column("Grade", justify="right")
                table.add_column("Date", style="dim")
                for name, grade, dt in result:
                    style = "green" if grade >= 50 else "red"
                    table.add_row(name, f"[{style}]{grade}[/{style}]", dt.strftime("%Y-%m-%d"))
                console.print(table)

        except Exception as e:
            error(f"Query failed: {e}")
            raise typer.Exit(1)


@query_app.command("all")
def query_all():
    """▶️ Run all queries with sample data."""
    with get_session() as session:
        teacher = session.query(Teacher).first()
        student = session.query(Student).first()
        group = session.query(Group).first()
        subject = session.query(Subject).first()

        if not all([teacher, student, group, subject]):
            error("Database is empty. Run seed.py first.")
            raise typer.Exit(1)

        console.print(
            Panel(
                f"[cyan]Teacher:[/] {teacher.full_name}\n"
                f"[cyan]Student:[/] {student.full_name}\n"
                f"[cyan]Group:[/] {group.name}\n"
                f"[cyan]Subject:[/] {subject.name}",
                title="📊 Sample Data",
                border_style="blue",
            )
        )

        for i in range(1, 13):
            console.print()
            query_run(
                num=i,
                subject=subject.name,
                teacher=teacher.full_name,
                student=student.full_name,
                group=group.name,
            )


# ============================================================================
# Stats Command
# ============================================================================


@app.command("stats")
def stats():
    """📊 Show database statistics."""
    with get_session() as session:
        teacher_count = session.query(Teacher).count()
        group_count = session.query(Group).count()
        student_count = session.query(Student).count()
        subject_count = session.query(Subject).count()
        grade_count = session.query(Grade).count()

        from sqlalchemy import func

        avg_grade = session.query(func.avg(Grade.value)).scalar() or 0

        table = Table(
            title="📊 Database Statistics",
            box=box.DOUBLE_EDGE,
            header_style="bold white on blue",
        )
        table.add_column("Entity", style="cyan")
        table.add_column("Count", justify="right", style="bold green")

        table.add_row("👨‍🏫 Teachers", str(teacher_count))
        table.add_row("👥 Groups", str(group_count))
        table.add_row("🎒 Students", str(student_count))
        table.add_row("📚 Subjects", str(subject_count))
        table.add_row("📝 Grades", str(grade_count))
        table.add_row("📈 Avg Grade", f"{avg_grade:.1f}")

        console.print(table)


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    app()
