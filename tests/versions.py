import time
from rich.console import Console
import bot as lodestone

"""
Test different Minecraft/Lodestone versions by creating a bot and checking if it connects successfully.
"""

versions = ["1.20.1", "1.19", "1.18", "1.17", "1.16", "1.15", "1.14", "1.13", "1.12", "1.11", "1.10", "1.9", "1.8"] 

console = Console()

with console.status("[bold]Checking versions...\n") as status:
    for version in versions:
        
        status.update(f"Checking version {version}")

        # Create bot with the current version  
        try:
            bot = lodestone.createBot(
                host='2b2t.org',
                username='TestBot',  
                version=version,
                checkTimeoutInterval=70,
                ls_skip_checks=True,
                hideErrors=False,
                ls_debug_mode=True
            )
        except:
            pass
        
        # Check connection
        if bot:
            print(f"Version {version} connected successfully!")
            status.update(f"Checking version {version} ([bold green]✔️[reset])")
        else:
            print(f"Version {version} failed to connect")
        
        # Stop bot
        bot.stop()

        # Add delay to avoid congestion
        time.sleep(10)