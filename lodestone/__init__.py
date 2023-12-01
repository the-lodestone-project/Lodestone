import os
import shutil
import git

if os.path.isdir('plugins'):
    try:
        from lodestone.plugins import Base as plugins
    except:
        from .plugins import Base as plugins
else:
    if os.path.isdir('plugins'):
        shutil.rmtree('plugins')
        git.Repo.clone_from("https://github.com/the-lodestone-project/Plugins", "plugins")
        try:
            source_dir = 'plugins/plugins'
            target_dir = 'plugins'
                
            file_names = os.listdir(source_dir)
                
            for file_name in file_names:
                shutil.move(os.path.join(source_dir, file_name), target_dir)
            
            shutil.rmtree('plugins/plugins')
        except:
            logger.warning("Plugins folder is empty!")
            pass
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
    
