<file-attachment-contents filename="README.md">

<h1 align="center">
  <br>
  <a href="https://github.com/SilkePilon/OpenDeliveryBot/"><img src="https://github.com/SilkePilon/OpenDeliveryBot/blob/main/logo.png?raw=true" alt="YouAgent" width="500"></a>
  <br>
  <br>
  Open Delivery Bot 📦
  <br>
</h1>

<h4 align="center">🤖📦 Deliver anything, anywere! powered by <a href="https://github.com/PrismarineJS/mineflayer" target="_blank">MineFlayer</a>.</h4>

<p align="center">
    <img alt="Node version" src="https://img.shields.io/static/v1?label=node&message=%20%3E=16.0.0&logo=node.js&color=2334D058" />
      <a href="https://github.com/reworkd/AgentGPT/blob/master/README.md"><img src="https://img.shields.io/badge/lang-English-blue.svg" alt="English"></a>
  <a href="https://github.com/reworkd/AgentGPT/blob/master/docs/README.zh-HANS.md"><img src="https://img.shields.io/badge/lang-简体中文-red.svg" alt="简体中文"></a>
  <a href="https://github.com/reworkd/AgentGPT/blob/master/docs/README.hu-Cs4K1Sr4C.md"><img src="https://img.shields.io/badge/lang-Hungarian-red.svg" alt="Hungarian"></a>
</p>

<p align="center">
  <a href="#about">About</a> •
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#how-to-install">Install</a> •
  <a href="#credits">Credits</a> •
  <a href="#license">License</a>
</p>

<!-- ![screenshot](https://raw.githubusercontent.com/SilkePilon/youdotcom/main/assets/images/YouDotCom.jpg) -->

## About 📬

Welcome to the Open Delivery Bot project! This open-source initiative empowers users to deploy a self-hosted delivery bot, offering an array of advanced functionalities. Our command-line interface (CLI) or remote web GUI allows effortless control and management, ensuring a seamless experience. 🤖

Open Delivery Bot shines with its dynamic features, including pathfinding and optimized elytra flight, accelerating your delivery processes for utmost efficiency. Say goodbye to manual intervention and embrace automation! 📦

## Getting Started 🏁

> [!IMPORTANT]
> Some parts of the code are still in development and do not work!

### 🐍 Local Setup

Here are step-by-step instructions on how to install and run the python script:

#### (1) Install Node.js 🟢 (2 simple steps)

1. Download and install Node.js 18 from https://nodejs.org/en/
2. Verify installation:

```
node -v
```

#### (2) Install Python 🐍 (2 simple steps)

1. Download and install Python 3 (if not already installed) from https://www.python.org/downloads/
2. Verify installation:

```
python3 --version
```

#### (3) Install pip ⏬ (2 simple steps)

1. Install pip3 (if not already installed):

Mac/Linux:

```
sudo apt install python3-pip  
```

Windows:

```
py -m ensurepip --default-pip
```

2. Verify installation:

```
pip3 --version
```

#### (4) Clone 💻 (2 simple steps)

1. Clone this repository 🍴

```
git clone https://github.com/SilkePilon/OpenDeliveryBot.git
```

2. Navigate into the repo directory 📂

```
cd OpenDeliveryBot  
```

#### (5) Install packages 📦 (1 simple step)

1. Use pip to install needed packages

```
pip install -r requirements.txt
```


#### (6) Config.json 📄 (1 step)

> [!IMPORTANT]
> Not changing these settings will result in the bot not working. 🛑

> [!WARNING]
> Do not share this file to anyone as it may contain your Minecraft login details. 🔒

<details open>
<summary>How to change to config file</summary>
<br>

The settings you NEED to edit are:

* `Username`: The Minecraft Email the bot will log into (use a name and no password for a cracked account). 📧
* `Password`: The password for your account (if not using cracked). 🔑
* `Host`: The IP address or hostname of the Minecraft server. 🖥
* `Port`: The port number the Minecraft server is listening on. Default is 25565. ⚡
* `Auth`: The authentication method your account requires (mojang/microsoft/cracked). Default is "microsoft". 🔐
* `Version`: Minecraft version to use when connecting to a server (false is auto). Default is false. 🕹
* `CheckTimeoutInterval`: How often in milliseconds the bot checks if it is still logged into the server. Default is 600000 (10 minutes). ⏱
* `ViewerPort`: The local port to run the viewer server on so you can visually see what the bot is doing. Default is 8000. 👀
* `Goto`: The x, y, z coordinates for the bot to navigate to. Default is "100 ~ 100" (x=100, y doesn't matter, z=100). 🗺
* `ChestRange`: How close a chest must be to the bot for the bot to pathfind to it. Default is 100 blocks. 📦
* `InitChestType`: The type of chest for the bot to get items from. Default is "Chest". 🗄
* `InitChestCords`: The coordinates of the initial chest. Default is "100 100 100". 📍
* `InitItemsName`: The name of the item(s) to get from the initial chest. Default is "SchulkerBox". 🎒
* `InitItemsCount`: The number of items to place in the initial chest. Default is 1. 🔢
* `ClientUsername`: The username for the client the delivery is made to. Default is "OpenDeliveryBot". 👤

This is how the file looks like in its default state:

```json
{
    "Username": "OpenDeliveryBot", 
    "Password": "",
    "Host": "127.0.0.1",
    "Port": 25565,
    "Auth": "microsoft",
    "Version": "false",
    "CheckTimeoutInterval": 600000,
    "ViewerPort": 8000,
    "Goto": "100 ~ 100",
    "ChestRage": 100,
    "InitChestType": "Chest",
    "InitChestCords": "100 100 100",
    "InitItemsName": "SchulkerBox",
    "InitItemsCount": 1,
    "ClientUsername": "OpenDeliveryBot"
}
```

</details>

#### (6) Run the bot 🤖 (1 simple step)

1. Run the bot

```
python3 main.py
```

Enjoy automated deliveries! 🎉

### 🚀 GitHub Codespaces

SOON!

---

## How To Use

SOON! 🕐

## Discord

SOON!

## Credits

<a href="https://github.com/PrismarineJS/mineflayer" target="_blank">MineFlayer</a>

---

</file-attachment-contents>
