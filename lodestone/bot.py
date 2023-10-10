from javascript import require, On
import datetime
import structlog
import os
import sys
import requests
import time
import fnmatch
import re
from datetime import date
from pathlib import Path
from javascript.proxy import Proxy
from tinydb import TinyDB, Query
import subprocess
from rich.console import Console
try:
    from utils import cprop, send_webhook
except ImportError:
    from .utils import cprop, send_webhook
User = Query()
filestruc = "/"
logger = structlog.get_logger()

if os.name == 'nt':
    filestruc = "\\"
else:
    filestruc = "/"

__all__ = ['Bot', 'createBot']

class GameState:
    """
    Stores information about the current game state. Should not initialize manually
    """
    def __init__(self, proxy: Proxy):
        self.proxy = proxy

    @cprop()
    def level_type(self) -> str:
        "The world generation type. Posssible values are in `types.LevelType`"

    @cprop()
    def dimension(self) -> str:
        "The current dimension. Posssible values are in `types.Dimension`"

    @cprop()
    def difficulty(self) -> str:
        "The current server difficulty. Posssible values are in `types.Difficulty`"

    @cprop()
    def game_mode(self) -> str:
        "The current game mode. Posssible values are in `types.GameMode`"

    @cprop()
    def hardcore(self) -> bool:
        "Whether the client is in hardcore mode or not"

    @cprop()
    def max_players(self) -> int:
        "The maximum number of players can be allowed on a server"

    @cprop()
    def server_brand(self) -> str:
        "the current server brand. Posssible values are in `types.BrandChannel`"

    @cprop()
    def min_y(self) -> int:
        "The minimum Y level in the world"

    @cprop()
    def height(self) -> int:
        "The height of the world"

    @cprop(proxy_name="height")
    def max_y(self) -> int:
        "The height of the world"


class TimeState:
    """
    Stores information about time. Should not initialize manually
    """
    def __init__(self, proxy: Proxy):
        self.proxy = proxy

    @cprop()
    def do_daylight_cycle(self) -> bool:
        "Whether the server does daylight cycle or not"

    @cprop()
    def big_time(self) -> int:
        "Total ticks elapsed since day 0"

    @cprop()
    def time(self) -> int:
        "Total ticks elapsed since day 0. Inaccruate. Use `TimeState.big_time`"

    @cprop()
    def time_of_day(self) -> int:
        "The current time of day, in ticks. This is used in the `/time set` command"

    @cprop()
    def day(self) -> int:
        "The number of days in a world"

    @cprop()
    def is_day(self) -> bool:
        "Whether `TimeState.time_of_day` is within 13,000 and 23,000 (AKA whether it's daytime or not)"

    @cprop()
    def moon_phase(self) -> int:
        "Current moon phase. Ranges from 0 -> 7"

    @cprop()
    def big_age(self) -> int:
        "Total ticks elapsed since day 0"

    @cprop()
    def age(self) -> int:
        "Total ticks elapsed since day 0. Inaccurate. Use `TimeState.big_age`"


class ExperienceState:
    """
    Stores information about XP. Should not initalize manually
    """
    def __init__(self, proxy: Proxy):
        self.proxy = proxy

    @cprop()
    def level(self) -> int:
        "Full levels of experience"

    @cprop()
    def points(self) -> int:
        "Total experience points"

    @cprop()
    def progress(self) -> float:
        "The progress to the next full level. Ranges from 0 -> 1 (0% -> 100%)"

class SkinPartsState:
    """
    Represents the skin parts that are visible / not visible. Should not initalize manually
    """
    def __init__(self, proxy: Proxy):
        self.proxy = proxy

    @cprop()
    def show_cape(self) -> bool:
        "Whether the cape is shown"

    @cprop()
    def show_jacket(self) -> bool:
        "Whether the jacket is shown"

    @cprop()
    def show_left_sleeve(self) -> bool:
        "Whether the left sleeve is shown"

    @cprop()
    def show_right_sleeve(self) -> bool:
        "Whether the right sleeve is shown"

    @cprop()
    def show_left_pants(self) -> bool:
        "Whether the left pant is shown"

    @cprop()
    def show_right_pants(self) -> bool:
        "Whether the right pant is shown"

    @cprop()
    def show_hat(self) -> bool:
        "Whether the hat is shown"


class SettingsState:
    """
    Represents the client settings that the server needs to know. Should not initialize manually
    """
    def __init__(self, proxy: Proxy):
        self.proxy = proxy

    @cprop()
    def chat(self) -> str:
        "The current chat settings. Possible values are in `types.ChatSetting`"

    @cprop()
    def colors_enabled(self) -> bool:
        "Whether colors are recieved in chat"

    @cprop()
    def view_distance(self) -> str | int:
        "The view distance of the client. Could be one of `types.ViewDistance` or an int"

    @cprop()
    def difficulty(self) -> str:
        "The difficulty of the client. Possible values are in `types.Difficulty`"

    @property
    def skin_parts(self) -> SkinPartsState:
        "The skin parts of the client."
        return SkinPartsState(self.proxy.skin_parts)

    @cprop()
    def enable_text_filtering(self) -> bool:
        "Unused value. Default = False"

    @cprop()
    def enable_server_listing(self) -> bool:
        "Whether the player should list in the Tablist or not"


class Bot:
    def __init__(
            self,
            host: str,
            *,
            auth: str = "microsoft",
            port: int = 25565,
            version: str = "false",
            password: str = "",
            checkTimeoutInterval: int = 20,
            armorManager: bool = False,
            viewerPort: int = 5001,
            quit_on_low_health: bool = True,
            low_health_threshold: int = 10,
            disableChatSigning: bool = False,
            profilesFolder: str = "",
            username: str = "lodestone",
            useReturn: bool = False,
            discordWebhook: str = None,
            useDiscordForums: bool = False,
            apiMode: bool = False,
            clientToken: str = None,
            accessToken: str = None,
            logErrors: bool = True,
            hideErrors: bool = True,
            keepAlive: bool = True,
            loadInternalPlugins: bool = True,
            respawn: bool = True,
            physicsEnabled: bool = True,
            defaultChatPatterns: bool = True,
            disableLogs: bool = False,
            enableChatLogging: bool = False,
            skipChecks: bool = False,
            disableViewer: bool = False,
            stopBotOnDeath: bool = False,
    ):
        """Create the bot"""
        self.stop_bot_on_death = stopBotOnDeath
        self.local_host = host
        self.local_auth = auth
        self.local_port = port
        self.local_version = version
        self.local_password = password
        self.local_check_timeout_interval = checkTimeoutInterval
        self.local_armor_manager = armorManager
        self.local_viewer_port = viewerPort
        self.local_quit_on_low_ealth = quit_on_low_health
        self.local_low_health_threshold = low_health_threshold
        self.local_disable_chat_signing = disableChatSigning
        self.local_profiles_folder = profilesFolder
        self.local_username = username
        self.local_client_token = clientToken
        self.local_access_token = accessToken
        self.local_log_errors = logErrors
        self.local_hide_errors = hideErrors
        self.local_keep_alive = keepAlive
        self.local_load_internal_plugins = loadInternalPlugins
        self.local_respawn = respawn
        self.local_physics_enabled = physicsEnabled
        self.local_default_chat_patterns = defaultChatPatterns
        self.local_disable_logs = disableLogs
        self.local_enable_chat_logging = enableChatLogging
        self.local_skip_checks = skipChecks if not discordWebhook else False
        self.local_discord_webhook = discordWebhook
        self.local_disable_viewer = disableViewer
        global logger
        self.logger = structlog.get_logger()
        logger = self.logger
        self.console = Console()
        # [:2]
        self.api_mode = apiMode
        if not self.local_skip_checks:
            self.nodeVersion, self.pipVersion, self.pythonVersion = self.__versionsCheck()
        if self.local_discord_webhook is not None:
            from discord import Embed
            self.Embed = Embed
            self.useDiscordForums = useDiscordForums
            embedVar = Embed(title="Successfully Connected to Webhook!", description=f"**Great news! The bot has successfully connected to this channel's webhook. From now on, it will send all the logs and valuable data right here, keeping you informed about everything happening on the server.**\n\n **Versions:**\n* [**Node**](https://nodejs.org/)**:      {self.nodeVersion}**\n* [**Pip**](https://pypi.org/project/pip/)**:          {self.pipVersion}**\n* [**Python**](https://www.python.org/)**:  {self.pythonVersion}**\n\n **Links:**\n* [**GitHub**](https://github.com/SilkePilon/OpenDeliveryBot)\n* [**Report Bugs**](https://github.com/SilkePilon/OpenDeliveryBot/issues)\n* [**Web Interface**](https://github.com/SilkePilon/OpenDeliveryBot-react)", color=0x3498db)
            embedVar.timestamp = datetime.datetime.utcnow()
            embedVar.set_footer(text='\u200b', icon_url="https://github.com/SilkePilon/OpenDeliveryBot/blob/main/chestlogo.png?raw=true")
            if useDiscordForums:
                today = date.today()
                send_webhook(discordWebhook, content=f"{today}", thread_name=f"{today}", username="OpenDeliveryBot", avatar_url="https://github.com/SilkePilon/OpenDeliveryBot/blob/main/chestlogo.png?raw=true", embed=embedVar)
            else:
                try:
                    send_webhook(discordWebhook, content="", username="OpenDeliveryBot", avatar_url="https://github.com/SilkePilon/OpenDeliveryBot/blob/main/chestlogo.png?raw=true", embed=embedVar)
                except:
                    self.logger.error(f"Detected that you are using a Forms channel but 'useDiscordForms' is set to False. Please change 'useDiscordForms' to True or provide a webhook url for a text channel.")
        self.discordWebhook = discordWebhook
        self.mineflayer = require('mineflayer')
        self.pathfinder = require('mineflayer-pathfinder')
        self.goals = require('mineflayer-pathfinder').goals
        if not self.local_disable_viewer:
            self.mineflayerViewer = require('prismarine-viewer').mineflayer
        self.armorManager = require("mineflayer-armor-manager")
        self.autoeat = require('mineflayer-auto-eat').plugin
        self.repl = require('repl')
        self.statemachine = require("mineflayer-statemachine")
        self.pythonCommand = self.__checkPythonCommand()
        if not skipChecks:
            with self.console.status("[bold green]Checking for updates...\n") as status:
                status.update("[bold green]Updaing javascript librarys...\n")
                os.system(f'{self.pythonCommand} -m javascript --update >/dev/null 2>&1')
                status.update("[bold green]Updaing pip package...\n")
                os.system(f'{self.pythonCommand} -m pip install -U lodestone >/dev/null 2>&1')
                time.sleep(3)
        self.logged_in = False
        self.use_return = useReturn
        self.msa_status = False
        self.server_name = f"{self.local_host}".lower().replace(".", "")
        if self.local_enable_chat_logging:
            self.chatDatabase = TinyDB(f"{self.server_name}Database.json")
        self.script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.bot: Proxy = self.__create_bot()
        self.proxy = self.bot
        self.msa_data = False
        self.__start()
        
        
    
    def __checkPythonCommand(self):
        try:
            subprocess.check_output(['python', '--version'])
            return 'python'
        except:
            try:
                subprocess.check_output(['python3', '--version']) 
                return 'python3'
            except:
                self.__logging(message='Python command not found, make sure python is installed!', error=True,
                               discord=False)
                sys.exit(1)
    
        
    def __logging(self, message, icon="🤖", error=False, info=False, warning=False, chat=False, imageUrl:str="", console:bool= True, discord:bool=True):
        if not self.local_disable_logs:
            if self.use_return:
                self.logger.info(f"[{icon}] {message}")
            elif self.discordWebhook is not None and discord == True:
                color = 0x3498db
                if error:
                    color = 0x992d22
                elif info:
                    color = 0x3498db
                elif warning:
                    color = 0xe67e22
                elif chat:
                    color = 0x2ecc71
                embed = self.Embed(title="", description=f"**[{icon}] {message}**", color=color)
                embed.timestamp = datetime.datetime.utcnow()
                if imageUrl != "":
                    embed.set_thumbnail(url=imageUrl)
                try:
                    embed.set_footer(text=f'{self.bot.username}', icon_url=f"https://mc-heads.net/avatar/{self.bot.username}/600.png")
                except:
                    embed.set_footer(text='\u200b', icon_url="https://github.com/SilkePilon/OpenDeliveryBot/blob/main/chestlogo.png?raw=true")
                if self.useDiscordForums:
                    today = date.today()
                    send_webhook(self.discordWebhook, content=f"{today}", thread_name=f"{today}", username="OpenDeliveryBot", avatar_url="https://github.com/SilkePilon/OpenDeliveryBot/blob/main/chestlogo.png?raw=true", embed=embed)
                else:
                    try:
                        send_webhook(self.discordWebhook, content=f"", username="OpenDeliveryBot", avatar_url="https://github.com/SilkePilon/OpenDeliveryBot/blob/main/chestlogo.png?raw=true", embed=embed)
                    except:
                        self.logger.error(f"Detected that you are using a Forms channel but 'useDiscordForms' is set to False. Please change 'useDiscordForms' to True or provide a webhook url for a text channel.")
            if console:
                if error:
                    self.logger.error(f"[{icon}] {message}")
                elif info:
                    self.logger.info(f"[{icon}] {message}")
                elif warning:
                    self.logger.warning(f"[{icon}] {message}")
                elif chat:
                    self.logger.info(f"[{icon}] {message}")
                else:
                    self.logger.info(f"[{icon}] {message}")
        
    @staticmethod
    def __findFiles(base, pattern):
        '''Return list of files matching pattern in base folder.'''
        return [n for n in fnmatch.filter(os.listdir(base), pattern) if
            os.path.isfile(os.path.join(base, n))]
        
    def __waitForMsa(self, timeout = 300): # 5 minutes
        if os.name == 'nt':
            basePath = os.getenv('APPDATA')
        else:
            basePath = Path().home()
        path = self.local_profiles_folder
        if not path:
            path = Path(f"{basePath}/.minecraft/nmp-cache/")
        msa_file = path / self.__findFiles(path, '*_mca-cache.json')[0]
        for _ in range(timeout):
            time.sleep(1)
            with open(msa_file) as check:
                if check.read() != "{}":
                    self.logger.info("Logged in successfully!")
                    return
        raise TimeoutError(
            f"Fetching for MSA code timed out. Timeout={timeout} seconds"
        )

    def __msa(self, *msa):
        with self.console.status("[bold green]Waiting for login...\n"):
            self.msa_data = msa[0]
            self.msa_status = True
            self.__logging(message="It seems you are not logged in! Open your termianl for more information.",
                           error=True, console=False)
            self.logger.error(f"It seems you are not logged in, please go to https://microsoft.com/link and enter the following code: {self.msa_data['user_code']}")
            # code=self.msa_data['user_code']
            self.__waitForMsa()
            if self.api_mode:
                self.bot.end()
                quit()
            self.msa_status = False
            # self.logger.info(f"{msa[0]['user_code']} MSA Code")

    def __versionsCheck(self):
        with self.console.status("[bold green]Checking versions...\n"):
            # Node
            result = subprocess.run(["node", "--version"], 
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True)
            node_version = result.stdout.strip()
            # Remove leading 'v'
            node_version = node_version[1:] if node_version.startswith('v') else node_version
            # Remove periods
            node_version = node_version.replace('.', '')
            if int(node_version[:2]) >= 18:
                pass
            else:
                self.logger.warning(f"Detected node version {node_version[:2]} witch is NOT supported!\nThis may cause problems. Please update to node 18 or above!")
                time.sleep(7)
                
                
            # Pip
            pip_ = 'pip' if self.__checkPythonCommand() == 'python' else 'pip3'
            result = subprocess.run([pip_, "--version"],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True)
            pip_version = result.stdout.strip()
            # Remove
            match = re.search(r'pip (\d+(?:\.\d+)*).*python (\d+(?:\.\d+)*)', pip_version)
            if match:
                pip_version = match.group(1)
                python_version = match.group(2)
            # if not self.local_disable_logs:
            #     self.logger.info(f"Detected Pip version {pip_version} witch is supported!")
            #     self.logger.info(f"Detected Python version {python_version} witch is supported!")
            return node_version, pip_version, python_version

    def __create_bot(self):
        if self.local_version == "auto" or self.local_version == "false":
            self.local_version = False
        else:
            self.version = str(self.local_version)
        localBot = self.mineflayer.createBot({
            'host': self.local_host,
            'port': self.local_port,
            'username': self.local_username,
            'password': self.local_password,
            'auth': self.local_auth,
            'version': self.local_version,
            'onMsaCode': self.__msa,
            'checkTimeoutInterval': 60 * 10000,
            'disableChatSigning': self.local_disable_chat_signing,
            'profilesFolder': self.local_profiles_folder,
            'logErrors': self.local_log_errors,
            'hideErrors': self.local_hide_errors,
            'keepAlive': self.local_keep_alive,
            'loadInternalPlugins': self.local_load_internal_plugins,
            'respawn': self.local_respawn,
            'physicsEnabled': self.local_physics_enabled,
            'defaultChatPatterns': self.local_default_chat_patterns
        })
        @On(localBot, "login")
        def on_login(*args):
            self.bot = localBot
            self.logged_in = True
            self.__logging(f"Connected to {self.local_host}", info=True, imageUrl=f"https://eu.mc-api.net/v3/server/favicon/{self.local_host}")
            self.__logging(f'Logged in as {self.bot.username}', info=True, imageUrl=f"https://mc-heads.net/avatar/{self.bot.username}/600.png")
            if not self.local_disable_viewer:
                self.__start_viewer()
            self.__setup_events()
            self.__load_plugins()
        return localBot


    def __start(self):
        while not self.logged_in:
            time.sleep(1) 
        # @On(self.bot, "login")
        # def on_login(*args):
        
        # r = self.repl.start('> ')
        # r.context.bot = self.bot
        # self.__auto_totem()
        self.__equip_armor()
        self.__logging(
            f'Cordinates: {int(self.bot.entity.position.x)}, {int(self.bot.entity.position.y)}, {int(self.bot.entity.position.z)}',
        info=True)

    @cprop()
    def registry(self): pass

    @cprop()
    def world(self): pass

    @cprop()
    def entity(self): pass

    @cprop()
    def entities(self): pass

    @cprop()
    def username(self): pass

    @cprop()
    def spawn_point(self): pass

    @cprop()
    def held_item(self): pass

    @cprop()
    def using_eld_item(self): pass

    @property
    def game(self): return GameState(self.proxy.game)
    
    @cprop()
    def physics_enabled(self): pass
    
    @cprop()
    def player(self): pass
    
    @cprop()
    def players(self): pass
    
    @cprop()
    def tablist(self): pass

    @cprop()
    def physics_enabled(self): pass

    @cprop()
    def player(self): pass

    @cprop()
    def players(self): pass

    @cprop()
    def is_raining(self): pass

    @cprop()
    def rain_state(self): pass

    @cprop()
    def thunder_state(self): pass

    @cprop()
    def chat_patterns(self): pass

    @property
    def settings(self): return SettingsState(self.proxy.settings)

    @property
    def experience(self): return ExperienceState(self.proxy.experience)

    @cprop()
    def health(self): pass

    @cprop()
    def food(self): pass

    @cprop()
    def food_saturation(self): pass

    @cprop()
    def oxygen_level(self): pass

    @cprop()
    def physics(self): pass

    @cprop()
    def firework_rocket_duration(self): pass

    @property
    def time(self): return TimeState(self.proxy.time)

    @cprop()
    def quick_bar_slot(self): pass

    @cprop()
    def inventory(self): pass

    @cprop()
    def target_dig_block(self): pass

    @cprop()
    def is_sleeping(self): pass

    @cprop()
    def scoreboards(self): pass

    @cprop()
    def scoreboard(self): pass

    @cprop()
    def teams(self): pass

    @cprop()
    def team_map(self): pass

    @cprop()
    def control_state(self): pass
    
        
    def __load_plugins(self):
        self.mcData = require('minecraft-data')(self.bot.version)
        self.Item = require("prismarine-item")(self.bot.registry)
        self.bot.loadPlugin(self.pathfinder.pathfinder)
        self.bot.loadPlugin(self.armorManager)
        self.bot.loadPlugin(self.autoeat)
        self.movements = self.pathfinder.Movements(self.bot, self.mcData)
        self.movements.canDig = False

        self.bot.pathfinder.setMovements(self.movements)
        self.windows = require('prismarine-windows')(self.bot.version)
        self.Item = require('prismarine-item')(self.bot.version)
    
    def __setup_events(self):
        @On(self.bot, "path_update")
        def path_update(_, r):
            if not self.local_disable_viewer:
                path = [self.bot.entity.position.offset(0, 0.5, 0)]
                for node in r['path']:
                    path.append({'x': node['x'], 'y': node['y'] + 0.5, 'z': node['z']})
                self.bot.viewer.drawLine('path', path, 	0x0000FF)
        if not self.local_disable_viewer:
            @On(self.bot.viewer, "blockClicked")
            def on_block_clicked(_, block, face, button):
                try:
                    if button != 2:
                        return
                    p = block.position.offset(0, 1, 0)
                    self.bot.pathfinder.goto(self.pathfinder.goals.GoalNear(p.x, p.y, p.z, 1), timeout=60)
                except:
                    self.__logging(f"Cant get to {p.x}, {p.y}, {p.z}", error=True)
        
        
        
        @On(self.bot, "death")
        def death(*args):
            self.__logging("Bot died..." + " stopping bot!" * int(self.stop_bot_on_death), warning=True)
            if self.stop_bot_on_death:
                self.bot.end()
                quit()

        @On(self.bot, "kicked")
        def kicked(this, reason, *a):
            self.__logging("Kicked from server..." + " stopping bot!" * int(self.stop_bot_on_death) + f"\n\nReason: {reason}", warning=True)
            if self.stop_bot_on_death:
                self.bot.end()
                quit()

        @On(self.bot, "autoeat_started")
        def autoeat_started(item, offhand, *a):
            self.__logging(f"Eating {item['name']} in {'offhand' if offhand else 'hand'}", info=True)

        @On(self.bot, "autoeat_finished")
        def autoeat_finished(item, offhand):
            self.__logging(f"Finished eating {item['name']} in {'offhand' if offhand else 'hand'}", info=True)

        @On(self.bot, "error")
        def error(_, error):
            self.__logging(error, error=True)

        @On(self.bot, 'chat')
        def handleMsg(this, sender, message, *args):
            if self.local_enable_chat_logging:
                if not sender:
                    sender = "unknown"
                if not self.chatDatabase.contains(User.username == sender):
                    self.chatDatabase.insert({'username': sender, 'messages': [message]}) 
                else:
                    user = self.chatDatabase.get(User.username == sender)
                    existing_messages = user['messages']
                    existing_messages.extend([f"{message}"])
                    self.chatDatabase.update({'messages': existing_messages}, User.username == sender)
                self.__logging(f"{sender}: {message}", chat=True, icon="💬")
            

    def __equip_armor(self):
        try:
            self.bot.armorManager.equipAll()
        except:
            return

    def __start_viewer(self):
        try:
            self.mineflayerViewer(self.bot, {"port": self.local_viewer_port})
            self.__logging(f"Viewer started on port {self.local_viewer_port}", info=True)
        except:
            self.__logging("There was an error while starting the viewer!", warning=True)
    
    def __log_players(self):
        # print(type(self.bot.players))
        # playerDatabase.insert_multiple(self.bot.players.valueOf())
        pass
            
    
    def chat(self, *message):
        self.bot.chat(' '.join(message))

    def command_safe(self, arg):
        if isinstance(arg, str) and arg.count(' '):
                return '"' + arg.replace('"', '\\"') + '"'
        elif isinstance(arg, bool):
            return repr(arg).lower()
        elif isinstance(arg, tuple):
            returns = []
            for i in arg:
                returns.append(self.command_safe(i))
            return returns
        else:
            return arg


    def command(self, command: str, *args):
        converted_args = []
        for arg in args:
            parsed = self.command_safe(arg)
            if isinstance(parsed, list):
                converted_args.extend(parsed)
            else:
                converted_args.append(parsed)
        self.chat('/' + command, *converted_args)

    def coordinates(self) -> str:
        if self.logged_in:
            return f"{int(self.entity.position.x)}, {int(self.entity.position.y)}, {int(self.entity.position.z)}"

    def chatHistory(self, username:str, server:str="") -> list:
        if not self.local_enable_chat_logging:
            self.__logging(f"Chat logging is not enabled, set enableChatLogging=True in the bot config", warning=True)
            return []
        if server == "":
            server = self.local_host
        if os.path.exists(f"{server}".lower().replace(".", "") + "Database.json"):
            serverHistory = TinyDB(f"{server}".lower().replace(".", "") + "Database.json")
            user = serverHistory.get(User.username == username)
            if user:
                return user['messages']
            else:
                self.__logging(f"{username} has no chat history", warning=True)
        else:
            self.__logging(f"{server} has no database", warning=True)
            return []
        
    def clearLogs(self):
        if not self.local_enable_chat_logging:
            self.__logging(f"Chat logging is not enabled, set enableChatLogging=True in the bot config", warning=True)
            return
        self.chatDatabase.truncate()
        self.__logging("All databases are cleared!")
    
    def stop(self):
        self.bot.end()
        self.__logging("Stopped bot!", warning=True)
        quit()
        
    def serverData(self, server:str=None) -> dict:
        if server is None:
            server = self.local_host
        data = requests.get(f"https://api.mcstatus.io/v2/status/java/{server}").json()
        return data

createBot = Bot
