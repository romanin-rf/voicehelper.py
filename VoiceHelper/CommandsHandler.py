from fuzzywuzzy import fuzz
from typing import Optional, Union, Any

# Класс обработки
class Command:
    def __init__(
        self,
        pattern: Optional[Union[str, list[str]]],
        method: Any
    ) -> None:
        self.pattern = pattern
        self.method = method

class CommandsHandler:
    def __init__(
        self,
        accuracy_threshold: int
    ) -> None:
        self.accuracy_threshold = accuracy_threshold
        self.commands: list[Command] = []
    
    def exsist_method(self, method: Any) -> bool:
        for i in self.commands:
            if i.method == method:
                return True
        return False
    
    def add_method(self, pattern: Optional[Union[str, list[str]]], method: Any) -> None:
        if isinstance(pattern, list):
            pattern = [i.lower() for i in pattern]
        elif isinstance(pattern, str):
            pattern = pattern.lower()
        self.commands.append(Command(pattern, method))
    
    def search_method(self, text: str) -> Optional[Any]:
        for i in self.commands:
            if i.pattern is not None:
                if isinstance(i.pattern, str):
                    if fuzz.ratio(i.pattern, text) >= self.accuracy_threshold:
                        return i.method
                elif isinstance(i.pattern, list):
                    for pattern in i.pattern:
                        if fuzz.ratio(pattern, text) >= self.accuracy_threshold:
                            return i.method
            else:
                return i.method