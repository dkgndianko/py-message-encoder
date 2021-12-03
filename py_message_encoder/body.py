from typing import Dict, Any, List


class MessageBody:
    def __init__(self, field_names: List[str], state: Dict = {}):
        self.state = dict()
        self.field_names = field_names
        if state:
            self.update(state)

    def __setitem__(self, key, value):
        if key not in self.field_names:
            raise KeyError(f"key '{key}' not in this message body")
        self.state[key] = value

    def __getitem__(self, key):
        if key not in self.field_names:
            raise KeyError(f"key '{key}' not in this message body")
        return self.state[key]

    def update(self, values: Dict[str, Any]):
        for key, value in values.items():
            self[key] = value

    def fields_count(self):
        return len(self.field_names)

    def __str__(self):
        return str(self.state)
