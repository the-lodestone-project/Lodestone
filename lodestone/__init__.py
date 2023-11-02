try:
    from bot import createBot, Bot
    from utils import llm
    from api import fastapi
    from server import createServer, Server
    from javascript import On as Event
    from plugin import plugins
    from logger import logger
except:
    from .bot import createBot, Bot
    from .utils import llm
    from .api import fastapi
    from .server import createServer, Server
    from javascript import On as Event
    from .plugin import plugins
    from .logger import logger