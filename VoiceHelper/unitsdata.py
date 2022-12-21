import os

VOSK_MODELS_LIST_URL: str = "https://github.com/romanin-rf/voicehelper.py-models/raw/main/models.json"
LOCAL_DIR: str = os.path.split(__file__)[0]
VOSK_MODELS_DIR: str = os.path.join(LOCAL_DIR, "models", "srec").replace(os.sep, "/")
SILERO_MODELS_DIR: str = os.path.join(LOCAL_DIR, "models", "ssynth").replace(os.sep, "/")
