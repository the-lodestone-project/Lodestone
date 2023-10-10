import discord
from discord import ApplicationContext as Context
from discord import Embed
from discord import EmbedField
from dotenv import load_dotenv
from os import environ
from javascript import eval_js as js_eval
from javascript import console as js_console
from javascript.errors import JavaScriptError

js_console = js_console

load_dotenv()

compass = discord.Bot()

@compass.event
async def on_ready():
    print("ready")

@compass.slash_command()
async def ping(ctx: Context):
    await ctx.respond(ephemeral=False, embed=Embed(
        title="**Pong! :ping_pong:**",
        description=f"The API ping is currently at *{round(compass.latency * 1000)} ms*."
    ))

@compass.slash_command()
async def eval_js(ctx: Context, code: str):
    global js_console
    try:
        console = []
        class Console:
            @staticmethod
            def log(*things):
                console.append(" ".join(things))

            @staticmethod
            def warn(*things):
                console.append("```ansi\n\x1b[43m" + " ".join(things) + "\n```")

            @staticmethod
            def clear():
                for i in range(len(console)):
                    del console[i]

            @staticmethod
            def debug(*objects):
                Console.log(*objects)

            @staticmethod
            def info(*things):
                console.append("```ansi\n\x1b[46m" + " ".join(things) + "\n```")

            @staticmethod
            def error(*things):
                console.append("```ansi\n\x1b[41m" + " ".join(things) + "\n```")

        js_console = Console
        js_console.log("Console initalized")

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
        embed.add_field(name="result", value="```ansi\n" + str(result) + "\n```")
        embed.add_field(name="return type", value=type(result))
        embed.add_field(name="console", value="\n\n".join(console))
    else:
        embed.add_field(name="**ERROR**", value="```ansi\n" + error + "\n```")
        embed.add_field(name="**ERROR (Python Side)**", value=error_py)
    await ctx.respond(embed=embed)

compass.run(environ["TOKEN"])