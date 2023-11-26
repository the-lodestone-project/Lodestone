import os
import sys
import click
from lodestone import fastapi
import subprocess
import time
from rich.console import Console
import lodestone
from dotenv import load_dotenv
import requests

@click.command(context_settings={"ignore_unknown_options": True})
@click.option("--console", "-c", default=False, is_flag=True, help="Force the app to use the console")
@click.option("--test", "-t", is_flag=True, help="Run version tests on Lodestone")
@click.option("--host", "-h", help="Host to run Lodestone's gui on", default=None)
@click.option("--port", "-p", help="Port to run Lodestone's gui on", default=8000)
@click.argument('args', nargs=-1)
def run(console, test, host, port, args):
    
    if test:
        versions = ["auto", "1.20.1", "1.19", "1.18", "1.17", "1.16", "1.15", "1.14", "1.13", "1.11", "1.10", "1.9", "1.8"]

        console = Console()

        with console.status("[bold]Checking versions...\n") as status:
            for version in versions:
                failed = ""
                status.update(f"Checking version {version}")

                # Create bot with the current version  
                try:
                    bot = lodestone.createBot(
                        host='2b2t.org',
                        username='TestBot',  
                        version=version,
                        checkTimeoutInterval=70,
                        ls_skip_checks=True,
                        hideErrors=False,
                        ls_debug_mode=True,
                        ls_disable_viewer=True
                    )
                except:
                    failed = "failed ([bold red]❌[reset])"
                    print(f"Version {version} failed to connect")
                    
                
                # Check connection
                if bot.tablist:
                    failed = "passed ([bold green]✔️[reset])"
                    status.update(f"Checking version {version} {failed}")
                else:
                    failed = "failed ([bold red]❌[reset])"
                    print(f"Version {version} failed to connect")
                
                # Stop bot
                bot.stop()

                # Add delay to avoid congestion
                for i in range(0, 10):
                    
                    status.update(f"{version} {failed} ({10 - i} until next version)")
                    time.sleep(1)
    
    def check_python_command():
        try:
            subprocess.check_output(['python', '--version'])
            return 'python'
        except:
            try:
                subprocess.check_output(['python3', '--version']) 
                return 'python3'
            except:
                print('Python command not found')
                sys.exit(1)

    python_command = check_python_command()

    is_linux = sys.platform.startswith('linux')
    is_mac = sys.platform == 'darwin'
    is_windows = sys.platform in ['win32', 'cygwin']

    script_directory = os.path.dirname(os.path.abspath(__file__))

    if console:
        os.system(f"{python_command} {script_directory}/console.py {' '.join(args)}")
    else:
        if host is None:
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            host = s.getsockname()[0]
            s.close()
            
        load_dotenv()
    
        username = os.getenv("LODESTONE_USERNAME")
        password = os.getenv("LODESTONE_PASSWORD")
        if username is None:
            print("For security reasons, you must set a username and password to protect your account.")
            username = input("Username: ")
            password = input("Password: ")
            os.environ["LODESTONE_USERNAME"] = f"{username}"
            os.environ["LODESTONE_PASSWORD"] = f"{password}"
            with open(".env", "w") as f:
                f.write(f"LODESTONE_USERNAME={username}\nLODESTONE_PASSWORD={password}")
                print("Login details saved to .env file. You can change these at any time.")
        
        if not os.path.isfile("favicon.ico"):
            img_data = requests.get("https://github.com/the-lodestone-project/Lodestone/raw/main/assets/favicon.png").content
            with open('favicon.png', 'wb') as handler:
                handler.write(img_data)
        
        
        try:
            lodestone.ui.queue().launch(server_name=f"{host}", server_port=port, show_api=False, auth=(f'{os.environ["LODESTONE_USERNAME"]}', f'{os.environ["LODESTONE_PASSWORD"]}'), share=False, quiet=True, favicon_path="favicon.png", auth_message="Please login with your set username and password. These are not your Minecraft credentials.")
        except OSError:
            raise OSError(f"Port {port} is already in use!")

if __name__ == "__main__":
    run()