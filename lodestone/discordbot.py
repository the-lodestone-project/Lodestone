import discord
from discord import app_commands
import lodestone
import traceback
import time
import asyncio
import datetime
from discord import Embed


class MyClient(discord.Client):
    def __init__(self) -> None:
        # Just default intents and a `discord.Client` instance
        # We don't need a `commands.Bot` instance because we are not
        # creating text-based commands.
        intents = discord.Intents.default()
        super().__init__(intents=intents)

        # We need an `discord.app_commands.CommandTree` instance
        # to register application commands (slash commands in this case)
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')

    async def setup_hook(self) -> None:
        # Sync the application command with Discord.
        await self.tree.sync()


def checkStatus(bot):
    try:
        _ = bot.bot.players
        return True
    except:
        return False


def embedMaker(title:str, description:str="", color=0x3498db):
    embedVar = Embed(title=title, description=description, color=color)
    embedVar.timestamp = datetime.datetime.utcnow()
    embedVar.set_footer(text='\u200b',icon_url="https://github.com/SilkePilon/OpenDeliveryBot/blob/main/chestlogo.png?raw=true")
    return embedVar


class Create(discord.ui.Modal, title='Create A Bot'):
    # Our modal classes MUST subclass `discord.ui.Modal`,
    # but the title can be whatever you want.

    # This will be a short input, where the user can enter their name
    # It will also have a placeholder, as denoted by the `placeholder` kwarg.
    # By default, it is required and is a short-style input which is exactly
    # what we want.
    email = discord.ui.TextInput(
        label='Minecraft Email',
        placeholder='example@gmail.com',
    )
    host = discord.ui.TextInput(
        label='Server Ip',
        placeholder='2b2t.org',
    )
    port = discord.ui.TextInput(
        label='Server Port',
        placeholder='25565',
    )
    version = discord.ui.TextInput(
        label='Minecraft Version',
        placeholder='1.20',
    )
    

    # This is a longer, paragraph style input, where user can submit feedback
    # Unlike the name, it is not required. If filled out, however, it will
    # only accept a maximum of 300 characters, as denoted by the
    # `max_length=300` kwarg.
    # feedback = discord.ui.TextInput(
    #     label='What do you think of this new feature?',
    #     style=discord.TextStyle.long,
    #     placeholder='Type your feedback here...',
    #     required=False,
    #     max_length=300,
    # )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        global mcbot
        mcbot = lodestone.createBot(host=self.host.value, port=self.port.value, username=self.email.value, version=self.version.value, enableChatLogging=True)
        maxLoops = 0
        while mcbot.msa_status == False:
            if maxLoops >= 15:
                await interaction.followup.send(ephemeral=True, embed=embedMaker(title="Succsessfuly logged in!"))
                break
            await asyncio.sleep(1) # Doing stuff
            maxLoops += 1
        if mcbot.msa_status == True:
            await interaction.followup.send(ephemeral=True, embed=embedMaker(title="It seems you are not logged in", description=f"Please go to **https://microsoft.com/link** and enter the following code: **{mcbot.msa_data['user_code']}**", color=0x992d22))
        mcbot.start()
        

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.channel.send(embed=embedMaker(title="Oops! Something went wrong.", color=0x992d22))

        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)

class History(discord.ui.Modal, title='Chat History'):
    # Our modal classes MUST subclass `discord.ui.Modal`,
    # but the title can be whatever you want.

    # This will be a short input, where the user can enter their name
    # It will also have a placeholder, as denoted by the `placeholder` kwarg.
    # By default, it is required and is a short-style input which is exactly
    # what we want.
    username = discord.ui.TextInput(
        label='Player Username',
        placeholder='Notch',
    )
    server = discord.ui.TextInput(
        label='Server Database',
        placeholder='2b2t.org',
    )

    # This is a longer, paragraph style input, where user can submit feedback
    # Unlike the name, it is not required. If filled out, however, it will
    # only accept a maximum of 300 characters, as denoted by the
    # `max_length=300` kwarg.
    # feedback = discord.ui.TextInput(
    #     label='What do you think of this new feature?',
    #     style=discord.TextStyle.long,
    #     placeholder='Type your feedback here...',
    #     required=False,
    #     max_length=300,
    # )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            history = mcbot.chatHistory(username=f"{self.username.value}", server=f"{self.server.value}")
            if history is None:
                history = f"{self.username.value} has no chat history"
        except Exception as e:
            history = str(e)
        
        await interaction.followup.send(ephemeral=True, embed=embedMaker(title=f"{self.username.value}'s chat history", description=f"{history}"))
        
        

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.channel.send(embed=embedMaker(title="Oops! Something went wrong.", color=0x992d22))

        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)
        
        
client = MyClient()


@client.tree.command(description="Create a bot")
async def create(interaction: discord.Interaction):
    # Send the modal with an instance of our `Feedback` class
    # Since modals require an interaction, they cannot be done as a response to a text command.
    # They can only be done as a response to either an application command or a button press.
    await interaction.response.send_modal(Create())
    
@client.tree.command(description="Get a players chat history")
async def history(interaction: discord.Interaction):
    # Send the modal with an instance of our `Feedback` class
    # Since modals require an interaction, they cannot be done as a response to a text command.
    # They can only be done as a response to either an application command or a button press.
    try:
        print(mcbot.bot.username)
        await interaction.response.send_modal(History())
    except:
        await interaction.response.send_message(embed=embedMaker(title="No running bot instances", description="Please Create a bot using **/create**", color=0x992d22))


client.run('')