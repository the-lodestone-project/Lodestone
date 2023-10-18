import lodestone
from lodestone import plugin_template

import sys


if len(sys.argv) < 3 or len(sys.argv) > 5:
    print("Usage : python bee.py <host> <port> [<name>] [<password>]")
    quit(1)

bot = lodestone.Bot(host=sys.argv[1], port=int(sys.argv[2]), password=sys.argv[4] if len(sys.argv) > 4 else '',
                    username=sys.argv[3] if len(sys.argv) > 3 else 'bee')

@bot.on("plugin_loaded")
def loaded(_, *plugins):
    bot.chat("Plugins loaded!", ", ".join(plugins))

bot.load_plugin(plugin_template.Plugin)
