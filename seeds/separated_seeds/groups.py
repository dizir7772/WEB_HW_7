from faker import Faker

from database.db import session
from database.models import Group


fake = Faker()
count_groups = 3


def create_groups():
    for _ in range(count_groups):
        group = Group(
            name=fake.license_plate()
        )
        session.add(group)
    session.commit()


if __name__ == '__main__':
    create_groups()
