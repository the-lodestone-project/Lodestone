try:
    from lodestone.bot import createBot, Bot
    from lodestone.utils import llm
    from plugins import plugins
    from lodestone.api import fastapi
    from lodestone.server import createServer, Server
    from lodestone.logger import logger
except:
    from .bot import createBot, Bot
    from .utils import llm
    from .plugins import plugins
    from .api import fastapi
    from .server import createServer, Server
    from .logger import logger
    
