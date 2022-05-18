import setuptools
import os

def globalizer(dirpath: str) -> list:
		files = []
		folder_abspath = os.path.abspath(dirpath)
		if os.path.isdir(folder_abspath):
			for i in os.listdir(folder_abspath):
				path = folder_abspath + os.sep + i
				if os.path.isdir(path):
					for _i in globalizer(path):
						files.append(_i)
				elif os.path.isfile(path):
					files.append(path)
		elif os.path.isfile(folder_abspath):
			files.append(folder_abspath)
		return files

setuptools.setup(
    name="voicehelper.py",
    version="0.1.1",
    description="These are two neural networks connected by the same module. One for recognition, the other for voice generation.",
    long_description=open("README.md", "r", errors="ignore").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/romanin-rf/voicehelper.py",
    author="Romanin",
    author_email="semina054@gmail.com",
    license="MIT",
    packages=setuptools.find_packages(),
    package_data={"VoiceHelper": globalizer("VoiceHelper")},
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=["numpy", "sounddevice", "torch", "vosk", "silero", "vbml", "rich"],
    setup_requires=["numpy", "sounddevice", "torch", "vosk", "silero", "vbml", "rich"]
)