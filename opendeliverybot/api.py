from fastapi import FastAPI
import uvicorn
from opendeliverybot.bot import MinecraftBot
import time
from javascript import require
import json
import structlog
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from rich.console import Console
import time 
from rich.panel import Panel
from rich.progress import track
from rich import print
from rich.layout import Layout
app = FastAPI()
logger = structlog.get_logger()
console = Console()
layout = Layout()

def api():

    print(Panel("Welcome to the Open Delivery Bot python package!\n\nAPI docs are avable at: https://open-delivery-bot-documentation.vercel.app/", title="Welcome", expand=False, border_style="green"))
    
    logger.info("API running at http://localhost:5000/ (beta)")
    
    
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        with console.status(f"[bold green][API] {request.method} {request.scope['path']} ...\n") as status:
            start_time = time.time()
            response = await call_next(request)
            process_time = time.time() - start_time
            # logger.warning(f"[API] {request.method} {request.scope['path']} ✅ {process_time} ms")
            status.update(f"[bold green][API] {request.method} {request.scope['path']} Done!\n")
            logger.info(f"[API] {request.method} {request.scope['path']}")
            return response

    @app.get("/")
    async def home():
        time.sleep(1)
        return JSONResponse(content="Welcome")
    
    @app.get("/api/v1/login")
    async def startup():
        try:
            msa.stop()
        except: pass
        config = {
        "server_ip": "blockmania.com",
        "server_port": 25565,
        "bot_name": "silke2007minecraft@gmail.com",
        "password": "",  
        "auth": "microsoft",
        "version": "1.12",
        "viewer_port": 5001,
        "chest_coords": [10, 64, -8],
        "chest_range": 64,
        "chest_type": "chest",
        "items_name": "cobblestone",
        "items_count": 64,
        "x_coord": 0,
        "y_coord": 70, 
        "z_coord": 0
        }
        global bot
        bot = MinecraftBot(config)
        bot.start()
        return JSONResponse(content={"status": f"{bot.bot.username}"})


    @app.get("/api/v1/get_msa")
    async def startup(email:str = ""):
        global msa
        try:
            msa.stop()
        except:
            pass
        config = {
        "server_ip": "og-network.net", 
        "server_port": 25565,
        "bot_name": email,
        "password": "",  
        "auth": "microsoft",
        "version": "1.19",
        "viewer_port": 5001,
        "chest_coords": [10, 64, -8],
        "chest_range": 64,
        "chest_type": "chest",
        "items_name": "cobblestone",
        "items_count": 64,
        "x_coord": 0,
        "y_coord": 70, 
        "z_coord": 0
        }
        msa = MinecraftBot(config, apiMode=True)
        maxLoops = 0
        while msa.msa_status == False:
            if maxLoops >= 20:
                return JSONResponse(content={'user_code': "Already signed in"})
            time.sleep(1)
            maxLoops += 1
        if msa.msa_status == True:
            
            return JSONResponse(content=msa.msa_data)
        


    uvicorn.run(app, log_level="critical", port=5000)
    # uvicorn.run(app, port=5000)