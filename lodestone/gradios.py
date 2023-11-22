import gradio as gr
import lodestone
from lodestone import plugins


global created
created = False
global chat_history
chat_history = []


def get_bot_status():
    if 'bot' in locals() or 'bot' in globals():
        return "Stop Bot"
    else:
        return "Start/Stop Bot"
    


def create(email, auth, host, port, version, viewer, plugin):
    try:
        if 'bot' in locals() or 'bot' in globals():
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
    
    plugin_list = []
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
            else:
                pass
    
    bot = lodestone.createBot(
        host=host,
        username=email,
        port=port,
        ls_viewer_port=viewer,
        version=version,
        profilesFolder="./cache",
        auth=auth,
        ls_skip_checks=True,
        ls_plugin_list=plugin_list
    )
    
    @bot.on('messagestr')
    def chat(this, message, messagePosition, jsonMsg, sender, *args):
        message = str(message).replace("\n","")
        if str(sender).lower() == "none":
            chat_history.append(f"{message}")
        else:
            chat_history.append(f"{sender}: {message}")
    
    info =f"""#Successfully logged in as {bot.username}"""
    
    
    
    gr.Info(f"Successfully logged in as {bot.username}\n{plugin_str}")
    return bot.username, info, "Stop Bot"



def get_username():
    try:
        return bot.username
    except:
        return "None"



def get_player_health():
    try:
        return bot.health
    except:
        return "Unknown"

def get_player_food():
    try:
        return bot.food
    except:
        return "Unknown"
    
def get_player_experience():
    try:
        return bot.experience.level
    except:
        return "Unknown"
    
def get_player_difficulty():
    try:
        
        if bot.settings.difficulty == 0:
            return "peaceful"
        elif bot.settings.difficulty == 1:
            return "easy"
        elif bot.settings.difficulty == 2:
            return "normal"
        elif bot.settings.difficulty == 3:
            return "hard"
    
    except:
        return "Unknown"
    

def get_all_data():
    try:
        return bot.player
    except:
        return "Unknown"




def get_latest_chats():
    try:
        if len(chat_history) > 30:
            chat_history.clear()
            return "No chat messages yet!"
        string = ""
        for i in chat_history[-9:]:
            string += i + "\n"
        return string
    except:
        return "No chat messages yet!"











def upload_file(files):
    global build_file
    file_paths = [file.name for file in files]
    build_file = file_paths
    print(file_paths)
    return file_paths


def build_schematic(files):
    try:
        bot.emit('build_schematic', f'{files.name}')
    except:
        print("not logged in!")


with gr.Blocks(theme=gr.themes.Soft()) as ui:
    with gr.Tab("Bot Settings"):
        # gr.Markdown(requests.get('https://raw.githubusercontent.com/the-lodestone-project/Lodestone/main/README.md').text)
        # gr.Image("https://github.com/the-lodestone-project/Lodestone/blob/main/assets/logo.png?raw=true", min_width=2000)
        with gr.Row():
            with gr.Column(scale=1, variant='panel'):
                with gr.Tab("Create Bot"):
                    email = gr.Textbox(placeholder="Notch", label="Username",info="Username to login with")
                    auth = gr.Dropdown(["microsoft", "offline"], value="microsoft", label="Authentication Method",info="Authentication method to login with")
                    host = gr.Textbox(placeholder="2b2t.org", label="Server Ip",info="Server ip to connect to")
                    port = gr.Number(value=25565, label="Sever Port", info="Server port to connect to. Most servers use 25565")
                    version = gr.Dropdown(["auto","1.20", "1.19", "1.18", "1.17", "1.16.4", "1.16", "1.15", "1.14", "1.13", "1.12", "1.11", "1.10", "1.9", "1.8"], value="auto", label="Version",info="Version to connect with. Use auto to automatically detect the version of the server")
                    with gr.Accordion("Optional Settings", open=False):
                        viewer = gr.Number(value=5001, label="Viewer Port", info="Viewer port to display the bot's view")
                        plugin = gr.Dropdown(["Schematic Builder", "Cactus Farm Builder"],multiselect=True, label="Plugins",info="Plugins to load on startup")
                    btn = gr.Button(value=get_bot_status,variant='primary')
                    
                    
                    
                    
                    out_username = gr.Textbox(value="", label="Logged in as")
                    info = gr.Textbox(value="", label="Info")
                    
                    btn.click(create, inputs=[email, auth, host, port, version, viewer, plugin], outputs=[out_username, info, btn], show_progress="minimal")
                with gr.Tab("Parameters"):
                    def live_view():
                        try:
                            if bot.viewer_port:
                                port = bot.viewer_port
                            else:
                                port = 5001
                        except:
                            port = 5001
                        return f'<iframe src="http://localhost:{port}" style="width:50vw; height:50vh;">Your browser doesnt support iframes</iframe>'
                    gr.HTML(f'<iframe src="http://localhost:{port}" style="width:50vw; height:50vh;">Your browser doesnt support iframes</iframe>')
                    pass
        
    with gr.Tab("Chat"):
        chatbot = gr.Textbox(value=get_latest_chats,every=5,label="Chat History (Updated every 5 seconds)")
        msg = gr.Textbox(label="Message to send",placeholder="Hello world!",elem_id="msg")
        clear = gr.ClearButton([msg, chatbot],value="Clear Chat History")

        def respond(message):
            try:
                bot.chat(message)
                return ""
            except:
                return ""
        
        def delete():
            chat_history.clear()
        
        clear.click(delete)
        msg.submit(respond, inputs=[msg],outputs=[msg])
        
    with gr.Tab("Plugins"):
        with gr.Tab("Schematic Builder"):
            file_output = gr.File()
            upload_button = gr.UploadButton("Click to Upload a schematic", file_count="single")
            upload_button.upload(upload_file, upload_button, file_output)
            build = gr.Button("Build schematic")
            build.click(build_schematic, inputs=[file_output])
    
        with gr.Tab("Build Cactus Farm"):
            gr.Markdown("")
            
    
    with gr.Tab("Movements"):
        with gr.Tab("Basic Movements"):
            with gr.Row():
                with gr.Column(scale=1, variant='panel'):
                    jump = gr.Button("Start Jumping")
                    jump = gr.Button("Stop Jumping")
                with gr.Column(scale=1, variant='panel'):
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

        
    
