import os
import sys
import click

@click.command(context_settings={"ignore_unknown_options": True})
@click.option("--console", default=False, is_flag=True, help="Use console UI instead of GUI")
@click.argument('args', nargs=-1)
def run(console, args):

    is_linux = sys.platform.startswith('linux')
    is_mac = sys.platform == 'darwin'
    is_windows = sys.platform in ['win32', 'cygwin']

    script_directory = os.path.dirname(os.path.abspath(__file__))

    if console:
        os.system(f"python {script_directory}/console_ui.py {' '.join(args)}")
    else:
        if is_linux or is_mac:
            if os.environ.get('DISPLAY') == '':
                print('No GUI, using console UI')
                os.system(f"python {script_directory}/console_ui.py {' '.join(args)}")
            else:
                print('Using GUI')
                os.system(f"python -m streamlit run {script_directory}/web_ui.py")
        elif is_windows:
            print('Using GUI')
            os.system(f"streamlit run {script_directory}/web_ui.py")
        else:
            print('Unknown platform, using console UI')
            os.system(f"python {script_directory}/console_ui.py {' '.join(args)}")

if __name__ == "__main__":
    run()