#
# This example demonstrates how to use anvils w/ mineflayer
#  the options are: (<Option> are required, [<Option>] are optional)
# 1. "anvil combine <itemName1> <itemName2> [<name>]"
# 2. "anvil rename <itemName> <name>"
#
# to use this:
# /op anvilman
# /gamemode anvilman creative
# /xp set anvilman 999 levels
#
# Put an anvil near the bot
# Give him a sword and an enchanted book
# say list
# say xp
# say anvil combine diamond_sword enchanted_book
#
import lodestone

import sys

if len(sys.argv) < 4 or len(sys.argv) > 6:
    print('Usage : python anvil.py <host> <port> [<name>] [<password>]')
    sys.exit(1)

bot = lodestone.createBot(
    host=sys.argv[1],
    port=int(sys.argv[2]),
    username=sys.argv[3] if len(sys.argv) > 3 else 'anvilman',
    password=sys.argv[4] if len(sys.argv) > 4 else None
)

def sayItems():
    bot.chat('/list')

def tossItem(item):
    bot.chat('/toss ' + item)

def combine(bot, firstSlot, secondSlot):
    bot.chat('/anvil combine ' + firstSlot + ' ' + secondSlot)

@bot.event
def on_chat(username, message):
    command = message.split(' ')
    if message == 'list':
        sayItems()
    elif message.startswith('toss '):
        tossItem(command[1])
    elif message == 'xp':
        bot.chat(str(bot.experience.level))
    elif message == 'gamemode':
        bot.chat(bot.game.gameMode)
    elif message.startswith('anvil combine '):
        if len(command) == 4:
            combine(bot, command[2], command[3])
        elif len(command) == 5:
            combine(bot, command[2], command[3] + ' ' + command[4])
