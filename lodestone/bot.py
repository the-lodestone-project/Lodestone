from javascript import require, On, Once, off, once
from javascript.proxy import Proxy
from rich.console import Console
from tinydb import TinyDB, Query
import shutil
import requests
import os
import sys
import time
import fnmatch
import re
import subprocess
import git
from typing import Callable
from importlib.metadata import version as version_checker
import dataclasses
import threading
try:
    from logger import logger
    from utils import cprop
except ImportError:
    from .logger import logger
    from .utils import cprop

User = Query()


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
    def set_inventory_slot(self) -> Callable[[int, Proxy], None]:
        "Sets the inventory slot (returns Function(slot: number, item: prismarine-item.Item))"
    
    @cprop()
    def fly_to(self) -> Callable[[Proxy], None]:
        "Fly to a location (returns Function(destination: vec3.Vec3))"
    
    @cprop()
    def start_flying(self) -> Callable[[], None]:
        "Start flying (returns Function())"

    @cprop()
    def stop_flying(self) -> Callable[[], None]:
        "Stop flying (returns Function()"

    def clear_slot(self, slot: int):
        "Clears the slot"
        self.set_inventory_slot(slot, None)

    @cprop()
    def clear_inventory(self) -> Callable[[], None]:
        "Clears the inventory (returns Function())"

@dataclasses.dataclass
class CommandContext:
    """
    Command Context for Bot Commands. Should not initialize manually
    """
    sender: str
    command: str
    full_command: str
    arguments: list
    time: float
    full_message: Proxy
    bot: 'Bot'

    def respond(self, *message, whisper = False, whisper_to: str):
        """
        Respond to the command. Use whisper_to only if whisper is True
        """
        if whisper:
            self.bot.whisper(whisper_to, *message)
        else:
            self.bot.chat(*message)



def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

class Bot(threading.Thread):
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
            checkTimeoutInterval: int = 60 * 10000,
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
            ls_plugin_list: [] = None,
            easyMcToken: str = None
            
    ):
        """
        Create the bot. Parameters in camelCase are passed into mineflayer. Parameters starting with ls_ is Lodestone specific
        """
        threading.Thread.__init__(self, daemon=True)
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
        self.plugin_list = ls_plugin_list if ls_plugin_list else []
        self.check_timeout_interval = checkTimeoutInterval
        self.easy_mc_token = easyMcToken

        self.custom_command_prefix = "!"
        self.custom_commands = {}
        """
        {
            "cmd_name": {
                "sender": sender or None,
                "callback": Callable[[CommandContext], None]
            }
        }
        """

        self.console = Console()
        self.extra_data = {}
        self.loaded_plugins = {}
        self.loaded_events = {}
        
        
        
        _ = require("mineflayer")
        _ = require("prismarine-viewer")
        _ = require("mineflayer-collectblock")
        _ = require("minecraft-data")
        _ = require("mineflayer-pathfinder")

        if not self.skip_checks:
            self.node_version, self.pip_version, self.python_version = self.__versions_check()
        else:
            self.node_version, self.pip_version, self.python_version = "unknown", "unknown", "unknown"

        if self.discord_webhook is not None:
            pass # needs plugin

        self.mineflayer = require('mineflayer')
        self.once_with_cleanup = require('mineflayer').promise_utils
        if not self.disable_viewer:
            self.mineflayer_viewer = require('prismarine-viewer')
        self.python_command = self.__check_python_command()
        if not ls_skip_checks:
            with self.console.status("[bold]Checking for updates...\n") as status:
                status.update("[bold]Updating javascript libraries...\n")
                subprocess.run(f'{self.python_command} -m javascript --update', stdout=subprocess.DEVNULL, shell=True, input=b"\n")
                status.update("[bold]Updating pip package...\n")
                subprocess.run(f'{self.python_command} -m pip install -U lodestone', stdout=subprocess.DEVNULL, shell=True, input=b"\n")
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


    # RIP def __getattr__(self, name)
    # You will be missed

    def load_plugin(self, plugin: type):
        """
        Loads a singular plugin (An uninitalized class object)

        ```python
        class Plugin:
            def __init__(self, bot: lodestone.Bot):
                print("Plugin Injected")
        ```
        """
        plugin_name = plugin.__name__
        initialized_plugin = plugin(self)
        self.loaded_plugins[plugin_name] = initialized_plugin
        self.emit("plugin_load", plugin_name)
    
    def __check_python_command(self):
        try:
            subprocess.check_output(['python', '--version'])
            return 'python'
        except:
            try:
                subprocess.check_output(['python3', '--version']) 
                return 'python3'
            except:
                self.log(message='Python command not found, make sure python is installed!', error=True, discord=False)
                sys.exit(1)

    def log(self, message, icon="🤖", error=False, info=False, warning=False, chat=False, image_url="", console=True, discord=True):
        if not self.disable_logs:
            if self.use_return:
                logger.info(f"[{icon}] {message}")
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
    
    def __wait_for_msa(self):
        @self.once('login')
        def await_login(*args):
            logger.info("Logged in successfully!")
            

    def __msa(self, *msa):
        self.msa_data = msa[0]
        self.msa_status = True
        self.log(message="It seems you are not logged in! Open your terminal for more information.", error=True,
                    console=False)
        msg = str(self.msa_data['message']).replace("\n", "")
        logger.error(f"It seems you are not logged in. {msg}")
        
        
        self.__wait_for_msa()
        if self.api_mode:
            self.bot.end()
            quit()
        self.msa_status = False

    def __versions_check(self):
        with self.console.status("[bold]Checking versions...\n"):
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
        
        if self.local_auth.lower() == "easymc":
            self.minecraft_protocol = require('minecraft-protocol')
            import types
            
            
            def easy_mc_auth(client, options):
                try:
                    res = requests.post('https://api.easymc.io/v1/token/redeem', headers={'Content-Type': 'application/json'}, json={"token":f"{options['easyMcToken']}"})
                    res_json =  res.json()
                    if res_json.get('error'):
                        raise Exception(f'EasyMC: {res_json["error"]}')
                        quit()
                    if not res_json:
                        raise Exception('Empty response from EasyMC.')
                        quit()
                    if len(res_json.get('session', '')) != 43 or len(res_json.get('mcName', '')) < 3 or len(res_json.get('uuid', '')) != 36:
                        raise Exception('Invalid response from EasyMC.')
                        quit()
                    session = {
                        'accessToken': res_json['session'],
                        'selectedProfile': {
                            'name': res_json['mcName'],
                            'id': res_json['uuid']
                        }
                    }
                    options.haveCredentials = True
                    client.session = session
                    options.username = client.username = session['selectedProfile']['name']
                    options.accessToken = session['accessToken']
                    client.emit('session', session)
                    options['connect'](client)
                except Exception as error:
                    print(error)
                    quit()


            try:
                local_bot = self.mineflayer.createBot({
                    'host': self.local_host,
                    'port': self.local_port,
                    'auth': easy_mc_auth,
                    'sessionServer': 'https://sessionserver.easymc.io',
                    'username': bytes(),
                    'version': self.local_version,
                    'checkTimeoutInterval': self.check_timeout_interval,
                    'logErrors': self.local_log_errors,
                    'hideErrors': self.local_hide_errors,
                    'keepAlive': self.local_keep_alive,
                })
                print(local_bot)
                self.bot = local_bot
                return local_bot
            except Exception as e:
                raise ValueError(f"Error while creating bot: {e}")
        else:    
            try:
                local_bot = self.mineflayer.createBot({
                    'host': self.local_host,
                    'port': self.local_port,
                    'username': self.local_username,
                    'password': self.local_password,
                    'auth': self.local_auth,
                    'version': self.local_version,
                    'onMsaCode': self.__msa,
                    'checkTimeoutInterval': self.check_timeout_interval,
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
                self.bot = local_bot
                return local_bot
            except Exception as e:
                raise ValueError(f"Error while creating bot: {e}")
            
        

    

    def __start(self):
        self.__setup_events()
        while not self.logged_in:
            time.sleep(1)
        self.log(
            f'Coordinates: {int(self.bot.entity.position.x)}, {int(self.bot.entity.position.y)}, {int(self.bot.entity.position.z)}',
            info=True)
        self.__load_plugins()

    def on(self, event: str):
        """
        Decorator for event registering

        ```python
        @bot.on('messagestr')
        def chat(_, message, *args):
            ...
        ```
        """
        def inner(function):
            On(self.proxy, event)(function)
        return inner
    
    def off(self, event: str, function):
        """
        Decorator for event unregistering

        ```python
        @bot.off('messagestr')
        def chat(_, message, *args):
            ...
        ```
        """
        print(function)
        off(emitter=self.proxy, event=f"{event}", handler=function)
        return
    

    def once(self, event: str):
        """
        Decorator for event registering

        ```python
        @bot.once('login')
        def login(*args):
            ...
        ```
        """
        def inner(function):
            Once(self.proxy, event)(function)
        return inner

    def emit(self, event: str, *params):
        """
        Emits an event which could be listened to

        ```python
        bot.emit('custom_chat', username, message)
        ```
        """
        self.bot.emit(event, *params)
        self.log(f"Emitting event {repr(event)}", info=True, discord=False)

    def add_method(self, target_name=None):
        """
        Decorator for adding a method dynamically.
        **IMPORTANT** You need the self argument! The self argument also points to your own plugin class, not the bot's

        ```python
        @add_method()
        def lobby(self, server="main"):
            self.bot.command("lobby", server)
        ```
        """
        def inner(function):
            def wrapper(*args, **kwargs):
                function(*args, **kwargs)
            wrapper.__name__ = function.__name__
            wrapper.__doc__ = function.__doc__

            if target_name:
                setattr(self, target_name, function)
            else:
                setattr(self, function.__name__, function)
            return wrapper
        return inner

    @cprop()
    def registry(self) -> Proxy: pass

    @cprop()
    def world(self) -> Proxy: pass

    @cprop()
    def entity(self) -> Proxy: pass

    @cprop()
    def entities(self) -> Proxy: pass

    @cprop()
    def username(self) -> str: pass

    @cprop()
    def spawn_point(self) -> Proxy: pass

    @cprop()
    def held_item(self) -> Proxy: pass

    @cprop()
    def using_held_item(self) -> bool: pass

    @property
    def game(self): return GameState(self.proxy.game)

    @property
    def creative(self): return CreativeMode(self.proxy.creative)
    
    @cprop()
    def physics_enabled(self) -> bool: pass
    
    @cprop()
    def player(self) -> Proxy: pass
    
    @cprop()
    def players(self) -> Proxy: pass
    
    @cprop()
    def tablist(self) -> Proxy: pass

    @cprop()
    def is_raining(self) -> bool: pass

    @cprop()
    def rain_state(self) -> int: pass

    @cprop()
    def thunder_state(self) -> int: pass

    @cprop()
    def chat_patterns(self) -> Proxy: pass

    @property
    def settings(self): return SettingsState(self.proxy.settings)

    @property
    def experience(self): return ExperienceState(self.proxy.experience)

    @cprop()
    def health(self) -> int: pass

    @cprop()
    def food(self) -> int: pass

    @cprop()
    def food_saturation(self) -> int: pass

    @cprop()
    def oxygen_level(self) -> int: pass

    @cprop()
    def physics(self) -> Proxy: pass

    @cprop()
    def firework_rocket_duration(self) -> int: pass

    @property
    def time(self): return TimeState(self.proxy.time)

    @cprop()
    def quick_bar_slot(self) -> int: pass

    @cprop()
    def inventory(self) -> Proxy: pass

    @cprop()
    def target_dig_block(self) -> Proxy: pass

    @cprop()
    def is_sleeping(self) -> bool: pass

    @cprop()
    def scoreboards(self) -> Proxy: pass

    @cprop()
    def scoreboard(self) -> Proxy: pass

    @cprop()
    def teams(self) -> Proxy: pass

    @cprop()
    def team_map(self) -> Proxy: pass

    @cprop()
    def control_state(self) -> Proxy: pass

    @cprop()
    def set_control_state(self) -> Callable[[str, bool], None]:
        """
        Returns Function(state: str, toggle: bool)
        """

    @cprop()
    def clear_control_states(self) -> Callable[[], None]:
        """
        Returns Function()
        """
        
    def __load_plugins(self):
        self.mc_data = require('minecraft-data')(self.bot.version)
        self.__pathfinder = require('mineflayer-pathfinder').pathfinder
        self.movements = require('mineflayer-pathfinder').Movements
        self.goals = require('mineflayer-pathfinder').goals
        
        self.bot.loadPlugin(self.__pathfinder)
        self.pathfinder = self.bot.pathfinder
        self.bot.loadPlugin(require('mineflayer-collectblock').plugin)
        self.movements = self.movements(self.bot, self.mc_data)
        self.bot.pathfinder.setMovements(self.movements)
    
    def __setup_events(self):
        @self.once("login")
        def on_login(*_):
            self.logged_in = True
            self.log(f"Connected to {self.local_host}", info=True)
            self.log(f'Logged in as {self.bot.username}', info=True)
            if not self.disable_viewer:
                self.__start_viewer()
            

        @self.on("path_update")
        def path_update(_, r):
            if not self.disable_viewer:
                path = [self.bot.entity.position.offset(0, 0.5, 0)]
                for node in r['path']:
                    path.append({'x': node['x'], 'y': node['y'] + 0.5, 'z': node['z']})
                self.bot.viewer.drawLine('path', path, 	0x0000FF)

        @self.on("death")
        def death(*_):
            self.log("Bot died" + ". Stopping bot!" * int(self.stop_bot_on_death), warning=True)
            if self.stop_bot_on_death:
                self.stop()
                quit()

        @self.on("kick")
        def kicked(_, reason, *__):
            self.log("Kicked from server" + ". Stopping bot!" * int(self.stop_bot_on_death) + f"\n\nReason: {reason}",
                     warning=True)
            if self.stop_bot_on_death:
                self.stop()
                quit()

        @self.on("error")
        def error(_, error):
            self.log(error, error=True)
            if error == "Authentication failed, timed out":
                self.stop()
                quit()

        @self.on("chat")
        def handleMsg(_, sender: str, message: str, *args):
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
                self.log(f"{sender}: {message}", icon="💬", chat=True)

            if message.startswith(self.custom_command_prefix):
                command = message.removeprefix(self.custom_command_prefix)
                commanded = self.custom_commands.get(command, None)
                if commanded:
                    if sender == commanded["sender"]:
                        cmd, *params = command.split()
                        commanded["callback"](CommandContext(
                            sender, cmd, command, params, time.time(), args[1], self
                        ))

    def __start_viewer(self):
        try:
            self.mineflayer_viewer.mineflayer(self.bot, {"port": self.viewer_port})
            # _ = require("node-canvas-webgl")
            # @self.once("spawn")
            # def ___start_viewer(*args):
            #     self.mineflayer_viewer.headless(self.bot, { "output": f"127.0.0.1:{self.viewer_port}", "frames": 200, "width": 512, "height": 512 })
            self.log(f"Viewer started on port {self.viewer_port}", info=True)
        except Exception as e:
            print(e)
            self.log("There was an error while starting the viewer!", warning=True)
            
    
    def chat(self, *message):
        """
        Send a message in the chat
        """
        self.bot.chat(' '.join(message))
        
    def whisper(self, username, *message):
        """
        Send a whisper to a user with a message
        """
        self.bot.whisper(username, ' '.join(message))

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


    def chat_history(self, username: str, server="") -> list:
        """
        Get all the chat history from a player in the database
        """
        if not self.enable_chat_logging:
            self.log(f"Chat logging is not enabled, set enableChatLogging=True in the bot config", warning=True)
            return []
        if server == "":
            server = self.local_host
        if os.path.exists(f"{server}".lower().replace(".", "") + "Database.json"):
            server_history = TinyDB(f"{server}".lower().replace(".", "") + "Database.json")
            user = server_history.get(User.username == username)
            if user:
                return user['messages']
            else:
                self.log(f"{username} has no chat history", warning=True)
        else:
            self.log(f"{server} has no database", warning=True)
            return []
        
    def clear_logs(self):
        """
        Clear all the chat logs from the database
        """
        if not self.enable_chat_logging:
            self.log(f"Chat logging is not enabled, set enableChatLogging=True in the bot config", warning=True)
            return
        self.chat_database.truncate()
        self.log("All databases are cleared!")
    
    def stop(self):
        """
        Stop the bot and all running code
        """
    
        self.bot.end()
        if not self.disable_viewer:
            self.bot.viewer.close()
        self.log("Ended bot!", warning=True)
        return
        
    def server_data(self, server:str=None) -> dict:
        """
        Get all the data from a server.
        if no server is provided the current server will be used
        """
        if server is None:
            server = self.local_host
        data = requests.get(f"https://api.mcstatus.io/v2/status/java/{server}").json()
        return data

    def set_data(self, item, value):
        """
        Sets custom data that can be later accessed. Also returns data.

        ```python
        bot.set_data("hello", "world")
        ... # some time consuming task later
        print(bot.get_data("hello")) # should print "world"
        ```
        """
        self.extra_data[item] = value
        return value

    def get_data(self, item, default: object = None, compare: object = "nothing to compare to"):
        """
        Gets custom data that is set prior. Also take in an optional compare parameter to do assertion with the obtained data.
        Default parameter for 'default' is None

        ```python
        # other code
        try:
            print(bot.get_data("custom_health", 200))
        except AssertionError:
            print("Bot is not at full health!")
        ```
        """
        result = self.extra_data.get(item, default)
        if not compare == "nothing to compare to": # there's a comparison
            if result != compare:
                raise AssertionError(
                    f"Incorrect value in custom data! Queried {repr(item)}={repr(result)}, instead expected {repr(item)}={repr(compare)}"
                )
        return result

    def set_prefix(self, new_prefix="!"):
        """
        Sets the bot's command prefix. This should not be empty as it will speed up responding to chat
        """
        self.custom_command_prefix = new_prefix

    def register_command(self, command_name: str, sender = None, returns: str | Callable[[CommandContext], None] = None, whisper: bool = True):
            """
            Registers a custom command that the bot listens to.

            Args:
                command_name (str): The name of the command to register.
                sender (Optional[str]): The sender of the command. If set, the bot will only respond if the senders match.
                returns (Optional[Union[str, Callable[[CommandContext], None]]]): The return value or callback function for the command.
                    - If a string is provided, the bot will respond with that string.
                    - If a callable function is provided, the bot will execute that function.
                whisper (bool): Indicates whether the bot should respond with a whisper. Default is True.

            Returns:
                None

            Examples:
                You can register a command with a return value using the following syntax:

                ```python
                bot.register_command("hello", returns="Hello there!")
                ```

                You can register a command with a callback function using the following syntax:

                ```python
                @bot.register_command("time")
                def get_time(ctx):
                    current_time = datetime.datetime.now()
                    ctx.respond(f"It is now {current_time}", whisper=True)
                ```

                Alternatively, you can use the `register_command` method as a decorator.

            Raises:
                TypeError: If the callback parameter is of an unsupported type.

            """
            command_sender = sender
            if isinstance(returns, str):
                self.custom_commands[command_name] = {
                    "sender": command_sender,
                    "callback": lambda ctx: ctx.respond(returns, whisper=whisper, whisper_to=command_sender)
                }
            elif callable(returns):
                self.custom_commands[command_name] = {
                    "sender": command_sender,
                    "callback": returns
                }
            elif returns is None:
                def inner(func):
                    def wrapper(ctx):
                        func(ctx)

                    wrapper.__name__ = func.__name__
                    wrapper.__doc__ = func.__doc__
                    wrapper.__dict__ = func.__dict__

                    self.custom_commands[command_name] = {
                        "sender": command_sender,
                        "callback": func
                    }
                    return wrapper
                return inner
            else:
                raise TypeError(
                    f"Cannot add custom command with callback of type {returns.__class__.__name__}!"
                )
            
    def collect_block(self, block:str, amount:int=1, max_distance:int=64):
        """
        Collect a block by name.

        Args:
            block (str): The name of the block to collect.
            amount (int, optional): The number of blocks to collect. Defaults to 1.
            max_distance (int, optional): The maximum distance to search for the block. Defaults to 64.

        Returns:
            None

        Raises:
            None

        Example:
            bot.collect_block("oak_log", amount=20)
        """
        # Get the correct block type
        self.collected = 0
        def collect():
            try:
                self.collected = 0 
                blockType = self.bot.registry.blocksByName[block]
                if not blockType:
                    return
                blocks = self.bot.findBlocks({
                    'matching': blockType.id,
                    'maxDistance': 64,
                    'count': amount
                })
                if len(blocks.valueOf()) == 0:
                    self.chat("I don't see that block nearby.")
                    return
                targets = []
                for i in range(min(len(blocks.valueOf()), amount)):
                    targets.append(self.bot.blockAt(blocks[i]))
                self.chat(f"Found {len(targets)}")
                try:
                    self.bot.collectBlock.collect(targets, timeout=10000)
                    # All blocks have been collected.
                    self.chat('Done')
                except Exception as err:
                    # An error occurred, report it.
                    print(err)
            except Exception as err:
                print(err)
        task = threading.Thread(target=collect)
        task.start()
        task.join()
        
        
    
    def goto(self, x: int, y: int, z: int, timeout: int = 600000000):
        """
        Go to the specified coordinates (x, y, z).

        Args:
            x (int): The x-coordinate.
            z (int): The z-coordinate.
            y (int, optional): The y-coordinate. Defaults to 0.
            timeout (int, optional): The timeout in milliseconds. Defaults to 600000000.

        Returns:
            None

        Examples:
            To move to the coordinates (10, 0, 20) with a timeout of 10 seconds:
            >>> bot.goto(10, 20, timeout=10000)
        """
        # Get the correct block type
        with self.console.status(f"[bold]Moving to ({x}, {y}, {z})...") as status:
            if y == None:
                self.bot.pathfinder.goto(self.goals.GoalNearXZ(int(x), int(z), 1), timeout=timeout)
            else:
                self.bot.pathfinder.goto(self.goals.GoalNear(int(x), int(y), int(z), 1), timeout=timeout)
            return
        
    def placeBlockWithOptions(self, referenceBlock, faceVector, options):
        dest = referenceBlock.position.plus(faceVector)
        oldBlock = self.bot.blockAt(dest)
        self.bot._genericPlace(referenceBlock, faceVector, options)
        newBlock = self.bot.blockAt(dest)
        if oldBlock.type == newBlock.type:
            @On(self.bot.world, f"blockUpdate:{dest}")
            def block_update(oldBlock, newBlock):
                print(newBlock)
                print(oldBlock)
                if not oldBlock or not newBlock or oldBlock.type != newBlock.type:
                    return
                else: 
                    raise Exception(f"No block has been placed: the block is still {oldBlock.name}")
        if not oldBlock and not newBlock:
            return
        if oldBlock and oldBlock.type == newBlock.type:
            raise Exception(f"No block has been placed: the block is still {oldBlock.name}")
        else:
            self.emit("blockPlaced", oldBlock, newBlock)

    def placeBlock(self, referenceBlock, faceVector, no_checks=False):
        if no_checks:
            try:
                dest = referenceBlock.position.plus(faceVector)
                # self.bot.lookAt(referenceBlock)
                oldBlock = self.bot.blockAt(dest)
                self.bot._genericPlace(referenceBlock, faceVector, { "swingArm": "right" })
                # self.bot.waitForTicks(ticks)
                
                newBlock = self.bot.blockAt(dest)
                self.emit("blockPlaced", oldBlock, newBlock)
                return True
            except:
                return False
        else:
            self.placeBlockWithOptions(referenceBlock, faceVector, { "swingArm": "right" })
            
    
            

createBot = Bot
