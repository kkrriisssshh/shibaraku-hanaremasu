import subprocess

subprocess.run('pyinstaller --onefile -w -F --add-binary "assets/kayo.ico;." main.py')