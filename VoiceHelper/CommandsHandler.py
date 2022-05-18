import vbml
from typing import Optional, Union, Any

# Классы обработки
class Command:
    def __init__(
        self,
        pattern: Optional[Union[vbml.Pattern, list[vbml.Pattern]]],
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
        self.patcher = vbml.Patcher()
    
    def exsist_method(self, method: Any) -> bool:
        for i in self.commands:
            if i.method == method:
                return True
        return False
    
    def add_method(self, pattern: Optional[Union[str, list[str]]], method: Any) -> None:
        if isinstance(pattern, list):
            pattern = [vbml.Pattern(i) for i in pattern]
        elif isinstance(pattern, str):
            pattern = vbml.Pattern(pattern)
        self.commands.append(Command(pattern, method))
    
    def search_method(self, text: str) -> Optional[tuple[Any, tuple]]:
        for i in self.commands:
            if i.pattern is not None:
                if isinstance(i.pattern, vbml.Pattern):
                    d = self.patcher.check(i.pattern, text)
                    if isinstance(d, dict):
                        return i.method, tuple(d.values())
                elif isinstance(i.pattern, list):
                    for p in i.pattern:
                        d = self.patcher.check(p, text)
                        if isinstance(d, dict):
                            return i.method, tuple(d.values())
            else:
                return i.method, tuple([])