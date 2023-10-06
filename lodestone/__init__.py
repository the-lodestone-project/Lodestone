try:
    from bot import createBot
    from utils import llm
    from api import fastapi
    from javascript import On as Event
except ImportError:
    from .bot import createBot
    from .utils import llm
    from .api import fastapi
    from javascript import On as Event