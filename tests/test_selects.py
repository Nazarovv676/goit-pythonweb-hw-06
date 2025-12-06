# tests/test_selects.py
"""Smoke tests for select queries."""

import pytest

# Try to import database components, skip tests if DB is not available
try:
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

    DB_AVAILABLE = True
except Exception:
    DB_AVAILABLE = False


pytestmark = pytest.mark.skipif(not DB_AVAILABLE, reason="Database not available")


@pytest.fixture
def session():
    """Provide a database session for tests."""
    with get_session() as sess:
        yield sess


def has_data(session) -> bool:
    """Check if database has seeded data."""
    return session.query(Student).count() > 0


class TestSelectQueries:
    """Test select query functions."""

    def test_select_1_returns_max_5_rows(self, session):
        """select_1 should return at most 5 students."""
        if not has_data(session):
            pytest.skip("No data in database - run seed.py first")

        result = select_1(session)
        assert isinstance(result, list)
        assert len(result) <= 5
        if result:
            assert isinstance(result[0], tuple)
            assert len(result[0]) == 2
            assert isinstance(result[0][0], str)  # student name
            assert isinstance(result[0][1], float)  # avg score

    def test_select_2_returns_tuple_or_none(self, session):
        """select_2 should return tuple or None."""
        if not has_data(session):
            pytest.skip("No data in database - run seed.py first")

        # Get a subject name from database
        subject = session.query(Subject).first()
        if not subject:
            pytest.skip("No subjects in database")

        result = select_2(session, subject.name)
        assert result is None or (isinstance(result, tuple) and len(result) == 2)

    def test_select_3_returns_list_of_tuples(self, session):
        """select_3 should return list of group averages."""
        if not has_data(session):
            pytest.skip("No data in database - run seed.py first")

        subject = session.query(Subject).first()
        if not subject:
            pytest.skip("No subjects in database")

        result = select_3(session, subject.name)
        assert isinstance(result, list)
        if result:
            assert isinstance(result[0], tuple)
            assert len(result[0]) == 2

    def test_select_4_returns_float(self, session):
        """select_4 should return a float."""
        if not has_data(session):
            pytest.skip("No data in database - run seed.py first")

        result = select_4(session)
        assert isinstance(result, float)
        assert result >= 0

    def test_select_5_returns_list(self, session):
        """select_5 should return list of subject names."""
        if not has_data(session):
            pytest.skip("No data in database - run seed.py first")

        teacher = session.query(Teacher).first()
        if not teacher:
            pytest.skip("No teachers in database")

        result = select_5(session, teacher.full_name)
        assert isinstance(result, list)

    def test_select_6_returns_list(self, session):
        """select_6 should return list of student names."""
        if not has_data(session):
            pytest.skip("No data in database - run seed.py first")

        group = session.query(Group).first()
        if not group:
            pytest.skip("No groups in database")

        result = select_6(session, group.name)
        assert isinstance(result, list)

    def test_select_7_returns_list_of_tuples(self, session):
        """select_7 should return list of grades."""
        if not has_data(session):
            pytest.skip("No data in database - run seed.py first")

        group = session.query(Group).first()
        subject = session.query(Subject).first()
        if not group or not subject:
            pytest.skip("No groups or subjects in database")

        result = select_7(session, group.name, subject.name)
        assert isinstance(result, list)

    def test_select_8_returns_float(self, session):
        """select_8 should return a float."""
        if not has_data(session):
            pytest.skip("No data in database - run seed.py first")

        teacher = session.query(Teacher).first()
        if not teacher:
            pytest.skip("No teachers in database")

        result = select_8(session, teacher.full_name)
        assert isinstance(result, float)

    def test_select_9_returns_list(self, session):
        """select_9 should return list of subjects."""
        if not has_data(session):
            pytest.skip("No data in database - run seed.py first")

        student = session.query(Student).first()
        if not student:
            pytest.skip("No students in database")

        result = select_9(session, student.full_name)
        assert isinstance(result, list)

    def test_select_10_returns_list(self, session):
        """select_10 should return list of subjects."""
        if not has_data(session):
            pytest.skip("No data in database - run seed.py first")

        student = session.query(Student).first()
        teacher = session.query(Teacher).first()
        if not student or not teacher:
            pytest.skip("No students or teachers in database")

        result = select_10(session, student.full_name, teacher.full_name)
        assert isinstance(result, list)


class TestAdvancedQueries:
    """Test advanced select queries."""

    def test_select_extra_1_returns_float_or_none(self, session):
        """select_extra_1 should return float or None."""
        if not has_data(session):
            pytest.skip("No data in database - run seed.py first")

        student = session.query(Student).first()
        teacher = session.query(Teacher).first()
        if not student or not teacher:
            pytest.skip("No students or teachers in database")

        result = select_extra_1(session, teacher.full_name, student.full_name)
        assert result is None or isinstance(result, float)

    def test_select_extra_2_returns_list(self, session):
        """select_extra_2 should return list of tuples."""
        if not has_data(session):
            pytest.skip("No data in database - run seed.py first")

        group = session.query(Group).first()
        subject = session.query(Subject).first()
        if not group or not subject:
            pytest.skip("No groups or subjects in database")

        result = select_extra_2(session, group.name, subject.name)
        assert isinstance(result, list)
        if result:
            assert isinstance(result[0], tuple)
            assert len(result[0]) == 3  # name, value, datetime
