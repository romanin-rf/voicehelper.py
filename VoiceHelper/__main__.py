import VoiceHelper
from rich.console import Console

# Консоль
c = Console()

# Класс нейросети
c.clear()
c.rule("Запуск")
vh = VoiceHelper.VoiceHelper()

# Команды
@vh.add_command(["скажи <text>"])
def Hello(text: str):
    vh.say(text)

@vh.add_command("пока")
def GoodBye():
    vh.say("До свидания!")
    vh.stop()

@vh.add_command("<text>")
def cLogger(text: str) -> None:
    c.print(f"[red]You[/] [green]->[/] [yellow]{text}[/]")

# Запуск
if __name__ == "__main__":
    c.rule("Логи")
    vh.start()