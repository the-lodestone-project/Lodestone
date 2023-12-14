
import click
from rich.console import Console
import lodestone
from dotenv import load_dotenv
import threading
import lodestone

@click.command()
@click.option("--username", "-u", help="Run lodestone tests", required=True, type=str)
@click.option("--host", "-h", help="Run lodestone tests", required=True, type=str, show_default=True)
@click.option("--port", "-p", default=25565, help="Run lodestone tests", required=False, type=int, show_default=True)
@click.option("--version", "-v", default="auto", help="Run lodestone tests", required=False, show_default=True, type=click.Choice(["1.8.8", "1.9" "15w40b", "1.9.1-pre2", "1.9.2", "1.9.4", "1.10", "16w20a", "1.10-pre1", "1.10", "1.10.1", "1.10.2", "1.11", "16w35a", "1.11", "1.11.2", "1.12", "17w15a", "17w18b", "1.12-pre4", "1.12", "1.12.1", "1.12.2", "1.13", "17w50a", "1.13", "1.13.1", "1.13.2-pre1", "1.13.2-pre2", "1.13.2", "1.14", "1.14", "1.14.1", "1.14.3", "1.14.4", "1.15", "1.15", "1.15.1", "1.15.2", "1.16", "20w13b", "20w14a", "1.16-rc1", "1.16", "1.16.1", "1.16.2", "1.16.3", "1.16.4", "1.17", "21w07a", "1.17", "1.17.1", "1.18", "1.18", "1.18.1", "1.18.2", "1.19", "1.19", "1.19.1", "1.19.2", "1.19.3", "1.19.4", "1.20", "1.20.1"], case_sensitive=False))
def run(username, host, port, version):
    def bot_process():
        bot = lodestone.createBot(
            host=host,
            port=port,
            username=username,
            version=version,
            ls_enable_chat_logging=False,
        )
    def input_process():
        while True:
            commad = input("lodestone > ")
            if "bot" in globals():
                print(commad)
            else:
                print("lodestone is not running")
    
    bot_thread = threading.Thread(target=bot_process)
    bot_thread.start()
    input_thread = threading.Thread(target=input_process)
    input_thread.start()
                
            
    
    

if __name__ == "__main__":
    run()