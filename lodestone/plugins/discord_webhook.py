import lodestone
try:
    from discord import Embed
except:
    pass
import datetime
try:
    from discord import SyncWebhook
except:
    pass
import ast
import inspect

class discord:
        """
        Build in Discord plugin
        """
        def __init__(self, bot: lodestone.Bot):
            "The injection method"
            self.bot = bot
            self.main() # run the main code to add the event
            self.code = inspect.getsource(inspect.getmodule(self.__class__))
            self.tree = ast.parse(self.code)
            self.events = []
            for node in ast.walk(self.tree):
                if isinstance(node, ast.Call) and hasattr(node.func, 'attr') and node.func.attr == 'on':
                    event = node.args[0].s
                    self.events.append(event)
            events_loaded = list(bot.loaded_events.keys())
            events_loaded.append(self.events) # add the event to the list
            bot.emit('event_loaded', *events_loaded)
            plugins_loaded = list(bot.loaded_plugins.keys())
            plugins_loaded.append(self.__class__.__name__) # add the plugin to the list
            bot.emit('plugin_loaded', *plugins_loaded)
            
            
        def main(self):
            @self.bot.on('discord_webhook') # this part of the code is ran when bot.emit('discord_webhook') is called
            def discord_webhook(bot, message:str, webhook:str, use_discord_forums:bool=False):
                hook = SyncWebhook.from_url(url=webhook) # connect to the webhook
                use_discord_forums:bool=False
                color=0x3498db
                embed = Embed(title="", description=f"**{message}**", color=color) # make the embed
                embed.timestamp = datetime.datetime.utcnow()
                try:
                    embed.set_footer(text=f'{self.bot.username}', icon_url=f"https://mc-heads.net/avatar/{self.bot.username}/600.png") # set the footer image to the players head
                except:
                    embed.set_footer(text='\u200b', icon_url="https://github.com/Project-Lodestone/Lodestone/blob/main/chestlogo.png?raw=True") # fallback footer image
                if use_discord_forums:
                    today = datetime.date.today() # get the current date
                    hook.send(content=f"{today}", thread_name=f"{today}", username="Lodestone", avatar_url="https://github.com/Project-Lodestone/Lodestone/blob/main/chestlogo.png?raw=True", embed=embed) # send the message in a forums channel
                else:
                    hook.send(content=f" ", username="Lodestone", avatar_url="https://github.com/Project-Lodestone/Lodestone/blob/main/chestlogo.png?raw=True", embed=embed) # send the message in a normal channel