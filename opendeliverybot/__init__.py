#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import necessary modules
from javascript import require, On  
import time
import contextlib
import io
import sys
import json
import os
from tqdm import tqdm
from datetime import datetime
import matplotlib.pyplot as plt


def clear():
  if os.name == 'nt':
    _ = os.system('cls')
  else:
    _ = os.system('clear')
clear()

@contextlib.contextmanager
def nostdout():
    save_stdout = sys.stdout
    sys.stdout = io.BytesIO()
    yield
    sys.stdout = save_stdout



# Initialize mineflayer bot and plugins
print("installing javascript libaries...")
pbar = tqdm(total=8)
with nostdout():
  mcData = require('minecraft-data')
pbar.update(1)
with nostdout():
  mineflayer = require('mineflayer')
pbar.update(1)
with nostdout():
  pathfinder = require('mineflayer-pathfinder')
pbar.update(1)
with nostdout():
  goals = require('mineflayer-pathfinder').goals
pbar.update(1)
with nostdout():
  mineflayerViewer = require('prismarine-viewer').mineflayer
pbar.update(1)
with nostdout():
  elytrafly = require("mineflayer-elytrafly-commonjs")
pbar.update(1)
with nostdout():
  taskManager = require("mineflayer-task-manager").taskManager
pbar.update(1)
with nostdout():
  Vec3 = require("vec3").Vec3
pbar.update(1)
time.sleep(2)
pbar.close()
clear()

if os.path.isfile("config.json") == False:
  with open('config.json', 'w') as g:
    g.write('''{
    "Username": "OpenDeliveryBot",
    "Password": "<PASSWORD>",
    "Host": "127.0.0.1",
    "Port": 25565,
    "Auth": "microsoft",
    "Version": "auto",
    "CheckTimeoutInterval": 600000,
    "ViewerPort": 8000,
    "Goto": ["100", "100", "100"],
    "ChestRage": 100,
    "InitChestType": "chest",
    "InitChestCords": ["100", "100", "100"],
    "InitItemsName": "SchulkerBox",
    "InitItemsCount": 1,
    "ClientUsername": "OpenDeliveryBot"
}''')


# Load bot config from JSON file
with open('config.json', 'r') as f:
    config = json.load(f)

# Constants
RANGE_GOAL = -1  
CLIENT_USERNAME = config['ClientUsername']
DEV = False

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
bot.loadPlugin(taskManager)
print('Started Open Delivery Bot')
  
# Login handler  
@On(bot, 'login')
def handle_login(*args):
  print(f'joined {config["Host"]}:{config["Port"]}')
  print(bot.entity.position)
  mineflayerViewer(bot, { "port": config['ViewerPort'] })
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
  if DEV == True:
    bot.taskManager.Add("Get Items From Chest", GetItems(config['InitItemsName'], config['InitItemsCount']), 500)
    bot.taskManager.Add("Go To Specified Location", GoToLocation(config['goto']), 500)
    bot.taskManager.Add("Deposit Items To Nearby Chest", DepositItems(""), 500)
    bot.taskManager.Add("Self-destruct And Respawn", Respawn(), 500)
    
    print(", ".join([e.name for e in bot.taskManager.GetWholeQueue()]))
  





# Function to find and open the init chest
def GetItems(items, count):
  
  if config['InitChestCords'] == ["0", "0", "0"]:
    

    foundChest = False
    
    while not foundChest:
        
      # Find nearby chest
      
      chestToOpen = bot.findBlock({
          'matching': [mcData.blocksByName[name].id for name in [f'{str(config["InitChestType"]).lower()}']],
          'maxDistance': 100,
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
  else:
    x = config['InitChestCords'][0]
    y = config['InitChestCords'][1]
    z = config['InitChestCords'][2]
    locaton = bot.pathfinder.goto(pathfinder.goals.GoalNear(x, y, z, 1), timeout=60)






# Function to go to cordinates
def GoToLocation(cordinates):
    x = cordinates[0]
    y = cordinates[1]
    z = cordinates[2]
    bot.chat(f'/tell {CLIENT_USERNAME} [OPEN DELIVERY BOT] Going to: [{str(x)}, {str(y)}, {str(z)}]')
    locaton = bot.pathfinder.goto(pathfinder.goals.GoalNear(x, y, z, 1), timeout=60)
    












# Function to find and open chest  
def DepositItems(items):

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
      

# Function to find lava and selfdiscructs
def Respawn():

  foundLava = False
  
  while not foundLava:
      
    # Find nearby lava
    LavaToFind = bot.findBlock({
        'matching': [mcData.blocksByName[name].id for name in ['lava']], 
        'maxDistance': 200,
    })
    
    if not LavaToFind and foundLava == False:
      bot.chat('no chest found')
      continue
      
    # Go to lava location  
    if LavaToFind.position.x:
      x = LavaToFind.position.x
      y = LavaToFind.position.y  
      z = LavaToFind.position.z
      locaton = bot.pathfinder.goto(pathfinder.goals.GoalNear(x, y, z, 1), timeout=60)
      break



# Handler for bot end  
@On(bot, 'end')
def handle_end(*args):
  print('Bot ended!', args)
