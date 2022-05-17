from . import VoiceHelper
from rich.console import Console

# Консоль
c = Console()

# Класс нейросети
c.clear()
c.rule("Запуск")
vh = VoiceHelper.VoiceHelper()

# Команды
@vh.add_command(["Привет"])
def Hello(text: str):
    vh.say("Здравствуйте!")

@vh.add_command(["Пока"])
def GoodBye(text: str):
    vh.say("До свидания!")
    vh.stop()

@vh.add_command()
def cLogger(text: str) -> None:
    c.print(f"[red]You[/] [green]->[/] [yellow]{text}[/]")

# Запуск
if __name__ == "__main__":
    c.rule("Логи")
    vh.start()