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


def _print_todos():
    todo_list = ['Do yoga',
                 'Make breakfast',
                 'Learn basics of SQL',
                 'Learn what is ORM', ]
    print('Today:')
    for index, todo in enumerate(todo_list):
        print(f'{index + 1}) {todo}')


def print_menu():
    global index
    todo_list = [
        "Today's tasks",
        "Week's tasks",
        "All tasks",
        'Add task',
    ]
    for index, todo in enumerate(todo_list):
        print(f'{index + 1}) {todo}')
    print('0) Exit')


def add_task(session):
    print('Enter task')
    task = input()
    print('Enter deadline')
    deadline = input()
    date_deadline = date.fromisoformat(deadline)
    new_row = Table(task=task, deadline=date_deadline)
    session.add(new_row)
    session.commit()
    print('The task has been added!')


def print_todos(session, period=None):
    strperiod = period

    if period == None:
        strperiod = 'All'

    if strperiod.upper() == 'ALL':
        print()
        print('All tasks:')
        task_list = session.query(Table).order_by(Table.deadline).all()
        if len(task_list) == 0:
            print("Nothing to do!")
            return

        for item_index, item in enumerate(task_list):
            print(f'{item_index + 1}. {item.task}. {item.deadline.strftime("%-d %b")}')

    elif strperiod.upper() == 'WEEK':
        week_list = DatetimeBorder(datetime=datetime.today().date()).week_date_list()
        for week_date in week_list:
            print()
            task_list = session.query(Table).filter_by(deadline=week_date).all()
            print(week_date.strftime('%A %d %b') + ':')

            if len(task_list) == 0:
                print("Nothing to do!")

            for item_index, item in enumerate(task_list):
                print(f'{item_index + 1}. {item}')

    elif strperiod.upper() == 'TODAY':
        print('Today', datetime.today().strftime('%d %b'))
        task_list = session.query(Table).filter_by(deadline=datetime.today()).all()

        if len(task_list) == 0:
            print("Nothing to do!")
            return

        for item_index, item in enumerate(task_list):
            print(f'{item_index + 1}. {item}')


class DatetimeBorder:

    def __init__(self, datetime=None, strdatetime=None, dictdatetime=None):
        self.datetime = None

        if datetime is not None:
            self.datetime = datetime

        if strdatetime is not None:
            self.datetime = date.fromisoformat(strdatetime)

        if dictdatetime is not None:
            self.datetime = datetime.date(dictdatetime.get('year'),
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


if __name__ == '__main__':
    import os

    # if not os.path.exists('todo.db'):
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

        # add new task
        if command == 4:
            add_task(session)
            continue
