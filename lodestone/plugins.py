import lodestone
from discord import Embed
import datetime
import aiohttp
from discord import SyncWebhook
from rich.console import Console
import asyncio
class plugins:
    class discord:
        """
        Build in Discord plugin
        """
        def __init__(self, bot: lodestone.Bot):
            "The injection method"
            self.bot = bot
            self.main() # run the main code to add the event
            events_loaded = list(bot.loaded_events.keys())
            events_loaded.append('discord_webhook') # add the event to the list
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
                    embed.set_footer(text='\u200b', icon_url="https://github.com/Project-Lodestone/Lodestone/blob/main/chestlogo.png?raw=true") # fallback footer image
                if use_discord_forums:
                    today = datetime.date.today() # get the current date
                    hook.send(content=f"{today}", thread_name=f"{today}", username="Lodestone", avatar_url="https://github.com/Project-Lodestone/Lodestone/blob/main/chestlogo.png?raw=true", embed=embed) # send the message in a forums channel
                else:
                    hook.send(content=f" ", username="Lodestone", avatar_url="https://github.com/Project-Lodestone/Lodestone/blob/main/chestlogo.png?raw=true", embed=embed) # send the message in a normal channel
                                    
        
            
            
            
            
        
