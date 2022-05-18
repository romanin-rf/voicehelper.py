# voicehelper.py
## Описание
Это модуль соединивший в себе две нейронные сети. Для упрощения создания голосового помошника.
## Установка
- Windows 10:
```cmd
pip install https://github.com/romanin-rf/voicehelper.py/releases/download/v0.1.1/voicehelper.py-0.1.1-py3.9.whl
```
## Пример
- main.py
```python
from rich.console import Console

# Класс консоли
c = Console()

# Функции
def log(user: str, text: str) -> None:
    c.print(f"[red]{user}[/] [green]->[/] [yellow]{text}[/]")

c.rule("Запуск")
# Импорт VoiceHelper-a
from VoiceHelper.VoiceHelper import *

# Иницализация
vh = VoiceHelper(
    speech_synthesizer=NueroNetworks.SpeechSynthesizer(thread_count=4),
    speech_recognition=NueroNetworks.SpeechRecognition()
)

# Команды
vh.add_command("скажи <text>")
def cSay(text: str):
    vh.say(text)

vh.add_command(["стоп", "пока"])
def cGoodBuy():
    vh.say("Пока")
    vh.stop()

# Логирование
vh.add_command("<text>")
def cLogger(text: str):
    log("You", text)

# Запуск
if __name__ == "__main__":
    c.rule("Логи")
    vh.start()
```
