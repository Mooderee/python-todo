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
            # Fallback if format is broken
            description = line[4:].strip()

        parsed_lines.append({'is_done': is_done, 'description': description})

    return parsed_lines


def save_tasks(task_list: list):
    lines_to_save = []

    for task in task_list:
        is_done = task.get('is_done')
        description = task.get('description')

        status = '[x]' if is_done else '[ ]'  # Pythonic ternary operator

        new_task = f"{status} - {description}\n"
        lines_to_save.append(new_task)

    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        f.writelines(lines_to_save)
    print("-> File saved.")


def add_task(task_list: list, description: str):
    new_task = {
        'is_done': False,
        'description': description
    }
    task_list.append(new_task)
    save_tasks(task_list)


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
        print(f"-> Toggled task {task_number}")


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


print("Welcom in the To Do app")
print(
'''Menu:
1) add task
2) remove task
3) modify task
4) display current tasks
5) exit app
''')

app_state = True

while app_state:

    user_input = int(input("select option: "))

    match user_input:
        case 1:
            #add task
            pass
        case 2:
            #remove task
            pass
        case 3:
            #modify task
            pass
        case 4:
            #display tasks
            pass
        case 5:
            #exit app
            pass
        case _:
            #invalid option selected
            pass

