try: 
    import discord
    from discord import ApplicationContext as Context
    from discord import Embed
    from discord.ui import Modal, InputText
    from discord import InputTextStyle, Interaction
except:
    pass
from dotenv import load_dotenv
from os import environ
from javascript import eval_js as js_eval
from javascript.errors import JavaScriptError

load_dotenv()

compass = discord.Bot()

class InputCode(Modal):
    def __init__(self, context: Context, *args, **kwargs):
        super().__init__(*args, **kwargs, title="Input Javascript Code")
        self.add_item(InputText(label="code", style=InputTextStyle.long, placeholder="console.log(\"This is awesome!\")", required=True))
        self.context = context

    async def callback(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        await eval_js_internal(self.context, self.children[0].value)

@compass.event
async def on_ready():
    print("ready")

@compass.slash_command(help="Pings the server")
async def ping(ctx: Context):
    await ctx.respond(ephemeral=False, embed=Embed(
        title="**Pong! :ping_pong:**",
        description=f"The API ping is currently at *{round(compass.latency * 1000)} ms*."
    ))

@compass.slash_command(help="Executes JavaScript code using JSE")
async def eval_js(ctx: Context):
    await ctx.send_modal(InputCode(ctx))

@compass.slash_command(help="#general is a bit cluttered with contributors!")
async def contributors_contribute(ctx: Context):
    await ctx.respond(embed=Embed(
        title="Contributors Contribute",
        description="Guys let's keep project contribution discussion in <#1160305403217858660>!"
    ))

async def eval_js_internal(ctx: Context, code: str):
    try:
        console__ = []
        class Console:
            @staticmethod
            def to_string(thing):
                return str(thing)

            @staticmethod
            def log(*things):
                console__.append(" ".join(Console.to_string(things)))

            @staticmethod
            def warn(*things):
                console__.append("\x1b[43m" + " ".join(Console.to_string(things)))

            @staticmethod
            def clear():
                for i in range(len(console__)):
                    del console__[i]

            @staticmethod
            def debug(*objects):
                Console.log(Console.to_string(objects))

            @staticmethod
            def info(*things):
                console__.append("\x1b[46m" + " ".join(Console.to_string(things)))

            @staticmethod
            def error(*things):
                console__.append("\x1b[41m" + " ".join(Console.to_string(things)))

        console = Console

        result = js_eval(code)
        error = "no errors"
    except JavaScriptError as e:
        result = None
        error = e.js
        if len(error) > 1012:
            error = error[:1012]
        error_py = e.py
        if not isinstance(error_py, type(None)):
            if len(error_py) > 1012:
                error_py = error_py[:1012]

    embed = Embed(
        title="**Evaluating Javascript!**",
        description=f"""
Evaluating:
```javascript
{code}
```
""")
    if error == "no errors":
        embed.add_field(name="result", value="```ansi\n" + (str(result) if result else " ") + "\n```", inline=False)
        embed.add_field(name="return type", value=type(result), inline=False)
        embed.add_field(name="console", value="```ansi\n" + ("\n".join(console__) if console__ else " ") + "\n```", inline=False)
    else:
        embed.add_field(name="**ERROR**", value="```ansi\n" + error + "\n```", inline=False)
        embed.add_field(name="**ERROR (Python Side)**", value=error_py, inline=False)
        embed.add_field(name="console", value="```ansi\n" + ("\n".join(console__) if console__ else " ") + "\n```", inline=False)
    await ctx.respond(embed=embed)

compass.run(environ["TOKEN"])