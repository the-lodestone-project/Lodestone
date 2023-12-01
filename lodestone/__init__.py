try:
    from lodestone.bot import createBot, Bot
    from lodestone.utils import llm
    from lodestone.plugins import plugins
    from lodestone.api import fastapi
    from lodestone.server import createServer, Server
    from javascript import On as Event
    from lodestone.logger import logger
    from old_code.gradios import ui
except:
    from .bot import createBot, Bot
    from .utils import llm
    from .plugins import plugins
    from .api import fastapi
    from .server import createServer, Server
    from javascript import On as Event
    from .logger import logger
    from ..old_code.gradios import ui
    
