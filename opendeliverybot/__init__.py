import os
import sys

mode = 1
try:
    if sys.stdin.isatty():
        mode = 0
except AttributeError:  # stdin is NoneType if not in terminal mode
    pass

if mode == 0:
    os.system("console.py")
else:
    os.system("streamlit run web.py")