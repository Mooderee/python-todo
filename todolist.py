from task import Task
from datetime import datetime

class TodoList:
    def __init__(self, tasks: list = None, storage = None):
        self.tasks = tasks if tasks else []
        self.storage = storage
    # The add_task method is responsible for creating a new Task object and adding it to the todo list. It also handles assigning a unique ID to each task and saving the updated list to storage.
    def add_task(self, description: str, is_done: bool = False, priority: int = 1, tags: list = None, end_date = None) -> None:
        #using lambda to calculate the next ID based on existing tasks. If there are no tasks, it starts at 1. Otherwise, it finds the max ID and adds 1.
        calculate_id = lambda tasks: 1 if not tasks else max(t.id for t in tasks) + 1
        new_id = calculate_id(self.tasks)

        new_task = Task (
            id = new_id,
            description = description,
            is_done = is_done,
            priority = priority,
            tags = tags,
            end_date =  end_date
        )

        self.tasks.append(new_task)

        if self.storage:
            self.storage.save_data(self.tasks)

    def remove_task(self, task_id: int) -> None:
            # 1. Find the specific task object with that ID
            task_to_remove = next((t for t in self.tasks if t.id == task_id), None)
        
            if task_to_remove:
                self.tasks.remove(task_to_remove)
                if self.storage:
                    self.storage.save_data(self.tasks)
                print(f"Task {task_id} removed.")
            else:
                print(f"Task with ID {task_id} not found.")
            
    def print_tasks(self, tasks_to_print: list[Task] = None) -> None:
        tasks = tasks_to_print if tasks_to_print is not None else self.tasks
        
        if not tasks:
            print("Your todo list is empty.")
            return

        for task in tasks:
            print(task)

    def sort_by_priority(self) -> None:
        self.tasks.sort(key=lambda task: task.priority, reverse=True)

    def sort_by_creation_date(self) -> None:
        self.tasks.sort(key=lambda task: task.created_at)  

    def sort_by_end_date(self) -> None:
        self.tasks.sort(key=lambda task: task.end_date if task.end_date else datetime.max)

    def filter_by_tags(self, selected_tag: str) -> list[Task]:
        filtered_tasks = [task for task in self.tasks if selected_tag in task.tags] #need to enforce tag being lowercase when added
        return filtered_tasks
        
    def reset_filters(self) -> None:
        self.tasks.sort(key=lambda task: task.id)