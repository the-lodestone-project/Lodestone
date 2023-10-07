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

class GameState:
    def __init__(self, proxy: Proxy):
        self.proxy = proxy

    @cprop()
    def level_type(self): pass

    @cprop()
    def dimension(self): pass

    @cprop()
    def difficulty(self): pass

    @cprop()
    def game_mode(self): pass

    @cprop()
    def hardcore(self): pass

    @cprop()
    def max_players(self): pass

    @cprop()
    def server_brand(self): pass

    @cprop()
    def min_y(self): pass

    @cprop()
    def height(self): pass

    @cprop(proxy_name="height")
    def max_y(self): pass


class TimeState:
    def __init__(self, proxy: Proxy):
        self.proxy = proxy

    @cprop()
    def do_daylight_cycle(self): pass

    @cprop()
    def big_time(self): pass

    @cprop()
    def time(self): pass

    @cprop()
    def time_of_day(self): pass

    @cprop()
    def day(self): pass

    @cprop()
    def is_day(self): pass

    @cprop()
    def moon_phase(self): pass

    @cprop()
    def big_age(self): pass

    @cprop()
    def age(self): pass


class ExperienceState:
    def __init__(self, proxy: Proxy):
        self.proxy = proxy

    @cprop()
    def level(self): pass

    @cprop()
    def points(self): pass

    @cprop()
    def progress(self): pass


class SettingsState:
    def __init__(self, proxy: Proxy):
        self.proxy = proxy

    @cprop()
    def chat(self): pass

    @cprop()
    def colors_enabled(self): pass

    @cprop()
    def view_distance(self): pass

    @cprop()
    def difficulty(self): pass

    @cprop()
    def skin_parts(self): pass

    @cprop()
    def enable_text_filtering(self): pass

    @cprop()
    def enable_server_listing(self): pass


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
        useDiscordForms: bool = False,
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
        skipChecks: bool = False
    ):
        """Create the bot"""
        self.host = host
        self.auth = auth
        self.port = port
        self.version = version
        self.password = password
        self.check_timeout_interval = checkTimeoutInterval
        self.armor_manager = armorManager
        self.viewer_port = viewerPort
        self.quit_on_low_health = quit_on_low_health
        self.low_health_threshold = low_health_threshold
        self.disableChatSigning = disableChatSigning
        self.profilesFolder = profilesFolder
        self.username = username
        self.clientToken = clientToken
        self.accessToken = accessToken
        self.logErrors = logErrors
        self.hideErrors = hideErrors
        self.keepAlive = keepAlive
        self.loadInternalPlugins = loadInternalPlugins
        self.respawn = respawn
        self.physicsEnabled = physicsEnabled
        self.defaultChatPatterns = defaultChatPatterns
        self.disableLogs = disableLogs
        self.enableChatLogging = enableChatLogging
        self.skipChecks = skipChecks
        
        global logger
        self.logger = structlog.get_logger()
        logger = self.logger
        self.console = Console()
        # [:2]
        self.apiMode = apiMode
        if not skipChecks:
            self.nodeVersion, self.pipVersion, self.pythonVersion = self.__versionsCheck()
        if discordWebhook is not None:
            from discord import Webhook
            from discord import Embed
            self.Embed = Embed
            self.useDiscordForms = useDiscordForms
            self.webhook = Webhook.from_url(f"{discordWebhook}")
            embedVar = Embed(title="Successfully Connected To The Webhook!", description=f"**Great news! The bot has successfully connected to this channel's webhook. From now on, it will send all the logs and valuable data right here, keeping you informed about everything happening on the server.**\n\n **Versions:**\n* [**Node**](https://nodejs.org/)**:      {self.nodeVersion[:2]}**\n* [**Pip**](https://pypi.org/project/pip/)**:          {self.pipVersion}**\n* [**Python**](https://www.python.org/)**:  {self.pythonVersion}**\n\n **Links:**\n* [**GitHub**](https://github.com/SilkePilon/OpenDeliveryBot)\n* [**Report Bugs**](https://github.com/SilkePilon/OpenDeliveryBot/issues)\n* [**Web Interface**](https://github.com/SilkePilon/OpenDeliveryBot-react)", color=0x3498db)
            embedVar.timestamp = datetime.datetime.utcnow()
            embedVar.set_footer(text='\u200b', icon_url="https://github.com/SilkePilon/OpenDeliveryBot/blob/main/chestlogo.png?raw=true")
            if useDiscordForms:
                today = date.today()
                send_webhook(self.webhook, content=f"{today}", thread_name=f"{today}", username="OpenDeliveryBot", avatar_url="https://github.com/SilkePilon/OpenDeliveryBot/blob/main/chestlogo.png?raw=true", embed=embedVar)
            else:
                try:
                    send_webhook(self.webhook, content="", username="OpenDeliveryBot", avatar_url="https://github.com/SilkePilon/OpenDeliveryBot/blob/main/chestlogo.png?raw=true", embed=embedVar)
                except:
                    self.logger.error(f"Detected that you are using a Forms channel but 'useDiscordForms' is set to False. Please change 'useDiscordForms' to True or provide a webhook url for a text channel.")
        self.discordWebhook = discordWebhook
        self.mineflayer = require('mineflayer')
        self.pathfinder = require('mineflayer-pathfinder')
        self.goals = require('mineflayer-pathfinder').goals
        self.mineflayerViewer = require('prismarine-viewer').mineflayer
        self.Vec3 = require("vec3").Vec3
        self.armorManager = require("mineflayer-armor-manager")
        self.autoeat = require('mineflayer-auto-eat').plugin
        self.repl = require('repl')
        self.statemachine = require("mineflayer-statemachine")
        self.pythonCommand = self.__checkPythonCommand()
        with self.console.status("[bold green]Checking for updates...\n") as status:
            status.update("[bold green]Updaing javascript librarys...\n")
            os.system(f'{self.pythonCommand} -m javascript --update >/dev/null 2>&1')
            status.update("[bold green]Updaing pip package...\n")
            os.system(f'{self.pythonCommand} -m pip install -U opendeliverybot >/dev/null 2>&1')
            time.sleep(3)
        self.logedin = False
        self.useReturn = useReturn
        self.msa_status = False
        self.servername = f"{self.host}".lower().replace(".", "")
        if self.enableChatLogging:
            self.chatDatabase = TinyDB(f"{self.servername}Database.json")
        self.script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.bot = self.__create_bot()
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
        if not self.disableLogs:
            if self.useReturn:
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
                if self.useDiscordForms:
                    today = date.today()
                    self.webhook.send(content=f"{today}", thread=f"{today}", username="OpenDeliveryBot", avatar_url="https://github.com/SilkePilon/OpenDeliveryBot/blob/main/chestlogo.png?raw=true", embed=embed)
                else:
                    try:
                        self.webhook.send(content=f"", username="OpenDeliveryBot", avatar_url="https://github.com/SilkePilon/OpenDeliveryBot/blob/main/chestlogo.png?raw=true", embed=embed)
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
        
    def __waitForMsa(self, code, timeout=10):
        if os.name == 'nt':
            basePath = os.getenv('APPDATA')
        else:
            basePath = Path().home()

        msa_file = Path(f"{basePath}/.minecraft/nmp-cache/")
        msa_file = f"{msa_file}/{self.__findFiles(msa_file, '*_mca-cache.json')[0]}"
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
        with self.console.status("[bold green]Waiting for login...\n") as status:
            self.msa_data = msa[0]
            self.msa_status = True
            self.__logging(message="It seems you are not logged in! Open your termianl for more information.",
                           error=True, console=False)
            self.logger.error(f"It seems you are not logged in, please go to https://microsoft.com/link and enter the following code: {self.msa_data['user_code']}")
            self.__waitForMsa(code=self.msa_data['user_code'])
            if self.apiMode:
                self.bot.end()
                quit()
            self.msa_status = False
            # self.logger.info(f"{msa[0]['user_code']} MSA Code")

    def __versionsCheck(self):
        with self.console.status("[bold green]Checking versions...\n") as status:
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
                if not self.disableLogs:
                    self.logger.info(f"Detected Node version {node_version[:2]} witch is supported!")
            else:
                self.logger.warning(f"Detected node version {node_version[:2]} witch is NOT supported!\nThis may cause problems. Please update to node 18 or above!")
                time.sleep(7)
                
                
            # Pip
            result = subprocess.run(["pip", "--version"], 
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True)
            pip_version = result.stdout.strip()
            # Remove
            match = re.search(r'pip (\d+(?:\.\d+)*).*python (\d+(?:\.\d+)*)', pip_version)
            if match:
                pip_version = match.group(1)
                python_version = match.group(2)
            if not self.disableLogs:
                self.logger.info(f"Detected Pip version {pip_version} witch is supported!")
                self.logger.info(f"Detected Python version {python_version} witch is supported!")
            return node_version, pip_version, python_version

    def __create_bot(self):
        if self.version == "auto" or self.version == "false":
            self.version = False
        else:
            self.version = str(self.version)
        localBot = self.mineflayer.createBot({
            'host': self.host,
            'port': self.port,
            'username': self.username,
            'password': self.password,
            'auth': self.auth,
            'version': self.version,
            'onMsaCode': self.__msa,
            'checkTimeoutInterval': 60 * 10000,
            'disableChatSigning': self.disableChatSigning,
            'profilesFolder': self.profilesFolder,
            'logErrors': self.logErrors,
            'hideErrors': self.hideErrors,
            'keepAlive': self.keepAlive,
            'loadInternalPlugins': self.loadInternalPlugins,
            'respawn': self.respawn,
            'physicsEnabled': self.physicsEnabled,
            'defaultChatPatterns': self.defaultChatPatterns
        })
        @On(localBot, "login")
        def on_login(*args):
            self.bot = localBot
            self.logedin = True
            self.__logging(f"Connecting to {self.host}", info=True,
                           imageUrl=f"https://eu.mc-api.net/v3/server/favicon/{self.host}")
            self.__logging(f'Logged in as {self.bot.username}', info=True,
                           imageUrl=f"https://mc-heads.net/avatar/{self.bot.username}/600.png")
            self.__start_viewer()
            self.__setup_events()
            self.__logging(
                f'Cordinates: {int(self.bot.entity.position.x)}, {int(self.bot.entity.position.y)}, {int(self.bot.entity.position.z)}',
                info=True)
            self.__load_plugins()
        return localBot


    def __start(self):
        while not self.logedin:
            time.sleep(1) 
        # @On(self.bot, "login")
        # def on_login(*args):
        
        # r = self.repl.start('> ')
        # r.context.bot = self.bot
        # self.__auto_totem()
        self.__equip_armor()

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
    def using_held_item(self): pass

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
            path = [self.bot.entity.position.offset(0, 0.5, 0)]
            for node in r['path']:
                path.append({'x': node['x'], 'y': node['y'] + 0.5, 'z': node['z']})
            self.bot.viewer.drawLine('path', path, 	0x0000FF)
        @On(self.bot.viewer, "blockClicked")
        def on_block_clicked(_, block, face, button):
            try:
                if button != 2:
                    return
                p = block.position.offset(0, 1, 0)
                self.bot.pathfinder.goto(self.pathfinder.goals.GoalNear(p.x, p.y, p.z, 1), timeout=60)
            except:
                self.__logging(f"Cant get to goal", error=True)
        
        
        
        @On(self.bot, "death")
        def death(*args):
            self.bot.end()
            self.__logging("Bot died... stopping bot!", warning=True)
        @On(self.bot, "kicked")
        def kicked(this, reason, *a):
            self.bot.end()
            self.__logging("Kicked from server... stopping bot!", warning=True)
        @On(self.bot, "autoeat_started")
        def autoeat_started(item, offhand, *a):
            self.__logging(f"Eating {item['name']} in {'offhand' if offhand else 'hand'}", info=True)
        @On(self.bot, "autoeat_finished")
        def autoeat_finished(item, offhand):
            self.__logging(f"Finished eating {item['name']} in {'offhand' if offhand else 'hand'}", info=True)
        @On(self.bot, "error")
        def error(_, error):
            self.__logging(error, error=True)
        @On(self.bot, "end")
        def create_new_bot(*a):
            self.bot = self.__create_bot()
        @On(self.bot, 'chat')
        def handleMsg(this, sender, message, *args):
            if self.enableChatLogging:
                if not sender:
                    sender = "unknown"
                if not self.chatDatabase.contains(User.username == sender):
                    self.chatDatabase.insert({'username': sender, 'messages': [message]}) 
                else:
                    user = self.chatDatabase.get(User.username == sender)
                    existing_messages = user['messages']
                    existing_messages.extend([f"{message}"])
                    self.chatDatabase.update({'messages': existing_messages}, User.username == sender)
                self.__logging(f"💬 {sender}: {message}", chat=True)
            

    def __equip_armor(self):
        try:
            self.bot.armorManager.equipAll()
        except:
            return

    def __start_viewer(self):
        self.mineflayerViewer(self.bot, {"port": self.viewer_port})
        self.__logging("Viewer started on port %s" % self.viewer_port, info=True)
    
    def __log_players(self):
        # print(type(self.bot.players))
        # playerDatabase.insert_multiple(self.bot.players.valueOf())
        pass
            
    def __item_By_Name(self, items, name):
            item = None
            for i in range(len(items)):
                item = items[i]
                if item and item['name'] == name:
                    return item
                return None
            
        
    # Needs to be changed to {"item": item_count}
    # def inventory(self):
    #     inv = []
    #     if self.bot and self.bot.inventory:
    #         for item in self.bot.inventory.items():
    #             inv.append(item.displayName)
    #     return inv
    
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
        self.chat(command, *converted_args)

    def coordinates(self) -> str:
        if self.logedin:
            return f"{int(self.entity.position.x)}, {int(self.entity.position.y)}, {int(self.entity.position.z)}"

    def chatHistory(self, username:str, server:str="") -> list:
        if not self.enableChatLogging:
            self.__logging(f"Chat logging is not enabled, set enableChatLogging=True in the bot config", warning=True)
            return []
        if server == "":
            server = self.host
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
        if not self.enableChatLogging:
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
            server = self.host
        data = requests.get(f"https://api.mcstatus.io/v2/status/java/{server}").json()
        return data
    
createBot = Bot
        
        
        