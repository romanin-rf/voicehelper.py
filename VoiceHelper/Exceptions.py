class ModelNotFoundError(Exception):
    def __init__(self) -> None:
        self.msg = "Could not find the model, even in the source model list."
    
    def __str__(self) -> str:
        return self.msg
    
    def __repr__(self) -> str:
        return self.__str__()

class AfterZipFileUnpackingCriticalError(Exception):
    def __init__(self) -> None:
        self.msg = "Unknown error after unpacking a zip-file."
    
    def __str__(self) -> str:
        return self.msg
    
    def __repr__(self) -> str:
        return self.__str__()