from user import User

class UserManager:
    def __init__(self, users: list[User] = None, storage = None):
        self.users = users if users else []
        self.storage = storage

    def add(self, username: str):
        # 1. Check if user already exists (prevent duplicates)
        if any(u.username.lower() == username.lower() for u in self.users):
            print(f"User '{username}' already exists!")
            return

        # 2. Create and Add
        new_user = User(username)
        self.users.append(new_user)
        
        # 3. Auto-save
        if self.storage:
            self.storage.save_data(self.users)
        print(f"User '{username}' created successfully.")

    def remove(self, username: str):
        # Filter out the user with that name
        initial_count = len(self.users)
        self.users = [u for u in self.users if u.username.lower() != username.lower()]
        
        if len(self.users) < initial_count:
            if self.storage:
                self.storage.save_data(self.users)
            print(f"User '{username}' deleted.")
        else:
            print(f"User '{username}' not found.")

    def get_user(self, username: str) -> User:
        # Helper to find a user object by name
        for user in self.users:
            if user.username.lower() == username.lower():
                return user
        return None

    def list_users(self):
        if not self.users:
            print("No users found.")
            return
            
        print("\n--- Available Users ---")
        for i, user in enumerate(self.users, 1):
            print(f"{i}. {user.username}")
        print("-----------------------")

