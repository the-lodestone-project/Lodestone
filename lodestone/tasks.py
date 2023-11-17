import lodestone
import time
import asyncio
from queue import PriorityQueue
class Idkwhattocallthis:
    def __init__(self, bot: lodestone.bot):
        self.bot = bot
        self.create_tree()
        self.create_priority_queues()
        self.add_tasks()
        self.start()
    
    class TreeTask:
        def __init__(self, action, item_or_block, bot: lodestone.bot, craft_count=1):
            self.action = action
            self.bot = bot
            self.craft_count = craft_count
            self.item_or_block = item_or_block
            self.dependencies = []
            self.completed = False
            
        def add_dependency(self, task, craft_count=1):
            task.craft_count = craft_count
            print(task.craft_count)
            self.dependencies.append(task)

        def is_available(self):
            return all(d.completed for d in self.dependencies)

        def get_next_task(self):
            return next(d for d in self.dependencies if not d.completed)
        
        def complete(self):
            print(f"Completing task: {self.item_or_block}")
            if self.action == "craft":
                try:
                    crafting_table = self.bot.bot.findBlocks({ 'matching': self.bot.bot.registry.blocksByName['crafting_table'].id, 'maxDistance': 20, 'count': 1 })[0]
                
                except:
                    print("error")
                    exit()
                self.bot.bot.pathfinder.goto(self.bot.pathfinder.goals.GoalNear(crafting_table.x, crafting_table.y, crafting_table.z, 1), timeout=600000000)
                while self.bot.pathfinder.isMoving:
                    time.sleep(1)
                print(self.craft_count)
                amount = int(self.craft_count)
                item = self.bot.bot.registry.itemsByName[self.item_or_block]
                craftingTableID = self.bot.bot.registry.blocksByName.crafting_table.id
                craftingTable = self.bot.bot.findBlock({
                    'matching': craftingTableID
                })
                if item:
                    recipe = self.bot.bot.recipesFor(item.id, None, 1, craftingTable)[0]
                    if recipe:
                        self.bot.bot.chat(f"I can make {self.item_or_block}")
                        try:
                            self.bot.bot.craft(recipe, amount, craftingTable)
                            self.bot.bot.chat(f"did the recipe for {self.item_or_block} {amount} times")
                        except Exception as err:
                            self.bot.bot.chat(f"error making {self.item_or_block}")
                    else:
                        self.bot.bot.chat(f"I cannot make {self.item_or_block}")
                else:
                    self.bot.bot.chat(f"unknown item: {self.item_or_block}")

            
            if self.action == "break":
                # Get the correct block type
                blockType = self.bot.bot.registry.blocksByName[self.item_or_block]
                if not blockType:
                    self.bot.bot.chat("I don't know any blocks with that name.")
                    return
                self.bot.bot.chat('Collecting the nearest ' + blockType.name)
                # Try and find that block type in the world
                def find_block():
                    block = self.bot.bot.findBlock({ 'matching': blockType.id, 'maxDistance': 64})
                    return block
                block = find_block()
                if not block:
                    self.bot.bot.chat("I don't see that block nearby.")
                    return
                # Collect the block if we found one
                self.bot.bot.collectBlock.collect(block)
            self.completed = True

        # Priority queues 

    class PriorityQueue:
        def __init__(self):
            self.queue = PriorityQueue()

        def put(self, priority, task):
            self.queue.put((priority, task))
        
        def get(self):
            return self.queue.get()[1]

        def empty(self):
            return self.queue.empty()

    
    def create_tree(self):
        # Create sample tree

        self.chop_wood = self.TreeTask(action="break", item_or_block="oak_log", bot=self.bot)

        self.make_planks = self.TreeTask(action="craft", item_or_block="oak_planks", bot=self.bot)
        self.make_planks.add_dependency(self.chop_wood)

        self.make_stick = self.TreeTask(action="craft", item_or_block="stick", bot=self.bot)
        self.make_stick.add_dependency(self.make_planks)

        self.make_pickaxe = self.TreeTask(action="craft", item_or_block="wooden_pickaxe", bot=self.bot)
        self.make_pickaxe.add_dependency(self.make_planks)
        self.make_pickaxe.add_dependency(self.make_stick)

    
    def create_priority_queues(self):
        # Create priority queues

        self.urgent_tasks = PriorityQueue()
        self.normal_tasks = PriorityQueue()


    def add_tasks(self):
        # Add tasks 

        # urgent_tasks.put(10, defend_task)
        self.normal_tasks.put((5, self.make_pickaxe))


    def process_tasks(self):
        if self.urgent_tasks.empty():
            task = self.normal_tasks.get()
        else:
            task = self.urgent_tasks.get()

        self.gather(task[1])

    # Gather function 

    def gather(self, task: TreeTask):
        if task.is_available():
            task.complete()
            return

        dep = task.get_next_task()
        self.gather(dep)
        self.gather(task)

    # Main bot loop
    def start(self):
        while not self.normal_tasks.empty() or not self.urgent_tasks.empty():
            self.process_tasks()
        print("DONE!")