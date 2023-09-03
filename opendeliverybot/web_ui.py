
import streamlit as st
from st_on_hover_tabs import on_hover_tabs
import streamlit_toggle as tog
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.stateful_button import button
from streamlit_extras.no_default_selectbox import selectbox
import streamlit.components.v1 as components
from streamlit_extras.grid import grid
from javascript import require, On
import pandas as pd
import numpy as np
from contextlib import redirect_stdout
import shlex
from streamlit.runtime.scriptrunner import get_script_run_ctx
from contextlib import contextmanager
from io import StringIO
import time
import math
import subprocess
import datetime
import requests
import json
import console_ui
import asyncio
import contextlib
from functools import wraps
from io import StringIO
# from bot import makeBot
from streamlit.runtime.scriptrunner import add_script_run_ctx
import os
import sys


import opendeliverybot.bot as bot





st.set_page_config(
    page_title="Bot controller",
    page_icon="🕹",
    layout="centered",
    initial_sidebar_state="auto",
)
script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
with open(f'{script_directory}/data\data.json', 'r') as f:
    data = json.load(f)

def webmode():
    def capture_output(func):
        """Capture output from running a function and write using streamlit."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Redirect output to string buffers
            stdout, stderr = StringIO(), StringIO()
            try:
                with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                    return func(*args, **kwargs)
            except Exception as err:
                st.write(f"Failure while executing: {err}")
            finally:
                if _stdout := stdout.getvalue():
                    st.write("Execution stdout:")
                    st.code(_stdout)
                if _stderr := stderr.getvalue():
                    st.write("Execution stderr:")
                    st.code(_stderr)

        return wrapper
    stprint = capture_output(print)
    
    
    
    
    
    st.markdown("<style>" + open(f"{script_directory}/frontend\styles.css").read() + "</style>", unsafe_allow_html=True)

    with st.sidebar:
        tabs = on_hover_tabs(
            tabName=["Settings", "Dashboard", "Analytics"],
            iconName=["settings", "dashboard", "analytics"],
            styles={
                "navtab": {
                    "background-color": "#111",
                    "color": "#818181",
                    "font-size": "18px",
                    "transition": ".3s",
                    "white-space": "nowrap",
                    "text-transform": "uppercase",
                },
                "tabOptionsStyle": {
                    ":hover :hover": {"color": "white", "cursor": "pointer"}
                },
                "iconStyle": {
                    "position": "fixed",
                    "left": "7.5px",
                    "text-align": "left",
                },
                "tabStyle": {
                    "list-style-type": "none",
                    "margin-bottom": "30px",
                    "padding-left": "30px",
                },
            },
            key="1",
        )

    if tabs == "Dashboard":
        st.title("Open Delivery Bot")
            
        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 2])

        with col1:
            x_coord = st.text_input("x", label_visibility="collapsed", placeholder="X coord")
                
        with col2:
            y_coord = st.text_input("y", label_visibility="collapsed", placeholder="Y coord")
            
        with col3:
            z_coord = st.text_input("z", label_visibility="collapsed", placeholder="Z coord")

        with col5:
            # def isViewerRunning():
            #     try:
            #         url = "http://127.0.0.1:1000"
            #         get_url = requests.get(url)
            #         code = get_url.status_code
                    
            #         if code == 200:
            #             return True
            #     except requests.exceptions.RequestException:
            #         return False
                
            

            # if isViewerRunning:
            #     start_dropoff_bot = st.button("Deliver item", disabled=True)
            # else:
            start_dropoff_bot = st.button("Deliver item")
            
        with col4:
            # if isViewerRunning:
            #     prismarineViewer_button = st.button("Open bot view", key="viewer_button", on_click=openViewer)
            # else:
            # prismarineViewer_button = st.button("Open bot view", key="viewer_button", on_click=openViewer)
            if start_dropoff_bot:
                try:
                    with open(f'{script_directory}/data\data.json', 'r') as file:
                        settings = json.load(file)
                        
                   
                    bot = bot.MinecraftBot(settings, streamlit=st)
                    
                    bot.start()
                    
                    
                    
                    st.toast("Bot started!", icon="✅")
                    st.button("Stop bot", on_click=bot.stop)
                except ValueError:
                    st.toast("Please enter a valid float number", icon="🚨")
        if start_dropoff_bot:
            Inv = st.empty()
            cord = st.empty()
            time.sleep(5)
            if bot.logedin == True:
                st.components.v1.iframe("http://127.0.0.1:1000", width=700, height=400, scrolling=False)
                while True:
                    Inv.text("Inventory: " + str(bot.inventory()))
                    cord.text("Coordinates: " + str(bot.coordinates()))
                
                    # screen.markdown('<iframe width="700rem" height="400rem" src="http://127.0.0.1:1000" frameborder="0" scrolling="auto" allowfullscreen id="render"></iframe>', unsafe_allow_html=True)
                    time.sleep(5)
            
            
            # render = st.markdown('<iframe width="700rem" height="400rem" src="http://127.0.0.1:1000" frameborder="0" scrolling="auto" allowfullscreen id="render"></iframe><br><br><br><br><br><br><br><br><br><br><br><br><br><br>', unsafe_allow_html=True)
            
        
    if tabs == "Settings":
        st.title("Bot settings")
        bot_name = st.text_input(label="Bot name", placeholder="BOT", value=data["bot_name"])

        col1, col2 = st.columns((2, 5))
        
        with col1:
            server_ip = st.text_input(label="Server ip", placeholder="127.0.0.1", value=data["server_ip"])
            viewer_ip = st.text_input(label="Viewer ip", placeholder="127.0.0.1", value=data["viewer_ip"])
            password = st.text_input(label="Password", type="password", value=data["password"])
            chest_type = selectbox("Select the chest type", ["chest", "trapped_chest"], no_selection_label=f"Selected: {data['chest_type']}")
                        
            def save_changes():
                with open(f'{script_directory}/data\data.json', 'r') as file:
                    data = json.load(file)
                
                data['server_ip'] = server_ip
                data['server_port'] = server_port
                data['bot_name'] = bot_name
                data['quit_on_low_health'] = healt_toggle
                data['low_health_threshold'] = range_slider
                data['password'] = password
                data['auth'] = auth
                data['viewer_ip'] = viewer_ip
                data['viewer_port'] = viewer_port
                data['chest_type'] = chest_type
                data['chest_range'] = chest_range
                data['version'] = version
                
                with open(f'{script_directory}/data\data.json', 'w') as file:
                    json.dump(data, file, indent=4)


        with col2:
            server_port = st.text_input(label="Server port", placeholder="25565", value=data["server_port"])
            viewer_port = st.text_input(label="Viewer port", placeholder="2000", value=data["viewer_port"])
            
            auth = selectbox("Select an authentication method", ["microsoft", "cracked"], no_selection_label=f"Selected: {data['auth']}")
            version = selectbox("Select an Minecraft version", ["auto", "1.19", "1.18", "1.17", "1.16", "1.15", "1.14", "1.13", "1.12"], no_selection_label=f"Selected: {data['version']}")
            chest_range = st.text_input(label="Chest range", placeholder="100", value=data["chest_range"])

        st.markdown("""---""")
        st.header("WIP section")
        add_vertical_space(1)
        
        wip_col1, wip_col2 = st.columns((2, 5))
        
        with wip_col1:
            healt_toggle = tog.st_toggle_switch(label="Quit on low health", 
                        key="Key1",
                        default_value=data["quit_on_low_health"], 
                        label_after = False, 
                        inactive_color = '#D3D3D3', 
                        active_color="#11567f", 
                        track_color="#29B5E8",
                        )
            
        with wip_col2:
            range_slider = st.slider(label=" ", label_visibility="collapsed" , min_value=1, max_value=19, value=data["low_health_threshold"], disabled=not healt_toggle)

        add_vertical_space(2)
        
        save_button = st.button(label="Save changes")
        
        if save_button:
            save_changes()
            st.toast("Saved changes!")
    
    if tabs == 'Analytics':
        st.title("Delivery analytics")
        st.header("WIP - Placeholder values only")
        csv_df = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
        my_grid = grid(2, [2, 4, 1], 1, 4, vertical_align="bottom")
        
        my_grid.dataframe(csv_df, use_container_width=True)
        my_grid.line_chart(csv_df, use_container_width=True)

webmode()
