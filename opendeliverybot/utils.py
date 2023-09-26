import time
from javascript import require
import json
import structlog
from rich.console import Console
import g4f
import asyncio
from claude_api import Client
logger = structlog.get_logger()
console = Console()

def llm(input:str, data=""):
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


def claude(input:str, cookie:str, data="", conversation_id=""):
    claude_api = Client(cookie)
    conversation_id = conversation_id or claude_api.create_new_chat()['uuid']
    with console.status(f"[bold green][CLAUDE] Please wait...\n") as status:
        try:
            response = claude_api.send_message(f"question about provided data: {input} data: {data} USE THIS DATA TO AWNSER THE QUESTION, KEEP IT SHORT, DONT USE USERNAMES AS A BASES FOR A AWNSER", conversation_id)
            return response
        except:
            logger.warning(f"[LLM] Claude is not available. This may be because you reached your message limit")