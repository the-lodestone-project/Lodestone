import os
import sys
from .console_ui import consoleui
import click

@click.command()
@click.option("--console", default="", help="Use console as main type of input")
@click.option("--gui", default="", help="Use Web Gui as main type of input")
def run(console, gui):
    is_linux = sys.platform.startswith('linux')
    is_mac = sys.platform == 'darwin'
    is_windows = os.environ.get('windir')
    
    
    if console != "":
        consoleui()
    if gui != "":
        os.system("streamlit run web_ui.py")
    
    if console == None and gui == None:
        if is_linux or is_mac:
            if os.environ.get('DISPLAY','') == '':
                print('No GUI on Linux/Mac, running console UI')  
                consoleui()
            else:
                print('Linux/Mac GUI found, running Streamlit')
                os.system("streamlit run web_ui.py")

        elif is_windows:
            print('Windows found, running Streamlit')
            os.system("streamlit run web_ui.py") 

        else:
            print('Unknown platform, defaulting to console UI')
            consoleui()
            
run()