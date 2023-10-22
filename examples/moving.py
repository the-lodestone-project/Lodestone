import lodestone

import sys
import time


class MovementPlugin:
    """
    Simple plugin that adds movements to theh bot!
    """
    def __init__(self, bot: lodestone.Bot):
        "The injection method"
        self.bot = bot
        self.internal_bot = bot.bot

        @bot.add_method()
        def forward(hold_time=1):
            """
            Holds the "W" key for hold_time seconds
            """
            self.bot.set_control_state("forward", True)
            time.sleep(hold_time)
            self.bot.set_control_state("forward", False)

        @bot.add_method()
        def backward(hold_time=1):
            """
            Holds the "S" key for hold_time seconds
            """
            self.bot.set_control_state("back", True)
            time.sleep(hold_time)
            self.bot.set_control_state("back", False)

        @bot.add_method()
        def left(hold_time=1):
            """
            Holds the "A" key for hold_time seconds
            """
            self.bot.set_control_state("left", True)
            time.sleep(hold_time)
            self.bot.set_control_state("left", False)

        @bot.add_method()
        def right(hold_time=1):
            """
            Holds the "D" key for hold_time seconds
            """
            self.bot.set_control_state("right", True)
            time.sleep(hold_time)
            self.bot.set_control_state("right", False)

        @bot.add_method()
        def jump():
            """
            Make the bot jump
            """
            self.bot.set_control_state("jump", True)
            time.sleep(0.2)
            self.bot.set_control_state("jump", False)

        @bot.add_method()
        def start_sneak():
            """
            Make the bot start sneaking
            """
            self.bot.set_control_state("sneak", True)

        @bot.add_method()
        def stop_sneak():
            """
            Make the bot stop sneaking
            """
            self.bot.set_control_state("sneak", False)

        @bot.add_method()
        def halt():
            """
            Halts all movement
            """
            self.bot.clear_control_states()


if len(sys.argv) < 3 or len(sys.argv) > 5:
    print(f"Usage : python {sys.argv[0]} <host> <port> [<name>] [<password>]")
    quit(1)

bot = lodestone.Bot(host=sys.argv[1], port=int(sys.argv[2]), password=sys.argv[4] if len(sys.argv) > 4 else '',
                    username=sys.argv[3] if len(sys.argv) > 3 else 'moving')

@bot.on("plugin_load")
def loaded(_, plugin):
    bot.chat("Loaded Plugin!", plugin)

@bot.on("chat")
def chat(_, username: str, message: str, *args):
    if username == bot.username: return
    if message.count(" ") < 1: return
    cmd, *args = message.split()
    if cmd in ('forward', 'backward', 'left', 'right'):
        try:
            arg = int(args[0])
            if arg < 1:
                bot.chat("Argument out of range of 1 < x")
                return
        except ValueError:
            bot.chat("Argument must be a number")
            return
    elif cmd in ('jump', 'sneak', 'unsneak', 'halt'):
        arg = None
    else:
        return

    match cmd:
        case 'forward':
            bot.forward(arg)
        case 'backward':
            bot.backward(arg)
        case 'left':
            bot.left(arg)
        case 'right':
            bot.right(arg)
        case 'jump':
            bot.jump()
        case 'sneak':
            bot.start_sneak()
        case 'unsneak':
            bot.stop_sneak()
        case 'halt':
            bot.halt()

bot.load_plugin(MovementPlugin)
