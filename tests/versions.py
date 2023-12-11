import time
from rich.console import Console
from lodestone import createBot

"""
Test different Minecraft/Lodestone versions by creating a bot and checking if it connects successfully.
"""

versions = ["1.8.8", "1.9" "15w40b", "1.9.1-pre2", "1.9.2", "1.9.4", "1.10", "16w20a", "1.10-pre1", "1.10", "1.10.1", "1.10.2", "1.11", "16w35a", "1.11", "1.11.2", "1.12", "17w15a", "17w18b", "1.12-pre4", "1.12", "1.12.1", "1.12.2", "1.13", "17w50a", "1.13", "1.13.1", "1.13.2-pre1", "1.13.2-pre2", "1.13.2", "1.14", "1.14", "1.14.1", "1.14.3", "1.14.4", "1.15", "1.15", "1.15.1", "1.15.2", "1.16", "20w13b", "20w14a", "1.16-rc1", "1.16", "1.16.1", "1.16.2", "1.16.3", "1.16.4", "1.17", "21w07a", "1.17", "1.17.1", "1.18", "1.18", "1.18.1", "1.18.2", "1.19", "1.19", "1.19.1", "1.19.2", "1.19.3", "1.19.4", "1.20", "1.20.1", "false"]

console = Console()

with console.status("[bold]Checking versions...\n") as status:
    for version in versions:
        
        status.update(f"Checking version {version}")

        # Create bot with the current version  
        try:
            bot = createBot(
                host='2b2t.org',
                username='TestBot',  
                version=version,
                checkTimeoutInterval=10000,
                ls_skip_checks=True,
                hideErrors=False,
                ls_debug_mode=True,
                ls_disable_viewer=True
            )
        except Exception as err:
            print(err)
            bot = False
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