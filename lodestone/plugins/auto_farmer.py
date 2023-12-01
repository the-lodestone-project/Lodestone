# needs to be converted to a plugin


import lodestone
import time

bot = lodestone.createBot(
    host='0.tcp.ap.ngrok.io',
    username='farmer',
    auth='offline',
    port=14995,
    version='1.19',
    ls_skip_checks=True
)

password = 'password'
menu_item_id = 'birch_sapling'
borken_counter = 0
scan_radius = 500

# @bot.on('spawn')
def start():
    global borken_counter
    # bot.chat(f'/login {password}')
    # time.sleep(3)
    # bot.chat('/menu')
    # @bot.once('windowOpen')
    # def on_window_open(window):
    #     boats = [x for x in window.slots if x is not None and x.displayName == menu_item_id]
    #     mouseButton = 0  # 0: left click, 1: right click
    #     mode = 0  # 0: single click
    #     bot.clickWindow(boats[0].slot, mouseButton, mode)
    # time.sleep(10)
    blockType = bot.bot.registry.blocksByName["sugar_cane"]
    def blockToHarvest(search_range=4, amount=1):
        curr_amount = 0
        sugarcaneBlocks = bot.bot.findBlocks({
            'matching': blockType.id,
            'count': scan_radius,
            'maxDistance': search_range,
            'useExtraInfo': False,
        })
        if len(sugarcaneBlocks.valueOf()) == 0:
            print("nah im good")
        breakableSugarCane = []
        for i in sugarcaneBlocks:
            print(i)
            if curr_amount == amount:
                return breakableSugarCane
            # stuff here
            idkblock = bot.bot.blockAt(i)
            belowBlock = bot.bot.blockAt(idkblock.position.offset(0, -1, 0))
            if not belowBlock or belowBlock.name != "sugar_cane":
                continue
            breakableSugarCane.append(idkblock)
            curr_amount += 1

    input('press enter to start')
    while True:
        blocks = blockToHarvest(amount=10)
        if blocks != None:
            for target in blocks:
                print(target.position)
                try:
                    bot.bot.dig(target, {'forceLook':True})
                    borken_counter += 1
                except Exception as e:
                    print(e)
                    print('error collecting reeds')
                    continue
        else:
            blocks = blockToHarvest(amount=1, search_range=100)
            if blocks:
                for target in blocks:
                    print(target.position)
                    try:
                        bot.goto(target.position.x, target.position.y, target.position.z)
                        bot.bot.dig(target, {'forceLook':False})
                        borken_counter += 1
                    except Exception as e:
                        print(e)
                        print('error collecting reeds')
                        continue
        time.sleep(0.5)
        
start()
    
