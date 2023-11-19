import lodestone
from discord import Embed
import datetime
from discord import SyncWebhook
from rich.console import Console
from rich.progress import Progress
import asyncio
import ast
import inspect
from javascript import require
import time
import os
import math
import threading
import json
from types import SimpleNamespace
import asyncio
from math import sqrt
import asyncio
import aiofiles
import urllib.request
from importlib import reload

class plugins:
    class discord:
        """
        Build in Discord plugin
        """
        def __init__(self, bot: lodestone.Bot):
            "The injection method"
            self.bot = bot
            self.main() # run the main code to add the event
            self.code = inspect.getsource(inspect.getmodule(self.__class__))
            self.tree = ast.parse(self.code)
            self.events = []
            for node in ast.walk(self.tree):
                if isinstance(node, ast.Call) and hasattr(node.func, 'attr') and node.func.attr == 'on':
                    event = node.args[0].s
                    self.events.append(event)
            events_loaded = list(bot.loaded_events.keys())
            events_loaded.append(self.events) # add the event to the list
            bot.emit('event_loaded', *events_loaded)
            plugins_loaded = list(bot.loaded_plugins.keys())
            plugins_loaded.append(self.__class__.__name__) # add the plugin to the list
            bot.emit('plugin_loaded', *plugins_loaded)
            
            
        def main(self):
            @self.bot.on('discord_webhook') # this part of the code is ran when bot.emit('discord_webhook') is called
            def discord_webhook(bot, message:str, webhook:str, use_discord_forums:bool=False):
                hook = SyncWebhook.from_url(url=webhook) # connect to the webhook
                use_discord_forums:bool=False
                color=0x3498db
                embed = Embed(title="", description=f"**{message}**", color=color) # make the embed
                embed.timestamp = datetime.datetime.utcnow()
                try:
                    embed.set_footer(text=f'{self.bot.username}', icon_url=f"https://mc-heads.net/avatar/{self.bot.username}/600.png") # set the footer image to the players head
                except:
                    embed.set_footer(text='\u200b', icon_url="https://github.com/Project-Lodestone/Lodestone/blob/main/chestlogo.png?raw=True") # fallback footer image
                if use_discord_forums:
                    today = datetime.date.today() # get the current date
                    hook.send(content=f"{today}", thread_name=f"{today}", username="Lodestone", avatar_url="https://github.com/Project-Lodestone/Lodestone/blob/main/chestlogo.png?raw=True", embed=embed) # send the message in a forums channel
                else:
                    hook.send(content=f" ", username="Lodestone", avatar_url="https://github.com/Project-Lodestone/Lodestone/blob/main/chestlogo.png?raw=True", embed=embed) # send the message in a normal channel
    class schematic:
        """
        Build in schematic plugin.
        `bot.build_schematic(file)` to start building.
        """
        def __init__(self, bot: lodestone.Bot):
            "The injection method"
            self.bot:lodestone.Bot = bot
            global Vec3
            global facingData
            global interactable
            global path
            global fs
            global Schematic
            global mcData
            global Item
            Vec3  = require('vec3').Vec3
            facingData = json.load(urllib.request.urlopen("https://raw.githubusercontent.com/the-lodestone-project/Lodestone/main/lodestone/facingData.json"))
            interactable = json.load(urllib.request.urlopen("https://raw.githubusercontent.com/the-lodestone-project/Lodestone/main/lodestone/facingData.json"))
            path = require('path')
            fs = require('fs').promises
            # const { builder, Build } = require('mineflayer-builder')
            Schematic = require('prismarine-schematic').Schematic
            mcData = require('minecraft-data')(bot.bot.version)
            Item = require('prismarine-item')(bot.bot.version)
            self.console = Console(force_terminal=True)
            self.code = inspect.getsource(inspect.getmodule(self.__class__))
            self.tree = ast.parse(self.code)
            self.events = []
            for node in ast.walk(self.tree):
                if isinstance(node, ast.Call) and hasattr(node.func, 'attr') and node.func.attr == 'on':
                    event = node.args[0].s
                    self.events.append(event)
            events_loaded = list(bot.loaded_events.keys())
            events_loaded.append(self.events) # add the event to the list
            bot.emit('event_loaded', *events_loaded)
            plugins_loaded = list(bot.loaded_plugins.keys())
            plugins_loaded.append(self.__class__.__name__) # add the plugin to the list
            bot.emit('plugin_loaded', *plugins_loaded)
            self.bot.build_schematic:callable = self.start
        
    
        class Build:
            def __init__(self, schematic, world, at):
                self.schematic = schematic
                self.world = world 
                self.at = at
                self.min = at.plus(schematic.offset)
                self.max = self.min.plus(schematic.size)
                
                
                
                self.actions = []
                self.error_actions = []
                self.update_actions()

                # Cache of blockstate to block
                Block = require('prismarine-block')(schematic.version)
                mcData = require('minecraft-data')(schematic.version)
                self.blocks = {}
                self.properties = {}
                self.items = {}
                for state_id in schematic.palette:
                    try:
                        block = Block.fromStateId(state_id, 0)
                        self.blocks[state_id] = block
                        self.properties[state_id] = block.getProperties()
                        self.items[state_id] = mcData.itemsByName[block.name]
                    except: 
                        lodestone.logger.error("got error with state id " + str(state_id))
                        continue
                    
                # How many actions?
                # lodestone.logger.info(len(self.actions))
            
            def update_actions(self):
                self.actions = []
                cursor = Vec3(0,0,0)
                for cursor.y in range(self.min.y, self.max.y):
                    for cursor.z in range(self.min.z, self.max.z):
                        for cursor.x in range(self.min.x, self.max.x):
                            try:
                                state_in_world = self.world.getBlockStateId(cursor)
                                new_vec3 = SimpleNamespace(x=cursor.x-self.at.x, y=cursor.y-self.at.y, z=cursor.z-self.at.z)
                                
                                wanted_state = self.schematic.getBlockStateId(Vec3(new_vec3.x, new_vec3.y, new_vec3.z))
                                if state_in_world != wanted_state:
                                    if wanted_state == 0:
                                        self.actions.append({'type': 'dig', 'pos': cursor.clone()})
                                    else:
                                        self.actions.append({'type': 'place', 'pos': cursor.clone(), 'state': wanted_state})
                            except:
                                lodestone.logger.error(f"cant get data about block at {cursor}")

            def update_block(self, pos):
                # is in area?
                self.update_actions()

            def get_item_for_state(self, state_id):
                return self.items[state_id]
            
            
            def get_facing(self, state_id, facing):
                if not facing: 
                    return {'facing': None, 'face_direction': False, 'is3D': False}
                block = self.blocks[state_id]
                data = facingData[block.name]
                if data['inverted'] == 'True' or data['inverted'] == True:
                    if facing == 'up': facing = 'down'
                    elif facing == 'down': facing = 'up'
                    elif facing == 'north': facing = 'south'
                    elif facing == 'south': facing = 'north'
                    elif facing == 'west': facing = 'east'
                    elif facing == 'east': facing = 'west'
                return {'facing': facing, 'face_direction': data['faceDirection'], 'is3D': data['is3D']}
            
            
            def get_shape_face_centers(self, shapes, direction, half=None):
                faces = []
                for shape in shapes:
                    halfsize = Vec3(shape[3] - shape[0], shape[4] - shape[1], shape[5] - shape[2]).scale(0.5)
                    center = Vec3(shape[0] + shape[3], shape[1] + shape[4], shape[2] + shape[5]).scale(0.5)
                    center = center.offset(halfsize.x * direction.x, halfsize.y * direction.y, halfsize.z * direction.z)
                    if half == 'top' and center.y <= 0.5:
                        if abs(direction.y) == 0: center.y += halfsize.y - 0.001
                        if center.y <= 0.5: continue
                    elif half == 'bottom' and center.y >= 0.5:
                        if abs(direction.y) == 0: center.y -= halfsize.y - 0.001
                        if center.y >= 0.5: continue
                    faces.append(center)
                return faces
            
            def get_possible_directions(self, state_id, pos):
                faces = [True] * 6
                properties = self.properties[state_id]
                block = self.blocks[state_id]
                if properties.axis:
                    if properties.axis == 'x': 
                        faces[0] = faces[1] = faces[2] = faces[3] = False
                    elif properties.axis == 'y': 
                        faces[2] = faces[3] = faces[4] = faces[5] = False
                    elif properties.axis == 'z':
                        faces[0] = faces[1] = faces[4] = faces[5] = False
                if properties.half == 'upper': 
                    return []
                if properties.half == 'top' or properties.type == 'top':
                    faces[0] = faces[1] = False
                if properties.half == 'mcbottom' or properties.type == 'mcbottom':
                    faces[0] = faces[1] = False
                if properties.facing:
                    facing_data = self.get_facing(state_id, properties.facing)
                    facing = facing_data['facing']
                    face_direction = facing_data['face_direction']
                    if face_direction:
                        if facing == 'north':
                            faces[0] = faces[1] = faces[2] = faces[4] = faces[5] = False
                        elif facing == 'south':
                            faces[0] = faces[1] = faces[3] = faces[4] = faces[5] = False
                        elif facing == 'west':
                            faces[0] = faces[1] = faces[2] = faces[3] = faces[4] = False
                        elif facing == 'east':
                            faces[0] = faces[1] = faces[2] = faces[3] = faces[5] = False 
                        elif facing == 'up':
                            faces[1] = faces[2] = faces[3] = faces[4] = faces[5] = False
                        elif facing == 'down':
                            faces[0] = faces[2] = faces[3] = faces[4] = faces[5] = False
                if properties.hanging:
                    faces[0] = faces[2] = faces[3] = faces[4] = faces[5] = False
                if block.material == 'plant':
                    faces[1] = faces[2] = faces[3] = faces[4] = faces[5] = False
                    
                dirs = []
                face_dirs = [Vec3(0, -1, 0), Vec3(0, 1, 0), Vec3(0, 0, -1), Vec3(0, 0, 1), Vec3(-1, 0, 0), Vec3(1, 0, 0)]
                for i, can_face in enumerate(faces):
                    if can_face:
                        dirs.append(face_dirs[i])
                        
                half = properties.half if properties.half else properties.type
                dirs = [dir for dir in dirs if self.get_shape_face_centers(self.world.getBlock(pos.plus(dir)).shapes, dir.scaled(-1), half)]
                # dirs = []
                # for dir in dirs:
                #     pos_vec_python = SimpleNamespace(x=pos.x+dir.x, y=pos.y+dir.y, z=pos.z+dir.z)
                #     pos_vec = Vec3(pos_vec_python.x, pos_vec_python.y, pos_vec_python.z)
                #     dir_vec = Vec3(dir.x, dir.y, dir.z)
                    
                #     if getShapeFaceCenters(self.world.getBlock(pos_vec).shapes, 
                #                             -dir_vec, 
                #                             half):
                #         dirs.append(dir)
                # lodestone.logger.info(dirs)
                return dirs

            def remove_action(self, action):
                try:
                    self.actions.remove(action)
                except:
                    pass
            
            
            def get_available_actions(self):
                filtered_actions = [action for action in self.actions if action['type'] == 'dig' or len(self.get_possible_directions(action['state'], action['pos'])) > 0]
                return filtered_actions
        
        def equip_item(self, id, item):
            if not any(x.type == id for x in self.bot.inventory.items()):
                slot = self.bot.bot.inventory.firstEmptyInventorySlot()
                if slot is None:
                    slot = 36
                
                # if self.bot.bot.player.gamemode == 0:
                #     self.bot.collect_block(f"{item.name}")
                # else:
                #     self.bot.bot.creative.setInventorySlot(slot, Item(id, 1))
                self.bot.bot.creative.setInventorySlot(slot, Item(id, 1))
            item = next(x for x in self.bot.inventory.items() if x.type==id)
            self.bot.bot.equip(item, "hand")
            
        def closest_action(self, actions):
            origin = self.bot.entity.position.offset(0.5, 0.5, 0.5)
            minDist = 9e9
            closest = None
            for action in actions:
                dist = action.pos.offset(0.5, 0.5, 0.5).distanceSquared(origin)
                if dist < minDist:
                    minDist = dist
                    closest = action
            return action
        
        def builder(self, build: Build, actions):
            layer = 1
            with Progress(console=self.console) as progress:
                task = progress.add_task(description="Building schematic...", total=len(build.actions))
                while len(build.actions) > 0:
                    try:
                        if len(actions) == 0:
                            # status.update("[bold]Ran out of actions for layer " + str(layer) + ".")
                            actions = build.get_available_actions()
                            layer += 1
                            # status.update(f"[bold]{len(actions)} available actions")
                            
                        def distance_squared(p1, p2):
                            return (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2 + (p1.z - p2.z) ** 2

                        actions.sort(key=lambda a: distance_squared(Vec3(a['pos'].x + 0.5, a['pos'].y + 0.5, a['pos'].z + 0.5), self.bot.entity.position))

                        action = actions[0]
                        
                        # status.update(f"[bold]Building schematic. ({len(actions)} available actions for layer {layer}) ({len(build.actions)}) (errors: {len(build.error_actions)})")
                        
                        if action["type"] == "place":

                            item = build.get_item_for_state(action["state"])
                            try:
                                lodestone.logger.info(f"Selecting {item.displayName}")
                            except:
                                lodestone.logger.info(f"Got an error while trying to place block at {action['pos']}")
                                continue
                            
                            
                            properties = build.properties[action["state"]]
                            half = properties["half"] if "half" in properties else properties["type"]

                            faces = build.get_possible_directions(action["state"], action["pos"])

                            for face in faces:
                                block = self.bot.bot.blockAt(action["pos"].plus(face))

                            facing_data = build.get_facing(action["state"], properties["facing"])
                            facing = facing_data["facing"]
                            is3D = facing_data["is3D"]
                            try:
                                goal = self.bot.goals.GoalPlaceBlock(action["pos"], self.bot.world, {
                                    "faces": faces,
                                    "facing": facing,
                                    "facing3D": is3D,
                                    "half": half
                                })
                            except Exception as e:
                                
                                try:
                                    actions.remove(action)
                                except:
                                    pass
                                build.remove_action(action)
                                build.error_actions.append(action)
                                continue
                            
                            self.bot.pathfinder.goto(goal, timeout=200)
                            
                            try:
                                progress.update(task, visible=False)
                                self.equip_item(item.id, item) # equip after pathfinder
                                progress.update(task, visible=True)
                            except Exception as e:
                                
                                try:
                                    actions.remove(action)
                                except:
                                    pass
                                build.remove_action(action)
                                build.error_actions.append(action)
                                continue
                            
                            faceAndRef = goal.getFaceAndRef(self.bot.bot.entity.position.floored().offset(0.5, 1.6, 0.5))
                            if not faceAndRef:
                                try:
                                    actions.remove(action)
                                except:
                                    pass
                                build.remove_action(action)
                                build.error_actions.append(action)
                                continue
                                    
                            self.bot.bot.lookAt(faceAndRef.to, True)
                            
                            refBlock = self.bot.bot.blockAt(faceAndRef.ref)
                            sneak = False
                            if dict(interactable).get(refBlock.name) != None:
                                sneak = True
                            
                            try:
                                delta = faceAndRef.to.minus(faceAndRef.ref)
                            except:
                                delta = Vec3(0.5, 0.5, 0.5)

                            if sneak: 
                                self.bot.set_control_state("sneak", True)
                            
                            try:
                                self.bot.bot.placeBlock(refBlock, faceAndRef.face.scaled(-1))
                            except Exception as e:
                                
                                try:
                                    actions.remove(action)
                                except:
                                    pass
                                build.remove_action(action)
                                build.error_actions.append(action)
                                continue

                            if sneak: 
                                self.bot.set_control_state("sneak", False)
                        
                            block = self.bot.bot.world.getBlock(action["pos"])
                            if block.stateId != action["state"]:
                                pass
                        try:
                            actions.remove(action)
                        except:
                            pass
                        build.remove_action(action)
                        progress.update(task, advance=1)
                    except Exception as e:
                        try:
                            actions.remove(action)
                        except:
                            pass
                        build.remove_action(action)
                        build.error_actions.append(action)
                        continue
                    
                
            layer = 1
            lodestone.logger.warning("Fixing errors")
            while len(build.error_actions) > 0:
                actions = build.error_actions
                while len(build.actions) > 0:
                    try:

                        if len(actions) == 0:
                            # status.update("[bold]Ran out of actions for layer " + str(layer) + ".")
                            actions = build.get_available_actions()
                            layer += 1
                            # status.update(f"[bold]{len(actions)} available actions")
                            
                        def distance_squared(p1, p2):
                            return (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2 + (p1.z - p2.z) ** 2

                        actions.sort(key=lambda a: distance_squared(Vec3(a['pos'].x + 0.5, a['pos'].y + 0.5, a['pos'].z + 0.5), self.bot.entity.position))

                        action = actions[0]
                        
                        # status.update(f"[bold]Building schematic! ({len(actions)} for layer {layer}) ({len(build.actions)}) (errors: {len(build.error_actions)})")
                        
                        if action["type"] == "place":

                            item = build.get_item_for_state(action["state"])
                            try:
                                lodestone.logger.info(f"Selecting {item.displayName}")
                            except:
                                lodestone.logger.info(f"Got an error while trying to place block at {action['pos']}")
                                continue
                            
                            properties = build.properties[action["state"]]
                            half = properties["half"] if "half" in properties else properties["type"]

                            faces = build.get_possible_directions(action["state"], action["pos"])

                            for face in faces:
                                block = self.bot.bot.blockAt(action["pos"].plus(face))

                            facing_data = build.get_facing(action["state"], properties["facing"])
                            facing = facing_data["facing"]
                            is3D = facing_data["is3D"]
                            try:
                                goal = self.bot.goals.GoalPlaceBlock(action["pos"], self.bot.world, {
                                    "faces": faces,
                                    "facing": facing,
                                    "facing3D": is3D,
                                    "half": half
                                })
                            except Exception as e:
                                
                                try:
                                    actions.remove(action)
                                except:
                                    pass
                                build.remove_action(action)
                                build.error_actions.append(action)
                                continue
                            
                            self.bot.pathfinder.goto(goal, timeout=200)
                            
                            try:
                                self.equip_item(item.id) # equip after pathfinder
                            except Exception as e:
                                
                                try:
                                    actions.remove(action)
                                except:
                                    pass
                                build.remove_action(action)
                                build.error_actions.append(action)
                                continue
                            
                            faceAndRef = goal.getFaceAndRef(self.bot.bot.entity.position.floored().offset(0.5, 1.6, 0.5))
                            if not faceAndRef:
                                try:
                                    actions.remove(action)
                                except:
                                    pass
                                build.remove_action(action)
                                build.error_actions.append(action)
                                continue
                                    
                            self.bot.bot.lookAt(faceAndRef.to, True)
                            
                            refBlock = self.bot.bot.blockAt(faceAndRef.ref)
                            sneak = False
                            if dict(interactable).get(refBlock.name) != None:
                                sneak = True
                            
                            try:
                                delta = faceAndRef.to.minus(faceAndRef.ref)
                            except:
                                delta = Vec3(0.5, 0.5, 0.5)

                            if sneak: 
                                self.bot.set_control_state("sneak", True)
                            
                            try:
                                self.bot.bot.placeBlock(refBlock, faceAndRef.face.scaled(-1))
                            except Exception as e:
                                
                                try:
                                    actions.remove(action)
                                except:
                                    pass
                                build.remove_action(action)
                                build.error_actions.append(action)
                                continue

                            if sneak: 
                                self.bot.set_control_state("sneak", False)
                        
                            block = self.bot.bot.world.getBlock(action["pos"])
                            if block.stateId != action["state"]:
                                pass
                        try:
                            actions.remove(action)
                        except:
                            pass
                        build.remove_action(action)
                    except Exception as e:
                        try:
                            actions.remove(action)
                        except:
                            pass
                        build.remove_action(action)
                        build.error_actions.append(action)
                        continue
                
                
        
        
        def start(self, file=""):
            """
            Starts the building process using the specified schematic file.

            Args:
                file (str): The path to the schematic file.

            Returns:
                None
            """
            with self.console.status("[bold]Loading schematic...") as status:
                
                os.environ["REQ_TIMEOUT"] = f"{self.bot.check_timeout_interval}"
                schematic = Schematic.read(fs.readFile(path.resolve(f'{file}')), self.bot.bot.version)
                at = self.bot.entity.position.floored()
                lodestone.logger.info(f'Building at {at.x, at.y, at.z}')
                # status.update("[bold]Generating actions...")
                build_file = self.Build(schematic, self.bot.world, at)
                # status.update("[bold]Generarated actions")
                self.bot.movements.canDig = False
                self.bot.movements.canOpenDoors = True
                # self.bot.pathfinder.setMovements(self.bot.movements)
                actions = build_file.get_available_actions()
                # status.update(f"[bold]{len(actions)} available actions")
                status.stop()
                _thread = threading.Thread(target=self.builder, args=(build_file, actions))
                _thread.start()
                    
                    
    class cactus:
        """
        Build in cactus farm builder plugin
        """
        def __init__(self, bot: lodestone.Bot):
            "The injection method"
            self.bot:lodestone.Bot = bot
            self.mcData = require('minecraft-data')(bot.bot.version)
            self.Item = require('prismarine-item')(bot.bot.version)
            self.Vec3  = require('vec3').Vec3
            self.console = Console(force_terminal=True)
            self.code = inspect.getsource(inspect.getmodule(self.__class__))
            self.tree = ast.parse(self.code)
            self.events = []
            for node in ast.walk(self.tree):
                if isinstance(node, ast.Call) and hasattr(node.func, 'attr') and node.func.attr == 'on':
                    event = node.args[0].s
                    self.events.append(event)
            events_loaded = list(bot.loaded_events.keys())
            events_loaded.append(self.events) # add the event to the list
            bot.emit('event_loaded', *events_loaded)
            plugins_loaded = list(bot.loaded_plugins.keys())
            plugins_loaded.append(self.__class__.__name__) # add the plugin to the list
            bot.emit('plugin_loaded', *plugins_loaded)
            self.bot.build_cactus:callable = self.start
            
        def __equip_item(self, name):
            id = self.bot.bot.registry.itemsByName[name].id
            if not any(x.type == id for x in self.bot.inventory.items()):
                slot = self.bot.bot.inventory.firstEmptyInventorySlot()
                if slot is None:
                    slot = 36
                
                # if self.bot.bot.player.gamemode == 0:
                #     self.bot.collect_block(f"{item.name}")
                # else:
                #     self.bot.bot.creative.setInventorySlot(slot, Item(id, 1))
                while True:
                    try:
                        self.bot.bot.creative.setInventorySlot(slot, self.Item(id, 1))
                        break
                    except:
                        continue
            item = next(x for x in self.bot.inventory.items() if x.type==id)
            self.bot.bot.equip(item, "hand")
            
        
        def __dig_layer(self):
            self.bot.bot.dig(self.bot.bot.blockAt(self.bot.entity.position.offset(2, -2, 0)), True)
            self.bot.bot.dig(self.bot.bot.blockAt(self.bot.entity.position.offset(2, -2, 2)), True)
            self.bot.bot.dig(self.bot.bot.blockAt(self.bot.entity.position.offset(0, -2, 2)), True)
            self.bot.bot.dig(self.bot.bot.blockAt(self.bot.entity.position.offset(-2, -2, 2)), True)
            self.bot.bot.dig(self.bot.bot.blockAt(self.bot.entity.position.offset(-2, -2, 0)), True)
            self.bot.bot.dig(self.bot.bot.blockAt(self.bot.entity.position.offset(-2, -2, -2)), True)
            self.bot.bot.dig(self.bot.bot.blockAt(self.bot.entity.position.offset(0, -2, -2)), True)
            self.bot.bot.dig(self.bot.bot.blockAt(self.bot.entity.position.offset(2, -2, -2)), True)
                    
            
        def __build_up(self):
            self.__equip_item('dirt')
            # referenceBlock = self.bot.bot.blockAt(self.bot.entity.position.offset(0, -1, 0))
            # jumpY = math.floor(self.bot.entity.position.y) + 1.0
            # self.bot.set_control_state('jump', True)
            # @self.bot.once('move')
            # def place_if_high_enough(*arg):
            #     print("trying")
            #     nonlocal tryCount
            #     if self.bot.entity.position.y > jumpY:
            #         try:
            #             self.bot.bot.placeBlock(referenceBlock, self.Vec3(0, 1, 0))
            #             self.bot.set_control_state('jump', False)
            #             #bot.chat('Placing a block was successful')
            #         except Exception as err:
            #             tryCount += 1
            #             if tryCount > 10:
            #                 self.bot.chat(err.message)
            #                 self.bot.set_control_state('jump', False)
            
            # tryCount = 0
            
            self.bot.set_control_state("jump", True)
            # Wait until the bot is high enough
            while True:
                positionBelow = self.bot.entity.position.offset(0, -0.5, 0)
                blockBelow = self.bot.bot.blockAt(positionBelow)
                if blockBelow.name == "air":
                    break
                self.bot.bot.waitForTicks(1)
            # Place a block
            sourcePosition = self.bot.entity.position.offset(0, -1.5, 0)
            sourceBlock = self.bot.bot.blockAt(sourcePosition)
            faceVector = {"x": 0, "y": 1, "z": 0}
            while True:
                try:
                    self.bot.bot.placeBlock(sourceBlock, faceVector)
                    break
                except:
                    continue
                
            # Stop jump
            self.bot.set_control_state("jump", False)
            
            
        

        def __build_layer(self):
            # Plaziert den Sand
            self.__equip_item('sand')
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(2, -1, 0)), self.Vec3(0, 1, 0))
            
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(2, -1, 2)), self.Vec3(0, 1, 0))
            
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(0, -1, 2)), self.Vec3(0, 1, 0))
            
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(-2, -1, 2)), self.Vec3(0, 1, 0))
            
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(-2, -1, 0)), self.Vec3(0, 1, 0))
            
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(-2, -1, -2)), self.Vec3(0, 1, 0))
            
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(0, -1, -2)), self.Vec3(0, 1, 0))
            
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(2, -1, -2)), self.Vec3(0, 1, 0))
            
            # Plaziert den Kaktus
            self.__equip_item('cactus')
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(2, 0, 0)), self.Vec3(0, 1, 0))
            
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(2, 0, 2)), self.Vec3(0, 1, 0))
            
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(0, 0, 2)), self.Vec3(0, 1, 0))
            
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(-2, 0, 2)), self.Vec3(0, 1, 0))
            
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(-2, 0, 0)), self.Vec3(0, 1, 0))
            
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(-2, 0, -2)), self.Vec3(0, 1, 0))
            
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(0, 0, -2)), self.Vec3(0, 1, 0))
            
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(2, 0, -2)), self.Vec3(0, 1, 0))
            
        
        def __build_fence_dirt(self):
            self.__equip_item('dirt')
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(2, -1, 2)), self.Vec3(0, 1, 0))
            self.__equip_item('iron_bars')
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(2, 0, 2)), self.Vec3(0, 0, -1))
            self.__equip_item('dirt')
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(0, -1, 2)), self.Vec3(0, 1, 0))
            self.__equip_item('iron_bars')
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(0, 0, 2)), self.Vec3(0, 0, -1))
            self.__equip_item('dirt')
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(-2, -1, 2)), self.Vec3(0, 1, 0))
            self.__equip_item('iron_bars')
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(-2, 0, 2)), self.Vec3(0, 0, -1))
            self.__equip_item('dirt')
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(-2, -1, -2)), self.Vec3(0, 1, 0))
            self.__equip_item('iron_bars')
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(-2, 0, -2)), self.Vec3(0, 0, 1))
            self.__equip_item('dirt')
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(0, -1, -2)), self.Vec3(0, 1, 0))
            self.__equip_item('iron_bars')
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(0, 0, -2)), self.Vec3(0, 0, 1))
            self.__equip_item('dirt')
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(2, -1, -2)), self.Vec3(0, 1, 0))
            self.__equip_item('iron_bars')
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(2, 0, -2)), self.Vec3(0, 0, 1))
            self.__equip_item('dirt')
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(2, -1, 0)), self.Vec3(0, 1, 0))
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(-2, -1, 0)), self.Vec3(0, 1, 0))


        def __place_dirt_layer(self):
            self.__equip_item('dirt')
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(2, -1, 0)), self.Vec3(0, 1, 0))
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(2, -1, 2)), self.Vec3(0, 1, 0))
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(0, -1, 2)), self.Vec3(0, 1, 0))
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(-2, -1, 2)), self.Vec3(0, 1, 0))
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(-2, -1, 0)), self.Vec3(0, 1, 0))
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(-2, -1, -2)), self.Vec3(0, 1, 0))
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(0, -1, -2)), self.Vec3(0, 1, 0))
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(2, -1, -2)), self.Vec3(0, 1, 0))
            # break
            
        def __place_last_cactus(self):
            self.bot.bot.dig(self.bot.bot.blockAt(self.bot.entity.position.offset(0, -2, 0)), True)
            self.bot.bot.dig(self.bot.bot.blockAt(self.bot.entity.position.offset(0, -3, 0)), True)
            self.bot.bot.dig(self.bot.bot.blockAt(self.bot.entity.position.offset(0, -4, 0)), True)
            time.sleep(1)
            self.__equip_item('sand')
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(0, -5, 0)), self.Vec3(0, 1, 0))
            self.__equip_item('cactus')
            time.sleep(1)
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(0, -4, 0)), self.Vec3(0, 1, 0))
        
        def __cactus(self, layers):
            with Progress(console=self.console) as progress:
                task = progress.add_task(description="Building cactus farm...", total=9 * layers)
                for layer in range(0, layers):
                    self.__build_layer()
                    progress.update(task, advance=1)
                    # time.sleep(2)
                    self.__build_up()
                    progress.update(task, advance=1)
                    # time.sleep(2)
                    self.__build_up()
                    progress.update(task, advance=1)
                    # time.sleep(2)
                    self.__build_fence_dirt()
                    progress.update(task, advance=1)
                    # time.sleep(2)
                    self.__build_up()
                    progress.update(task, advance=1)
                    # time.sleep(2)
                    self.__place_dirt_layer()
                    progress.update(task, advance=1)
                    # time.sleep(2)
                    self.__build_up()
                    progress.update(task, advance=1)
                    # time.sleep(2)
                    self.__dig_layer()
                    progress.update(task, advance=1)
                    # time.sleep(2)
                    self.__place_last_cactus()
                    # time.sleep(2)
                    progress.update(task, advance=1)
            
            progress.stop_task(task)
            progress.stop()
                
                
        def start(self,layers):
            lodestone.logger.info(f"Building cactus farm...\n{layers * 9}x sand\n{layers * 9}x cactus\n{layers * 9}x dirt\n{layers * 6}x iron bars")
            self.__cactus(layers)
            lodestone.logger.info("Done building cactus farm")
            # _thread = threading.Thread(target=self.__cactus, args=[layers])
            # _thread.start()
    
    class discordrp:
        """
        Build in cactus farm builder plugin
        """
        def __init__(self, bot: lodestone.Bot):
            "The injection method"
            self.bot:lodestone.Bot = bot
            self.code = inspect.getsource(inspect.getmodule(self.__class__))
            self.tree = ast.parse(self.code)
            plugins_loaded = list(bot.loaded_plugins.keys())
            plugins_loaded.append(self.__class__.__name__)
            bot.emit('plugin_loaded', *plugins_loaded)
            client_id = "1143589220821258270" 
            from pypresence import Presence
            RPC = Presence(client_id=client_id)
            RPC.connect()
            RPC.update(
                        state=f"{self.bot.local_host} - {self.bot.bot.version}",
                        details=f"{self.bot.username}",
                        large_image=(f"https://mc-heads.net/avatar/{self.bot.username}/180/nohelm.png"), 
                        large_text=f"{self.bot.username}",
                        small_image=(f"https://eu.mc-api.net/v3/server/favicon/{self.bot.local_host}"), small_text=f"{self.bot.local_host} on {self.bot.bot.version}",
                        start=time.time(),
                        # buttons=[{"label": "Join Server", "url": f"https://{self.bot.local_host}"}]
            )
            
            self.bot.discordrp = RPC.update
            
            













                
        
        
                     
        
            
            
            
            
        
