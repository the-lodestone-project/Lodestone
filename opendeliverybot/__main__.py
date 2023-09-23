import os
import sys
import click
from opendeliverybot.api import api

@click.command(context_settings={"ignore_unknown_options": True})
@click.option("--console", default=False, is_flag=True, help="Force the app to use the console")
@click.argument('args', nargs=-1)
def run(console, args):

    is_linux = sys.platform.startswith('linux')
    is_mac = sys.platform == 'darwin'
    is_windows = sys.platform in ['win32', 'cygwin']

    script_directory = os.path.dirname(os.path.abspath(__file__))

    if console:
        os.system(f"python {script_directory}/test-console.py {' '.join(args)}")
    else:
        if is_linux or is_mac:
            if os.environ.get('DISPLAY') == '':
                os.system(f"python {script_directory}/test-console.py {' '.join(args)}")
            else:
                # print('Web ui is still in developmet and is not working atm, rerun the command again with --console')
                api()
        elif is_windows:
            # print('Web ui is still in developmet and is not working atm, rerun the command again with --console')
            api()
        else:
            os.system(f"python {script_directory}/test-console.py {' '.join(args)}")

if __name__ == "__main__":
    run()