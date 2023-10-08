import time
import discord
import aiohttp
from javascript import require
import json
import structlog
from functools import wraps
from rich.console import Console
import g4f
import asyncio
logger = structlog.get_logger()
console = Console()

def llm(input: str, data = ""):
    _providers = [
        g4f.Provider.Bing,
        g4f.Provider.DeepAi,
        g4f.Provider.GptGo,
        g4f.Provider.Bard
        
    ]

    output = []


    async def run_provider(provider: g4f.Provider.AsyncProvider):
    
        try:
            response = await provider.create_async(
                model=g4f.models.default.name,
                messages=[{"role": "user", "content": f"question about provided data: {input} data: {data} USE THIS DATA TO AWNSER THE QUESTION, KEEP IT SHORT"}],
            )
            output.append({provider.__name__: response})
        except Exception as e:
            logger.warning(f"[LLM] {provider.__name__} is not available.")

    async def run_all():
        calls = [
            run_provider(provider) for provider in _providers
        ]
        await asyncio.gather(*calls)
    with console.status(f"[bold green][LLM] Please wait...\n") as status:
        asyncio.run(run_all())
        
    defualt = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        messages=[{"role": "user", "content": f"question about provided data: {input} data: {data} USE THIS DATA TO AWNSER THE QUESTION, KEEP IT SHORT"}],
    )  # alterative model setting
    if "<!DOCTYPE html>" in defualt: 
        logger.warning(f"[LLM] defualt is not available. Trying another...")
        defualtnew = g4f.ChatCompletion.create(
            model=g4f.models.gpt_35_turbo,
            messages=[{"role": "user", "content": f"question about provided data: {input} data: {data} USE THIS DATA TO AWNSER THE QUESTION, KEEP IT SHORT"}],
        )  # alterative model setting
        output.append({"base": defualtnew})
    else:
        output.append({"base": defualt})
    return output

# def claude(input: str, cookie: str, data = "", conversation_id = ""):
#     claude_api = Client(cookie)
#     conversation_id = conversation_id or claude_api.create_new_chat()['uuid']
#     with console.status(f"[bold green][CLAUDE] Please wait...\n") as status:
#         try:
#             response = claude_api.send_message(f"question about provided data: {input} data: {data} USE THIS DATA TO AWNSER THE QUESTION, KEEP IT SHORT, DONT USE USERNAMES AS A BASES FOR A AWNSER", conversation_id)
#             return response
#         except:
#             logger.warning(f"[LLM] Claude is not available. This may be because you reached your message limit")

def convert_case(string, case = "pascal"):
    match case:
        case "snake":
            new = []
            for seq in string.split("_"):
                new.append(seq.lower())
            name = "_".join(new)
        case "camel":
            new = []
            for seq in string.split("_"):
                new.append(seq.title())
            name = "".join(new)
        case "pascal":
            new = []
            one = True
            for seq in string.split("_"):
                new.append(seq.lower() if one else seq.title())
                one = False
            name = "".join(new)
        case _:
            name = string
    return name

def cprop(cap = "pascal", proxy_name = ""):
    def decorator(func):
        @property
        def wrapped(self):
            name = proxy_name
            if not name:
                name = convert_case(func.__name__, cap)
            return getattr(self.proxy, name)
        return wrapped
    return decorator

def send_webhook(webhook, *args, **kwargs):
    async def send_webhook__(webhook, *args, **kwargs):
        async with aiohttp.ClientSession() as session:
            await discord.Webhook.from_url(webhook, session=session).send(*args, **kwargs)

    return asyncio.run(send_webhook__(webhook, *args, **kwargs))
