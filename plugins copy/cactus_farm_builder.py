import lodestone
from rich.console import Console
from rich.progress import Progress
import ast
import inspect
from javascript import require

import plugins

class cactus(plugins.Base):
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
            self.building_up = False
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
            
            old_pos = int(self.bot.entity.position.y)
            self.__equip_item('dirt')
            @self.bot.on("physicsTick")
            def run(*arg):  
                if self.bot.get_data("tower") == 1:
                    if int(self.bot.entity.position.y) == int(old_pos) + 1:
                        self.bot.bot.waitForTicks(50)
                        if int(self.bot.entity.position.y) == int(old_pos) + 1:
                            self.bot.set_data("tower", 0)
                    self.bot.bot.setControlState("jump", True)
                    eferenceBlock = self.bot.bot.blockAt(self.bot.bot.entity.position.offset(0, -1, 0))
                    placeBlockVar = self.bot.bot._genericPlace(eferenceBlock, self.Vec3(0,1,0), { "swingArm": "right" })
                else:
                    self.bot.bot.setControlState("jump", False)
            
            self.bot.set_data("tower", 1)
            
            


            
            
        

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
            self.bot.bot.waitForTicks(50)
            self.__equip_item('sand')
            
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(0, -5, 0)), self.Vec3(0, 1, 0))
            self.__equip_item('cactus')
            self.bot.bot.waitForTicks(50)
            self.bot.bot.placeBlock(self.bot.bot.blockAt(self.bot.entity.position.offset(0, -4, 0)), self.Vec3(0, 1, 0))
        
        def __cactus(self, layers):
            with Progress(console=self.console) as progress:
                task = progress.add_task(description="Building cactus farm...", total=8 * layers)
                for layer in range(0, layers):
                    self.__build_layer()
                    progress.update(task, advance=1)
                    self.bot.bot.waitForTicks(50)
                    self.__build_up()
                    progress.update(task, advance=1)
                    self.bot.bot.waitForTicks(50)
                    self.__build_up()
                    progress.update(task, advance=1)
                    self.bot.bot.waitForTicks(50)
                    self.__build_fence_dirt()
                    progress.update(task, advance=1)
                    self.bot.bot.waitForTicks(50)
                    self.__build_up()
                    progress.update(task, advance=1)
                    self.bot.bot.waitForTicks(50)
                    self.__place_dirt_layer()
                    progress.update(task, advance=1)
                    self.bot.bot.waitForTicks(50)
                    self.__build_up()
                    progress.update(task, advance=1)
                    self.bot.bot.waitForTicks(50)
                    self.__dig_layer()
                    progress.update(task, advance=1)
                    self.bot.bot.waitForTicks(50)
                    self.__place_last_cactus()
                    self.bot.bot.waitForTicks(50)
                    progress.update(task, advance=1)
            
            progress.stop_task(task)
            progress.stop()
                
                
        def start(self,layers):
            lodestone.logger.info(f"Building cactus farm...\n{layers * 9}x sand\n{layers * 9}x cactus\n{layers * 9}x dirt\n{layers * 6}x iron bars")
            self.__cactus(layers)
            lodestone.logger.info("Done building cactus farm")
            # _thread = threading.Thread(target=self.__cactus, args=[layers])
            # _thread.start()