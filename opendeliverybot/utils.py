import time
from javascript import require
import json
import structlog
from rich.console import Console
import g4f
import asyncio
logger = structlog.get_logger()
console = Console()

def LLM(input:str, data=""):
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
    output.append({"base": defualt})
    return output