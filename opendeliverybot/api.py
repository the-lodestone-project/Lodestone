from fastapi import FastAPI
import uvicorn
from opendeliverybot.bot import MinecraftBot
import time
from javascript import require
import json
from fastapi.responses import JSONResponse
app = FastAPI()
global config
global account

def api():
    @app.get("/api/v1/login")
    async def startup():
        config = {
        "server_ip": "menu.mc-complex.com", 
        "server_port": 25565,
        "bot_name": "silke2007minecraft@gmail.com",
        "password": "",  
        "auth": "microsoft",
        "version": "1.12",
        "viewer_port": 1000,
        "chest_coords": [10, 64, -8],
        "chest_range": 64,
        "chest_type": "chest",
        "items_name": "cobblestone",
        "items_count": 64,
        "x_coord": 0,
        "y_coord": 70, 
        "z_coord": 0
        }

        account = MinecraftBot(config)
        return JSONResponse(content={"message": "Bot started"})


    @app.get("/api/v1/get_msa")
    async def startup(email:str = ""):
        config = {
        "server_ip": "blockmania.com", 
        "server_port": 25565,
        "bot_name": email,
        "password": "",  
        "auth": "microsoft",
        "version": "1.12",
        "viewer_port": 1000,
        "chest_coords": [10, 64, -8],
        "chest_range": 64,
        "chest_type": "chest",
        "items_name": "cobblestone",
        "items_count": 64,
        "x_coord": 0,
        "y_coord": 70, 
        "z_coord": 0
        }

        account = MinecraftBot(config)
        msa_status = False
        loops = 0
        time.sleep(6)
        try:
            if account.bot.username != None:
                account.stop()
                JSONResponse(content={"msa": "Already logged in!"})
                msa_status = True
            while msa_status == False:
                if loops >= 30:
                    account.stop()
                    return JSONResponse(content={"msa": f"Max tries exceeded!"})
                
                try:
                    if account.msa_data['user_code'] != False:
                        account.stop()
                        return JSONResponse(content={"msa": f"{account.msa_data['user_code']}"})
                except:
                    continue
                loops += 1
        except:
            account.stop()
            return JSONResponse(content={"msa": f"Error"})


    
    uvicorn.run(app)