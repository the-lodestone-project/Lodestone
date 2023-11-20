from rich.console import Console
try:
    from discord import Embed
except:
    pass
import structlog
import datetime
import sys
import re
import time
from datetime import date
import os
import platform
import urllib.request
import json
import subprocess


logger = structlog.get_logger()

filestruc = "/"
if os.name == 'nt':
    filestruc = "\\"

__all__ = ['Server', 'createServer']

class Server:
    def __init__(
            self,
            motd: str = "Lodestone test server",
            *,
            maxPlayers: int = 20,
            installPath: str = "LodestoneServer",
            serverType: str = "Paper",
            ram: int = 2048,
            onlineMode: bool = True,
            logging: bool = True,
            gameMode: int = 1,
            difficulty: int = 1,
            worldFolder: str = "world",
            generation: dict = {'name': 'diamond_square', 'options': {'worldHeight': 80}},
            kickTimeout: int = 10000,
            modpe: bool = False,
            viewDistance: int = 10,
            playerListText: dict = {'header': 'Flying squid','footer': 'Test server'},
            everybodyOp: bool = True,
            maxEntities: int = 100,
            version: str = "1.20",
            port: int = 25565,
            

            ls_disable_logs: bool = False,
            ls_skip_checks: bool = False,
            ls_debug_mode: bool = False,
            ls_discord_webhook: str = None,
            ls_use_discord_forums: bool = False,
    ):
        """
        Create the bot. Parameters in camelCase are passed into mineflayer. Parameters starting with ls_ is Lodestone specific
        """
        if ls_debug_mode:
            os.environ["DEBUG"] = "minecraft-protocol"
        else:
            os.environ["DEBUG"] = ""

        self.local_motd = motd
        self.local_ram = ram
        self.local_max_players = maxPlayers
        self.local_port = port
        self.local_server_type = serverType
        self.local_version = version
        self.local_install_path = installPath
        self.local_online_mode = onlineMode
        self.local_logging = logging
        self.local_game_mode = gameMode
        self.local_difficulty = difficulty
        self.local_world_folder = worldFolder
        self.local_generation = generation
        self.local_kick_timeout = kickTimeout
        self.local_modpe = modpe
        self.local_view_distance = viewDistance
        self.local_player_list_text = playerListText
        self.local_everybody_op = everybodyOp

        self.local_max_entities = maxEntities
        self.disable_logs = ls_disable_logs
        self.skip_checks = ls_skip_checks
        self.discord_webhook = ls_discord_webhook
        self.use_discord_forums = ls_use_discord_forums

        self.console = Console()
        self.extra_data = {}
        self.loaded_plugins = {}

        if not self.skip_checks:
            self.node_version, self.pip_version, self.python_version = self.__versions_check()
        else:
            self.node_version, self.pip_version, self.python_version = "unknown", "unknown", "unknown"

        # if self.discord_webhook is not None:
        #     embed = Embed(
        #         title="Successfully Connected to Webhook!",
        #         description=f"""
        #         **Great news!** The bot has successfully connected to this channel's webhook.
        #         From now on, it will send all the logs and valuable data right here, keeping you informed about everything happening on the server.
                
        #         **Versions: **
        #         * [**Node**](https://nodejs.org/): {self.node_version}
        #         * [**Pip**](https://pypi.org/project/pip/): {self.pip_version}
        #         * [**Python**](https://www.python.org/): {self.python_version}
                
        #         **Links: **
        #         * [**GitHub**](https://github.com/SilkePilon/Lodestone)
        #         * [**Report Bugs**](https://github.com/SilkePilon/Lodestone/issues)
        #         * [**Web Interface**](https://github.com/SilkePilon/Mineflayer.py-react)
        #         """,
        #         color=0x3498db
        #     )
        #     embed.timestamp = datetime.datetime.utcnow()
        #     embed.set_footer(text='\u200b', icon_url="https://github.com/SilkePilon/Lodestone/blob/main/chestlogo.png?raw=true")
        #     if ls_use_discord_forums:
        #         today = date.today()
        #         send_webhook(ls_discord_webhook, content=f"{today}", thread_name=f"{today}", username="Lodestone", avatar_url="https://github.com/SilkePilon/Lodestone/blob/main/chestlogo.png?raw=true", embed=embed)
        #     else:
        #         try:
        #             send_webhook(ls_discord_webhook, content="", username="Lodestone", avatar_url="https://github.com/SilkePilon/Lodestone/blob/main/chestlogo.png?raw=true", embed=embed)
        #         except Exception as e:
        #             print(e)
        #             logger.error(f"Detected that you are using a Forums channel but 'useDiscordForums' is set to False. Please change 'useDiscordForums' to True or provide a webhook url for a text channel.")

        self.python_command = self.__check_python_command()
        if not ls_skip_checks:
            with self.console.status("[bold green]Checking for updates...\n") as status:
                status.update("[bold green]Updating pip package...\n")
                os.system(f'{self.python_command} -m pip install -U lodestone >/dev/null 2>&1')
        self.script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.__create_server()
    
    def __check_python_command(self):
        try:
            subprocess.check_output(['python', '--version'])
            return 'python'
        except:
            try:
                subprocess.check_output(['python3', '--version']) 
                return 'python3'
            except:
                self.__logging(message='Python command not found, make sure python is installed!', error=True,
                               discord=False)
                sys.exit(1)

    def __logging(self, message, icon="💾", error=False, info=False, warning=False, chat=False, image_url="", console=True, discord=True):
        if not self.disable_logs:
            if self.discord_webhook and discord:
                try:
                    from discord import Embed
                except:
                    pass
                color = 0x3498db
                if error:
                    color = 0x992d22
                elif info:
                    color = 0x3498db
                elif warning:
                    color = 0xe67e22
                elif chat:
                    color = 0x2ecc71
                embed = Embed(title="", description=f"**[{icon}] {message}**", color=color)
                embed.timestamp = datetime.datetime.utcnow()
                if image_url != "":
                    embed.set_thumbnail(url=image_url)
                try:
                    embed.set_footer(text=f'{self.bot.username}', icon_url=f"https://mc-heads.net/avatar/{self.bot.username}/600.png")
                except:
                    embed.set_footer(text='\u200b', icon_url="https://github.com/SilkePilon/Lodestone/blob/main/chestlogo.png?raw=true")
                # if self.use_discord_forums:
                #     today = date.today()
                #     send_webhook(self.discord_webhook, content=f"{today}", thread_name=f"{today}", username="Lodestone", avatar_url="https://github.com/SilkePilon/Lodestone/blob/main/chestlogo.png?raw=true", embed=embed)
                # else:
                #     try:
                #         send_webhook(self.discord_webhook, content=f"", username="Lodestone", avatar_url="https://github.com/SilkePilon/Lodestone/blob/main/chestlogo.png?raw=true", embed=embed)
                #     except Exception as e:
                #         print(e)
                #         logger.error(f"Detected that you are using a Forums channel but 'useDiscordForums' is set to False. Please change 'useDiscordForums' to True or provide a webhook url for a text channel.")
            if console:
                if error:
                    logger.error(f"[{icon}] {message}")
                elif info:
                    logger.info(f"[{icon}] {message}")
                elif warning:
                    logger.warning(f"[{icon}] {message}")
                elif chat:
                    logger.info(f"[{icon}] {message}")
                else:
                    logger.info(f"[{icon}] {message}")

    def __versions_check(self):
        with self.console.status("[bold green]Checking versions..."):
            # Node
            result = subprocess.run(["node", "--version"], 
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True)
            node_version = result.stdout.strip()
            # Remove leading 'v'
            node_version = node_version.removeprefix("v")
            # Remove periods
            node_version = node_version.replace('.', '')
            if int(node_version[:2]) >= 18:
                pass
            else:
                logger.warning(f"""
                                Detected node version {node_version[:2]} which isn't supported!
                                This may cause problems. Please update to node 18 or above!
                                """)

            # Pip
            pip_ = 'pip' if self.__check_python_command() == 'python' else 'pip3'
            result = subprocess.run([pip_, "--version"],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True)
            pip_version = result.stdout.strip()
            # Remove
            match = re.search(r'pip (\d+(?:\.\d+)*).*python (\d+(?:\.\d+)*)', pip_version)
            if match:
                pip_version = match.group(1)
                python_version = match.group(2)
            return node_version, pip_version, python_version

    def __create_server(self):


      # SETUP PROGRESS BAR
      global pbar
      pbar = None
      console = Console()
      status = console.status("[bold green]Downloading...")
      


      def get_folder():
        path = str(self.local_install_path)
        isExist = os.path.exists(path + "/")
        if not isExist:
          os.makedirs(path)
        if path is not None:
            # Getting the list of directories
            dir = os.listdir(path)
            
            # Checking if the list is empty or not
            if len(dir) == 0:
                # Dir is empty
                return path
            else:
                self.__logging("Directory isn't empty", error=True)
                exit()

      def get_server_type():
        server_type = str(self.local_server_type).lower()
        if (server_type == "paper") or (server_type == "vanilla"):
            return server_type.capitalize()
        else:
            self.__logging("Enter a valid answer.", error=True)
            exit()


      def get_latest_paper(version):
          self.__logging("Getting latest paper server url from: https://papermc.io", info=True)

          with urllib.request.urlopen(f"https://papermc.io/api/v2/projects/paper/versions/{version}") as baseurl:
              basedata = json.loads(baseurl.read().decode())
              buildsList = []
              for i in basedata["builds"]:
                  buildsList.append(i)
              
              self.__logging(f"Found correct version, {version}: searching for download link...", info=True)
              
              with urllib.request.urlopen(f"https://papermc.io/api/v2/projects/paper/versions/{version}/builds/{buildsList[-1]}") as buildurl:
                  builddata = json.loads(buildurl.read().decode())
                  name = builddata["downloads"]["application"]["name"]
                  final = f"https://papermc.io/api/v2/projects/paper/versions/{version}/builds/{buildsList[-1]}/downloads/{name}"
                  return final

      def download_file(path, url, name):
          self.__logging(f"Downloading server to {path}, as {name}", info=True)
          self.__logging("Downloading latest server file: ", info=True)
          with console.status("[bold green]Downloading...") as status:
            urllib.request.urlretrieve(url, os.path.join(path, name))
            status.update("[bold green]Done...")
          self.__logging("Download Complete!", info=True)


      def get_latest_vanilla(version):
          self.__logging("Getting latest vanilla server url from: https://launchermeta.mojang.com/mc/game/version_manifest.json", info=True)
          
          # Get json file with all versions
          with urllib.request.urlopen("https://launchermeta.mojang.com/mc/game/version_manifest.json") as url:
              data = json.loads(url.read().decode())
              for i in data["versions"]:
                  id = i["id"]
                  versionJson = i["url"]
                  
                  if id == version:
                      self.__logging(f"Found correct version, {version}: searching for download link...", info=True)

                      with urllib.request.urlopen(versionJson) as versionUrl:
                          dataUrl = json.loads(versionUrl.read().decode())
                          download = dataUrl["downloads"]["server"]["url"]

                          return download                   

      def first_run(path):
            self.__logging("The server will now start and stop to create folders.", info=True)
            time.sleep(1)
            os.chdir(os.path.abspath(path)) # CD into server folder
            try:
                result = subprocess.run(['java', '-jar', 'server.jar'], check = True)
            except subprocess.CalledProcessError:
                self.__logging("Could not start the server, make sure Java is installed.", error=True)
                exit()

            
            try:
              with open('eula.txt', 'r+') as file:
                  for line in file:
                      print(line.replace('eula=false', 'eula=true'), end='')
              self.__logging("Eula accepted.", info=True)
            except FileNotFoundError:
              self.__logging("Unsupported Java detected!", error=True)
              exit()

      def modify_props():
        serv_prop = open("server.properties", "r+")
        lines_prop = serv_prop.readlines()
        
        # seed = str(input("\nWhich seed would you like to set: "))
        # lines_prop[4] = f"level-seed={seed}\n"
        
        # self.__logging(f"Seed changed to {seed}.", info=True)

        name = str(self.local_motd)
        lines_prop[10] = f"motd={name}\n"

        self.__logging(f"Server name changed to {name}.", info=True)


        players = str(self.local_max_players)
        lines_prop[18] = f"max-players={players}\n"
        
        self.__logging(f"Player limit changed to {players}.", info=True)


        view = str(self.local_view_distance)
        lines_prop[23] = "view-distance=" + view + "\n"
        
        self.__logging(f"Render distance changed to {view}.", info=True)


        port = str(self.local_port)
        lines_prop[27] = f"server-port={port}\n"
        
        self.__logging(f"Server port changed to {port}.", info=True)
        

        online = self.local_online_mode
        if online == True:
            online_check = "enabled."
            lines_prop[19] = "online-mode=true\n"
            
        if online == False:
            online_check = "disabled."
            lines_prop[19] = "online-mode=false\n"
            
        self.__logging(f"Online mode {online_check}", info=True)


        self.__logging("Saving config and exiting...", info=True)

        # Save file
        serv_prop.writelines(lines_prop)
        serv_prop.close()

      def make_start_script():
          running = True
          while running:

             
                  # Finds running OS
                  running_os = platform.system()

                 
                  # Linux/macOS - make .sh file
                  if running_os == "Linux" or os == "Darwin":
                      if self.local_server_type.lower() == "paper":
                        script_type = "y"
                      else:
                        script_type = "n"
                      start_sh = open("start.sh", "x")

                      # Optimized start script
                      if script_type == "y":
                          ram = str(self.local_ram)
                          
                          start_sh.writelines('#!/bin/bash\njava -Xmx'+ram+'M -Xms'+ram+'M -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true -jar server.jar nogui')
                          start_sh.close()
                          # Make file executable
                          os.chmod('start.sh', 0o777)
                          running2 = False
                          running = False

                          self.__logging("Created script", info=True)

                      # Normal start script
                      elif script_type == "n":
                          ram = str(self.local_ram)
                          
                          start_sh.writelines('#!/bin/bash\njava -Xmx'+ram+'M -Xms'+ram+'M -jar server.jar nogui')
                          start_sh.close()
                          # Make file executable
                          os.chmod('start.sh', 0o777)
                          running2 = False
                          running = False

                          self.__logging("Created script", info=True)

                      # Wrong answer
                      else:
                          self.__logging("Enter a valid answer.", warning=True)

                  # Windows - make .bat file
                  elif running_os == "Windows":
                      if self.local_server_type.lower() == "paper":
                        script_type = "y"
                      else:
                        script_type = "n"
                      start_sh = open("start.bat", "x")

                      # Optimized start script
                      if script_type == "y":
                          ram = str(self.local_ram)
                          
                          start_sh.writelines('java -Xmx'+ram+'M -Xms'+ram+'M -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true -jar server.jar nogui')
                          start_sh.close()

                          running2 = False
                          running = False

                          self.__logging("Created script", info=True)

                      # Normal start script
                      elif script_type == "n":
                          ram = str(self.local_ram)
                          
                          start_sh.writelines('java -Xmx'+ram+'M -Xms'+ram+'M -jar server.jar nogui')
                          start_sh.close()

                          running2 = False
                          running = False

                          self.__logging("Created script", info=True)
                  


      def main():

          running = True
          while running:
              
              # Ask where to install server
              path = get_folder()

              # Ask server type
              if get_server_type() == "Vanilla":
                  # Tries to find vanilla URL
                  get_dl_question = True
                  while get_dl_question:
                      version = str(self.local_version)
                      url = get_latest_vanilla(version)
                      if url is None:
                          self.__logging(f"Didn't find a download link for version {version}.", error=True)
                          continue
                      else:
                          self.__logging(f"Found download link for version {version}: {url}", info=True)

                          # Download
                          download_file(path, url, "server.jar")

                          get_dl_question = False # Go to next question
              else:
                  #Tries to find paper URL
                  get_dl_question = True
                  while get_dl_question:
                      version = str(self.local_version)
                      url = get_latest_paper(version)
                      if url is None:
                          self.__logging(f"Didn't find a download link for version {version}.", error=True)
                          continue
                      else:
                          self.__logging(f"Found download link for version {version}: {url}", info=True)

                          # Download
                          download_file(path, url, "server.jar")

                          get_dl_question = False # Go to next question

              # Setup server
              first_run(path)
              modify_props()

              # Finish server + start script
              make_start_script()

              self.__logging("Server is done, simply start it by running the start script!", info=True)
              running = False


      main()

      
      
          

createServer = Server