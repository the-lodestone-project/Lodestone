import lodestone

class RPCPlugin:
    """
    Example plugin example used to add Discord Rich Presence to your bot
    """
    def __init__(self, bot: lodestone.Bot):
        "The injection method"
        self.bot = bot
        self.internal_bot = bot.bot
