from sqlalchemy import func, desc

from database.db import session
from database.models import Group, Teacher, Lesson, Student, Score


# --1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів
def select_1() -> list:
    result = session.query(Student.name, func.round(func.avg(Score.value), 2).label('avg_score')) \
        .select_from(Score)\
        .join(Student)\
        .group_by(Student.id)\
        .order_by(desc('avg_score'))\
        .limit(5)\
        .all()
    return result


# --2. Знайти студента із найвищим середнім балом з певного предмета
def select_2() -> list:
    result = session.query(Student.name, Lesson.name, func.round(func.avg(Score.value), 2).label('max_score'))\
        .select_from(Score).join(Student).join(Lesson)\
        .where(Lesson.id == 1)\
        .group_by(Lesson.id, Student.id)\
        .order_by(desc('max_score'))\
        .limit(1)\
        .all()
    return result


# --3. Знайти середній бал у групах з певного предмета
def select_3() -> list:
    result = session.query(Lesson.name, Group.name, func.round(func.avg(Score.value), 2).label('avg_score')) \
        .select_from(Score).join(Student, isouter=True).join(Lesson, isouter=True).join(Group, isouter=True) \
        .where(Score.lesson_id == 1) \
        .group_by(Group.id, Lesson.id) \
        .order_by(desc('avg_score')) \
        .all()
    return result


# --4. Знайти середній бал на потоці (по всій таблиці оцінок)
def select_4() -> list:
    result = session.query(func.round(func.avg(Score.value), 2)) \
        .select_from(Score) \
        .all()
    return result


# --5. Знайти які курси читає певний викладач
def select_5() -> list:
    result = session.query(Teacher.name, Lesson.name) \
        .select_from(Lesson).join(Teacher) \
        .where(Teacher.id == 3) \
        .all()
    return result


# --6. Знайти список студентів у певній групі
def select_6() -> list:
    result = session.query(Group.name, Student.name) \
        .select_from(Group).join(Student) \
        .where(Group.id == 2) \
        .all()
    return result


# --7. Знайти оцінки студентів у окремій групі з певного предмета
def select_7() -> list:
    result = session.query(Group.name, Lesson.name, Student.name, Score.value) \
        .select_from(Score).join(Student, isouter=True).join(Lesson, isouter=True).join(Group, isouter=True) \
        .where(Score.lesson_id == 1) \
        .where(Group.id == 1) \
        .order_by(desc(Score.value)) \
        .all()
    return result


# --8. Знайти середній бал, який ставить певний викладач зі своїх предметів
def select_8() -> list:
    result = session.query(Teacher.name, Lesson.name, func.round(func.avg(Score.value), 2)) \
        .select_from(Score).join(Lesson, isouter=True).join(Teacher, isouter=True) \
        .where(Teacher.id == 3) \
        .group_by(Lesson.id, Teacher.name) \
        .all()
    return result


# -9. Знайти список курсів, які відвідує студент
def select_9() -> list:
    result = session.query(Student.name, Lesson.name) \
        .select_from(Score).join(Lesson, isouter=True).join(Student, isouter=True) \
        .where(Student.id == 13) \
        .group_by(Lesson.id, Student.name) \
        .all()
    return result


# --10. Список курсів, які певному студенту читає певний викладач
def select_10() -> list:
    result = session.query(Student.name, Lesson.name, Teacher.name) \
        .select_from(Score).join(Lesson).join(Student).join(Teacher) \
        .where(Teacher.id == 3) \
        .where(Student.id == 13) \
        .group_by(Lesson.id, Student.id, Teacher.id) \
        .all()
    return result


# --11. Середній бал, який певний викладач ставить певному студентові
def select_11() -> list:
    result = session.query(Teacher.name, Student.name, func.round(func.avg(Score.value), 2)) \
        .select_from(Score).join(Student, isouter=True).join(Lesson, isouter=True).join(Teacher, isouter=True) \
        .where(Teacher.id == 2) \
        .where(Student.id == 11) \
        .group_by(Student.id, Teacher.id) \
        .all()
    return result


# --12. Оцінки студентів у певній групі з певного предмета на останньому занятті
def select_12() -> list:
    subq = session.query(func.max(Score.date)).scalar_subquery()
    result = session.query(Group.name, Teacher.name, Lesson.name, Student.name, Score.value) \
        .select_from(Score).join(Student, isouter=True).join(Lesson, isouter=True)\
        .join(Teacher, isouter=True).join(Group, isouter=True) \
        .where(Teacher.id == 3) \
        .where(Group.id == 3) \
        .where(Score.date == subq) \
        .all()
    return result


if __name__ == '__main__':
    while True:
        num = input("Enter number of select (1-12, 'e' for exit): ")
        if num == "e":
            break
        result = eval(f"select_{num}()")
        for n, item in enumerate(result, start=1):
            print(n, item)
