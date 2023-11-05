from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey


Base = declarative_base()


# Таблиця студентів з вказівкою до якої групи належить
class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete="CASCADE"))
    group = relationship("Group", back_populates="students", passive_deletes=True)
    scores = relationship("Score", back_populates="student", passive_deletes=True)


# Таблиця груп
class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    students = relationship("Student", back_populates="group", passive_deletes=True)


# Таблиця викладачів
class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    lessons = relationship("Lesson", back_populates="teacher", passive_deletes=True)


# Таблиця предметів з вказівкою викладача, який читає предмет
class Lesson(Base):
    __tablename__ = 'lessons'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    teacher_id = Column(Integer, ForeignKey('teachers.id', ondelete="CASCADE"))
    teacher = relationship("Teacher", back_populates="lessons", passive_deletes=True)
    scores = relationship("Score", back_populates="lesson", passive_deletes=True)


# Таблиця де кожен студент має оцінки з предметів із зазначенням коли оцінку отримано
class Score(Base):
    __tablename__ = 'scores'
    id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey('lessons.id', ondelete="CASCADE"))
    student_id = Column(Integer, ForeignKey('students.id', ondelete="CASCADE"))
    value = Column(Integer)
    date = Column(Date)
    lesson = relationship("Lesson", back_populates="scores", passive_deletes=True)
    student = relationship("Student", back_populates="scores", passive_deletes=True)

