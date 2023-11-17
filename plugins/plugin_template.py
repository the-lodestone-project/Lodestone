import lodestone

class Plugin:
    """
    Example plugin example used to test stuff and extent Lodestone's functionalities
    """
    def __init__(self, bot: lodestone.Bot):
        "The injection method"
        self.bot = bot
        self.internal_bot = bot.bot
