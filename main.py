from storage import JSONStorage
from todolist import TodoList
from task import Task
from user_manager import UserManager, User

def main():
    #user management setup
    user_storage = JSONStorage("users.json")
    users_data = user_storage.load_data(User) 
    user_manager = UserManager(users_data, user_storage)

    while True:
        #outerloop for login and user management
        print("\n=== TODO APP LOGIN ===")
        print("1. Login")
        print("2. Create New User")
        print("3. Delete User")
        print("4. Exit")
        
        choice = input("Choose (1-4): ").strip()
        current_user = None

        match choice:
            case "1":
                user_manager.list_users()
                username = input("Enter username: ").strip()
                current_user = user_manager.get_user(username)
                if not current_user:
                    print("Error: User not found.")
            
            case "2":
                username = input("Enter new username: ").strip()
                if username:
                    user_manager.add(username)
            
            case "3":
                username = input("Enter username to delete: ").strip()
                user_manager.remove(username)
            
            case "4":
                print("Exiting application. Goodbye.")
                break
            
            case _:
                print("Invalid choice. Please try again.")

        # innerloop for task management after successful login
        if current_user:
            print(f"\nWelcome, {current_user.username}!")
            
            user_filename = f"{current_user.username}_todo.json"
            task_storage = JSONStorage(user_filename)
            loaded_tasks = task_storage.load_data(Task)
            my_list = TodoList(loaded_tasks, task_storage)

            while True:
                print(f"\n--- {current_user.username}'s Tasks ---")
                print("1. Add Task")
                print("2. List Tasks")
                print("3. Complete/Toggle Task")
                print("4. Remove Task")
                print("5. Sort & Filter")
                print("6. Logout")
                
                cmd = input("Select command: ").strip()

                match cmd:
                    case "1":
                        desc = input("Task description: ")
                        prio = input("Priority (1-5): ")
                        tags = input("Tags (comma separated): ")
                        end_date = input("End date (YYYY-MM-DD HH:MM, optional): ")
                        
                        prio = int(prio) if prio.isdigit() else 1
                        tags_list = [t.strip().lower() for t in tags.split(",")] if tags else []
                        
                        my_list.add_task(desc, priority=prio, tags=tags_list, end_date=end_date)
                        print("SUCCESS: Task added.")

                    case "2":
                        my_list.print_tasks()

                    case "3":
                        try:
                            user_input = input("Enter Task # to toggle: ")
                            selection_index = int(user_input)
                        except ValueError:
                            print("Error: Please enter a valid number.")

                        if 1 <= selection_index <= len(my_list.tasks):
                            task = my_list.tasks[selection_index - 1]
                            task.toggle()
                            my_list.storage.save_data(my_list.tasks)
                            print(f"Task '{task.description}' marked as {'done' if task.is_done else 'not done'}.")
                        else:
                            print("Invalid task number.")

                    case "4":
                        if not my_list.tasks:
                            print("No tasks to remove.")
                            continue
                        try:
                            user_input = input("Enter Task to remove: ")

                            try:
                                user_input = int(user_input)
                            except ValueError:
                                print("Error: Please enter a valid number.")
                                continue

                            if user_input == 0:
                                print("Invalid task selected.")
                                continue
                                
                            if 1 <= user_input <= len(my_list.tasks):
                                task_to_remove = my_list.tasks[user_input - 1]
                                my_list.remove_task(task_to_remove.id)
                            else:
                                print("Invalid task number.")

                        except ValueError:
                            print("Error: Please enter a valid number.")

                    case "5":
                        print("\n--- SORT & FILTER ---")
                        print("1. Sort by Priority (High -> Low)")
                        print("2. Sort by Date...")
                        print("3. Filter by Tag")
                        print("4. Reset Order")
                        
                        sub_cmd = input("Select option: ").strip()
                        
                        match sub_cmd:
                            case "1":
                                my_list.sort_by_priority()
                                print("Sorted by Priority:")
                                my_list.print_tasks()

                            case "2":
                                #sub-menu for date sorting options
                                print("\n   1. By Creation Date (Oldest First)")
                                print("   2. By Due Date (Urgent First)")
                                date_choice = input("   Choose Date Sort: ").strip()
                                
                                if date_choice == "1":
                                    my_list.sort_by_creation_date()
                                    print("Sorted by Creation Date:")
                                elif date_choice == "2":
                                    my_list.sort_by_end_date()
                                    print("Sorted by Due Date:")
                                else:
                                    print("Invalid date choice.")
                                
                                my_list.print_tasks()

                            case "3":
                                tag = input("Enter tag: ").strip().lower()
                                results = my_list.filter_by_tags(tag)
                                if results:
                                    print(f"\n--- Found {len(results)} tasks ---")
                                    my_list.print_tasks(results)
                                else:
                                    print(f"No tasks found with tag #{tag}.")

                            case "4":
                                my_list.reset_filters()
                                print("Order reset:")
                                my_list.print_tasks()

                            case _:
                                print("Invalid sort option.")

                    case "6":
                        print("Logging out...")
                        break 
                    
                    case _:
                        print("Unknown command.")

if __name__ == "__main__":
    main()