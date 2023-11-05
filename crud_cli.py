import argparse

from sqlalchemy import func, desc

from database.db import session
from database.models import Group, Teacher, Lesson, Student, Score


parser = argparse.ArgumentParser(description='DB University CRUD Command Line Interface')
parser.add_argument('-a', '--action',
                    help="Chose action from next list: c(reate), r(ead), u(pdate), d(elete)", default="r")
parser.add_argument('-m', '--model',
                    help="Chose model from next list: st(udent), g(roup), t(eacher), l(esson), sc(ore)", default="l")
parser.add_argument('-n', '--name', help="Enter name", default=None)
parser.add_argument('-i', '--id', help="Enter id for model", default=None)

args = vars(parser.parse_args())  # object -> dict

action = args.get('action')
model = args.get('model')
name = args.get('name')
note_id = args.get('id')

models_dict = {"st": Student, "g": Group, "t": Teacher, "l": Lesson, "sc": Score}


def handler() -> list | str:
    if action == "c":
        return create_func(model, name, note_id)
    elif action == "r":
        return read_func(model)
    elif action == "u":
        return update_func(model, name, note_id)
    elif action == "d":
        return delete_func(model, note_id)
    else:
        pass


def create_func(model: str, name: str, note_id: int) -> str:
    if model not in models_dict:
        pass

    elif model in ["t", "g"]:
        note = models_dict.get(model)(name=name)
        session.add(note)
        session.commit()
        return "Done"

    elif model in ["st"]:
        note = models_dict.get(model)(name=name, group_id=note_id)
        session.add(note)
        session.commit()
        return "Done"

    elif model in ["l"]:
        note = models_dict.get(model)(name=name, teacher_id=note_id)
        session.add(note)
        session.commit()
        return "Done"

    elif model in ["sc"]:
        print("Too many args, let's implement it next time")


def read_func(model: str) -> list:
    if model not in models_dict:
        pass
    elif model != "sc":
        result = session.query(models_dict.get(model).name).select_from(models_dict.get(model)).all()
        return result
    elif model == "sc":
        result = session.query(
            Student.name, func.round(func.avg(Score.value), 2).label('avg_score')) \
            .select_from(models_dict.get(model)) \
            .join(Student) \
            .group_by(Student.id) \
            .order_by(desc('avg_score')).all()
        return result


def update_func(model: str, name: str, note_id: int) -> str:
    try:
        if model not in models_dict:
            pass

        elif model in ["t", "g", "st", "l"]:
            note = session.query(models_dict.get(model)).get(note_id)
            note.name = name
            session.add(note)
            session.commit()
            return "Done"
        elif model == "sc":
            note = session.query(models_dict.get(model)).get(note_id)
            note.value = name
            session.add(note)
            session.commit()
            return "Done"
    except AttributeError:
        print("Id is not exist")


def delete_func(model: str, note_id: int) -> str:
    try:
        if model not in models_dict:
            pass

        elif model in ["t", "g", "st", "l", "sc"]:
            note = session.query(models_dict.get(model)).get(note_id)
            note.name = name
            session.delete(note)
            session.commit()
            return "Done"

    except AttributeError:
        print("Id is not exist")


if __name__ == '__main__':
    res = handler()
    try:
        for n, i in enumerate(res, start=1):
            print(n, i)
    except TypeError:
        print("Write right args, use -h for help")
