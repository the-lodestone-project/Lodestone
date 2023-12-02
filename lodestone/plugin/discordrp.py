import lodestone
import ast
import inspect

class discordrp:
        """
        Build in cactus farm builder plugin
        """
        def __init__(self, bot: lodestone.Bot):
            "The injection method"
            self.bot:lodestone.Bot = bot
            self.code = inspect.getsource(inspect.getmodule(self.__class__))
            self.tree = ast.parse(self.code)
            plugins_loaded = list(bot.loaded_plugins.keys())
            plugins_loaded.append(self.__class__.__name__)
            bot.emit('plugin_loaded', *plugins_loaded)
            client_id = "1143589220821258270" 
            from pypresence import Presence
            RPC = Presence(client_id=client_id)
            RPC.connect()
            RPC.update(
                        state=f"{self.bot.local_host} - {self.bot.bot.version}",
                        details=f"{self.bot.username}",
                        large_image=(f"https://mc-heads.net/avatar/{self.bot.username}/180/nohelm.png"), 
                        large_text=f"{self.bot.username}",
                        small_image=(f"https://eu.mc-api.net/v3/server/favicon/{self.bot.local_host}"), small_text=f"{self.bot.local_host} on {self.bot.bot.version}",
                        start=time.time(),
                        # buttons=[{"label": "Join Server", "url": f"https://{self.bot.local_host}"}]
            )
            
            self.bot.discordrp = RPC.update