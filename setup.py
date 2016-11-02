import sys
from cx_Freeze import setup, Executable



build_exe_options = {"packages": ["os", "sys", "datetime", "pymysql", "hashlib", "uuid", "time", "random", "functools", "serial"],
                     "includes":["PyQt5"],
                     "excludes": ["PyQt5.uic"],
                     "include_files": ["data/"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"
    
setup(  name = "BIO-Attendance",
        version = "0.1",
        description = "Biomeetrics attendance desktop application for report generation.",
        options = {"build_exe": build_exe_options},
        executables = [Executable("index.py", base=base)])