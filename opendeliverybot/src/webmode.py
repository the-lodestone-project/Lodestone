import streamlit as st
from st_on_hover_tabs import on_hover_tabs
import streamlit_toggle as tog
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.stateful_button import button
from streamlit_extras.no_default_selectbox import selectbox
from streamlit_extras.grid import grid
from javascript import require, On
import pandas as pd
import numpy as np
import math
import datetime
import requests
import json
import asyncio
from bot import makeBot

st.set_page_config(
    page_title="Bot controller",
    page_icon="🕹",
    layout="centered",
    initial_sidebar_state="auto",
)

with open('data\data.json', 'r') as f:
    data = json.load(f)
        
def webmode():
    st.markdown("<style>" + open("frontend\styles.css").read() + "</style>", unsafe_allow_html=True)

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
                    ":hover :hover": {"color": "red", "cursor": "pointer"}
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
        st.title("Bot controller")
            
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
                
            def openViewer():
                render = st.markdown('<iframe width="700rem" height="400rem" src="http://127.0.0.1:1000" frameborder="0" scrolling="auto" allowfullscreen id="render"></iframe>', unsafe_allow_html=True)

            # if isViewerRunning:
            #     start_dropoff_bot = st.button("Deliver item", disabled=True)
            # else:
            start_dropoff_bot = st.button("Deliver item")
            
        with col4:
            # if isViewerRunning:
            #     prismarineViewer_button = st.button("Open bot view", key="viewer_button", on_click=openViewer)
            # else:
            prismarineViewer_button = st.button("Open bot view", key="viewer_button", on_click=openViewer)
            if start_dropoff_bot:
                try:
                    makeBot(x_coord, y_coord, z_coord, data)
                    
                    st.toast("Bot started!", icon="✅")

                except ValueError:
                    st.toast("Please enter a valid float number", icon="🚨")
            
        
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
                with open('data\data.json', 'r') as file:
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
                
                with open('data\data.json', 'w') as file:
                    json.dump(data, file, indent=4)


        with col2:
            server_port = st.text_input(label="Server port", placeholder="25565", value=data["server_port"])
            viewer_port = st.text_input(label="Viewer port", placeholder="2000", value=data["viewer_port"])
            
            auth = selectbox("Select an authentication method", ["Microsoft", "Cracked"], no_selection_label=f"Selected: {data['auth']}")
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