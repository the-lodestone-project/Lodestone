#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import necessary modules
from javascript import require, On  
import time
import json
from datetime import datetime
import matplotlib.pyplot as plt

# Initialize mineflayer bot and plugins
mineflayer = require('mineflayer')
pathfinder = require('mineflayer-pathfinder')
goals = require('mineflayer-pathfinder').goals
mineflayerViewer = require('prismarine-viewer').mineflayer
inventoryViewer = require('mineflayer-web-inventory')
elytrafly = require("mineflayer-elytrafly-commonjs")
Vec3 = require("vec3").Vec3


# Load bot config from JSON file
with open('config.json', 'r') as f:
    config = json.load(f)

# Constants
RANGE_GOAL = -1  
CLIENT_USERNAME = config['ClientUsername']


# Create version
if config['Version'] == "auto":
  version = False
else:
  version = config['Version']

# Create bot instance 
bot = mineflayer.createBot({
  'host': config['Host'],
  'port': config['Port'],
  'username': config['Username'],
  'password': config['Password'],
  'auth': config['Auth'],
  'hideErrors': True,
  'version': version,
  'checkTimeoutInterval': config['CheckTimeoutInterval'],
})

# Load plugins
bot.loadPlugin(pathfinder.pathfinder) 
bot.loadPlugin(elytrafly.elytrafly)
print('Started mineflayer')
  
# Login handler  
@On(bot, 'login')
def handle_login(*args):
  print(f'joined {config["Host"]}:{config["Port"]}')
  print(bot.entity.position)
  mineflayerViewer(bot, { "port": config['ViewerPort'] })
  inventoryViewer(bot)
  global mcData
  mcData = require('minecraft-data')(bot.version)
  movements = pathfinder.Movements(bot, mcData)
  
  with open("playes.log", "w") as x:
    x.write(str(bot.players))
  
  with open("cords.log", "a") as x:
    x.write(f"{datetime.now()}  |  {config['Host']}:{config['Port']}  |  X:{str(bot.entity.position.x)}, Y:{str(bot.entity.position.y)}, Z:{str(bot.entity.position.z)}")
  
  # Disable digging if needed
  movements.canDig = False

  bot.pathfinder.setMovements(movements)
  
  # Main login logic
  # LookForChest("")   

# Function to find and open chest  
def LookForChest(items):

  foundChest = False
  
  while not foundChest:
      
    # Find nearby chest
    chestToOpen = bot.findBlock({
        'matching': [mcData.blocksByName[name].id for name in ['chest']], 
        'maxDistance': config['ChestRage'],
    })
    
    if not chestToOpen and foundChest == False:
      bot.chat('no chest found')
      continue
      
    # Go to chest location  
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
      
# Handler for bot end  
@On(bot, 'end')
def handle_end(*args):
  print('Bot ended!', args)
