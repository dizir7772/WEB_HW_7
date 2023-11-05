import random
from datetime import datetime, date, timedelta

from faker import Faker

from database.db import session
from database.models import Teacher, Group, Student, Lesson, Score


fake = Faker("uk-UA")
count_teachers = 5
count_groups = 3
count_students = 40
count_lessons = 8


def create_teachers() -> None:
    for _ in range(count_teachers):
        teacher = Teacher(
            name=fake.name()
        )
        session.add(teacher)
    session.commit()



def create_groups() -> None:
    for _ in range(count_groups):
        group = Group(
            name=fake.license_plate()
        )
        session.add(group)
    session.commit()


def create_students() -> None:
    groups = session.query(Group).all()
    for _ in range(count_students):
        student = Student(
            name=fake.name(),
            group_id=random.choice(groups).id
        )
        session.add(student)
    session.commit()


def create_lessons() -> None:
    teachers = session.query(Teacher).all()
    for _ in range(count_lessons):
        lesson = Lesson(
            name=fake.job(),
            teacher_id=random.choice(teachers).id
        )
        session.add(lesson)
    session.commit()


def create_scores() -> None:
    lessons = session.query(Lesson).all()
    students = session.query(Student).all()

    start_date = datetime.strptime("2022-09-01", "%Y-%m-%d")
    end_date = datetime.strptime("2023-06-15", "%Y-%m-%d")


    def get_list_date(start: date, end: date) -> list[date]:
        result = []
        current_date = start
        while current_date <= end:
            if current_date.isoweekday() < 6:
                result.append(current_date)
            current_date += timedelta(1)
        return result

    list_dates = get_list_date(start_date, end_date)

    for day in list_dates:
        random_lesson = random.choice(lessons).id
        random_students = [random.choice(students).id for _ in range(5)]
        for student in random_students:
            score = Score(
                lesson_id=random_lesson,
                student_id=student,
                value=random.randint(1, 12),
                date=day.date()
            )
            session.add(score)
    session.commit()


if __name__ == '__main__':
    create_teachers()
    create_groups()
    create_students()
    create_lessons()
    create_scores()
