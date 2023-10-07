from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion
import click
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from fuzzyfinder import fuzzyfinder
import threading
import time
import lodestone
from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel
BotKeywords = ['bot.start()', 'bot.stop()','bot.inventory()', 'bot.version', 'bot.config', 'help', 'documentation', 'discord', 'players']

class BotCompleter(Completer):
    def get_completions(self, document, complete_event):
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        matches = fuzzyfinder(word_before_cursor, BotKeywords)
        for m in matches:
            yield Completion(m, start_position=-len(word_before_cursor))
def get_input():
    while 1:
        while True:
            with patch_stdout(raw=True):
                try:
                    if bot.bot.username:
                        username = bot.bot.username
                    else:
                        username = "username unknown (press enter to refresh)"
                except:
                    username = "username unknown (press enter to refresh)"
                try:
                    if bot.bot.version:
                        version = bot.bot.version
                    else:
                        version = "unknown"
                except:
                    version = "unknown"
                user_input = prompt(f'{username} ({version}) > ',
                                    history=FileHistory('history.txt'),
                                    completer=BotCompleter(),
                                    auto_suggest=AutoSuggestFromHistory(),
                                    in_thread=True
                                    )
                if user_input == "":
                    continue
                if user_input == "players":
                    def get_content(players):
                        username = players
                        return f"[b]{username}[/b]"


                    console = Console()


                    user_renderables = [Panel(get_content(player), expand=True) for player in bot.bot.players]
                    console.print(Columns(user_renderables))
                    continue
                if "bot" in user_input:
                    if user_input == "bot.stop()":
                        bot.stop()
                        quit()
                    try:
                        print(eval(user_input))
                    except Exception as e:
                        print("error", e)
                else:
                    bot.bot.chat(user_input)
    
def print_output(email, password, host, port, auth, version, check_timeout, viewer_port, goto, chest_range, init_chest_type, init_chest_cords, init_items_name, init_items_count, recipient_username, quit_on_low_health, low_health_threashold, armor_equip):
    global bot
    bot = lodestone.createBot(
        host=host,
        port=port,
        username=email,
        auth=auth,
        version=version,
        password=password,
        enableChatLogging=True,
    )



import click
@click.command()
@click.option("--email", prompt=True, help="Username/Email for login.")
@click.option("--password", help="Password for login.")  
@click.option("--host", prompt=True, help="Hostname or IP address of server.")
@click.option("--port", default=25565, help="Port number of server.")
@click.option("--auth", default="microsoft", help="Authentication method.")
@click.option("--version", default="auto", help="Game version.",prompt=True)
@click.option("--check_timeout", default=600000, help="Timeout interval for checks.")
@click.option("--viewer_port", default=8000, help="Port for viewer.")
@click.option("--goto", default=["100", "100", "100"],  help="Coordinates to go to.")
@click.option("--chest_range", default=100, help="Range to search for chests.")
@click.option("--init_chest_type", default="chest", help="Type of chest to look for when starting.")
@click.option("--init_chest_cords", default=["100", "100", "100"],  help="Coordinates to base chest.")  


# needs an fix with prompt=True
@click.option("--init_items_name", default="SchulkerBox", help="Name of items to get from the base chest.")
@click.option("--init_items_count", default=1, help="Number of items to get from the base chest.")
#

@click.option("--recipient_username", default="OpenDeliveryBot", help="Username to deliver to.")
@click.option("--quit_on_low_health", default=True, help="Disconect the bot if the bot is on low health")
@click.option("--low_health_threashold", default=10, help="How low the health must be for the bot to quit")
@click.option("--armor_equip", default=True, help="If the bot needs to equip available armor.")
def console(email, password, host, port, auth, version, check_timeout, viewer_port, goto, chest_range, init_chest_type, init_chest_cords, init_items_name, init_items_count, recipient_username, quit_on_low_health, low_health_threashold, armor_equip):
    thread1 = threading.Thread(target=print_output, args=(email, password, host, port, auth, version, check_timeout, viewer_port, goto, chest_range, init_chest_type, init_chest_cords, init_items_name, init_items_count, recipient_username, quit_on_low_health, low_health_threashold, armor_equip))
    thread2 = threading.Thread(target=get_input)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
    
if __name__ == '__main__':
    console()