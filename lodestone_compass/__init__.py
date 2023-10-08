import discord
from discord import ApplicationContext as Context
from discord import Embed
from discord import EmbedField
from dotenv import load_dotenv
from os import environ
from javascript import eval_js as js_eval
from javascript.errors import JavaScriptError
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
    try:
        result = js_eval(code)
    except JavaScriptError as e:
        result = None
        error = e.js
        if len(error) > 1024: error = error[:1024]
        error_py = e.py
        if not isinstance(error_py, type(None)):
            if len(error_py) > 1024: error_py = error_py[:1024]

    embed = Embed(
        title="**Evaluating Javascript!**",
        description=f"""
        Evaluating:
        ```javascript
        {code}
        ```
        """)
    if result is not None:
        embed.add_field(name="result", value=str(result))
        embed.add_field(name="return type", value=type(result))
    else:
        embed.add_field(name="**ERROR**", value=error)
        embed.add_field(name="**ERROR (Python Side)**", value=error_py)
    await ctx.respond(embed=embed)

compass.run(environ["TOKEN"])