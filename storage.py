import json
from typing import Type, TypeVar, List
# Generic type variable for model classes
T = TypeVar('T') 

class JSONStorage:
    def __init__(self, filename: str):
        self.filename = filename
    #using object injection to make storage more flexible and reusable across different data types (users, tasks, etc.)
    def load_data(self, model_class: Type[T]) -> List[T]:
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
        # If file doesn't exist or is empty/corrupted, return an empty list instead of crashing.
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        # Convert list of dictionaries to list of model instances using the from_dict class method.
        return [model_class.from_dict(item) for item in raw_data]

    # Convert list of model instances to list of dictionaries and save to JSON file.
    def save_data(self, items: list) -> None:
        raw_data = [item.to_dict() for item in items]

        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(raw_data, f, indent=2)