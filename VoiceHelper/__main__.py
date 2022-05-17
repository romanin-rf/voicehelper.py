from . import *
from rich.console import Console

c = Console()
vh = VoiceHelper()

def log(text: str) -> None:
    c.print(f"[blue]YOU[/] -> [green]{text}[/]")

@vh.add_command(["привет", "здравствуй"])
def Hello(text: str):
    log(text)
    vh.say("Привет!")

@vh.add_command(["пока", "выключить", "спокойной ночи"])
def GoodBye(text: str):
    log(text)
    vh.say("Пока!")
    vh.stop()

@vh.add_command()
def Testing(text: str):
    log(text)

# Включение
if __name__ == "__main__":
    c.clear()
    c.rule("LOGS")
    vh.start()