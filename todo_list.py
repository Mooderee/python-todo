import os

FILE_NAME = 'todo.txt'


def parse_raw_lines_to_tasks(raw_lines_list: list) -> list:
    parsed_lines = []

    for line in raw_lines_list:
        line = line.strip()
        if not line:
            continue

        is_done = False
        if line.startswith('[x]'):
            is_done = True

        parts = line.split(" - ", 1)

        if len(parts) > 1:
            description = parts[1].strip()
        else:
            description = line[4:].strip()

        parsed_lines.append({'is_done': is_done, 'description': description})

    return parsed_lines


def save_tasks(task_list: list):
    lines_to_save = []

    for task in task_list:
        is_done = task.get('is_done')
        description = task.get('description')

        status = '[x]' if is_done else '[ ]'

        new_task = f"{status} - {description}\n"
        lines_to_save.append(new_task)

    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        f.writelines(lines_to_save)
    print("-> File saved.")

def print_tasks(task_list: list):

    for index, task in enumerate(task_list):
        is_done = task.get('is_done')
        description = task.get('description')

        status = '[x]' if is_done else '[ ]'

        print(f"{index + 1}: {status} - {description}")


def add_task(task_list: list, description: str):
    new_task = {
        'is_done': False,
        'description': description
    }
    task_list.append(new_task)
    save_tasks(task_list)
    print(f"-> Added task: {description}")


def get_index(task_list: list, task_number: str) -> int | None:
    try:
        task_index = int(task_number) - 1
    except ValueError:
        print("! Invalid task number (not a number)")
        return None

    if 0 <= task_index < len(task_list):
        return task_index
    else:
        print("! Task number out of range")
        return None


def remove_task(task_list: list, task_number: str):
    task_index = get_index(task_list, task_number)

    if task_index is not None:
        removed = task_list.pop(task_index)
        save_tasks(task_list)
        print(f"-> Removed: {removed['description']}")


def toggle_status(task_list: list, task_number: str):
    task_index = get_index(task_list, task_number)

    if task_index is not None:
        task_to_toggle = task_list[task_index]
        task_to_toggle['is_done'] = not task_to_toggle['is_done']
        save_tasks(task_list)
        print(f"-> Changed status: {task_to_toggle['description']}")


def change_description(task_list: list, task_number: str, description: str):

    if not description.strip():
        print("! No description provided")
        return

    task_index = get_index(task_list, task_number)
    if task_index is not None:
        task_to_change = task_list[task_index]
        task_to_change['description'] = description
        save_tasks(task_list)
        print(f"-> Changed description to {description}")


tasks = []

if os.path.exists(FILE_NAME):
    with open(FILE_NAME, 'r', encoding='utf-8') as f:
        raw_lines = f.readlines()
        tasks = parse_raw_lines_to_tasks(raw_lines)
        print("File loaded successfully.")
else:
    # Create the file if it doesn't exist
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        pass
    print("Created new todo file.")


print("Welcome in the To Do app")
menu = (
'''Menu:
1) display current tasks
2) add task
3) remove task
4) modify task
5) exit app
''')

app_state = True

while app_state:

    print(menu)

    try:
        option_selected = int(input("select option: "))
    except ValueError:
        print("! Invalid option selected")
        print("Please select option from 1 to 5")
        continue

    match option_selected:
        case 1:
            if tasks:
                print_tasks(tasks)
            else:
                print("! No tasks have been added")

        case 2:
            print("Please provide description for the new task")
            description = input("Description: ")
            if description == "":
                print("Description cannot be empty!")
                continue

            add_task(tasks, description)
        case 3:
            print("Current tasks:")

            if tasks:
                print_tasks(tasks)
            else:
                print("! No tasks have been added")
                continue

            print("Please provide number of the task to be removed")
            task_to_remove = (input("Task number: "))
            remove_task(tasks, task_to_remove)
        case 4:
            print("Please provide number of the task to be modified")
            task_to_modify = (input("Task number: "))

            if task_to_modify == "":
                print("Incorrect task number has been provided")
                continue

            modify_option = 0
            print("Modify a task: provide 1 to change status of the task or 2 to change description")
            try:
                modify_option = int(input("Modify option: "))
            except ValueError:
                print("! Invalid option selected")
                continue

            if modify_option == 1:
                toggle_status(tasks, task_to_modify)
            elif modify_option == 2:
                print("Please provide description for the new task")
                description = input("Description: ")

                if description == "":
                    print("Description cannot be empty!")
                    continue

                change_description(tasks, task_to_modify, description)
            else:
                print("! Invalid option selected")
                continue

        case 5:
            print("Closing the application")
            app_state = False
        case _:
            print("! Invalid option selected")
            print("Please select option from 1 to 5")
            continue

