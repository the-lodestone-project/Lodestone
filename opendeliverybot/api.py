from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import bot

app = FastAPI()

global_config = {
    "server_ip": "",
    "server_port": "25565",
    "bot_name": "",
    "password": "",
    "auth": "microsoft",
    "version": "auto",
    "check_timeout_interval": 20,
    "armor_manager": True,
    "viewer_ip": "127.0.0.1",
    "viewer_port": "1000",
    "chest_type": None,
    "chest_coords": [
        "-62",
        "72",
        "47"
    ],
    "items_name": "ShulkerBox",
    "items_count": 1,
    "chest_range": "10",
    "quit_on_low_health": False,
    "low_health_threshold": 10
}


bot = bot.MinecraftBot(global_config)

class BotResponse(BaseModel):
    time: datetime
    status: str
    
class Config(BaseModel):
   # config fields

@app.post("/config")
async def update_config(config: Config):
    global_config.update(config.model_dump())
    return BotResponse(time=datetime.now(), status="success")


@app.post("/start")
async def start_bot():
    bot.start()
    return BotResponse(time=datetime.now(), status="started")

@app.post("/stop")
async def stop_bot():
    bot.stop()
    return BotResponse(time=datetime.now(), status="stopped")

@app.get("/inventory", response_model=BotResponse) 
async def get_inventory():
    return BotResponse(time=datetime.now(), status=bot.inventory())

@app.get("/coordinates", response_model=BotResponse)
async def get_coordinates():
    return BotResponse(time=datetime.now(), status=bot.coordinates())