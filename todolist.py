import sqlite3
import uuid
import sys

def load_tasks():
    with sqlite3.connect('todoList.db') as con:
        cursor = con.cursor()
    
        cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            completed INTEGER NOT NULL DEFAULT 0,
            due_date TEXT
        )
        ''')

def add_task(task_name, task_description=None, due_date=None):
    with sqlite3.connect('todoList.db') as con:
        cursor = con.cursor()

        cursor.execute('''
        INSERT INTO tasks(id, name, description, completed, due_date)
        VALUES (?, ?, ?, 0, ?)
        ''', (str(uuid.uuid4()), task_name, task_description, due_date,))
        
        con.commit()
        print("\nTask added!")

def list_tasks():
    with sqlite3.connect('todoList.db') as con:
        cursor = con.cursor()

        cursor.execute('SELECT * FROM tasks')
        tasks = cursor.fetchall()

        if not tasks:
            print("\nNo tasks :(")
        else:
            for task in tasks:
                status = "Completed" if task[3] == 1 else "Not Complete"
                print(f"\nID: {task[0]}\nTask: {task[1]}\nDescription: {task[2]}\nStatus: {status}\nDue: {task[4]}\n\n")

def remove_task(remove):
    with sqlite3.connect('todoList.db') as con:
        cursor = con.cursor()

        cursor.execute("DELETE FROM tasks WHERE id = ?", (remove,))
        con.commit()

        if cursor.rowcount > 0: print("\nTask removed.")
        else: print("\nTask unable to be removed. Check uuid or if task exists.\n")

def mark_complete(task):
    with sqlite3.connect('todoList.db') as con:
        cursor = con.cursor()

        cursor.execute('SELECT completed FROM tasks WHERE id = ?', (task,))
        completeCheck = cursor.fetchone()
        if completeCheck[0] == 1: 
            print("\nTask already complete\n")
            return
        if completeCheck[0] == None: print("Task not found.")

        cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (1, task))
        con.commit()

        if cursor.rowcount > 0: print("\nTask updated.")
        else: print("\nTask not updated. Check uuid or if task exists.")

def main():
    load_tasks()

    while True:
        print("\nWelcome to the To-Do list!")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Remove Task")
        print("4. Mark Task As Complete")
        print("5. Exit\n")

        while True:
            try:
                choice = int(input("What would you like to do?\n")) 
                break
            except ValueError:
                print("Please type an integer")

        if choice == 1:
            task_name = input("\nEnter task name: ")
            description = input("\nEnter description of task: ")
            due_date = input("\nEnter due date (optional): ")
            add_task(task_name, description, due_date)
        elif choice == 2:
            list_tasks()
        elif choice == 3:
            removeChoice = input("\nWhich task would you like to remove? (enter uuid): ")
            remove_task(removeChoice)
        elif choice == 4:
            markComplete = input("\nWhich task would you like to mark as complete? (enter uuid): ")
            mark_complete(markComplete)
        elif choice == 5:
            print("\nGoodbye.")
            sys.exit(0)

if __name__ == "__main__":
    main()

