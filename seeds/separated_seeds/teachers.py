from faker import Faker

from database.db import session
from database.models import Teacher


fake = Faker("uk-UA")
count_teachers = 5


def create_teachers():
    for _ in range(count_teachers):
        teacher = Teacher(
            name=fake.name()
        )
        session.add(teacher)
    session.commit()


if __name__ == '__main__':
    create_teachers()
