import os

LOCAL_DIR: str = os.path.split(__file__)[0].replace(os.sep, "/")
VOSK_MODELS_DIR: str = (LOCAL_DIR + os.sep + "models" + os.sep + "srec").replace(os.sep, "/")