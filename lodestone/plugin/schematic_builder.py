import lodestone
from rich.console import Console
from rich.progress import Progress
import ast
import inspect
from javascript import require
import os
import threading
import json
from types import SimpleNamespace
import urllib.request

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