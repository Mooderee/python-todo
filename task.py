from asyncio import tasks
from datetime import datetime


DATE_FORMAT = "%Y-%m-%d %H:%M"

class Task:
    def __init__(self, id: int, description: str, is_done: bool = False, priority: int = 1, tags: list = None, created_at = None, end_date = None):
        self.id = id
        self.description = description
        self.is_done = is_done
        self.priority  = priority

        self.tags = tags  if tags is not None else []


        if created_at is None:
            self.created_at = datetime.now()
        elif isinstance(created_at, str):
            self.created_at  = datetime.strptime(created_at, DATE_FORMAT)
        else:
            self.created_at = created_at

        if not end_date:
            self.end_date = None
        elif isinstance(end_date, str):
            try:
                self.end_date = datetime.strptime(end_date, DATE_FORMAT)
            except ValueError:
                print(f"Warning: Invalid date format '{end_date}'. Task saved without end date.")
                self.end_date = None
        else:
            self.end_date = end_date

# The __str__ method defines how the object is represented as a string, which is useful for printing.
    def __str__(self):
        status = '[x]' if self.is_done else '[ ]'
        
        if self.tags:
            tags_string = " " + " ".join([f"#{tag}" for tag in self.tags])
        else:
            tags_string = ""

        created_str = f" [Created: {self.created_at.strftime('%Y-%m-%d')}]"

        end_str = ""
        if self.end_date:
            end_str = f" [Due: {self.end_date.strftime('%Y-%m-%d')}]"

        return f"{status} {self.description} (Priority: {self.priority}){tags_string}{created_str}{end_str}"    

    def toggle(self) -> None:
        self.is_done = not self.is_done

    def add_tag(self, tag_name:str) -> None:
        if tag_name not in self.tags:
            self.tags.append(tag_name)
    # The to_dict method converts the Task object into a dictionary format, which is necessary for saving to JSON. It also formats the datetime objects as strings.
    def to_dict(self) -> dict:
        return{
            "id": self.id,
            "description": self.description,
            "is_done": self.is_done,
            "priority": self.priority,
            "tags": self.tags,
            "created_at": self.created_at.strftime(DATE_FORMAT),
            "end_date": self.end_date.strftime(DATE_FORMAT) if self.end_date else None
        }
    #using a class method as a factory to create Task objects from dictionaries, which is useful when loading from JSON.
    @classmethod    
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            id = data.get("id"),
            description = data.get("description"),
            is_done = data.get("is_done"),
            priority = data.get("priority"),
            tags = data.get("tags"),
            created_at = data.get("created_at"),
            end_date = data.get("end_date")
        )
