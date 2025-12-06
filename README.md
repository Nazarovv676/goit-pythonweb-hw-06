# University Database (goit-pythonweb-hw-06)

A PostgreSQL-backed university database project using SQLAlchemy 2.0, Alembic migrations, and Faker for data seeding.

## Features

- **SQLAlchemy 2.0** with modern `Mapped[]` type hints
- **Alembic** for database migrations
- **Faker** for realistic test data generation
- **12 analytical queries** for data analysis (10 required + 2 advanced)
- **Beautiful CLI** with Typer + Rich for managing the database
- **Bilingual support** (English/Ukrainian) for query descriptions

## Schema

The database consists of 5 tables:

- **Groups** - Student groups (e.g., AD-101, AD-102)
- **Students** - Students enrolled in groups
- **Teachers** - Teachers who teach subjects
- **Subjects** - Subjects taught by teachers
- **Grades** - Student grades for subjects (1-100 scale)

### Relationships

```
Group (1) ──── (*) Student
Teacher (1) ──── (*) Subject
Student (1) ──── (*) Grade
Subject (1) ──── (*) Grade
```

## Quickstart

### 1. Start PostgreSQL with Docker

```bash
docker run --name postgres-hw06 \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -p 5432:5432 \
  -d postgres:16
```

### 2. Create `.env` file

```bash
cp .env.example .env
# Edit .env if needed (default values work with the Docker command above)
```

### 3. Install dependencies

```bash
poetry install
```

### 4. Run database migrations

```bash
poetry run alembic upgrade head
```

### 5. Seed the database

```bash
poetry run python seed.py
```

### 6. Explore the CLI

```bash
# Show all available commands
poetry run python main.py --help

# Show database statistics
poetry run python main.py stats
```

## CLI Usage

The CLI uses a hierarchical command structure with subcommands for each entity.

### 📊 Database Statistics

```bash
poetry run python main.py stats
```

### 👨‍🏫 Teacher Management

```bash
# List all teachers (with subjects they teach)
poetry run python main.py teacher list

# Show teacher details
poetry run python main.py teacher show --id 1

# Create a new teacher
poetry run python main.py teacher create --name "John Smith"

# Update a teacher
poetry run python main.py teacher update --id 1 --name "Jane Smith"

# Delete a teacher (use --force if they have subjects)
poetry run python main.py teacher delete --id 1
```

### 👥 Group Management

```bash
# List all groups
poetry run python main.py group list

# Show group with all students
poetry run python main.py group show --id 1

# Create a new group
poetry run python main.py group create --name "AD-104"

# Update a group
poetry run python main.py group update --id 1 --name "AD-105"

# Delete a group
poetry run python main.py group delete --id 1
```

### 🎒 Student Management

```bash
# List all students (optionally filter by group)
poetry run python main.py student list
poetry run python main.py student list --group 1 --limit 20

# Show student details with grades
poetry run python main.py student show --id 1

# Create a new student
poetry run python main.py student create --name "Alice Johnson" --group 1

# Update a student
poetry run python main.py student update --id 1 --name "Alice Smith" --group 2

# Delete a student
poetry run python main.py student delete --id 1
```

### 📚 Subject Management

```bash
# List all subjects
poetry run python main.py subject list

# Create a new subject
poetry run python main.py subject create --name "History" --teacher 1

# Update a subject
poetry run python main.py subject update --id 1 --name "World History" --teacher 2

# Delete a subject
poetry run python main.py subject delete --id 1
```

### 📝 Grade Management

```bash
# List grades (filter by student or subject)
poetry run python main.py grade list
poetry run python main.py grade list --student 1
poetry run python main.py grade list --subject 1 --limit 50

# Add a new grade
poetry run python main.py grade add --student 1 --subject 1 --value 85
```

### 🔍 Query Commands

```bash
# List all available queries (with EN/UA descriptions)
poetry run python main.py query list

# Run a specific query (uses sample data if params not provided)
poetry run python main.py query run --num 1

# Run query with specific parameters
poetry run python main.py query run --num 2 --subject "Mathematics"
poetry run python main.py query run --num 5 --teacher "John Smith"
poetry run python main.py query run --num 6 --group "AD-101"
poetry run python main.py query run --num 7 --group "AD-101" --subject "Physics"

# Run all queries with sample data
poetry run python main.py query all
```

## Queries Reference

| # | Description (EN) | Опис (UA) |
|---|------------------|-----------|
| 1 | Top 5 students by average grade | Знайти 5 студентів із найбільшим середнім балом |
| 2 | Best student in a subject | Знайти студента із найвищим середнім балом з предмета |
| 3 | Average grade per group for subject | Знайти середній бал у групах з предмета |
| 4 | Overall average grade | Знайти середній бал на потоці |
| 5 | Subjects taught by teacher | Знайти які курси читає викладач |
| 6 | Students in a group | Знайти список студентів у групі |
| 7 | Grades in group for subject | Знайти оцінки студентів у групі з предмета |
| 8 | Average grade by teacher | Знайти середній бал, який ставить викладач |
| 9 | Subjects attended by student | Знайти список курсів, які відвідує студент |
| 10 | Subjects by teacher for student | Список курсів, які студенту читає викладач |
| 11 | Avg grade teacher→student | Середній бал, який викладач ставить студенту |
| 12 | Last lesson grades | Оцінки на останньому занятті |

### Programmatic Query Usage

```python
from app.db import get_session
from my_select import select_1, select_2, select_4

with get_session() as session:
    # Top 5 students by average grade
    top_students = select_1(session)
    for name, avg in top_students:
        print(f"{name}: {avg:.2f}")
    
    # Best student in Mathematics
    best = select_2(session, "Mathematics")
    if best:
        print(f"Best in Math: {best[0]} ({best[1]:.2f})")
    
    # Overall average
    print(f"Stream average: {select_4(session):.2f}")
```

## Running Tests

```bash
poetry run pytest
```

## Troubleshooting

### Connection Errors

- Ensure PostgreSQL is running: `docker ps | grep postgres`
- Check `.env` has correct `DATABASE_URL`
- Verify port 5432 is not in use by another service

### Missing Migrations

```bash
# Check migration status
poetry run alembic current

# Apply pending migrations
poetry run alembic upgrade head
```

### Empty Database

```bash
# Re-seed the database
poetry run python seed.py
```

### Reset Database

```bash
# Downgrade all migrations
poetry run alembic downgrade base

# Re-apply migrations
poetry run alembic upgrade head

# Re-seed
poetry run python seed.py
```

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── db.py          # Database configuration
│   └── models.py      # SQLAlchemy models
├── alembic/
│   ├── env.py         # Alembic environment
│   └── versions/      # Migration files
├── tests/
│   └── test_selects.py
├── alembic.ini        # Alembic configuration
├── main.py            # Beautiful CLI (Typer + Rich)
├── my_select.py       # Analytical queries
├── seed.py            # Database seeder
├── pyproject.toml     # Poetry configuration
├── .env.example       # Environment template
└── README.md
```

## Technologies

- **Python 3.11+**
- **SQLAlchemy 2.0** - Modern ORM with type hints
- **Alembic** - Database migrations
- **Faker** - Realistic test data generation
- **Typer** - Modern CLI framework
- **Rich** - Beautiful terminal output
- **PostgreSQL** - Database
- **Poetry** - Dependency management

## License

MIT
