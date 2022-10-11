import setuptools
import os

# Функция получения полных путей к папкам и подпапкам
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

# Получение информации о установке
try:
    from wheel.bdist_wheel import bdist_wheel
except ImportError:
    cmdclass = {}
else:
    class bdist_wheel_tag_name(bdist_wheel):
        def get_tag(self):
            abi = 'none'
            # TODO: Надо дописать проверку системы
            return 'py39', abi, 'win_amd64'
    cmdclass = {'bdist_wheel': bdist_wheel_tag_name}

# Установка
setuptools.setup(
    name="voicehelper.py",
    version="0.1.4",
    description="These are two neural networks connected by the same module. One for recognition, the other for voice generation.",
    long_description=open("README.md", "r", errors="ignore").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/romanin-rf/voicehelper.py",
    author="Romanin",
    author_email="semina054@gmail.com",
    license="MIT",
    packages=setuptools.find_packages(),
    package_data={"VoiceHelper": globalizer("VoiceHelper" + os.sep + "models")},
    include_package_data=True,
    cmdclass=cmdclass,
    python_requires=">=3.9",
    install_requires=["numpy", "sounddevice", "pysoundfile", "torch", "vosk", "silero", "vbml", "rich"],
    setup_requires=["numpy", "sounddevice", "pysoundfile", "torch", "vosk", "silero", "vbml", "rich"]
)