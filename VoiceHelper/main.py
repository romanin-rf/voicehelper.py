import VoiceHelper as VH
from rich.console import Console

# Консоль
c = Console()

# Логирование
def log_neuro(text: str) -> None:
    c.print(f"[blue]NeuralNetwork[/] [green]->[/] [yellow]{text}[/]")

def log_user(text: str) -> None:
    c.print(f"[red]YOU[/] [green]->[/] [yellow]{text}[/]")

# Загрузка нейросети
c.rule("Загрузка нейросетей")
vh = VH.VoiceHelper(
    VH.SpeechSynthesizer(speaker='kseniya', last_callback=log_neuro),
    VH.SpeechRecognition('ru_small', last_callback=log_user)
)

# Команды
@vh.add_command(["привет", "здравствуй"])
def Hello(text: str):
    vh.say("Привет!")

@vh.add_command(["пока", "выключить", "спокойной ночи"])
def GoodBye(text: str):
    vh.say("Пока!")
    vh.stop()

# Включение
if __name__ == "__main__":
    c.rule("Логи")
    vh.start()