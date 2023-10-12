import lodestone
import sys
import math


if len(sys.argv) < 3 or len(sys.argv) > 5:
    print("Usage : python bee.py <host> <port> [<name>] [<password>]")
    quit(1)

bot = lodestone.Bot(
    host = sys.argv[1],
    port = int(sys.argv[2]),
    username = sys.argv[3] if len(sys.argv) > 3 else 'bee',
    password = sys.argv[4] if len(sys.argv) > 4 else ''
)

print(dir(bot))

def loop(n):
    for i in range(n):
        position = bot.entity.position
        bot.creative.fly_to(position.offset(
            math.sin(i) * 2,
            0.5,
            math.cos(i) * 2
        ))
    bot.chat("My flight was amazing!")

@bot.on("chat")
def chat(_, username, message):
    if username == bot.username: return
    match message:
        case "loaded":
            bot.bot.waitForChunksToLoad()
            bot.chat("Ready!")
        case "fly":
            bot.command("creative")
            bot.creative.start_flying()
            loop(10)

