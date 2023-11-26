import gradio as gr
import lodestone
from lodestone import plugins
import time

global created
created = False
global chat_history
chat_history = []
global plugin_list
plugin_list = []


css = """
.error {
  color: red
}
"""



def get_bot_status():
    if 'bot' in globals():
        return "Stop Bot"
    else:
        return "Start/Stop Bot"

def change_tab():
    return gr.Tabs.update(selected=1)



def create(email, auth, host, port, version, viewer, plugin, enable_viewer, skip_checks):
    try:
        if 'bot' in globals():
            def stop_bot():
                try:
                    global bot
                    bot.stop()
                    gr.Info("Successfully stopped bot!")
                    del bot
                except Exception as e:
                    print(e)
                    pass
            stop_bot()
            return "Already logged in!", "Already logged in!", "Login/Create Bot"
    except Exception as e:
        print(e)
        pass
    if not host or not email or not version:
        gr.Warning("not all fields are filled in!")
        return "Unknown", "Unknown", "Login/Create Bot"
    
    
    global bot
    plugin_str = ""
    if plugin:
        plugin_str += "Plugins: "
        for new_plugin in plugin:
            if new_plugin == "Schematic Builder":
                plugin_str += "Schematic Builder, "
                plugin_list.append(plugins.schematic)
            elif new_plugin == "Cactus Farm Builder":
                plugin_str += "Cactus Farm Builder, "
                plugin_list.append(plugins.cactus)
            elif new_plugin == "Discord Rich Presence":
                plugin_str += "Discord Rich Presence, "
                plugin_list.append(plugins.discordrp)
            else:
                pass
    if enable_viewer == False:
        enable_viewer = True
    elif enable_viewer == True:
        enable_viewer = False
    bot = lodestone.createBot(
        host=host,
        username=email,
        port=port,
        ls_viewer_port=viewer,
        version=version,
        profilesFolder="./cache",
        auth=auth,
        ls_disable_viewer=enable_viewer,
        ls_skip_checks=skip_checks,
        ls_plugin_list=plugin_list
    )
    
    @bot.on('messagestr')
    def chat_history_add(this, message, messagePosition, jsonMsg, sender, *args):
        message = str(message).replace("\n","")
        if str(sender).lower() == "none":
            chat_history.append(f"{message}")
        else:
            chat_history.append(f"{sender}: {message}")
    
    info =f"""Successfully logged in as {bot.username}"""
    
    
    
    gr.Info(f"Successfully logged in as {bot.username}\n{plugin_str}")
    return bot.username, info, "Stop Bot"


def create_multiple(email, auth, host, port, version, amount):
    try:
        if 'bot' in globals():
            def stop_bot():
                try:
                    global bot
                    bot.stop()
                    gr.Info("Successfully stopped bot!")
                    del bot
                except Exception as e:
                    print(e)
                    pass
            stop_bot()
            return "Already logged in!", "Already logged in!", "Login/Create Bot"
    except Exception as e:
        print(e)
        pass
    if not host or not email or not version:
        gr.Warning("not all fields are filled in!")
        return "Unknown", "Unknown", "Login/Create Bot"
    
    
    for bots in range(0, amount):
        lodestone.createBot(
            host=host,
            username=email+str(bots),
            port=port,
            ls_disable_viewer=True,
            version=version,
            profilesFolder="./cache",
            auth=auth,
            ls_skip_checks=True,
        )
    
    global bot
    bot = amount
    # @bot.on('messagestr')
    # def chat(this, message, messagePosition, jsonMsg, sender, *args):
    #     message = str(message).replace("\n","")
    #     if str(sender).lower() == "none":
    #         chat_history.append(f"{message}")
    #     else:
    #         chat_history.append(f"{sender}: {message}")
    
    info =f"""Successfully created {amount} bots!"""
    
    
    
    gr.Info(f"Successfully created {amount} bots!")
    return amount, info, "Stop Bot"



def get_username():
    if 'bot' in globals():
        return bot.username
    else:
        return "None"



def get_player_health():
    if 'bot' in globals():
        return bot.health
    else:
        return "Unknown"

def get_player_food():
    if 'bot' in globals():
        return bot.food
    else:
        return "Unknown"
    
def get_player_experience():
    if 'bot' in globals():
        return bot.experience.level
    else:
        return "Unknown"
    
def get_player_difficulty():
    if 'bot' in globals():
        
        if bot.settings.difficulty == 0:
            return "peaceful"
        elif bot.settings.difficulty == 1:
            return "easy"
        elif bot.settings.difficulty == 2:
            return "normal"
        elif bot.settings.difficulty == 3:
            return "hard"
    
    else:
        return "Unknown"
    

def get_all_data():
    if 'bot' in globals():
        return bot.player
    else:
        return "Unknown"




def get_latest_chats():
    if 'bot' in globals():
        if len(chat_history) > 30:
            chat_history.clear()
            return "No chat messages yet!"
        string = ""
        for i in chat_history[-9:]:
            string += i + "\n"
        return string
    else:
        return "No chat messages yet!"



# def upload_file(files):
#     global build_file
#     file_paths = [file.name for file in files]
#     build_file = file_paths
#     print(file_paths)
#     return file_paths


def build_schematic(files, x, z):
    if not x or not z or not files:
        gr.Warning("not all fields are filled in!")
        return
    if 'bot' in globals():
        bot.goto(x, z)
        time.sleep(2)
        bot.build_schematic(f'{files.name}')
    else:
        gr.Warning("You need to login first!")
        


with gr.Blocks(theme=gr.themes.Soft(), title="The Lodestone Project") as ui:
    with gr.Tab("Bot Settings"):
        # gr.Markdown(requests.get('https://raw.githubusercontent.com/the-lodestone-project/Lodestone/main/README.md').text)
        # gr.Image("https://github.com/the-lodestone-project/Lodestone/blob/main/assets/logo.png?raw=true", min_width=2000)
        with gr.Tab("Signle Bot"):
            email = gr.Textbox(placeholder="Notch", label="Username",info="Username to login with")
            auth = gr.Dropdown(["microsoft", "offline"], value="microsoft", label="Authentication Method",info="Authentication method to login with")
            host = gr.Textbox(placeholder="2b2t.org", label="Server Ip",info="Server ip to connect to")
            port = gr.Number(value=25565, label="Sever Port", info="Server port to connect to. Most servers use 25565",precision=0)
            version = gr.Dropdown(["auto","1.20", "1.19", "1.18", "1.17", "1.16.4", "1.16", "1.15", "1.14", "1.13", "1.12", "1.11", "1.10", "1.9", "1.8"], value="auto", label="Version",info="Version to connect with. Use auto to automatically detect the version of the server")
            with gr.Accordion("Optional Settings", open=False):
                enable_viewer = gr.Checkbox(value=True, label="Enable Viewer", info="Enable the viewer to see the bot's view",interactive=True)
                skip_checks = gr.Checkbox(value=True, label="Skip Checks/Updates", info="Skip checks to speed up the bot",interactive=True)
                viewer = gr.Number(value=5001, label="Viewer Port", info="Viewer port to display the bot's view",precision=0)
                plugin = gr.Dropdown(["Schematic Builder", "Cactus Farm Builder", "Discord Rich Presence"],multiselect=True, label="Plugins",info="Plugins to load on startup")
            btn = gr.Button(value=get_bot_status,variant='primary')
            
            
            
            
            out_username = gr.Textbox(value="", label="Logged in as")
            info = gr.Textbox(value="", label="Info")
            
            btn.click(create, inputs=[email, auth, host, port, version, viewer, plugin, enable_viewer, skip_checks], outputs=[out_username, info, btn], show_progress="minimal")
        # with gr.Tab("Parameters"):
        #     def live_view():
        #         try:
        #             if bot.viewer_port:
        #                 port = bot.viewer_port
        #             else:
        #                 port = 5001
        #         except:
        #             port = 5001
        #         return f'<iframe src="http://localhost:{port}" style="width:50vw; height:50vh;">Your browser doesnt support iframes</iframe>'
        #     gr.HTML(f'<iframe src="http://localhost:{port}" style="width:50vw; height:50vh;">Your browser doesnt support iframes</iframe>')
        #     pass
        with gr.Tab("Multiple Bot"):
            email = gr.Textbox(placeholder="Notch", label="Username Prefix",info="Username prefix. The bot will login with this prefix and a number after it")
            auth = gr.Dropdown(["offline"], value="offline", label="Authentication Method",info="Authentication method to login with")
            host = gr.Textbox(placeholder="2b2t.org", label="Server Ip",info="Server ip to connect to")
            port = gr.Number(value=25565, label="Sever Port", info="Server port to connect to. Most servers use 25565",precision=0)
            version = gr.Dropdown(["auto","1.20", "1.19", "1.18", "1.17", "1.16.4", "1.16", "1.15", "1.14", "1.13", "1.12", "1.11", "1.10", "1.9", "1.8"], value="auto", label="Version",info="Version to connect with. Use auto to automatically detect the version of the server")
            amount = gr.Slider(minimum=1, maximum=50, step=1, label="Amount", info="Amount of bots to create", interactive=True)
            with gr.Accordion("Optional Settings", open=False):
                enable_viewer = gr.Checkbox(value=False, label="Enable Viewer", info="Enable the viewer to see the bot's view",interactive=False)
                viewer = gr.Number(value=5001, label="Viewer Port", info="Viewer port to display the bot's view",precision=0, interactive=False)
                # plugin = gr.Dropdown(["Schematic Builder", "Cactus Farm Builder", "Discord Rich Presence"],multiselect=True, label="Plugins",info="Plugins to load on startup")
            btn = gr.Button(value=get_bot_status,variant='primary')
            
            
            
            
            out_username = gr.Textbox(value="", label="Bot count")
            info = gr.Textbox(value="", label="Info")
            
            btn.click(create_multiple, inputs=[email, auth, host, port, version, amount], outputs=[out_username, info, btn], show_progress="minimal")
        
    with gr.Tab("Chat"):
        chat = gr.TextArea(value=get_latest_chats,every=5,label="Chat History (Updated every 5 seconds)",lines=10)
        msg = gr.Textbox(label="Message to send",placeholder="Hello world!")
        clear = gr.ClearButton([msg, chat],value="Clear Chat History")

        def respond(message):
            if 'bot' in globals():
                bot.chat(message)
                return ""
            else:
                return ""
        
        def delete():
            chat_history.clear()
        
        clear.click(delete)
        msg.submit(respond, inputs=[msg],outputs=[msg])
        
    with gr.Tab("Plugins"):
        with gr.Accordion("Schematic Builder", open=False):
            
            def check():
                if not plugins.schematic in plugin_list:
                    return "The Schematic Builder plugin is not loaded"
                else:
                    return "pluginloaded"
               
            gr.Textbox(value=check, every=30, show_label=False)
            # with gr.Row():
            #     with gr.Column(scale=1, ):
            file_output = gr.File(file_types=[".schematic", ".nbt", ".schem"], label="Schematic File (.schematic .nbt .schem)",file_count="single")
            with gr.Row():
                with gr.Column(scale=1, ):
                    x = gr.Number(label="X Coordinate",info="The X coord to build at", precision=0)
                with gr.Column(scale=1, ):
                    z = gr.Number(label="Z Coordinate",info="The Z coord to build at", precision=0)
            # upload_button = gr.UploadButton("Click to Upload a schematic", file_count="single")
            # upload_button.upload(upload_file, upload_button, file_output)
            build = gr.Button("Build schematic", variant='primary')
            build.click(build_schematic, inputs=[file_output, x, z])
            
            
        with gr.Accordion("Build Cactus Farm", open=False):
            gr.Markdown("")
            
        with gr.Accordion("Auto Farm", open=False):
            with gr.Row():
                with gr.Column(scale=1, ):
                    crop_type = gr.Dropdown(["wheat_seeds", "wheat", "beetroot_seeds", "beetroot", "carrot", "potato", "poisonous_potato", "melon", "melon_slice", "melon_seeds", "melon_stem", "attached_melon_stem", "pumpkin", "carved_pumpkin", "pumpkin_seeds", "pumpkin_stem", "attached_pumpkin_stem", "torchflower_seeds", "torchflower_crop", "torchflower", "pitcher_pod", "pitcher_crop", "pitcher_plant", "farmland", "bamboo", "cocoa_beans", "sugar_cane", "sweet_berries", "cactus", "mushrooms", "kelp", "sea_pickle", "nether_wart", "chorus_fruit", "fungus", "glow_berries"], label="Crop Type",info="The Crop type to farm", interactive=True)
                with gr.Column(scale=1, ):
                    seed_name = gr.Dropdown(["wheat_seeds", "wheat", "beetroot_seeds", "beetroot", "carrot", "potato", "poisonous_potato", "melon", "melon_slice", "melon_seeds", "melon_stem", "attached_melon_stem", "pumpkin", "carved_pumpkin", "pumpkin_seeds", "pumpkin_stem", "attached_pumpkin_stem", "torchflower_seeds", "torchflower_crop", "torchflower", "pitcher_pod", "pitcher_crop", "pitcher_plant", "farmland", "bamboo", "cocoa_beans", "sugar_cane", "sweet_berries", "cactus", "mushrooms", "kelp", "sea_pickle", "nether_wart", "chorus_fruit", "fungus", "glow_berries"], label="Seed Name",info="The Seed name to plant back", interactive=True)
                with gr.Column(scale=1, ):
                    harvest_name = gr.Dropdown(["wheat_seeds", "wheat", "beetroot_seeds", "beetroot", "carrot", "potato", "poisonous_potato", "melon", "melon_slice", "melon_seeds", "melon_stem", "attached_melon_stem", "pumpkin", "carved_pumpkin", "pumpkin_seeds", "pumpkin_stem", "attached_pumpkin_stem", "torchflower_seeds", "torchflower_crop", "torchflower", "pitcher_pod", "pitcher_crop", "pitcher_plant", "farmland", "bamboo", "cocoa_beans", "sugar_cane", "sweet_berries", "cactus", "mushrooms", "kelp", "sea_pickle", "nether_wart", "chorus_fruit", "fungus", "glow_berries"], label="Harvest Name",info="The block name to harvest", interactive=True)
                
            with gr.Row():
                with gr.Column(scale=1, ):
                    x = gr.Number(label="X Coordinate",info="The X coord to build at", precision=0)
                with gr.Column(scale=1, ):
                    z = gr.Number(label="Z Coordinate",info="The Z coord to build at", precision=0)
            
            with gr.Row():
                with gr.Column(scale=1, ):
                    x = gr.Number(label="X Coordinate",info="The X coord to build at", precision=0)
                with gr.Column(scale=1, ):
                    z = gr.Number(label="Z Coordinate",info="The Z coord to build at", precision=0)
            with gr.Accordion("Optional Settings", open=False):
                gr.Markdown("Optional Settings")
            start_farm = gr.Button("Start auto Farming", variant='primary')
            
        with gr.Accordion("Discord Rich Presence", open=False):        
            with gr.Row():
                with gr.Column(scale=1, ):
                    state = gr.Textbox(label="State",info="The state to display")
                with gr.Column(scale=1, ):
                    details = gr.Textbox(label="Details",info="The details to display")
                with gr.Column(scale=1, ):
                    large_image = gr.Textbox(label="Large Image (url)",info="The large image to display")
                with gr.Column(scale=1, ):
                    large_text = gr.Textbox(label="Large Text",info="The large text to display")
                with gr.Column(scale=1, ):
                    small_image = gr.Textbox(label="Small Image (url)",info="The small image to display")
                with gr.Column(scale=1, ):
                    small_text = gr.Textbox(label="Small Text",info="The small text to display")
            
            def update_presence_def(state="No state provided", details="No details Provided", large_image=None, large_text=None, small_image=None, small_text=None):
                print(details)
                if 'bot' in globals():
                    bot.discordrp(state=state, details=details, start=time.time())
                else:
                    pass
            
            update_presence = gr.Button("Update Presence", variant='primary')
            update_presence.click(update_presence_def, inputs=[state, details, large_image, large_text, small_image, small_text])
            
    
    with gr.Tab("Movements"):
        with gr.Tab("Basic Movements"):
            with gr.Row():
                with gr.Column(scale=1, ):
                    jump = gr.Button("Start Jumping")
                    jump = gr.Button("Stop Jumping")
                with gr.Column(scale=1, ):
                    jump = gr.Button("Start walking forward")
                    jump = gr.Button("Stop walking forward")
        with gr.Tab("Follow Player/Entity"):
            gr.Markdown("")
                
            

    with gr.Tab("Player Info"):
        # refresh_button = gr.Button("Refresh")
        with gr.Row():
            with gr.Column(scale=1):
                health = gr.Textbox(value=get_player_health, label=f"Health", every=5)
            with gr.Column(scale=1):
                food = gr.Textbox(value=get_player_food, label=f"Food", every=5)
            with gr.Column(scale=1):
                experience = gr.Textbox(value=get_player_experience, label=f"Experience Level", every=5)
            with gr.Column(scale=1):
                difficulty = gr.Textbox(value=get_player_difficulty, label=f"Difficulty", every=5)
            with gr.Column(scale=1):
                all_data = gr.Textbox(value=get_all_data, label=f"All Data", every=5)
        # refresh_button.click(get_player_info, outputs=[health, food, experience])

    with gr.Tab("System Resources"):
        # refresh_button = gr.Button("Refresh")
        import psutil
        import platform
        
        def cpu():
            return psutil.cpu_percent(interval=5)
        
        def ram_used():
            return psutil.virtual_memory().percent
        
        def ram_available():
            
            ram=  psutil.virtual_memory().available / (1024.0 ** 3)
            return "{:.1f}".format(ram)
        
        
        with gr.Row():
            with gr.Column(scale=1):
                health = gr.Textbox(value=ram_used, label=f"Ram Used (%)", every=5)
            with gr.Column(scale=1):
                food = gr.Textbox(value=ram_available, label=f"Available Ram (GB)", every=5)
            with gr.Column(scale=1):
                experience = gr.Textbox(value=cpu, label=f"CPU usage (%)", every=5)
            with gr.Column(scale=1):
                difficulty = gr.Textbox(value=platform.system, label=f"System Type")
        # refresh_button.click(get_player_info, outputs=[health, food, experience])
if __name__ == "__main__":
    ui.queue().launch(server_port=8000, show_api=False, quiet=True)

    # gr.themes.builder()
    
