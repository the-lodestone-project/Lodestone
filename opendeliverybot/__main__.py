import os
import sys
from .console_ui import consoleui

mode = 1
try:
    if sys.stdin.isatty():
        mode = 0
except AttributeError:  # stdin is NoneType if not in terminal mode
    pass

if mode == 0:
    consoleui()
else:
    os.system("streamlit run web.py")