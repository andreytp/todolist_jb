from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime
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
        'Add task',
    ]
    for index, todo in enumerate(todo_list):
        print(f'{index + 1}) {todo}')
    print('0) Exit')


def add_task(session):
    new_row = Table(task=input(), deadline=datetime.today())
    session.add(new_row)
    session.commit()

def print_todos(session):

    task_list = session.query(Table).all()

    if len(task_list) == 0:
        print("Nothing to do!")
        return

    for index, item in enumerate(task_list):
        print(f'{index + 1}. {item}')



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
        command = input('>')

        # exit
        if command == '0':
            print('Bye!')
            break

        # today's tasks
        if command == '1':
            print_todos(session)
            continue

        # add new task
        if command == '2':
            add_task(session)
            continue
