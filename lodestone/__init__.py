import os

if os.path.isdir('plugins'):
    try:
        from lodestone.plugins import Base as plugins
    except:
        from .plugins import Base as plugins
else:
    import lodestone
    lodestone.bot.get_plugins()
    try:
        from lodestone.plugins import Base as plugins
    except:
        from .plugins import Base as plugins

try:
    from lodestone.bot import createBot, Bot
    from lodestone.utils import llm
    from lodestone.api import fastapi
    from lodestone.server import createServer, Server
    from javascript import On as Event
    from lodestone.logger import logger
    from lodestone.gradios import ui
except:
    from .bot import createBot, Bot
    from .utils import llm
    from .api import fastapi
    from .server import createServer, Server
    from javascript import On as Event
    from .logger import logger
    from .gradios import ui
    
