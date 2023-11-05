import random
from datetime import datetime, date, timedelta

from database.db import session
from database.models import Lesson, Student, Score



def create_scores():
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
    create_scores()

