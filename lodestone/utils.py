import discord
import requests
import structlog
from rich.console import Console
import asyncio
logger = structlog.get_logger()
console = Console()

def llm(input: str, data = ""):
    import g4f
    _providers = [
        g4f.Provider.Bing,
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
        except Exception:
            logger.warning(f"[LLM] {provider.__name__} is not available.")

    async def run_all():
        calls = [
            run_provider(provider) for provider in _providers
        ]
        await asyncio.gather(*calls)
    with console.status(f"[bold green][LLM] Please wait...\n"):
        asyncio.run(run_all())
        
    default = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        messages=[{"role": "user", "content": f"question about provided data: {input} data: {data} USE THIS DATA TO AWNSER THE QUESTION, KEEP IT SHORT"}],
    )  # alterative model setting
    if "<!DOCTYPE html>" in default:
        logger.warning(f"[LLM] default is not available. Trying another...")
        defualtnew = g4f.ChatCompletion.create(
            model=g4f.models.gpt_35_turbo,
            messages=[{"role": "user", "content": f"question about provided data: {input} data: {data} USE THIS DATA TO AWNSER THE QUESTION, KEEP IT SHORT"}],
        )  # alterative model setting
        output.append({"base": defualtnew})
    else:
        output.append({"base": default})
    return output


def convert_case(string, case = "pascal"):
    match case:
        case "snake":
            new = []
            for seq in string.split("_"):
                new.append(seq.lower())
            name = "_".join(new)
        case "pascal":
            new = []
            for seq in string.split("_"):
                new.append(seq.title())
            name = "".join(new)
        case "camel":
            new = []
            one = True
            for seq in string.split("_"):
                new.append(seq.lower() if one else seq.title())
                one = False
            name = "".join(new)
        case _:
            name = string
    return name

def cprop(cap = "camel", proxy_name = ""):
    def decorator(func):
        @property
        def wrapped(self):
            name = proxy_name
            if not name:
                name = convert_case(func.__name__, cap)
            return getattr(self.proxy, name)
        try:
            wrapped.__name__ = func.__name__ 
        except AttributeError:
            pass # ignore if func is a property
        wrapped.__doc__ = func.__doc__
        try:
            wrapped.__annotations__ = func.__annotations__
        except AttributeError:
            pass # ignore if setting annotations fails

        return wrapped
    return decorator
