import lodestone

class RPC:
    """
    Example plugin example used to test stuff and extent Lodestone's functionalities
    """
    def __init__(self, bot: lodestone.Bot):
        "The injection method"
        plugins_loaded = list(bot.loaded_plugins.keys())
        plugins_loaded.append(self.__class__.__name__)
        bot.emit('plugin_loaded', *plugins_loaded)
