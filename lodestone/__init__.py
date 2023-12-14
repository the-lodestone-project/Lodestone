try:
    from lodestone.bot import createBot, Bot
    from lodestone.utils.utils import llm
    from lodestone.modules.api import fastapi
    from lodestone.server import createServer, Server
    from lodestone.modules.logger import logger
except:
    from .bot import createBot, Bot
    from .utils.utils import llm
    from .modules.api import fastapi
    from .server import createServer, Server
    from .modules.logger import logger
    
