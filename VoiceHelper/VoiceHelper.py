from . import NueroNetworks, CommandsHandler
from typing import Optional, Union, NoReturn, Any

class VoiceHelper:
    def __init__(
        self,
        speech_synthesizer: Optional[NueroNetworks.SpeechSynthesizer]=None,
        speech_recognition: Optional[NueroNetworks.SpeechRecognition]=None,
        accuracy_threshold: Optional[int]=None
    ) -> None:
        self.SSynth = speech_synthesizer or NueroNetworks.SpeechSynthesizer()
        self.SRec = speech_recognition or NueroNetworks.SpeechRecognition()
        self.AccuracyThreshold = accuracy_threshold or 90
        self.CommandsHandler = CommandsHandler.CommandsHandler(self.AccuracyThreshold)
    
    def __callback(self, text: str):
        method = self.CommandsHandler.search_method(text)
        if method is not None:
            method(text)
    
    def add_command(self, pattern: Optional[Union[str, list[str]]]=None):
        def adder(method):
            if not self.CommandsHandler.exsist_method(method):
                self.CommandsHandler.add_method(pattern, method)
            def wrapper(text: str):
                return method(text)
            return wrapper
        return adder
    
    def say(self, text: str) -> None:
        self.SSynth.say(text)
    
    def start(self) -> NoReturn:
        self.SRec.start(self.__callback)
    
    def stop(self) -> NoReturn:
        self.SRec.stop()
