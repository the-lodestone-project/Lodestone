import os
import sys
from .console_ui import consoleui

is_linux = sys.platform.startswith('linux')
is_mac = sys.platform == 'darwin'
is_windows = os.environ.get('windir') 

if is_linux or is_mac:
  if os.environ.get('DISPLAY','') == '':
    print('No GUI on Linux/Mac, running console UI')  
    consoleui()
  else:
    print('Linux/Mac GUI found, running Streamlit')
    os.system("streamlit run web.py")

elif is_windows:
  print('Windows found, running Streamlit')
  os.system("streamlit run web.py") 

else:
  print('Unknown platform, defaulting to console UI')
  consoleui()