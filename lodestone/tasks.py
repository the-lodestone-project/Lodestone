import lodestone
import time
import asyncio
from queue import PriorityQueue
class Idkwhattocallthis:
    def __init__(self, bot: lodestone.bot):
        self.bot = bot
        self.__create_tree()
        self.__create_priority_queues()
        self.__add_tasks()
        self.__start()
        
    
    
    
    class create_task:
        def __init__(self, item_or_block, amount=1, obtain=None,craft=None):
            self.obtain = obtain
            self.craft = craft
            self.bot = Idkwhattocallthis.bot
            self.amount = amount
            self.item_or_block = item_or_block
            self.dependencies = []
            self.completed = False
            
        def add_dependency(self, task):
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

            
            if self.obtain:
                self.bot.collect_block(f"{self.item_or_block}", amount=amount, max_distance=100)
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

    
    def __create_tree(self):
        # Create sample tree

        self.wood = self.create_task(obtain=True, item_or_block="oak_log", bot=self.bot, amount=1)

        self.make_planks = self.create_task(action="craft", item_or_block="oak_planks", bot=self.bot)
        self.make_planks.add_dependency(self.chop_wood)

        self.make_stick = self.create_task(action="craft", item_or_block="stick", bot=self.bot)
        self.make_stick.add_dependency(self.make_planks)

        self.make_pickaxe = self.create_task(action="craft", item_or_block="wooden_pickaxe", bot=self.bot)
        self.make_pickaxe.add_dependency(self.make_planks)
        self.make_pickaxe.add_dependency(self.make_stick)

    
    def __create_priority_queues(self):
        # Create priority queues

        self.urgent_tasks = PriorityQueue()
        self.normal_tasks = PriorityQueue()


    def __add_tasks(self):
        # Add tasks 

        # urgent_tasks.put(10, defend_task)
        self.normal_tasks.put((5, self.make_pickaxe))


    def __process_tasks(self):
        if self.urgent_tasks.empty():
            task = self.normal_tasks.get()
        else:
            task = self.urgent_tasks.get()

        self.gather(task[1])

    # Gather function 

    def __gather(self, task: create_task):
        if task.is_available():
            task.complete()
            return

        dep = task.get_next_task()
        self.gather(dep)
        self.gather(task)

    # Main bot loop
    def __start(self):
        while not self.normal_tasks.empty() or not self.urgent_tasks.empty():
            self.__process_tasks()
        print("DONE!")