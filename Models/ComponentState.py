import json


class ComponentState:
    def __init__(self, occupied_capacity: int, is_busy: bool = False):
        self.occupied_capacity = occupied_capacity
        self.is_busy = is_busy

    def __str__(self) -> str:
        return json.dumps(self.__dict__)
