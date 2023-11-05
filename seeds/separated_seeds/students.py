import random

from faker import Faker

from database.db import session
from database.models import Student, Group

fake = Faker("uk-UA")
count_students = 40


def create_students():
    groups = session.query(Group).all()
    for _ in range(count_students):
        student = Student(
            name=fake.name(),
            group_id=random.choice(groups).id
        )
        session.add(student)
    session.commit()


if __name__ == '__main__':
    create_students()
