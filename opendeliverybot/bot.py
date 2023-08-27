import streamlit as st
from javascript import require, On
import datetime
import asyncio
import math
import json
import csv
    
def makeBot(x_coord, y_coord, z_coord, data):
    mineflayer = require('mineflayer')
    pathfinder = require('mineflayer-pathfinder')
    goals = require('mineflayer-pathfinder').goals
    mineflayerViewer = require('prismarine-viewer').mineflayer
    Vec3 = require("vec3").Vec3
    windows = require('prismarine-windows')(data["version"])
    Item = require('prismarine-item')(data["version"])
    armorManager = require("mineflayer-armor-manager")
    tpsPlugin = require('mineflayer-tps')(mineflayer)
    
    bot = mineflayer.createBot({
        'host': data["server_ip"],
        'port': data["server_port"],
        'username': data["bot_name"],
        'password': data["password"],
        'auth': data["auth"],
        'version': data["version"],
        'checkTimeoutInterval': data["check_timeout_interval"],
    })
    
    def add_values_to_csv(data, bot):
        now = datetime.datetime.now()
        server_info = f"{data['server_ip']}:{data['server_port']}"
        start_x = str(bot.entity.position.x)
        start_y = str(bot.entity.position.y)
        start_z = str(bot.entity.position.z)
        
        delivered_item = data["items_name"]

        distance = math.sqrt((x_coord - start_x)**2 + (z_coord - start_z)**2)

        row = [now, server_info, start_x, start_y, start_z, x_coord, y_coord, z_coord, distance, delivered_item]

        with open('logs\\analytics.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)
    
    def logPlayers(bot):
        with open("logs\players.log", "w") as x:
            x.write(f'{str(bot.players)}\n')
        
    bot.loadPlugin(pathfinder.pathfinder)
    bot.loadPlugin(armorManager)
    
    @On(bot, 'login')
    def handle_login(*args):
        mineflayerViewer(bot, { "firstPerson": True, "port": data["viewer_port"] })
        global mcData
        mcData = require('minecraft-data')(bot.version)
        movements = pathfinder.Movements(bot, mcData)
        
        try:
            bot.armorManager.equipAll()
        except Exception as e:
            print(e)
        
        logPlayers(bot)

        movements.canDig = False
        
        bot.pathfinder.setMovements(movements)
        
        @On(bot, "death")
        def death(this):
            bot.end()
            bot.viewer.close()
            st.toast("Bot died... stopping bot!")
        
        @On(bot, "kicked")
        def kicked(this, reason, *a):
            bot.end()
            bot.viewer.close()
            st.toast("Kicked from server... stopping bot!")
                
        def itemByName(items, name):
            item = None
            for i in range(len(items)):
                item = items[i]
                if item and item['name'] == name:
                    return item
                return None
        
        def GetItems():
            x = data["chest_coords"][0]
            y = data["chest_coords"][1]
            z = data["chest_coords"][2]
            locaton = bot.pathfinder.setGoal(pathfinder.goals.GoalNear(x, y, z, 1), timeout=60)
            
            chestToOpen = bot.findBlock({
                'matching': [mcData.blocksByName[name].id for name in [f'{str(data["chest_type"]).lower()}']],
                'maxDistance': 10,
            })
            
            if chestToOpen:

                chest = bot.openContainer(bot.blockAt(Vec3(-62, 72, 47)))
                
                item = itemByName(chest.containerItems(), data["items_name"])
                
                if item:
                    try:
                        windows.withdraw(item.type, None, data['items_count'])
                    except Exception as err:
                        bot.chat(f"unable to withdraw {data['items_count']} {item.name}")
                else:
                    bot.chat(f"unknown item {data['items_name']}")
                
                asyncio.sleep(5)
                
                chest.close()                
                
            else:
                bot.chat("Can't find the chest")
        
        def GoToLocation():
                x = float(x_coord)
                y = float(x_coord)
                z = float(z_coord)
                locaton =  bot.pathfinder.setGoal(pathfinder.goals.GoalNear(x, y, z, 1), timeout=60)
        
        def DepositItems():

            foundChest = False
            
            while not foundChest:
                
                chestToOpen = bot.findBlock({
                    'matching': [mcData.blocksByName[name].id for name in ['chest']], 
                    'maxDistance': data["chest_range"],
                })
            
                if not chestToOpen and foundChest == False:
                    st.toast("No delivery chest found")
                    break
                    
                if chestToOpen.position.x:
                    x = chestToOpen.position.x
                    y = chestToOpen.position.y  
                    z = chestToOpen.position.z

                    locaton = bot.pathfinder.setGoal(pathfinder.goals.GoalNear(x, y, z, 1), timeout=60)
                    
                    try:
                        chest = bot.openContainer(chestToOpen)
                    except Exception:
                        print(Exception)
                        continue
                    
                    item = next((item for item in chest.slots if item and item.name == f'{data["items_name"]}'), None)
                    windows.deposit(item, "null", "null", "null")
                    
                    chest.close()

                    foundChest = True
                    
                    break
                
            add_values_to_csv(data, bot)
            
        GetItems()
            