import gradio as gr
import requests
import bot
import time
import lodestone
from plugin import plugins
def create(email, host, port, version, auth):
    if not host or not port or not version:
        return "Not all "
    global mcbot
    mcbot = bot.createBot(
        host=host,
        username=email,
        port=port,
        version=version,
        profilesFolder="./cache",
        auth=auth,
        ls_skip_checks=True,
        ls_plugin_list=[plugins.schematic]
    )
    gr.Info('This is a warning message.')
    return mcbot.username


def upload_file(files):
    global build_file
    file_paths = [file.name for file in files]
    build_file = file_paths
    print(file_paths)
    return file_paths


def build_sch(files):
    try:
        mcbot.emit('build_schematic', f'{files.name}')
    except:
        print("not logged in!")


with gr.Blocks() as demo:
    with gr.Tab("Build Your Bot"):
        # gr.Markdown(requests.get('https://raw.githubusercontent.com/the-lodestone-project/Lodestone/main/README.md').text)
        gr.Image("https://github.com/the-lodestone-project/Lodestone/blob/main/logo.png?raw=true", min_width=2000)
        email = gr.Textbox(placeholder="Noth", label="Your Minecraft Username")
        auth = gr.Dropdown(["microsoft", "offline"], value="microsoft", label="Auth")
        host = gr.Textbox(placeholder="2b2t.org", label="The Mnecraft Server")
        port = gr.Number(value=25565, label="The port of the server")
        version = gr.Dropdown(["auto","1.20", "1.19", "1.18", "1.17", "1.16.4", "1.16", "1.15", "1.14", "1.13", "1.12", "1.11", "1.10", "1.9", "1.8"], value="auto", label="Miecraft Version")
        btn = gr.Button("Login/Create Bot")
        
        
        
        
        out_username = gr.Textbox(value="", label="Logged in as")
        
        
        btn.click(create, inputs=[email, host, port, version, auth], outputs=[out_username])
        
    with gr.Tab("Build Schematic"):
        file_output = gr.File()
        upload_button = gr.UploadButton("Click to Upload a schematic", file_count="single")
        upload_button.upload(upload_file, upload_button, file_output)
        build = gr.Button("Build schematic")
        build.click(build_sch, inputs=[file_output])
        gr.Markdown("")
        # gr.HTML('<iframe src="http://localhost:5001/" title="Live View"></iframe>')
        
        # msa = gr.Textbox(value="", label="Output")
        # btn.click(create, inputs=[email, host, port, version], outputs=[msa])


demo.launch()