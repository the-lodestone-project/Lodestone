import lodestone
import re
try:
    from discord import SyncWebhook, Embed
except:
    pass
import datetime
from types import FunctionType

class DiscordWebhook:
    def __init__(self, bot: lodestone.Bot):
        "The injection method"
        self.bot = bot
        self.webhook_url = None
        self.bot_log: FunctionType = self.bot.log
        self.bot_log = FunctionType(
            self.bot_log.__code__,
            self.bot_log.__globals__,
            self.bot_log.__name__,
            self.bot_log.__defaults__,
            self.bot_log.__closure__
        )
        self.bot_log.__dict__.update(self.bot.log.__dict__)
        self.thread = 0

    def set_webhook(self, webhook_url, use_discord_forums = False):
        self.webhook_url = webhook_url
        self.bot.emit("discord_webhook", "Webhook set up!", use_discord_forums)

    def log(self, message, icon="🤖", error=False, info=False, warning=False, chat=False, console=True):
        self.bot_log(message, icon, error, info, warning, chat, console)
        self.send_discord(message, True)

    def send_discord(self, message: str, thread = None):
        if self.webhook_url is None or not re.fullmatch("(https://|http://|)(canary.|ptb.|www\.|)discord.com/api/webhooks/\d+/[a-zA-Z-0-9]+", self.webhook_url):
            raise ValueError(
                "Webhook URL is missing or invalid"
            )
        hook = SyncWebhook.from_url(url=self.webhook_url)  # connect to the webhook

        color = 0x3498db
        embed = Embed(title="", description=f"**{message}**", color=color)  # make the embed
        embed.timestamp = datetime.datetime.utcnow()

        try:
            avatar_url = f"https://mc-heads.net/avatar/{self.bot.username}/600.png"
            embed.set_footer(text=f'{self.bot.username}',
                             icon_url=avatar_url)  # set the footer image to the players head
        except:
            avatar_url = "https://github.com/Project-Lodestone/Lodestone/blob/main/chestlogo.png?raw=true"
            embed.set_footer(text='\u200b',
                             icon_url=avatar_url)  # fallback footer image

        if thread:
            if isinstance(thread, str):
                self.thread = hook.send(content="", thread_name=f"{thread}", username="Lodestone",
                          avatar_url=avatar_url,
                          embed=embed, wait=True).thread  # send the message in a forums channel
            else:
                self.thread = hook.send(content="", thread=self.thread, username="Lodestone",
                                        avatar_url=avatar_url,
                                        embed=embed, wait=True).thread  # send the message in a forums channel
        else:
            hook.send(content=f" ", username="Lodestone",
                      avatar_url=avatar_url,
                      embed=embed)  # send the message in a normal channel

    def on_discord_webhook(self, message: str, use_discord_forums: bool = False):
        today = datetime.date.today()
        self.send_discord(message, f"{today}" if use_discord_forums else None)
