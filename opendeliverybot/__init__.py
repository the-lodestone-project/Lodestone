#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import necessary modules
from javascript import require, On  
import time
import contextlib
import io
import sys
import click
import json
import os
from tqdm import tqdm
from datetime import datetime


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
pbar = tqdm(total=8)
pbar.set_description("installing javascript libaries", refresh=True)
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



# Function for implementing the loading animation
def load_animation(text):
  
    # String to be displayed when the application is loading
    load_str = text
    ls_len = len(load_str)
  
  
    # String for creating the rotating line
    animation = "|/-\\"
    anicount = 0
      
    # used to keep the track of
    # the duration of animation
    counttime = 0        
      
    # pointer for travelling the loading string
    i = 0                     
  
    while (counttime != 100):
          
        # used to change the animation speed
        # smaller the value, faster will be the animation
        time.sleep(0.075) 
                              
        # converting the string to list
        # as string is immutable
        load_str_list = list(load_str) 
          
        # x->obtaining the ASCII code
        x = ord(load_str_list[i])
          
        # y->for storing altered ASCII code
        y = 0                             
  
        # if the character is "." or " ", keep it unaltered
        # switch uppercase to lowercase and vice-versa 
        if x != 32 and x != 46:             
            if x>90:
                y = x-32
            else:
                y = x + 32
            load_str_list[i]= chr(y)
          
        # for storing the resultant string
        res =''             
        for j in range(ls_len):
            res = res + load_str_list[j]
              
        # displaying the resultant string
        sys.stdout.write("\r"+res + animation[anicount])
        sys.stdout.flush()
  
        # Assigning loading string
        # to the resultant string
        load_str = res
  
          
        anicount = (anicount + 1)% 4
        i =(i + 1)% ls_len
        counttime = counttime + 1
      
    # for windows OS
    clear()
    
load_animation("starting open delivery bot... ")



@click.command()
@click.option("--username", help="Username for login.")
@click.option("--password", help="Password for login.")  
@click.option("--host", prompt=True, help="Hostname or IP address of server.")
@click.option("--port", default=25565, help="Port number of server.")
@click.option("--auth", default="microsoft", help="Authentication method.",prompt=True)
@click.option("--version", default="auto", help="Game version.",prompt=True)
@click.option("--check_timeout", default=600000, help="Timeout interval for checks.")
@click.option("--viewer_port", default=8000, help="Port for viewer.")
@click.option("--goto", default=["100", "100", "100"], multiple=True, help="Coordinates to go to.", prompt=True)
@click.option("--chest_range", default=100, help="Range to search for chests.")
@click.option("--init_chest_type", default="chest", help="Type of chest to look for when starting.")
@click.option("--init_chest_cords", default=["100", "100", "100"], multiple=True, help="Coordinates to base chest.", prompt=True)  
@click.option("--init_items_name", default="SchulkerBox", help="Name of items to get from the base chest.", prompt=True)
@click.option("--init_items_count", default=1, help="Number of items to get from the base chest.",prompt=True)
@click.option("--client_username", default="OpenDeliveryBot", help="Username to deliver to.", prompt=True)
def main(username, password, host, port, auth, version, check_timeout, viewer_port, goto, chest_range, init_chest_type, init_chest_cords, init_items_name, init_items_count, client_username):

  DEV = False
  # Create version
  if version == "auto":
    version = False

  # Create bot instance 
  bot = mineflayer.createBot({
    'host': host,
    'port': port,
    'username': username,
    'password': password,
    'auth': auth,
    'hideErrors': True,
    'version': version,
    'checkTimeoutInterval': check_timeout,
  })

  # Load plugins
  bot.loadPlugin(pathfinder.pathfinder) 
  bot.loadPlugin(elytrafly.elytrafly)
  bot.loadPlugin(taskManager)
  print('Started Open Delivery Bot')
    
  # Login handler  
  @On(bot, 'login')
  def handle_login(*args):
    print(f'joined {host}:{port}')
    print(bot.entity.position)
    mineflayerViewer(bot, { "port": viewer_port })
    global mcData
    mcData = require('minecraft-data')(bot.version)
    movements = pathfinder.Movements(bot, mcData)
    
    with open("playes.log", "w") as x:
      x.write(str(bot.players))
    
    with open("cords.log", "a") as x:
      x.write(f"{datetime.now()}  |  {host}:{port}  |  X:{str(bot.entity.position.x)}, Y:{str(bot.entity.position.y)}, Z:{str(bot.entity.position.z)}")
    
    # Disable digging if needed
    movements.canDig = False

    bot.pathfinder.setMovements(movements)
    
    # Main login logic
    if DEV == True:
      bot.taskManager.Add("Get Items From Chest", GetItems(init_items_name, init_items_count), 500)
      bot.taskManager.Add("Go To Specified Location", GoToLocation(goto), 500)
      bot.taskManager.Add("Deposit Items To Nearby Chest", DepositItems(""), 500)
      bot.taskManager.Add("Self-destruct And Respawn", Respawn(), 500)
      
      print(", ".join([e.name for e in bot.taskManager.GetWholeQueue()]))
    





  # Function to find and open the init chest
  def GetItems(items, count):
    
    if init_chest_cords == ["0", "0", "0"]:
      

      foundChest = False
      
      while not foundChest:
          
        # Find nearby chest
        
        chestToOpen = bot.findBlock({
            'matching': [mcData.blocksByName[name].id for name in [f'{str(init_chest_type).lower()}']],
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

          bot.chat(f'/tell {client_username} [OPEN DELIVERY BOT] Found a nearby chest to deliver: [{str(x)}, {str(y)}, {str(z)}]')
          locaton = bot.pathfinder.goto(pathfinder.goals.GoalNear(x, y, z, 1), timeout=60)
          
          try:
            chest = bot.openContainer(chestToOpen)  
          except Exception:    
            bot.chat(f'/tell {client_username} [OPEN DELIVERY BOT] Please place a new chest in my location.')
            continue
              
          print(chest.containerItems())
          item = next((item for item in chest.slots if item and item.name == f'{init_items_name}'), None)
          time.sleep(10)
          chest.close()
          bot.chat(f'/tell {client_username} [OPEN DELIVERY BOT] Items have been successfully delivered at: [{str(x)}, {str(y)}, {str(z)}] on [{datetime.now()}]')
          foundChest = True
          break
    else:
      x = init_chest_cords[0]
      y = init_chest_cords[1]
      z = init_chest_cords[2]
      locaton = bot.pathfinder.goto(pathfinder.goals.GoalNear(x, y, z, 1), timeout=60)






  # Function to go to cordinates
  def GoToLocation(cordinates):
      x = cordinates[0]
      y = cordinates[1]
      z = cordinates[2]
      bot.chat(f'/tell {client_username} [OPEN DELIVERY BOT] Going to: [{str(x)}, {str(y)}, {str(z)}]')
      locaton = bot.pathfinder.goto(pathfinder.goals.GoalNear(x, y, z, 1), timeout=60)
      












  # Function to find and open chest  
  def DepositItems(items):

    foundChest = False
    
    while not foundChest:
        
      # Find nearby chest
      chestToOpen = bot.findBlock({
          'matching': [mcData.blocksByName[name].id for name in ['chest']], 
          'maxDistance': chest_range,
      })
      
      if not chestToOpen and foundChest == False:
        bot.chat('no chest found')
        continue
        
      # Go to chest location  
      if chestToOpen.position.x:
        x = chestToOpen.position.x
        y = chestToOpen.position.y  
        z = chestToOpen.position.z

        bot.chat(f'/tell {client_username} [OPEN DELIVERY BOT] Found a nearby chest to deliver: [{str(x)}, {str(y)}, {str(z)}]')
        locaton = bot.pathfinder.goto(pathfinder.goals.GoalNear(x, y, z, 1), timeout=60)
        
        try:
          chest = bot.openContainer(chestToOpen)  
        except Exception:    
          bot.chat(f'/tell {client_username} [OPEN DELIVERY BOT] Please place a new chest in my location.')
          continue
            
        print(chest.containerItems())
        time.sleep(10)
        chest.close()
        bot.chat(f'/tell {client_username} [OPEN DELIVERY BOT] Items have been successfully delivered at: [{str(x)}, {str(y)}, {str(z)}] on [{datetime.now()}]')
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


#run main
main()