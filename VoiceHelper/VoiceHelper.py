import os
import time
import unitsdata
import sounddevice as sd
import queue
import json
# Big Libs
import vosk
import torch
# More
from fuzzywuzzy import fuzz
# Type Alias
from typing import Literal, Optional, NoReturn, Union, Any

# Функции
def get_model_path(name: str, *, models_path: Optional[str]=None) -> Optional[str]:
    models_path = models_path or unitsdata.VOSK_MODELS_DIR
    if name in os.listdir(models_path):
        return models_path + "/" + name

# Классы
class SpeechSynthesizer:
    def __init__(
        self,
        language: Optional[str]=None,
        model_id: Optional[str]=None,
        sample_rate: Optional[int]=None,
        speaker: Optional[Literal['aidar', 'baya', 'kseniya', 'xenia']]=None,
        put_accent: Optional[bool]=None,
        put_yo: Optional[bool]=None,
        device_type: Optional[Literal['cpu', 'gpu']]=None,
        *,
        last_callback: Optional[Any]=None
    ) -> None:
        self.Language = language or "ru"
        self.ModelID = model_id or "ru_v3"
        self.SampleRate = (sample_rate or 48000)
        self.Speaker = speaker or "baya"
        self.PutAccent = put_accent or True
        self.PutYo = put_yo or True
        self.TorchDevice = torch.device(device_type or 'cpu')
        try:
            self.Model, self._, = torch.hub.load(
                repo_or_dir="snakers4/silero-models",
                model="silero_tts",
                language=self.Language,
                speaker=self.ModelID
            )
        except:
            self.Model, self._, = torch.hub.load(
                repo_or_dir="snakers4/silero-models",
                model="silero_tts",
                source="local",
                language=self.Language,
                speaker=self.ModelID
            )
        self.LastCallback = last_callback
        self.Model.to(self.TorchDevice)
    
    def __play(self, audio) -> None:
        sd.play(audio)
        time.sleep((len(audio) / self.SampleRate) + 0.5)
        sd.stop()
    
    def __generate_audio(self, text: str):
        return self.Model.apply_tts(
            text=text,
            speaker=self.Speaker,
            sample_rate=self.SampleRate,
            put_accent=self.PutAccent,
            put_yo=self.PutYo
        )
    
    def say(self, text: str) -> None:
        self.__play(
            self.__generate_audio(text)
        )
        if not(self.LastCallback is None):
            self.LastCallback(text)

class SpeechRecognition:
    def __init__(
        self,
        name: Optional[Literal["ru_small", "ru_big"]]=None,
        *,
        device_id: Optional[int]=None,
        sample_rate: Optional[int]=None,
        models_path: Optional[str]=None,
        last_callback: Optional[Any]=None
    ) -> None:
        self.Name: str = name or "ru_small"
        self.DeviceID: int = device_id or 1
        self.SampleRate: int = sample_rate or 16000
        self.Model = vosk.Model(
            get_model_path(
                self.Name,
                models_path=models_path
            )
        )
        self.LastCallback = last_callback
        self.Queue = queue.Queue()
        self.Listening: bool = False
    
    def __callback(self, indata, frames: int, time, status):
        self.Queue.put(bytes(indata))
    
    def __stream(self, callback) -> None:
        with sd.RawInputStream(
            samplerate=self.SampleRate,
            blocksize=8000,
            device=self.DeviceID,
            dtype="int16",
            channels=1,
            callback=self.__callback
        ):
            rec = vosk.KaldiRecognizer(self.Model, self.SampleRate)
            while self.Listening:
                if rec.AcceptWaveform(self.Queue.get()):
                    answer = json.loads(rec.Result())["text"]
                    if answer != "":
                        callback(answer)
                        if not(self.LastCallback is None):
                            self.LastCallback(answer)

    def start(self, callback) -> NoReturn:
        self.Listening = True
        self.__stream(callback)
    
    def stop(self) -> NoReturn:
        self.Listening = False

# Классы обработки
class Command:
    def __init__(self, pattern: Optional[Union[str, list[str]]], method: Any, *, mrt: Optional[int]=None) -> None:
        self.pattern: Optional[Union[str, list[str]]] = pattern
        self.method = method
        self.mrt = mrt or 90
    
    def get(self, text: Optional[str]) -> Optional[Any]:
        if not(self.pattern is None):
            if isinstance(self.pattern, str):
                if fuzz.ratio(self.pattern, text) >= self.mrt:
                    return self.method
            elif isinstance(self.pattern, list):
                for i in self.pattern:
                    if fuzz.ratio(i, text) >= self.mrt:
                        return self.method
        else:
            return self.method

class VoiceHandler:
    def __init__(
        self,
        mrt: Optional[int]=None
    ) -> None:
        self.mrt = mrt or 90
        self.commands: list[Command] = []

    def add_method(self, text: Optional[Union[str, list[str]]], method: Any) -> None:
        if isinstance(text, str):
            text = text.lower()
        elif isinstance(text, list):
            text = [i.lower() for i in text]
        self.commands.append(
            Command(text, method, mrt=self.mrt)
        )

    def exsist_method(self, method: Any) -> bool:
        for i in self.commands:
            if method == i.method:
                return True
        return False

    def search_method(self, text: Optional[str]) -> Optional[Any]:
        for i in self.commands:
            m = i.get(text)
            if not(m is None):
                return m

# Главный класс
class VoiceHelper:
    def __init__(
        self,
        speech_synthesizer: Optional[SpeechSynthesizer]=None,
        speech_recognition: Optional[SpeechRecognition]=None,
        
    ) -> None:
        self.SSyn = speech_synthesizer or SpeechSynthesizer()
        self.SRec = speech_recognition or SpeechRecognition()
        self.VHand = VoiceHandler()
    
    def __callback(self, text: str) -> NoReturn:
        m = self.VHand.search_method(text)
        if not(m is None):
            return m(text)

    def say(self, text: str) -> None:
        self.SSyn.say(text)
    
    def add_command(self, text: Optional[Union[str, list[str]]]=None) -> None:
        def adder(method: Any):
            if not self.VHand.exsist_method(method):
                self.VHand.add_method(text, method)
            def wrapper(text: str):
                return method(text)
            return wrapper
        return adder
    
    def start(self) -> NoReturn:
        self.SRec.start(self.__callback)

    def stop(self) -> NoReturn:
        self.SRec.stop()