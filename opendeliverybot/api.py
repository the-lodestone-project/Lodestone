from fastapi import FastAPI
import uvicorn
from bot import MinecraftBot
import json
from fastapi.responses import JSONResponse
app = FastAPI()

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

player = MinecraftBot(config, useReturn=True)

@app.get("/start")
async def startup():
    player.start()
    return JSONResponse(content={"message": "Bot started"})

@app.get("/inventory")
async def get_inventory():
    return JSONResponse(content={"inventory": player.inventory()})

@app.get("/coordinates") 
async def get_coordinates():
    return JSONResponse(content={"coordinates": player.coordinates()})

@app.get("/username")
async def get_username():
    return JSONResponse(content={"username": player.bot.username})

@app.get("/stop")
async def stop_bot():
    player.stop()
    return JSONResponse(content={"message": "Bot stopped"})

if __name__ == "__main__":
    uvicorn.run(app)