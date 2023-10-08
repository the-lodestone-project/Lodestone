try:
    from bot import createBot, Bot
    from utils import llm
    from api import fastapi
    from javascript import On as Event
except ModuleNotFoundError:
    from .bot import createBot, Bot
    from .utils import llm
    from .api import fastapi
    from javascript import On as Event