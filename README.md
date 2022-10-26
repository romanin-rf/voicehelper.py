# voicehelper.py
## Описание
Это модуль соединивший в себе две нейронные сети. Для упрощения создания голосового помошника.
## Установка
- **Windows**:
```cmd
pip install --upgrade voicehelper.py
```
## Название моделей для загрузки
- Для [SpeechSynthesizer](https://github.com/snakers4/silero-models#v3)
- Для [SpeechRecognition](https://github.com/romanin-rf/voicehelper.py-models#for-speechrecognition)


## Пример
- Пример создания Голосового Ассистента
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
- Пример генерации голоса
```python
from VoiceHelper.NueroNetworks import SpeechSynthesizer

ss = VoiceHelper.SpeechSynthesizer(sample_rate=48000, thread_count=1) # по умолчанию стоит русская речь

with open("test.wav", "wb") as file:
    file.write(ss.get_audio_bytes("Привет!", "WAV", "PCM_32"))
```
