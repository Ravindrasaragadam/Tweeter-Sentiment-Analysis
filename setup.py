from cx_Freeze import setup, Executable

base = None

executables = [Executable("Analysis.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {
        'packages': packages,
    },
}

setup(
    name="Tweeter Sentiment Analysis",
    options=options,
    version="1.0",
    description='Tweeter tweets analysis',
    executables=executables
)
