# voicehelper.py
## Описание
Это модуль соединивший в себе две нейронные сети. Для упрощения создания голосового помошника.
## Установка
- **Windows**:
```cmd
pip install https://github.com/romanin-rf/voicehelper.py/releases/download/v0.1.2/voicehelper.py-0.1.2-py3.9.whl
```
## Пример
- main.py
```python
import VoiceHelper
from rich.console import Console

# Консоль
c = Console()

# Класс нейросети
c.clear()
c.rule("Запуск")

# Процесс иницализации
try:
    ssynth = VoiceHelper.SpeechSynthesizer(
        device_type="cuda"
    )
except:
    ssynth = VoiceHelper.SpeechSynthesizer(
        device_type="cpu"
    )
vh = VoiceHelper.VoiceHelper(
    ssynth,
    VoiceHelper.SpeechRecognition()
)

# Команды
@vh.add_command("привет")
def Hello(event: VoiceHelper.Event):
    vh.say("Ага, я здесь!")

@vh.add_command(["скажи <text>"])
def cSay(event: VoiceHelper.Event, text: str):
    vh.say(text)

@vh.add_command("пока")
def cGoodBye(event: VoiceHelper.Event):
    vh.say("До свидания!")
    vh.stop()

@vh.add_command("<text>")
def cLogger(event: VoiceHelper.Event, text: str) -> None:
    c.print(f"[red]You[/] [green]->[/] [yellow]{text}[/]")

# Запуск
if __name__ == "__main__":
    c.rule("Логи")
    vh.start()
```
