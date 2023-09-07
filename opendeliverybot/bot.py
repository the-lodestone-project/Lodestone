# import streamlit as st
from javascript import require, On
import datetime
import asyncio
import math
import json
import csv
import structlog
import os
import sys


global api_bot

filestruc = "/"

if os.name == 'nt':
    filestruc = "\\"
else:
    filestruc = "/"




class MinecraftBot:
    
    def __init__(self, config: dict, streamlit = False, useReturn = False):
        """Main bot run loop"""
        self.st = streamlit
        self.mineflayer = require('mineflayer')
        self.pathfinder = require('mineflayer-pathfinder')
        self.goals = require('mineflayer-pathfinder').goals
        self.mineflayerViewer = require('prismarine-viewer').mineflayer
        self.Vec3 = require("vec3").Vec3
        self.armorManager = require("mineflayer-armor-manager")
        self.autoeat = require('mineflayer-auto-eat').plugin
        self.repl = require('repl')
        self.config = config
        self.logedin = False
        self.useReturn = useReturn
        self.logger = structlog.get_logger()
        self.script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.bot = self.__create_bot()
        api_bot = self.bot
        
    def __steamlit(self, message, icon="🤖"):
        if self.useReturn == True:
            self.logger.info(f"{message}")
        elif self.st != False:
            self.st.toast(f"{message}", icon=icon)
        else:
            self.logger.info(f"{message}")
    
    def __steamlit_error(self, err, **kwargs):
        if self.st != False:
            self.st.toast(f"{err}", icon="🚨")
        else:
            self.logger.info(f"{err}")

    def __create_bot(self):
        self.__steamlit(f"Joined {self.config['server_ip']}")
        if self.config['version'] == "auto":
            self.version = False
        else:
            self.version = str(self.config['version'])
        return self.mineflayer.createBot({
            'host': self.config['server_ip'],
            'port': self.config['server_port'],
            'username': self.config['bot_name'],
            'password': self.config['password'],
            'auth': self.config['auth'],
            'version': self.version,
            'hideErrors': True,
        })
        
        
    

    def start(self):
        @On(self.bot, "login")
        def on_login(*args):
            # r = self.repl.start('> ')
            # r.context.bot = self.bot
            self.logedin = True
            self.__start_viewer()
            self.__setup_events()
            self.__steamlit(f'Cordinates: {self.bot.entity.position.x}, {self.bot.entity.position.y}, {self.bot.entity.position.z}')
            self.__load_plugins()
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
        self.bot.loadPlugin(self.tpsPlugin)
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
                self.__steamlit(f"Cant get to goal")
        
        
        
        @On(self.bot, "death")
        def death(*args):
            self.bot.end()
            
            self.__steamlit("Bot died... stopping bot!")
        
        @On(self.bot, "kicked")
        def kicked(this, reason, *a):
            self.bot.end()
            
            self.__steamlit("Kicked from server... stopping bot!")
            
        @On(self.bot, "autoeat_started")
        def autoeat_started(item, offhand, *a):
            self.__steamlit(f"Eating {item['name']} in {'offhand' if offhand else 'hand'}")
            
        @On(self.bot, "autoeat_finished")
        def autoeat_finished(item, offhand):
            self.__steamlit(f"Finished eating {item['name']} in {'offhand' if offhand else 'hand'}")
            
        @On(self.bot, "error")
        def error(_, error):
            self.__steamlit_error(error)
        
        @On(self.bot, "end")
        def create_new_bot(*a):
            self.bot = self.__create_bot()
            
        @On(self.bot, 'chat')
        def handleMsg(this, sender, message, *args):
            if sender and (sender != self.bot.username):
                self.__steamlit(f"{sender}: {message}", icon="💬")
            

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
        self.__steamlit("Viewer started on port %s" % self.config['viewer_port'])
    
    def __log_players(self):
        with open(f"{self.script_directory}{filestruc}logs{filestruc}players.log", "w+") as x:
            x.write(f'{str(self.bot.players)}\n')
            
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

        with open(f'{self.script_directory}{filestruc}logs{filestruc}analytics.csv', 'a+', newline='') as file:
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
                self.__steamlit("No delivery chest found")
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
        
        
    def inventory(self):
        inv = []
        if self.bot and self.bot.inventory:
            for item in self.bot.inventory.items():
                inv.append(item.displayName)
        return inv
        
    
    
    def coordinates(self):
        if self.logedin == True:
            return f"{self.bot.entity.position.x}, {self.bot.entity.position.y}, {self.bot.entity.position.z}"
    
    def stop(self):
        self.bot.end()
        self.__steamlit("Stopped bot!")
        