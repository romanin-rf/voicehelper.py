import os
import io
import time
import sounddevice as sd
import soundfile as sf
import queue
import json
# More
from . import unitsdata
# Big Libs
import vosk
import torch
# Type Alias
from typing import Literal, Optional, NoReturn, Any

# Функции
def get_model_sr_path(name: str, *, models_path: Optional[str]=None) -> Optional[str]:
    models_path = models_path or unitsdata.VOSK_MODELS_DIR
    if name in os.listdir(models_path):
        return models_path + "/" + name

def get_model_ss_path(lang: str, model_id: str, *, models_path: Optional[str]=None) -> Optional[str]:
    models_path = models_path or unitsdata.SILERO_MODELS_DIR
    name = f"{lang}-{model_id}.pt"
    if name in os.listdir(models_path):
        return models_path + "/" + name

def generate_ss_model_path(lang: str, model_id: str, *, models_path: Optional[str]=None) -> Optional[str]:
    models_path = models_path or unitsdata.SILERO_MODELS_DIR
    model_path = models_path + "/" + f"{lang}-{model_id}.pt"
    if not os.path.exists(model_path):
        return model_path

# Классы
class SpeechSynthesizer:
    def __init__(
        self,
        language: Optional[str]=None,
        model_id: Optional[str]=None,
        sample_rate: Optional[Literal[48000, 24000, 16000, 8000]]=None,
        speaker: Optional[str]=None,
        put_accent: Optional[bool]=None,
        put_yo: Optional[bool]=None,
        device_type: Optional[Literal["cpu", "cuda"]]=None,
        thread_count: Optional[int]=None,
        *,
        models_path: Optional[str]=None,
        last_callback: Optional[Any]=None
    ) -> None:
        self.Language = language or "ru"
        self.ModelID = model_id or "ru_v3"
        self.SampleRate = (sample_rate or 48000)
        self.Speaker = speaker or "baya"
        self.PutAccent = put_accent or True
        self.PutYo = put_yo or True
        self.TorchDevice = torch.device((device_type or 'cpu'))
        self.ThreadCount = thread_count or 2
        torch.set_num_threads(self.ThreadCount)
        model_path = get_model_ss_path(self.Language, self.ModelID, models_path=models_path)
        if model_path is None:
            model_path = generate_ss_model_path(self.Language, self.ModelID, models_path=models_path)
            torch.hub.download_url_to_file(
                f"https://models.silero.ai/models/tts/{self.Language}/{self.ModelID}.pt",
                model_path
            )
        self.Model = torch.package.PackageImporter(model_path).load_pickle("tts_models", "model")
        self.Model.to(self.TorchDevice)
        self.LastCallback = last_callback
    
    def __play(self, audio) -> None:
        sd.play(audio)
        time.sleep((len(audio) / self.SampleRate) + 0.5)
        sd.stop()
    
    def __generate_audio(self, text: str) -> torch.Tensor:
        return self.Model.apply_tts(
            text=text,
            speaker=self.Speaker,
            sample_rate=self.SampleRate,
            put_accent=self.PutAccent,
            put_yo=self.PutYo
        )
    
    def get_audio_bytes(
        self,
        text: str,
        form: Literal["WAV", "WAVEX", "OGG", "AIFF", "CAF", "RAW"]=None,
        subtype: Literal["DOUBLE", "FLOAT", "PCM_U8", "PCM_S8", "PCM_16", "PCM_24", "PCM_32"]=None
    ) -> bytes:
        bio, form, subtype = io.BytesIO(), form or "WAV", subtype or "PCM_32"
        sf.write(bio, self.__generate_audio(text), self.SampleRate, subtype="FLOAT", format="WAV")
        bio.seek(0)
        return bio.read()
    
    def get_audio(self, text: str) -> torch.Tensor:
        return self.__generate_audio(text)
    
    def play_audio(self, audio: Any) -> None:
        self.__play(audio)
    
    def say(self, text: str) -> None:
        self.__play(
            self.__generate_audio(text)
        )
        if not(self.LastCallback is None):
            self.LastCallback(text)

class SpeechRecognition:
    def __init__(
        self,
        name: Optional[str]=None,
        sample_rate: Optional[int]=None,
        *,
        device_id: Optional[int]=None,
        models_path: Optional[str]=None,
        last_callback: Optional[Any]=None
    ) -> None:
        self.Name: str = name or "ru_small"
        self.SampleRate: int = sample_rate or 16000
        self.DeviceID: int = device_id or 1
        self.Model = vosk.Model(
            get_model_sr_path(
                self.Name,
                models_path=models_path
            )
        )
        self.LastCallback = last_callback
        self.Queue = queue.Queue()
        self.Listening: bool = False
    
    def __callback(self, indata, frames: int, time, status: sd.CallbackFlags):
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
                        self.Queue.task_done()
                        if self.LastCallback is not None:
                            self.LastCallback(answer)
                        callback(answer)

    def start(self, callback) -> NoReturn:
        self.Listening = True
        self.__stream(callback)
    
    def stop(self) -> NoReturn:
        self.Listening = False