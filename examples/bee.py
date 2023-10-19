from javascript.errors import JavaScriptError
import lodestone

import sys
import math


if len(sys.argv) < 3 or len(sys.argv) > 5:
    print(f"Usage : python {sys.argv[0]} <host> <port> [<name>] [<password>]")
    quit(1)

bot = lodestone.Bot(host=sys.argv[1], port=int(sys.argv[2]), password=sys.argv[4] if len(sys.argv) > 4 else '',
                    username=sys.argv[3] if len(sys.argv) > 3 else 'bee')

def loop(n):
    for i in range(n):
        position = bot.entity.position
        bot.creative.fly_to(position.offset(
            math.sin(i) * 2,
            0.5,
            math.cos(i) * 2
        ))
    bot.chat("My flight was amazing!")
    bot.creative.stop_flying()

@bot.on("chat")
def chat(_, username, message, *args):
    if username == bot.username: return
    match message:
        case "loaded":
            bot.bot.waitForChunksToLoad()
            bot.chat("Ready!")
        case "fly":
            bot.command("creative")
            bot.creative.start_flying()
            try:
                loop(10)
            except JavaScriptError:
                bot.chat("An error occurred!")
                bot.creative.stop_flying()

