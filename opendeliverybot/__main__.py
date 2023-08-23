import streamlit as st
from st_on_hover_tabs import on_hover_tabs
import streamlit_toggle as tog
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.stateful_button import button
from streamlit_extras.no_default_selectbox import selectbox
from javascript import require, On
import datetime
import webbrowser
import json
import asyncio

st.set_page_config(
    page_title="Bot controller",
    page_icon="🕹",
    layout="centered",
    initial_sidebar_state="auto",
)

with open('data\data.json', 'r') as f:
    data = json.load(f)

class coords_vec:
    def __init__(self, x_coord, y_coord, z_coord):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.z_coord = z_coord

class advPositionVec3:
    def __init__(self, x, y, z):
        self.position = {'x': x, 'y': y, 'z': z}

    def __str__(self):
        return f"Vec3 {{ x: {self.position['x']}, y: {self.position['y']}, z: {self.position['z']} }}"

def makeBot(x_coord, y_coord, z_coord):
    mineflayer = require('mineflayer')
    # pathfinder = require('mineflayer-pathfinder')
    # goals = require('mineflayer-pathfinder').goals
    navigatePlugin = require('mineflayer-navigate')(mineflayer)
    mineflayerViewer = require('prismarine-viewer').mineflayer
    Vec3 = require("vec3").Vec3
    windows = require('prismarine-windows')(data["version"])
    Item = require('prismarine-item')(data["version"])
    
    bot = mineflayer.createBot({
        'host': data["server_ip"],
        'port': data["server_port"],
        'username': data["bot_name"],
        'password': data["password"],
        'auth': data["auth"],
        'version': data["version"],
        'checkTimeoutInterval': data["check_timeout_interval"],
    })
    
    # bot.loadPlugin(pathfinder.pathfinder)
    navigatePlugin(bot)
    
    @On(bot, 'login')
    def handle_login(*args):
        mineflayerViewer(bot, { "firstPerson": True, "port": data["viewer_port"] })
        global mcData
        mcData = require('minecraft-data')(bot.version)
        # movements = pathfinder.Movements(bot, mcData)
    
        with open("logs\players.log", "w") as x:
            x.write(str(bot.players))
        
        with open("logs\coords.log", "a") as x:
            x.write(f'{datetime.datetime.now()}  |  {data["server_ip"]}:{data["server_port"]}  |  X:{str(bot.entity.position.x)}, Y:{str(bot.entity.position.y)}, Z:{str(bot.entity.position.z)}')

        # movements.canDig = False
        
        # bot.pathfinder.setMovements(movements)
        
        pos1 = coords_vec(float(x_coord), float(y_coord), float(z_coord))
        
        @On(bot, "death")
        def death(this):
            bot.end()
            bot.viewer.close()
            st.toast("Bot died... stopping bot!")
        
        @On(bot, "kicked")
        def kicked(this, reason, *a):
            bot.end()
            bot.viewer.close()
            st.toast("Kicked from server... stopping bot!")
                
        def itemByName(items, name):
            item = None
            for i in range(len(items)):
                item = items[i]
                if item and item['name'] == name:
                    return item
                return None
        
        def GetItems():
            x = data["chest_coords"][0]
            y = data["chest_coords"][1]
            z = data["chest_coords"][2]
            # locaton = bot.pathfinder.setGoal(pathfinder.goals.GoalNear(x, y, z, 1), timeout=60)
            target = Vec3(-107, 65, 0)
            bot.navigate.to(target)
            
            
            foundChest = False
        
            while not foundChest:
                
                chestToOpen = bot.findBlock({
                    'matching': [mcData.blocksByName[name].id for name in [f'{str(data["chest_type"]).lower()}']],
                    'maxDistance': 10,
                })
                
                # if not chestToOpen and foundChest == False:
                #     bot.chat('no chest found')
                #     bot.end()
                #     bot.viewer.close()
                
                if chestToOpen:
                    x = chestToOpen.position.x
                    y = chestToOpen.position.y  
                    z = chestToOpen.position.z

                    # locaton = bot.pathfinder.setGoal(pathfinder.goals.GoalNear(x, y, z, 1), timeout=60)
                
                if chestToOpen:
                    target = Vec3(x, y, z)
                    bot.navigate.to(target)
                                        
                    chest = bot.openChest(chestToOpen)
                    
                    @On("windowOpen", windows)
                    def window(window):
                        item = itemByName(chest.containerItems(), data["items_name"])
                        
                        if item:
                            try:
                                windows.withdraw(item.type, None, data['items_count'])
                            except Exception as err:
                                bot.chat(f"unable to withdraw {data['items_count']} {item.name}")
                        else:
                            bot.chat(f"unknown item {data['items_name']}")
                    
                    chest.close()

                    foundChest = True
                    
                    break
                
                else:
                    bot.chat("Can't find the chest")
        
        GetItems()
        
        def GoToLocation():
                x = float(x_coord)
                y = float(x_coord)
                z = float(z_coord)
                locaton =  bot.pathfinder.setGoal(pathfinder.goals.GoalNear(x, y, z, 1), timeout=60)
        
        def DepositItems():

            foundChest = False
            
            while not foundChest:
                
                chestToOpen = bot.findBlock({
                    'matching': [mcData.blocksByName[name].id for name in ['chest']], 
                    'maxDistance': data["chest_range"],
                })
            
                if not chestToOpen and foundChest == False:
                    st.toast("No delivery chest found")
                    break
                    
                if chestToOpen.position.x:
                    x = chestToOpen.position.x
                    y = chestToOpen.position.y  
                    z = chestToOpen.position.z

                    locaton = bot.pathfinder.setGoal(pathfinder.goals.GoalNear(x, y, z, 1), timeout=60)
                    
                    try:
                        chest = bot.openContainer(chestToOpen)
                    except Exception:
                        print(Exception)
                        continue
                    
                    item = next((item for item in chest.slots if item and item.name == f'{data["items_name"]}'), None)
                    windows.deposit(item, "null", "null", "null")
                    
                    chest.close()

                    foundChest = True
                    
                    break
        
        async def queueFunc():        
            queue = asyncio.Queue(maxsize=3)
            
            await queue.put(GetItems)
            await queue.put(GoToLocation)
            await queue.put(DepositItems)
        
            async def consumer():
                while True:
                    task = await queue.get()
                    await task()
                    queue.task_done()
            
            tasks = [
                asyncio.create_task(consumer()),
                asyncio.create_task(consumer()),
                asyncio.create_task(consumer())
            ]
            await asyncio.gather(*tasks)

        # asyncio.run(queueFunc())
        # GoToLocation()
        # DepositItems()
        
def main():
    st.markdown(
        "<style>"
        + open(
            "frontend\styles.css"
        ).read()
        + "</style>",
        unsafe_allow_html=True,
    )

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

        def openViewer():
            webbrowser.open(f'http://{data["viewer_ip"]}:{data["viewer_port"]}')

        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 2])

        with col1:
            x_coord = st.text_input("x", label_visibility="collapsed", placeholder="X coord")
                
        with col2:
            y_coord = st.text_input("y", label_visibility="collapsed", placeholder="Y coord")
            
        with col3:
            z_coord = st.text_input("z", label_visibility="collapsed", placeholder="Z coord")

        with col5:
            start_dropoff_bot = st.button("Deliver item", )
            
        with col4:
            if start_dropoff_bot:
                prismarineViewer_button = st.button("Open bot view", key="viewer_button", on_click=openViewer)
                try:
                    makeBot(x_coord, y_coord, z_coord)
                    # mineflayer = require('mineflayer')
                    # pathfinder = require('mineflayer-pathfinder')
                    # mineflayerViewer = require('prismarine-viewer').mineflayer
                    
                    # bot = mineflayer.createBot({
                    #     'host': data["server_ip"],
                    #     'port': data["server_port"],
                    #     'username': data["bot_name"],
                    # })
                    
                    # bot.loadPlugin(pathfinder.pathfinder)
                    
                    # @On(bot, 'login')
                    # def handle_login(*args):
                    #     mineflayerViewer(bot, { "port": data["viewer_port"] })
                    #     print("test")
                    
                    # @On(bot, 'chat')
                    # def handleMsg(this, sender, message, *args):
                    #     player = bot.players[sender]
                    #     target = player.entity
                    #     print(target)
                    
                    # @On(bot, "death")
                    # def death(this):
                    #     bot.end()
                    #     bot.viewer.close()
                    #     st.toast()
                    
                    # st.toast("Bot started!", icon="✅")

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

main()
