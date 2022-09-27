from . import CommandsHandler
from . import NueroNetworks
from typing import Optional, Union, NoReturn

class VoiceHelper:
    def __init__(
        self,
        speech_synthesizer=None,
        speech_recognition=None,
        accuracy_threshold: Optional[int]=None
    ) -> None:
        self.SSynth = speech_synthesizer or NueroNetworks.SpeechSynthesizer()
        self.SRec = speech_recognition or NueroNetworks.SpeechRecognition()
        self.AccuracyThreshold = accuracy_threshold or 90
        self.CommandsHandler = CommandsHandler.CommandsHandler(self.AccuracyThreshold)
    
    def __callback(self, text: str) -> None:
        data = self.CommandsHandler.search_method(text)
        if data is not None:
            method, args = data
            method(*args)
    
    def add_command(self, pattern: Optional[Union[str, list[str]]]=None):
        def adder(method):
            if not self.CommandsHandler.exsist_method(method):
                self.CommandsHandler.add_method(pattern, method)
            def wrapper(*args):
                return method(*args)
            return wrapper
        return adder
    
    def say(self, text: str) -> None:
        self.SSynth.say(text)
    
    def get_audio(self, text: str) -> NueroNetworks.torch.Tensor:
        return self.SSynth.get_audio(text)

    def play_audio(self, audio: NueroNetworks.torch.Tensor) -> None:
        self.SSynth.play_audio(audio)
    
    def start(self) -> NoReturn:
        self.SRec.start(self.__callback)
    
    def stop(self) -> NoReturn:
        self.SRec.stop()
