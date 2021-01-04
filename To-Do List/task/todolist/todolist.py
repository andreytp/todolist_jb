from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, date, timedelta
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


class DatetimeBorder:

    def __init__(self, value_datetime=None, strdatetime=None, dictdatetime=None):
        self.datetime = None

        if value_datetime is not None:
            self.datetime = value_datetime

        if strdatetime is not None:
            self.datetime = date.fromisoformat(strdatetime)

        if dictdatetime is not None:
            self.datetime = value_datetime.date(dictdatetime.get('year'),
                                                dictdatetime.get('month'),
                                                dictdatetime.get('day'))

    def week_start(self):
        weekday = self.datetime.weekday()
        return self.datetime + timedelta(days=-weekday)

    def week_end(self):
        weekday = self.datetime.weekday()
        return self.datetime + timedelta(days=(6 - weekday))

    def week_date_list(self):
        weekday = self.datetime.weekday()
        return [self.datetime + timedelta(days=(i - weekday)) for i in range(7)]


def _print_todos():
    todo_list = ['Do yoga',
                 'Make breakfast',
                 'Learn basics of SQL',
                 'Learn what is ORM', ]
    print('Today:')
    for todo_index, todo in enumerate(todo_list):
        print(f'{todo_index + 1}) {todo}')


def print_menu():
    todo_list = [
        "Today's tasks",
        "Week's tasks",
        "All tasks",
        "Missed tasks",
        'Add task',
        'Delete task',
    ]
    for index, todo in enumerate(todo_list):
        print(f'{index + 1}) {todo}')
    print('0) Exit')


def add_task(sqla_session):
    print('Enter task')
    task = input()
    print('Enter deadline')
    deadline = input()
    date_deadline = date.fromisoformat(deadline)
    new_row = Table(task=task, deadline=date_deadline)
    sqla_session.add(new_row)
    sqla_session.commit()
    print('The task has been added!')


def print_todos(sqla_session, period=None):
    strperiod = period

    if period is None:
        strperiod = 'All'

    if strperiod.upper() == 'ALL':
        print_all_todos(sqla_session)

    elif strperiod.upper() == 'WEEK':
        print_weeks_todos(sqla_session)

    elif strperiod.upper() == 'TODAY':
        print_today_todos(sqla_session)

    elif strperiod.upper() == 'MISSED':
        print_missed_todos(sqla_session)


def print_missed_todos(sqla_session):
    print('Missed tasks:')
    task_list = sqla_session.query(Table). \
        filter(Table.deadline < datetime.today().date()). \
        order_by(Table.deadline).all()
    if len(task_list) == 0:
        print("Nothing to do!")
    for item_index, item in enumerate(task_list):
        print(f'{item_index + 1}. {item.task}. {item.deadline.strftime("%-d %b")}')


def print_today_todos(sqla_session):
    print('Today', datetime.today().strftime('%d %b'))
    task_list = sqla_session.query(Table).filter_by(deadline=datetime.today()).all()
    if len(task_list) == 0:
        print("Nothing to do!")
    for item_index, item in enumerate(task_list):
        print(f'{item_index + 1}. {item}')


def print_weeks_todos(sqla_session):
    week_list = DatetimeBorder(value_datetime=datetime.today().date()).week_date_list()
    for week_date in week_list:
        print()
        task_list = sqla_session.query(Table).filter_by(deadline=week_date).all()
        print(week_date.strftime('%A %d %b') + ':')

        if len(task_list) == 0:
            print("Nothing to do!")

        for item_index, item in enumerate(task_list):
            print(f'{item_index + 1}. {item}')


def print_all_todos(sqla_session):
    print()
    print('All tasks:')
    task_list = sqla_session.query(Table).order_by(Table.deadline).all()
    if len(task_list) == 0:
        print("Nothing to do!")
    for item_index, item in enumerate(task_list):
        print(f'{item_index + 1}. {item.task}. {item.deadline.strftime("%-d %b")}')


def delete_task(sqla_session):
    print('Choose the number of the task you want to delete:')
    task_list = sqla_session.query(Table).order_by(Table.deadline).all()
    if len(task_list) == 0:
        print("Nothing to do!")
    todos_dict = {}
    for item_index, item in enumerate(task_list):
        print(f'{item_index + 1}. {item.task}. {item.deadline.strftime("%-d %b")}')
        todos_dict[item_index + 1] = item.id
    item_to_delete = int(input())
    row = sqla_session.query(Table).filter_by(id=todos_dict[item_to_delete]).all()
    if len(row) != 0:
        sqla_session.delete(row[0])
        sqla_session.commit()
        print('The task has been deleted!')


if __name__ == '__main__':

    from sqlalchemy import create_engine

    engine = create_engine('sqlite:///todo.db?check_same_thread=False')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    while True:
        print()
        print_menu()
        command = int(input('>'))

        # exit
        if command == 0:
            print('Bye!')
            break

        # today's tasks
        if command == 1:
            print_todos(session, period='today')
            continue

        # week's tasks
        if command == 2:
            print_todos(session, period='week')
            continue

        # all tasks
        if command == 3:
            print_todos(session, period='all')
            continue

        # missed tasks
        if command == 4:
            print_todos(session, period='missed')
            continue

        # add new task
        if command == 5:
            add_task(session)
            continue

        # delete task
        if command == 6:
            delete_task(session)
            continue
