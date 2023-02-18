import subprocess
import wget
import zipfile
import os

upx_file_path = "assets/upx.exe"
upx_url = "https://github.com/upx/upx/releases/download/v4.0.2/upx-4.0.2-win64.zip"
upx_zip_file = "upx-4.0.2-win64.zip"

if not os.path.isfile(upx_file_path):
    wget.download(upx_url, upx_zip_file)
    with zipfile.ZipFile(upx_zip_file, 'r') as zip_ref:
        zip_ref.extractall("assets")
    os.remove(upx_zip_file)

subprocess.run('pyinstaller --onefile -w -F --add-binary "assets/kayo.ico;." main.py')
subprocess.run([upx_file_path, "-9", "-v", "-f", "-o" "shibaraku-hanaremasu.exe", "dist\input_file.exe"])