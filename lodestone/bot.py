from javascript import require, On, once
import datetime
import asyncio
import math
import json
import csv
import structlog
import os
import sys
import time
import fnmatch
import re
from datetime import date
from pathlib import Path
from tinydb import TinyDB, Query
import subprocess
from rich.console import Console
import functools
User = Query()
filestruc = "/"

if os.name == 'nt':
    filestruc = "\\"
else:
    filestruc = "/"




class createBot:
    def __init__(self, 
host:str,
auth:str="microsoft",
port:int=25565,
version:str="false",
password:str="",
checkTimeoutInterval:int=20,
armorManager:bool=False,
viewerPort:int=5001,
quit_on_low_health:bool=True,
low_health_threshold:int=10,
disableChatSigning:bool=False,
profilesFolder:str="",
username:str="MineflayerPy",
useReturn:bool = False,
discordWebhook:str = None,
useDiscordForms:bool = False,
apiMode:bool = False,
clientToken = None,
accessToken = None,
logErrors:bool = True,
hideErrors:bool = True,
keepAlive:bool = True,
loadInternalPlugins:bool = True,
respawn:bool = True,
physicsEnabled:bool = True,
defaultChatPatterns:bool = True,
disableLogs:bool = False
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
        
        
        
        
        
        global logger
        self.logger = structlog.get_logger()
        logger = self.logger
        self.console = Console()
        # [:2]
        self.apiMode = apiMode
        self.nodeVersion, self.pipVersion, self.pythonVersion = self.__versionsCheck()
        if discordWebhook != None:
            from discord import SyncWebhook
            from discord import Embed
            self.Embed = Embed
            self.useDiscordForms = useDiscordForms
            self.webhook = SyncWebhook.from_url(f"{discordWebhook}")
            embedVar = Embed(title="Sucsesfully Connected To The Webhook!", description=f"**Great news! The bot has successfully connected to this channel's webhook. From now on, it will send all the logs and valuable data right here, keeping you informed about everything happening on the server.**\n\n **Versions:**\n* [**Node**](https://nodejs.org/)**:      {self.nodeVersion[:2]}**\n* [**Pip**](https://pypi.org/project/pip/)**:          {self.pipVersion}**\n* [**Python**](https://www.python.org/)**:  {self.pythonVersion}**\n\n **Links:**\n* [**GitHub**](https://github.com/SilkePilon/OpenDeliveryBot)\n* [**Report Bugs**](https://github.com/SilkePilon/OpenDeliveryBot/issues)\n* [**Web Interface**](https://github.com/SilkePilon/OpenDeliveryBot-react)", color=0x3498db)
            embedVar.timestamp = datetime.datetime.utcnow()
            embedVar.set_footer(text='\u200b',icon_url="https://github.com/SilkePilon/OpenDeliveryBot/blob/main/chestlogo.png?raw=true")
            if useDiscordForms == True:
                today = date.today()
                self.webhook.send(content=f"{today}", thread_name=f"{today}", username="OpenDeliveryBot", avatar_url="https://github.com/SilkePilon/OpenDeliveryBot/blob/main/chestlogo.png?raw=true", embed=embedVar)
            else:
                try:
                    self.webhook.send(content="", username="OpenDeliveryBot", avatar_url="https://github.com/SilkePilon/OpenDeliveryBot/blob/main/chestlogo.png?raw=true", embed=embedVar)
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
        self.chatDatabase = TinyDB(f"{self.servername}Database.json")
        self.script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.bot = self.__create_bot()
        self.msa_data = False
        
        
        
    
    def __checkPythonCommand(self):
        try:
            subprocess.check_output(['python', '--version'])
            return 'python'
        except:
            try:
                subprocess.check_output(['python3', '--version']) 
                return 'python3'
            except:
                self.__loging(message='Python command not found, make sure python is installed!', error=True, discord=False)
                sys.exit(1)

    
    
        
    def __loging(self, message, icon="🤖", error=False, info=False, warning=False, chat=False, imageUrl:str="", console:bool= True, discord:bool=True):
        if self.disableLogs == False:
            if self.useReturn == True:
                self.logger.info(f"{message}")
            elif self.discordWebhook != None and discord == True:
                color = 0x3498db
                if error == True:
                    color = 0x992d22
                elif info == True:
                    color = 0x3498db
                elif warning == True:
                    color = 0xe67e22
                elif chat == True:
                    color = 0x2ecc71
                embed = self.Embed(title="", description=f"**{message}**", color=color)
                embed.timestamp = datetime.datetime.utcnow()
                if imageUrl != "":
                    embed.set_thumbnail(url=imageUrl)
                try:
                    embed.set_footer(text=f'{self.bot.username}',icon_url=f"https://mc-heads.net/avatar/{self.bot.username}/600.png")
                except:
                    embed.set_footer(text='\u200b',icon_url="https://github.com/SilkePilon/OpenDeliveryBot/blob/main/chestlogo.png?raw=true")
                if self.useDiscordForms == True:
                    today = date.today()
                    self.webhook.send(content=f"{today}", thread=f"{today}", username="OpenDeliveryBot", avatar_url="https://github.com/SilkePilon/OpenDeliveryBot/blob/main/chestlogo.png?raw=true", embed=embed)
                else:
                    try:
                        self.webhook.send(content=f"", username="OpenDeliveryBot", avatar_url="https://github.com/SilkePilon/OpenDeliveryBot/blob/main/chestlogo.png?raw=true", embed=embed)
                    except:
                        self.logger.error(f"Detected that you are using a Forms channel but 'useDiscordForms' is set to False. Please change 'useDiscordForms' to True or provide a webhook url for a text channel.")
            if console == True:
                if error == True:
                    self.logger.error(f"{message}")
                elif info == True:
                    self.logger.info(f"{message}")
                elif warning == True:
                    self.logger.warning(f"{message}")
                elif chat == True:
                    self.logger.info(f"{message}")
                else:
                    self.logger.info(f"{message}")
        
    
    def __findFiles(self, base, pattern):
        '''Return list of files matching pattern in base folder.'''
        return [n for n in fnmatch.filter(os.listdir(base), pattern) if
            os.path.isfile(os.path.join(base, n))]
        
    def __waitForMsa(self, code):
        if os.name == 'nt':
            basePath = os.getenv('APPDATA')
        else:
            basePath = Path().home()
        
        
        while True:
            time.sleep(1)
            msa_file = Path(f"{basePath}/.minecraft/nmp-cache/")
            msa_file = f"{msa_file}/{self.__findFiles(msa_file, '*_mca-cache.json')[0]}"
            with open(msa_file, "r") as check:
                # not optimized!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                if check.read() != "{}":
                    self.logger.info("Logged in successfully!")
                    return
        
    
            
    def __msa(self, *msa):
        with self.console.status("[bold green]Waiting for login...\n") as status:
            self.msa_data = msa[0]
            self.msa_status = True
            self.__loging(message=f"It seems you are not logged in! Open your termianl for more information.", error=True, console=False)
            self.logger.error(f"It seems you are not logged in, please go to https://microsoft.com/link and enter the following code: {self.msa_data['user_code']}")
            self.__waitForMsa(code=self.msa_data['user_code'])
            if self.apiMode == True:
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
                if self.disableLogs == False:
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
            if self.disableLogs == False:
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
            'hideErrors': self.hideErrors,
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
            self.__loging(f"Connecting to {self.host}", info=True, imageUrl=f"https://eu.mc-api.net/v3/server/favicon/{self.host}")
            self.__loging(f'Logged in as {self.bot.username}', info=True, imageUrl=f"https://mc-heads.net/avatar/{self.bot.username}/600.png")
            self.__start_viewer()
            self.__setup_events()
            self.__loging(f'Cordinates: {int(self.bot.entity.position.x)}, {int(self.bot.entity.position.y)}, {int(self.bot.entity.position.z)}', info=True)
            self.__load_plugins()
        return localBot
    
    
    
    

    def start(self):
        while self.logedin == False:
            time.sleep(1) 
        # @On(self.bot, "login")
        # def on_login(*args):
        
        # r = self.repl.start('> ')
        # r.context.bot = self.bot
        # self.__auto_totem()
        self.__equip_armor()
        self.__log_players()
        self.registry = self.bot.registry
        self.world = self.bot.world
        self.entity = self.bot.entity
        self.entities = self.bot.entities
        self.username = self.bot.username 
        self.spawnPoint = self.bot.spawnPoint
        self.heldItem = self.bot.heldItem
        self.usingHeldItem = self.bot.usingHeldItem

        self.game_levelType = self.bot.game.levelType
        self.game_dimension = self.bot.game.dimension
        self.game_difficulty = self.bot.game.difficulty
        self.game_gameMode = self.bot.game.gameMode
        self.game_hardcore = self.bot.game.hardcore
        self.game_maxPlayers = self.bot.game.maxPlayers
        self.game_serverBrand = self.bot.game.serverBrand
        self.game_minY = self.bot.game.minY
        self.game_height = self.bot.game.height

        self.physicsEnabled = self.bot.physicsEnabled
        
        self.player = self.bot.player
        self.players = self.bot.players
        self.tablist = self.bot.tablist

        self.isRaining = self.bot.isRaining
        self.rainState = self.bot.rainState
        self.thunderState = self.bot.thunderState

        self.chatPatterns = self.bot.chatPatterns
        
        self.settings_chat = self.bot.settings.chat
        self.settings_colorsEnabled = self.bot.settings.colorsEnabled
        self.settings_viewDistance = self.bot.settings.viewDistance
        self.settings_difficulty = self.bot.settings.difficulty
        self.settings_skinParts = self.bot.settings.skinParts
        self.settings_enableTextFiltering = self.bot.settings.enableTextFiltering
        self.settings_enableServerListing = self.bot.settings.enableServerListing

        self.experience_level = self.bot.experience.level
        self.experience_points = self.bot.experience.points
        self.experience_progress = self.bot.experience.progress

        self.health = self.bot.health
        self.food = self.bot.food
        self.foodSaturation = self.bot.foodSaturation
        self.oxygenLevel = self.bot.oxygenLevel
        
        self.physics = self.bot.physics
        self.fireworkRocketDuration = self.bot.fireworkRocketDuration

        self.time_doDaylightCycle = self.bot.time.doDaylightCycle
        self.time_bigTime = self.bot.time.bigTime
        self.time_time = self.bot.time.time
        self.time_timeOfDay = self.bot.time.timeOfDay
        self.time_day = self.bot.time.day
        self.time_isDay = self.bot.time.isDay
        self.time_moonPhase = self.bot.time.moonPhase
        self.time_bigAge = self.bot.time.bigAge
        self.time_age = self.bot.time.age

        self.quickBarSlot = self.bot.quickBarSlot
        self.inventory = self.bot.inventory
        self.targetDigBlock = self.bot.targetDigBlock
        self.isSleeping = self.bot.isSleeping

        self.scoreboards = self.bot.scoreboards
        self.scoreboard = self.bot.scoreboard
        self.teams = self.bot.teams
        self.teamMap = self.bot.teamMap

        self.controlState = self.bot.controlState
        
    
        
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
                self.__loging(f"Cant get to goal", error=True)
        
        
        
        @On(self.bot, "death")
        def death(*args):
            self.bot.end()
            self.__loging("Bot died... stopping bot!", warning=True)
        @On(self.bot, "kicked")
        def kicked(this, reason, *a):
            self.bot.end()
            self.__loging("Kicked from server... stopping bot!", warning=True)
        @On(self.bot, "autoeat_started")
        def autoeat_started(item, offhand, *a):
            self.__loging(f"Eating {item['name']} in {'offhand' if offhand else 'hand'}", info=True)
        @On(self.bot, "autoeat_finished")
        def autoeat_finished(item, offhand):
            self.__loging(f"Finished eating {item['name']} in {'offhand' if offhand else 'hand'}", info=True) 
        @On(self.bot, "error")
        def error(_, error):
            self.__loging(error, error=True)
        @On(self.bot, "end")
        def create_new_bot(*a):
            self.bot = self.__create_bot()
        @On(self.bot, 'chat')
        def handleMsg(this, sender, message, *args):
            if not sender:
                sender = "unknown"
            if not self.chatDatabase.contains(User.username == sender):
                self.chatDatabase.insert({'username': sender, 'messages': [message]}) 
            else:
                user = self.chatDatabase.get(User.username == sender)
                existing_messages = user['messages']
                existing_messages.extend([f"{message}"])
                self.chatDatabase.update({'messages': existing_messages}, User.username == sender)
            self.__loging(f"💬 {sender}: {message}", chat=True)
            

    def __equip_armor(self):
        try:
            self.bot.armorManager.equipAll()
        except:
            return

    def __start_viewer(self):
        self.mineflayerViewer(self.bot, {"port": self.viewer_port})
        self.__loging("Viewer started on port %s" % self.viewer_port, info=True)
    
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
    
    def chat(self, message:str):
        self.bot.chat(message)
        
    
    
    def coordinates(self):
        if self.logedin == True:
            return f"{int(self.bot.entity.position.x)}, {int(self.bot.entity.position.y)}, {int(self.bot.entity.position.z)}"
        
    def chatHistory(self, username:str, server:str=""):
        if server == "":
            server = self.host
        if os.path.exists(f"{server}".lower().replace(".", "") + "Database.json"):
            serverHistory = TinyDB(f"{server}".lower().replace(".", "") + "Database.json")
            user = serverHistory.get(User.username == username)
            if user:
                return user['messages']
            else:
                self.__loging(f"{username} has no chat history", warning=True)
        else:
            self.__loging(f"{server} has no database", warning=True)
            return []
        
    def clearLogs(self):
        self.chatDatabase.truncate()
        self.__loging("All databases are cleared!")
    
    def stop(self):
        self.bot.end()
        self.__loging("Stopped bot!", warning=True)
        
        
        