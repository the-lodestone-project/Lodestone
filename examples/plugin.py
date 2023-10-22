import lodestone
from lodestone import plugin_template

import sys


if len(sys.argv) < 3 or len(sys.argv) > 5:
    print(f"Usage : python {sys.argv[0]} <host> <port> [<name>] [<password>]")
    quit(1)

bot = lodestone.Bot(host=sys.argv[1], port=int(sys.argv[2]), password=sys.argv[4] if len(sys.argv) > 4 else '',
                    username=sys.argv[3] if len(sys.argv) > 3 else 'plugin')

@bot.on("plugin_load")
def loaded(_, plugin):
    bot.chat("Loaded Plugin!", plugin)

bot.load_plugin(plugin_template.Plugin)
