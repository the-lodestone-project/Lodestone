from javascript import require, On, Once
from javascript.proxy import Proxy
from rich.console import Console
from discord import Embed
from tinydb import TinyDB, Query
import requests
import structlog

import datetime
import os
import sys
import time
import fnmatch
import re
from datetime import date
from pathlib import Path
import subprocess

try:
    from utils import cprop, send_webhook
except ImportError:
    from .utils import cprop, send_webhook

User = Query()

logger = structlog.get_logger()

filestruc = "/"
if os.name == 'nt':
    filestruc = "\\"

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

class CreativeMode:
    """
    Provides some creative mode functionalities. Should not initalize manully
    """
    def __init__(self, proxy: Proxy):
        self.proxy = proxy

    @cprop()
    def set_inventory_slot(self):
        "Sets the inventory slot (returns Function(slot: number, item: prismarine-item.Item))"
    
    @cprop()
    def fly_to(self):
        "Fly to a location (returns Function(destination: vec3.Vec3))"
    
    @cprop()
    def start_flying(self):
        "Start flying (returns Function())"

    @cprop()
    def stop_flying(self):
        "Stop flying (returns Function()"

    def clear_slot(self, slot: int):
        "Clears the slot"
        self.set_inventory_slot(slot, None)

    @cprop()
    def clear_inventory(self):
        "Clears the inventory (returns Function())"

class Bot:
    def __init__(
            self,
            host: str,
            *,
            auth: str = "microsoft",
            port: int = 25565,
            version: str = "false",
            password: str = "",
            respawn: bool = True,
            disableChatSigning: bool = False,
            profilesFolder: str = "",
            username: str = "lodestone",
            hideErrors: bool = True,
            logErrors: bool = True,
            keepAlive: bool = True,
            loadInternalPlugins: bool = True,
            physicsEnabled: bool = True,
            defaultChatPatterns: bool = True,

            ls_disable_logs: bool = False,
            ls_enable_chat_logging: bool = False,
            ls_skip_checks: bool = False,
            ls_disable_viewer: bool = False,
            ls_stop_bot_on_death: bool = False,
            ls_debug_mode: bool = False,
            ls_viewer_port: int = 5001,
            ls_use_return: bool = False,
            ls_discord_webhook: str = None,
            ls_use_discord_forums: bool = False,
            ls_api_mode: bool = False,

            ls_plugins: list = None
    ):
        """
        Create the bot. Parameters in camelCase are passed into mineflayer. Parameters starting with ls_ is Lodestone specific
        """
        if ls_debug_mode:
            os.environ["DEBUG"] = "minecraft-protocol"
        else:
            os.environ["DEBUG"] = ""

        self.local_host = host
        self.local_auth = auth
        self.local_port = port
        self.local_version = version
        self.local_password = password
        self.local_disable_chat_signing = disableChatSigning
        self.local_profiles_folder = profilesFolder
        self.local_username = username
        self.local_hide_errors = hideErrors
        self.local_log_errors = logErrors
        self.local_keep_alive = keepAlive
        self.local_load_internal_plugins = loadInternalPlugins
        self.local_respawn = respawn
        self.local_physics_enabled = physicsEnabled
        self.local_default_chat_patterns = defaultChatPatterns

        self.viewer_port = ls_viewer_port
        self.disable_logs = ls_disable_logs
        self.enable_chat_logging = ls_enable_chat_logging
        self.skip_checks = ls_skip_checks
        self.disable_viewer = ls_disable_viewer
        self.discord_webhook = ls_discord_webhook
        self.stop_bot_on_death = ls_stop_bot_on_death
        self.use_discord_forums = ls_use_discord_forums
        self.api_mode = ls_api_mode
        self.plugin_list = ls_plugins if ls_plugins else []

        self.console = Console()
        self.extra_data = {}
        self.loaded_plugins = {}

        if not self.skip_checks:
            self.node_version, self.pip_version, self.python_version = self.__versions_check()
        else:
            self.node_version, self.pip_version, self.python_version = "unknown", "unknown", "unknown"

        if self.discord_webhook is not None:
            embed = Embed(
                title="Successfully Connected to Webhook!",
                description=f"""
                **Great news!** The bot has successfully connected to this channel's webhook.
                From now on, it will send all the logs and valuable data right here, keeping you informed about everything happening on the server.
                
                **Versions: **
                * [**Node**](https://nodejs.org/): {self.node_version}
                * [**Pip**](https://pypi.org/project/pip/): {self.pip_version}
                * [**Python**](https://www.python.org/): {self.python_version}
                
                **Links: **
                * [**GitHub**](https://github.com/SilkePilon/Lodestone)
                * [**Report Bugs**](https://github.com/SilkePilon/Lodestone/issues)
                * [**Web Interface**](https://github.com/SilkePilon/Mineflayer.py-react)
                """,
                color=0x3498db
            )
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text='\u200b', icon_url="https://github.com/SilkePilon/Lodestone/blob/main/chestlogo.png?raw=true")
            if ls_use_discord_forums:
                today = date.today()
                send_webhook(ls_discord_webhook, content=f"{today}", thread_name=f"{today}", username="Lodestone", avatar_url="https://github.com/SilkePilon/Lodestone/blob/main/chestlogo.png?raw=true", embed=embed)
            else:
                try:
                    send_webhook(ls_discord_webhook, content="", username="Lodestone", avatar_url="https://github.com/SilkePilon/Lodestone/blob/main/chestlogo.png?raw=true", embed=embed)
                except Exception as e:
                    print(e)
                    logger.error(f"Detected that you are using a Forums channel but 'useDiscordForums' is set to False. Please change 'useDiscordForums' to True or provide a webhook url for a text channel.")

        self.mineflayer = require('mineflayer')
        self.pathfinder = require('mineflayer-pathfinder')
        self.goals = require('mineflayer-pathfinder').goals
        if not self.disable_viewer:
            self.mineflayer_viewer = require('prismarine-viewer').mineflayer
        self.armor_manager = require("mineflayer-armor-manager")
        self.auto_eat = require('mineflayer-auto-eat').plugin
        self.statemachine = require("mineflayer-statemachine")
        self.python_command = self.__check_python_command()
        if not ls_skip_checks:
            with self.console.status("[bold green]Checking for updates...\n") as status:
                status.update("[bold green]Updating javascript librarys...\n")
                os.system(f'{self.python_command} -m javascript --update >/dev/null 2>&1')
                status.update("[bold green]Updating pip package...\n")
                os.system(f'{self.python_command} -m pip install -U lodestone >/dev/null 2>&1')
        self.logged_in = False
        self.use_return = ls_use_return
        self.msa_status = False
        self.server_name = f"{self.local_host}".lower().replace(".", "")
        if self.enable_chat_logging:
            self.chat_database = TinyDB(f"{self.server_name}Database.json")
        self.script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.bot: Proxy = self.__create_bot()
        self.proxy = self.bot
        self.msa_data = False
        self.__start()

        # loads plugins
        for plugin in self.plugin_list:
            self.load_plugin(plugin)
        
    def load_plugin(self, plugin: type):
        """
        Loads a singular plugin (A class object. Not initalized)
        """
        plugin_name = plugin.__name__
        initialized_plugin = plugin(self)
        self.loaded_plugins[plugin_name] = initialized_plugin
    
    def __check_python_command(self):
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

    def __logging(self, message, icon="🤖", error=False, info=False, warning=False, chat=False, image_url="", console=True, discord=True):
        if not self.disable_logs:
            if self.use_return:
                logger.info(f"[{icon}] {message}")
            elif self.discord_webhook and discord:
                from discord import Embed
                color = 0x3498db
                if error:
                    color = 0x992d22
                elif info:
                    color = 0x3498db
                elif warning:
                    color = 0xe67e22
                elif chat:
                    color = 0x2ecc71
                embed = Embed(title="", description=f"**[{icon}] {message}**", color=color)
                embed.timestamp = datetime.datetime.utcnow()
                if image_url != "":
                    embed.set_thumbnail(url=image_url)
                try:
                    embed.set_footer(text=f'{self.bot.username}', icon_url=f"https://mc-heads.net/avatar/{self.bot.username}/600.png")
                except:
                    embed.set_footer(text='\u200b', icon_url="https://github.com/SilkePilon/Lodestone/blob/main/chestlogo.png?raw=true")
                if self.use_discord_forums:
                    today = date.today()
                    send_webhook(self.discord_webhook, content=f"{today}", thread_name=f"{today}", username="Lodestone", avatar_url="https://github.com/SilkePilon/Lodestone/blob/main/chestlogo.png?raw=true", embed=embed)
                else:
                    try:
                        send_webhook(self.discord_webhook, content=f"", username="Lodestone", avatar_url="https://github.com/SilkePilon/Lodestone/blob/main/chestlogo.png?raw=true", embed=embed)
                    except Exception as e:
                        print(e)
                        logger.error(f"Detected that you are using a Forums channel but 'useDiscordForums' is set to False. Please change 'useDiscordForums' to True or provide a webhook url for a text channel.")
            if console:
                if error:
                    logger.error(f"[{icon}] {message}")
                elif info:
                    logger.info(f"[{icon}] {message}")
                elif warning:
                    logger.warning(f"[{icon}] {message}")
                elif chat:
                    logger.info(f"[{icon}] {message}")
                else:
                    logger.info(f"[{icon}] {message}")
        
    @staticmethod
    def __find_files(base, pattern):
        """Return list of files matching pattern in base folder."""
        return [n for n in fnmatch.filter(os.listdir(base), pattern) if
            os.path.isfile(os.path.join(base, n))]
        
    def __wait_for_msa(self, timeout = 300): # 5 minutes
        if os.name == 'nt':
            base_path = os.getenv('APPDATA')
        else:
            base_path = Path().home()
        path = self.local_profiles_folder
        if not path:
            path = Path(f"{base_path}/.minecraft/nmp-cache/")
        msa_file = path / self.__find_files(path, '*_mca-cache.json')[0]
        for _ in range(timeout):
            time.sleep(1)
            with open(msa_file) as check:
                if check.read() != "{}":
                    logger.info("Logged in successfully!")
                    return
        raise TimeoutError(
            f"Fetching for MSA code timed out. Timeout={timeout} seconds"
        )

    def __msa(self, *msa):
        with self.console.status("[bold green]Waiting for login...\n"):
            self.msa_data = msa[0]
            self.msa_status = True
            self.__logging(message="It seems you are not logged in! Open your terminal for more information.",
                           error=True, console=False)
            logger.error(f"It seems you are not logged in, please go to https://microsoft.com/link and enter the following code: {self.msa_data['user_code']}")
            self.__wait_for_msa()
            if self.api_mode:
                self.bot.end()
                quit()
            self.msa_status = False
            # logger.info(f"{msa[0]['user_code']} MSA Code")

    def __versions_check(self):
        with self.console.status("[bold green]Checking versions...\n"):
            # Node
            result = subprocess.run(["node", "--version"], 
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True)
            node_version = result.stdout.strip()
            # Remove leading 'v'
            node_version = node_version.removeprefix("v")
            # Remove periods
            node_version = node_version.replace('.', '')
            if int(node_version[:2]) >= 18:
                pass
            else:
                logger.warning(f"""
                                Detected node version {node_version[:2]} which isn't supported!
                                This may cause problems. Please update to node 18 or above!
                                """)

            # Pip
            pip_ = 'pip' if self.__check_python_command() == 'python' else 'pip3'
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
            return node_version, pip_version, python_version

    def __create_bot(self):
        if self.local_version == "auto" or self.local_version == "false":
            self.local_version = False
        else:
            self.version = str(self.local_version)
        local_bot = self.mineflayer.createBot({
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
        @On(local_bot, "login")
        def on_login(*args):
            self.bot = local_bot
            self.logged_in = True
            self.__logging(f"Connected to {self.local_host}", info=True,
                           image_url=f"https://eu.mc-api.net/v3/server/favicon/{self.local_host}")
            self.__logging(f'Logged in as {self.bot.username}', info=True,
                           image_url=f"https://mc-heads.net/avatar/{self.bot.username}/600.png")
            if not self.disable_viewer:
                self.__start_viewer()
            self.__setup_events()
            self.__load_plugins()
        return local_bot


    def __start(self):
        while not self.logged_in:
            time.sleep(1)
        self.__equip_armor()
        self.__logging(
            f'Coordinates: {int(self.bot.entity.position.x)}, {int(self.bot.entity.position.y)}, {int(self.bot.entity.position.z)}',
            info=True)

    def on(self, event: str):
        """
        Decorator for event registering

        @bot.on('messagestr')
        def chat(this, message, *args):
            ...
        """
        def inner(function):
            On(self.proxy, event)(function)
        return inner

    def once(self, event: str):
        """
        Decorator for event registering

        @bot.once('login')
        def login(*args):
            ...
        """
        def inner(function):
            Once(self.proxy, event)(function)
        return inner

    def emit(self, event: str, *params):
        """
        Emits an event which could be listened to

        bot.emit('custom_chat', username, message)
        """
        self.bot.emit(event, *params)
        self.__logging(f"Emitting event {repr(event)} with parameters {params}", info=True, discord=False)

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

    @property
    def creative(self): return CreativeMode(self.proxy.creative)
    
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
        self.mc_data = require('minecraft-data')(self.bot.version)
        self.bot.loadPlugin(self.pathfinder.pathfinder)
        self.bot.loadPlugin(self.armor_manager)
        self.bot.loadPlugin(self.auto_eat)
        self.movements = self.pathfinder.Movements(self.bot, self.mc_data)
        self.movements.canDig = False

        self.bot.pathfinder.setMovements(self.movements)
        self.windows = require('prismarine-windows')(self.bot.version)
        self.Item = require('prismarine-item')(self.bot.version)
    
    def __setup_events(self):
        @self.on("path_update")
        def path_update(_, r):
            if not self.disable_viewer:
                path = [self.bot.entity.position.offset(0, 0.5, 0)]
                for node in r['path']:
                    path.append({'x': node['x'], 'y': node['y'] + 0.5, 'z': node['z']})
                self.bot.viewer.drawLine('path', path, 	0x0000FF)

        if not self.disable_viewer:
            @On(self.bot.viewer, "blockClicked")
            def on_block_clicked(_, block, face, button):
                try:
                    if button != 2:
                        return
                    p = block.position.offset(0, 1, 0)
                    self.bot.pathfinder.goto(self.pathfinder.goals.GoalNear(p.x, p.y, p.z, 1), timeout=60)
                except:
                    self.__logging(f"Can't get to {p.x}, {p.y}, {p.z}", error=True)
        
        
        
        @self.on("death")
        def death(*args):
            self.__logging("Bot died..." + " stopping bot!" * int(self.stop_bot_on_death), warning=True)
            if self.stop_bot_on_death:
                self.bot.end()
                quit()

        @self.on("kick")
        def kicked(this, reason, *a):
            self.__logging(
                "Kicked from server..." + " stopping bot!" * int(self.stop_bot_on_death) + f"\n\nReason: {reason}",
                warning=True)
            if self.stop_bot_on_death:
                self.bot.end()
                quit()

        @self.on("autoeat_started")
        def autoeat_started(item, offhand, *a):
            self.__logging(f"Eating {item['name']} in {'offhand' if offhand else 'hand'}", info=True)

        @self.on("autoeat_finished")
        def autoeat_finished(item, offhand):
            self.__logging(f"Finished eating {item['name']} in {'offhand' if offhand else 'hand'}", info=True)

        @self.on("error")
        def error(_, error):
            self.__logging(error, error=True)

        @self.on("chat")
        def handleMsg(this, sender, message, *args):
            if self.enable_chat_logging:
                if not sender:
                    sender = "unknown"
                if not self.chat_database.contains(User.username == sender):
                    self.chat_database.insert({'username': sender, 'messages': [message]})
                else:
                    user = self.chat_database.get(User.username == sender)
                    existing_messages = user['messages']
                    existing_messages.extend([f"{message}"])
                    self.chat_database.update({'messages': existing_messages}, User.username == sender)
                self.__logging(f"{sender}: {message}", icon="💬", chat=True)

    def __equip_armor(self):
        try:
            self.bot.armorManager.equipAll()
        except:
            return

    def __start_viewer(self):
        try:
            self.mineflayer_viewer(self.bot, {"port": self.viewer_port})
            self.__logging(f"Viewer started on port {self.viewer_port}", info=True)
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

    def chat_history(self, username: str, server="") -> list:
        if not self.enable_chat_logging:
            self.__logging(f"Chat logging is not enabled, set enableChatLogging=True in the bot config", warning=True)
            return []
        if server == "":
            server = self.local_host
        if os.path.exists(f"{server}".lower().replace(".", "") + "Database.json"):
            server_history = TinyDB(f"{server}".lower().replace(".", "") + "Database.json")
            user = server_history.get(User.username == username)
            if user:
                return user['messages']
            else:
                self.__logging(f"{username} has no chat history", warning=True)
        else:
            self.__logging(f"{server} has no database", warning=True)
            return []
        
    def clear_logs(self):
        if not self.enable_chat_logging:
            self.__logging(f"Chat logging is not enabled, set enableChatLogging=True in the bot config", warning=True)
            return
        self.chat_database.truncate()
        self.__logging("All databases are cleared!")
    
    def stop(self):
        self.bot.end()
        self.__logging("Stopped bot!", warning=True)
        quit()
        
    def server_data(self, server:str=None) -> dict:
        if server is None:
            server = self.local_host
        data = requests.get(f"https://api.mcstatus.io/v2/status/java/{server}").json()
        return data

    def set_data(self, item, value):
        """
        Sets custom data that can be later accessed. Also returns data.

        bot.set_data("hello", "world")
        ... # some time consuming task later
        print(bot.get_data("hello")) # should print "world"
        """
        self.extra_data[item] = value
        return value

    def get_data(self, item, default: object = None, compare: object = "nothing to compare to"):
        """
        Gets custom data that is set prior. Also take in an optional compare parameter to do assertion with the obtained data.
        Default parameter for 'default' is None

        ... # some other code
        try:
            print(bot.get_data("custom_health", 200))
        except AssertionError:
            print("Bot not at full health!")
        """
        result = self.extra_data.get(item, default)
        if not compare == "nothing to compare to": # there's a comparison
            if result != compare:
                raise AssertionError(
                    f"Incorrect value in custom data! Queried {repr(item)}={repr(result)}, instead expected {repr(item)}={repr(compare)}"
                )
        return result

createBot = Bot