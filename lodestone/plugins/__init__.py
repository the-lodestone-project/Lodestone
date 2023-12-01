from .cactus_farm_builder import cactus
from .discord_webhook import discord
from .schematic_builder import schematic
from .discordrp import discordrp

class plugins:
    def __init__(self):
        self.cactus = cactus()
        self.discordrp = discordrp()
        self.discord = discord()
        self.schematic = schematic()
        super().__init__()
