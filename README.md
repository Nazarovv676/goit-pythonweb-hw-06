# University Database (goit-pythonweb-hw-06)

A PostgreSQL-backed university database project using SQLAlchemy 2.0, Alembic migrations, and Faker for data seeding.

## Features

- **SQLAlchemy 2.0** with modern `Mapped[]` type hints
- **Alembic** for database migrations
- **Faker** for realistic test data generation
- **10 analytical queries** for data analysis
- **CRUD CLI** for managing Teachers, Groups, Students, and Subjects

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

### 6. Run queries

```python
# In Python shell or script
from app.db import get_session
from my_select import select_1, select_2, select_3

with get_session() as session:
    # Top 5 students by average grade
    print(select_1(session))
    
    # Best student in a subject
    print(select_2(session, "Mathematics"))
    
    # Average grade per group for a subject
    print(select_3(session, "Physics"))
```

Or run all queries:

```bash
poetry run python -c "
from app.db import get_session
from my_select import *

with get_session() as session:
    print('=== Top 5 Students ===')
    for name, avg in select_1(session):
        print(f'  {name}: {avg:.2f}')
    
    print('\n=== Average Grade (Stream) ===')
    print(f'  {select_4(session):.2f}')
"
```

### 7. Use the CRUD CLI

```bash
# List all teachers
poetry run python main.py -a list -m Teacher

# Create a new teacher
poetry run python main.py -a create -m Teacher --name "John Smith"

# Update a teacher
poetry run python main.py -a update -m Teacher --id 1 --name "Jane Smith"

# Remove a teacher
poetry run python main.py -a remove -m Teacher --id 1

# List all groups
poetry run python main.py -a list -m Group

# Create a new group
poetry run python main.py -a create -m Group --name "AD-104"

# List all students
poetry run python main.py -a list -m Student

# Create a new student
poetry run python main.py -a create -m Student --full-name "Alice Johnson" --group-id 1

# Update a student
poetry run python main.py -a update -m Student --id 1 --full-name "Alice Smith" --group-id 2

# Create a subject
poetry run python main.py -a create -m Subject --name "History" --teacher-id 1

# List all subjects
poetry run python main.py -a list -m Subject
```

## Queries Reference

| Function | Description |
|----------|-------------|
| `select_1(session)` | Top 5 students by highest average grade |
| `select_2(session, subject_name)` | Student with highest average in a subject |
| `select_3(session, subject_name)` | Average grade per group for a subject |
| `select_4(session)` | Average grade across entire stream |
| `select_5(session, teacher_name)` | Subjects taught by a teacher |
| `select_6(session, group_name)` | Students in a group |
| `select_7(session, group_name, subject_name)` | Grades in a group for a subject |
| `select_8(session, teacher_name)` | Average grade assigned by a teacher |
| `select_9(session, student_name)` | Subjects attended by a student |
| `select_10(session, student_name, teacher_name)` | Subjects taught to student by teacher |
| `select_extra_1(session, teacher_name, student_name)` | Avg grade from teacher to student |
| `select_extra_2(session, group_name, subject_name)` | Latest lesson grades |

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
├── main.py            # CRUD CLI
├── my_select.py       # Analytical queries
├── seed.py            # Database seeder
├── pyproject.toml     # Poetry configuration
├── .env.example       # Environment template
└── README.md
```

## License

MIT

