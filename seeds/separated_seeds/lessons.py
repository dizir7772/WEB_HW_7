import random

from faker import Faker

from database.db import session
from database.models import Teacher, Lesson

fake = Faker("uk-UA")
count_lessons = 8


def create_lessons():
    teachers = session.query(Teacher).all()
    for _ in range(count_lessons):
        lesson = Lesson(
            name=fake.job(),
            teacher_id=random.choice(teachers).id
        )
        session.add(lesson)
    session.commit()


if __name__ == '__main__':
    create_lessons()
