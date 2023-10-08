
# A simple bot that logs everything that is said to the console.

import lodestone
import sys

if len(sys.argv) < 4 or len(sys.argv) > 6:
    print('Usage : python ansi.py <host> <port> [<name>] [<password>]')
    sys.exit(1)

bot = lodestone.createBot(
    host=sys.argv[1],
    port=int(sys.argv[2]),
    username=sys.argv[3] if len(sys.argv) > 3 else 'ansi',
    password=sys.argv[4] if len(sys.argv) > 4 else None
)

@lodestone.Event(bot.bot, 'messagestr')
def chat(this, message, messagePosition, jsonMsg, sender, *args):
    message = str(message).replace("\n\n","")
    print(f"{sender}: {message}")
