#!/usr/bin/python
# -*- coding: utf-8 -*-
from javascript import require, On
import time
from datetime import datetime
mineflayer = require('mineflayer')
pathfinder = require('mineflayer-pathfinder')
goals = require('mineflayer-pathfinder').goals
mineflayerViewer = require('prismarine-viewer').mineflayer
inventoryViewer = require('mineflayer-web-inventory')
elytrafly = require("mineflayer-elytrafly-commonjs")
Vec3 = require("vec3").Vec3
import matplotlib.pyplot as plt


RANGE_GOAL = -1
CLIENT_USERNAME = "Douwestrijder01"
HOST = "2b2t.org"

bot = mineflayer.createBot({
    'host': HOST,
    'port': 25565,
    'username': 'silke2007minecraft@gmail.com',
    'password': 'Landrover01',
    'auth': 'microsoft',
    'hideErrors': True,
    'version': False,
    'checkTimeoutInterval': 60 * 100000
    })

bot.loadPlugin(pathfinder.pathfinder)
bot.loadPlugin(elytrafly.elytrafly)
print('Started mineflayer')


    


@On(bot, 'login')
def handle(*args):
    print(f'joined {HOST}')
    print(bot.entity.position)
    mineflayerViewer(bot, { "port": 80 })
    inventoryViewer(bot)
    mcData = require('minecraft-data')(bot.version)
    movements = pathfinder.Movements(bot, mcData)
    print(bot.players)
    #If you want to Deactivate sth
    movements.canDig = False

    bot.pathfinder.setMovements(movements)
    # bot.elytrafly.elytraFlyTo(Vec3(bot.entity.position.x + 100, 0, bot.entity.position.z))
    
    def LookForChest(range, items):
        foundChest = False

        while not foundChest:
            
                chestToOpen = bot.findBlock({
                    'matching': [mcData.blocksByName[name].id for name in ['chest']],
                    'maxDistance': range
                })
                
                if not chestToOpen and foundChest == False:
                    bot.chat('no chest found')
                    continue
                if chestToOpen.position.x:
                    x = chestToOpen.position.x
                    y = chestToOpen.position.y
                    z = chestToOpen.position.z

                    bot.chat(f'/tell {CLIENT_USERNAME} [OPEN DELIVERY BOT] Found a nearby chest to deliver: [{str(x)}, {str(y)}, {str(z)}]')
                    locaton = bot.pathfinder.goto(pathfinder.goals.GoalNear(x, y, z, 1), timeout=60)
                    
                    try:
                        chest = bot.openContainer(chestToOpen)
                    except Exception:
                        
                        bot.chat(f'/tell {CLIENT_USERNAME} [OPEN DELIVERY BOT] Please place a new chest in my location.')
                        continue
                        
                    print(chest.containerItems())
                    time.sleep(10)
                    chest.close()
                    bot.chat(f'/tell {CLIENT_USERNAME} [OPEN DELIVERY BOT] Items have been successfully delivered at: [{str(x)}, {str(y)}, {str(z)}] on [{datetime.now()}]')
                    foundChest = True
                    break

            # except Exception as e:
            #     print("no chests found!", e)
            #     pass
            
            
            
    
    while True:
        distance = input("range: ")
        LookForChest(distance, "")
    

@On(bot, 'end')
def handle(*args):
    print('Bot ended!', args)
