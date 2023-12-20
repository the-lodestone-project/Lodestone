
import click
from rich.console import Console
import lodestone
from dotenv import load_dotenv
import threading
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
import time
import os

global bot


lodestone_commands = ['config', 'exit']


@click.command()
@click.option("--username", "-u", help="Run lodestone tests", required=True, type=str)
@click.option("--host", "-h", help="Run lodestone tests", required=True, type=str, show_default=True)
@click.option("--port", "-p", default=25565, help="Run lodestone tests", required=False, type=int, show_default=True)
@click.option("--version", "-v", default="false", help="Run lodestone tests", required=False, show_default=True, type=click.Choice(["1.8.8", "1.9" "15w40b", "1.9.1-pre2", "1.9.2", "1.9.4", "1.10", "16w20a", "1.10-pre1", "1.10", "1.10.1", "1.10.2", "1.11", "16w35a", "1.11", "1.11.2", "1.12", "17w15a", "17w18b", "1.12-pre4", "1.12", "1.12.1", "1.12.2", "1.13", "17w50a", "1.13", "1.13.1", "1.13.2-pre1", "1.13.2-pre2", "1.13.2", "1.14", "1.14", "1.14.1", "1.14.3", "1.14.4", "1.15", "1.15", "1.15.1", "1.15.2", "1.16", "20w13b", "20w14a", "1.16-rc1", "1.16", "1.16.1", "1.16.2", "1.16.3", "1.16.4", "1.17", "21w07a", "1.17", "1.17.1", "1.18", "1.18", "1.18.1", "1.18.2", "1.19", "1.19", "1.19.1", "1.19.2", "1.19.3", "1.19.4", "1.20", "1.20.1"], case_sensitive=False))
@click.option("--debug", "-d", default=False, help="Run lodestone tests", required=False, type=bool, show_default=True)
@click.option("--viewer", default=True, help="Run lodestone tests", required=False, type=bool, show_default=True)
def run(username, host, port, version, debug, viewer):
    def bot_process():
        global bot
        bot = lodestone.createBot(
            host=host,
            port=port,
            username=username,
            version=version,
            ls_enable_chat_logging=False,
            ls_skip_checks=True,
        )
        
        @bot.on('messagestr')
        def chat(this, message, messagePosition, jsonMsg, sender, *args):
            message = str(message).replace("\n\n","")
            if sender == None or sender == "None":
                print(f"{message}")
            else:
                print(f"{sender}: {message}")
                
    class tab_complete(Completer):
        def get_completions(self, document, complete_event):
            if document.text.startswith("!"):
                if document.text == " ":
                    return
                word_before_cursor = document.get_word_before_cursor()
                for m in lodestone_commands:
                    if word_before_cursor == "!":
                        m = "!" + m
                    else: 
                        m = m
                    yield Completion(m, start_position=-len(word_before_cursor))
            else:
                if not "/" in document.text:
                    return
                if document.text == " ":
                    return
                word_before_cursor = document.get_word_before_cursor()
                matches = bot.bot.tabComplete(word_before_cursor)
                for m in matches:
                    if word_before_cursor == "/":
                        m = "/" + m['match']
                    else: 
                        m = m['match']
                    yield Completion(m, start_position=-len(word_before_cursor))
        
    def input_process():
        while True:
            if "bot" in globals():
                with patch_stdout(raw=True):
                    commad = prompt(f'{username} ({version}) > ',in_thread=True, completer=tab_complete(), mouse_support=True, complete_while_typing=True)
                    if commad.startswith("!"):
                        commad = commad.replace("!", "")
                        if commad == "config":
                            print(username, host, port, version, debug, viewer)
                        if commad == "exit":
                            bot.stop()
                            time.sleep(0.5)
                            os._exit(0)
                    else:
                        bot.chat(commad)
    
    bot_thread = threading.Thread(target=bot_process)
    bot_thread.start()
    input_thread = threading.Thread(target=input_process)
    input_thread.start()
                
            
    
    

if __name__ == "__main__":
    run()