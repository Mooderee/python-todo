class User:
    def __init__(self, username: str):
        self.username = username

    def to_dict(self) -> dict:
        return {
            "username": self.username
        }
#same pattern as Task: using a class method as a factory to create User objects from dictionaries.
    @classmethod    
    def from_dict(cls, data: dict) -> "User":
        return cls(
            username = data.get("username")
        )
