# import the package
import mineflayer
 
# set main settings
config = {
    "server_ip": "og-network.net",
    "server_port": "25565",
    "bot_name": "silke2007minecraft@gmail.com",
    "password": "",
    "auth": "microsoft",
    "version": "1.19",
    "check_timeout_interval": 20,
    "armor_manager": True,
    "viewer_ip": "127.0.0.1",
    "viewer_port": "5001",
    "quit_on_low_health": False,
    "low_health_threshold": 10
}
 
# create the bot
bot = mineflayer.createBot(config=config)
 
# do not run code here that needs acces to the bot!
 
# start the bot
bot.start()
 
# run code on the bot here!