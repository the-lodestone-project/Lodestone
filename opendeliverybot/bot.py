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
from tinydb import TinyDB
import subprocess
from rich.console import Console
import functools
playerDatabase = TinyDB("playerDatabase.json")
# new_item = {"name": "Book", "quantity": 5}
# playerDatabase.insert(new_item) 

global api_bot

filestruc = "/"

if os.name == 'nt':
    filestruc = "\\"
else:
    filestruc = "/"




class MinecraftBot:
    def __init__(self, config: dict, useReturn = False, discordWebhook = None, useDiscordForms = False, apiMode = False):
        """Main bot run loop"""
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

            self.logger.info(f'Done!')
        self.config = config
        self.logedin = False
        self.useReturn = useReturn
        self.msa_status = False
    
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
        
        if self.useReturn == True:
            self.logger.info(f"{message}")
        elif self.discordWebhook != None and discord == True:
            color = 0x3498db
            if error == True:
                color = 0x992d22
            if info == True:
                color = 0x3498db
            if warning == True:
                color = 0xe67e22
            if chat == True:
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
            self.logger.info(f"Detected Pip version {pip_version} witch is supported!")
            self.logger.info(f"Detected Python version {python_version} witch is supported!")
            return node_version, pip_version, python_version
        
            
    

    def __create_bot(self):
        if self.config['version'] == "auto":
            self.version = False
        else:
            self.version = str(self.config['version'])
        localBot = self.mineflayer.createBot({
            'host': self.config['server_ip'],
            'port': self.config['server_port'],
            'username': self.config['bot_name'],
            'password': self.config['password'],
            'auth': self.config['auth'],
            'version': self.version,
            'hideErrors': False,
            'onMsaCode': self.__msa
        })
        @On(localBot, "login")
        def on_login(*args):
            self.bot = localBot
            self.logedin = True
            self.__loging(f"Connecting to {self.config['server_ip']}", info=True, imageUrl=f"https://eu.mc-api.net/v3/server/favicon/{self.config['server_ip']}")
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
        
        # self.__get_items()
        # self.__go_to_location()
        # self.__deposit_items()
        
    
        
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
                    return  # only right click
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
            if sender:
                self.__loging(f"💬 {sender}: {message}", chat=True)
            

    def __equip_armor(self):
        self.bot.armorManager.equipAll()
        
        
    # def __auto_totem(self):
    #     totemId = self.bot.registry.itemsByName['totem_of_undying'].id  # Get the correct id
    #     if 'totem_of_undying' in self.bot.registry.itemsByName:
    #         import time

    #         def equip_totem():
    #             totem = self.bot.inventory.find_inventory_item(totemId, None)
    #             if totem:
    #                 self.bot.equip(totem, 'off-hand')

    #         while True:
    #             equip_totem()
    #             time.sleep(0.05)

    def __start_viewer(self):
        self.mineflayerViewer(self.bot, {"port": self.config['viewer_port']})
        self.__loging("Viewer started on port %s" % self.config['viewer_port'], info=True)
    
    def __log_players(self):
        print(type(self.bot.players))
        playerDatabase.insert_multiple(self.bot.players.valueOf())
            
    def __item_By_Name(self, items, name):
            item = None
            for i in range(len(items)):
                item = items[i]
                if item and item['name'] == name:
                    return item
                return None
            
    def __add_values_to_csv(self, data, bot):
        now = datetime.datetime.now()
        server_info = f"{data['server_ip']}:{data['server_port']}"
        start_x = str(bot.entity.position.x)
        start_y = str(bot.entity.position.y)
        start_z = str(bot.entity.position.z)
        
        delivered_item = data["items_name"]

        distance = math.sqrt((self.config['x_coord'] - start_x)**2 + (self.config['z_coord'] - start_z)**2)

        row = [now, server_info, start_x, start_y, start_z, self.config['x_coord'], self.config['y_coord'], self.config['z_coord'], distance, delivered_item]
        os.makedirs(os.path.dirname(f'{self.script_directory}{filestruc}logs{filestruc}analytics.csv'), exist_ok=True)
        with open(f'{self.script_directory}{filestruc}logs{filestruc}analytics.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)

    def __go_to_location(self, x, y, z):
        self.pathfinder.setGoal(
            self.goals.GoalNear(x, y, z, 1),
            timeout=60
        )
    
    def __get_items(self):
        x = self.config["chest_coords"][0]
        y = self.config["chest_coords"][1]
        z = self.config["chest_coords"][2]
        locaton = self.bot.pathfinder.setGoal(self.pathfinder.goals.GoalNear(x, y, z, 1), timeout=60)
        
        chestToOpen = self.bot.findBlock({
            'matching': [self.mcData.blocksByName[name].id for name in [f'{str(self.config["chest_type"]).lower()}']],
            'maxDistance': 10,
        })
        
        if chestToOpen:

            chest = self.bot.openContainer(self.bot.blockAt(self.Vec3(-62, 72, 47)))
            
            item = self.__item_By_Name(chest.containerItems(), self.config["items_name"])
            
            if item:
                try:
                    self.windows.withdraw(item.type, None, self.config['items_count'])
                except Exception as err:
                    self.bot.chat(f"unable to withdraw {self.config['items_count']} {item.name}")
            else:
                self.bot.chat(f"unknown item {self.config['items_name']}")
            
            asyncio.sleep(5)
            
            chest.close()                
            
        else:
            self.bot.chat("Can't find the chest")

    def __deposit_items(self):

        foundChest = False
        
        while not foundChest:
            
            chestToOpen = self.bot.findBlock({
                'matching': [self.mcData.blocksByName[name].id for name in ['chest']], 
                'maxDistance': self.config["chest_range"],
            })
        
            if not chestToOpen and foundChest == False:
                self.__loging("No delivery chest found", error=True)
                break
                
            if chestToOpen.position.x:
                x = chestToOpen.position.x
                y = chestToOpen.position.y  
                z = chestToOpen.position.z

                locaton = self.bot.pathfinder.setGoal(self.pathfinder.goals.GoalNear(x, y, z, 1), timeout=60)
                
                try:
                    chest = self.bot.openContainer(chestToOpen)
                except Exception:
                    print(Exception)
                    continue
                
                item = next((item for item in chest.slots if item and item.name == f'{self.config["items_name"]}'), None)
                self.windows.deposit(item, "null", "null", "null")
                
                chest.close()

                foundChest = True
                
                break
            
        self.__add_values_to_csv(self.config, self.bot)
        
    # Needs to be changed to {"item": item_count}
    def inventory(self):
        inv = []
        if self.bot and self.bot.inventory:
            for item in self.bot.inventory.items():
                inv.append(item.displayName)
        return inv
    
    def chat(self, message:str):
        self.bot.chat(message)
        
    
    
    def coordinates(self):
        if self.logedin == True:
            return f"{int(self.bot.entity.position.x)}, {int(self.bot.entity.position.y)}, {int(self.bot.entity.position.z)}"
        
    def custom_code(self, code:str=""):
        """Run Custom Code on the bot"""
        if self.logedin == True:
            self.__loging("Running custom code on the bot is not reconmended!", warning=True)
            bot = self.bot
            response = eval(code)(bot)
            return response
    
    def stop(self):
        self.bot.end()
        self.__loging("Stopped bot!", warning=True)
        