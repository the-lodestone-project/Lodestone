try:
    from lodestone.bot import createBot, Bot
    from lodestone.utils import llm
    from lodestone.api import fastapi
    from lodestone.server import createServer, Server
    from javascript import On as Event
    from lodestone.plugin import plugins
    from lodestone.logger import logger
    from lodestone.gradios import ui
except:
    from .bot import createBot, Bot
    from .utils import llm
    from .api import fastapi
    from .server import createServer, Server
    from javascript import On as Event
    from .plugin import plugins
    from .logger import logger
    from .gradios import ui