from utils import llm, claude
import bot
config = {
    "server_ip": "org.earthmc.net",
    "server_port": "25565",
    "bot_name": "silke2007minecraft@gmail.com",
    "password": "",
    "auth": "microsoft",
    "version": "1.19.4",
    "check_timeout_interval": 20,
    "armor_manager": True,
    "viewer_ip": "127.0.0.1",
    "viewer_port": "5001",
    "quit_on_low_health": False,
    "low_health_threshold": 10
}

mcbot = bot.createBot(config=config)
mcbot.start()
print(claude(input="can you give me some of the info about the players?",data=mcbot.bot.players, cookie="sessionKey=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"))
mcbot.clearLogs()
print(mcbot.chatHistory(username="LeyLox"))