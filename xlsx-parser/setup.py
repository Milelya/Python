
import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [Executable("main.py", base=base)]

setup(
    name="Multitech Tri",
    version="0.2",
    description="A.Roques",
    executables=executables,
)