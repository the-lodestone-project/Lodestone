<file-attachment-contents filename="README.md">

<h1 align="center">
  <br>
  <a href="https://github.com/SilkePilon/lodestone/"><img src="assets/C4B08ED9-101B-4789-8ECF-8B82E1435824.jpeg" alt="Lodestone" width="560"></a>
  <br>
</h1>

<h4 align="center">🤖 Create Minecraft bots with a powerful, stable, and high level Python API.</h4>

<p align="center">
    <img alt="Node version" src="https://img.shields.io/static/v1?label=node&message=%20%3E=18.0.0&logo=node.js&color=2334D058" />
      <a href="https://python.org/"><img src="https://img.shields.io/badge/Python-FFD43B?logo=python&logoColor=blue" alt="Python"></a>
  <a href="https://github.com/reworkd/AgentGPT/blob/master/docs/README.zh-HANS.md"><img src="https://img.shields.io/badge/JavaScript-323330?logo=minecraft&logoColor=F7DF1E" alt="javascript"></a>
  <a href="soon!"><img src="https://img.shields.io/badge/Discord-5865F2?logo=discord&logoColor=white" alt="Hungarian"></a>
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

Lodestone is an incredibly powerful and flexible framework for building Minecraft bots of all kinds.
Whether you’re new to Minecraft bot development or a seasoned pro, Lodestone provides all the tools you need to bring your bot ideas to life.
Let’s dive into how to get up and running with Lodestone.

## Features

* Supports Minecraft 1.8, 1.9, 1.10, 1.11, 1.12, 1.13, 1.14, 1.15, 1.16, 1.17, 1.18, 1.19 and 1.20.1.
* Entity knowledge and tracking.
* Block knowledge. You can query the world around you. Milliseconds to find any block.
* Physics and movement - handle all bounding boxes
* Attacking entities and using vehicles.
* Inventory management.
* Crafting, chests, dispensers, enchantment tables.
* Digging and building.
* Miscellaneous stuff such as knowing your health and whether it is raining.
* Activating blocks and using items.
* Chat.

## Getting Started 🏁

> [!IMPORTANT]
> Some parts of the code are still in development and do not work!

All instalation instructons and documentation can be found [here](https://lodestone-documentation.vercel.app/ "docs") but here is the general idea.

Install
To start building a Lodestone based bot, you first have to install the lodestone, package. run the following command to install the package:
'''pip install lodestone'''

💡
If you already have the lodestone package installed you can skip this step, you only need to install lodestone for the bot to work.
Create a bot.py
Create the following bot.py file in your project’s root directory:
'''import lodestone
 
bot = lodestone.createBot(
  host='localhost',
  username='Bot',
)'''

With the above configuration, Lodestone will create a bot with the name bot that joins the java server localhost (localy run server). Other Lodestone bot creation configurations can be found Here.
Run your bot
After coding your very own Minecraft bot you can simply run the following command to start the bot!:
Terminal
# can be python3 on some systems
python bot.py

And run the next or next dev command specified in package.jsonto start developing the project! 🎉
Sign in
Lastly, if your not already signed in bot will ask you to sign in using Microsoft by default. The message will look something like this:
'''It seems you are not logged in, please go to https://microsoft.com/link and enter the following code: ********'''

after you sucsessfully sign in in to your account account the bot will be created.
Full auth configurations can be found here.


### Arguments & Options 📄

> [!IMPORTANT]
> Not changing some of these settings will result in the bot not working. 🛑

> [!WARNING]
> Do not share your Minecraft info to anyone. 🔒

<details open>
<summary>How to use the arguments</summary>
<br>

The command line arguments available are:

* `--email`: The Minecraft Email the bot will log into (use a name and no password for a cracked account). 📧
* `--password`: The password for your account (if not using cracked). 🔑
* `--host`: The IP address or hostname of the Minecraft server. 🖥
* `--port`: The port number the Minecraft server is listening on. Default is 25565. ⚡
* `--auth`: The authentication method your account requires (mojang/microsoft/cracked). Default is "microsoft". 🔐
* `--version`: Minecraft version to use when connecting to a server. Default is auto. 🕹
* `--check_timeout`: How often in milliseconds the bot checks if it is still logged into the server. Default is 600000 (10 minutes). ⏱
* `--viewer_port`: The local port to run the viewer server on so you can visually see what the bot is doing. Default is 8000. 👀
* `--quit_on_low_health`: Disconect the bot if the bot is on low health. Default is "True". 👤
* `--low_health_threashold`: How low the health must be for the bot to quit. Default is "10". 👤
* `--armor_equip`: If the bot needs to equip all available armor. Default is "True". 👤

</details>

### 🚀 GitHub Codespaces (run the bot in the cloud)

> [!IMPORTANT]
> If the console gets spammed with random data, try changing the version from false to a version you know is supported by the server.

1. Copy this code to you clipboard and run it once the terminal is available

```bash
python -m opendeliverybot
```

2. Open GitHub CodeSpaces below

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/SilkePilon/OpenDeliveryBot)

---

## Contributors ❤️
| Name                | Helped With                               | GitHub   | Discord   |
| --------------------- | ----------------------------------------- | ----------- | ----------- |
| **Katzengott**            | fishing bot and cactus bot | [@Katzengott](https://github.com/Katzengott) | edelkatze |



## Roadmap

- [X] Add config.json file
- [X] Add [click](https://github.com/pallets/click)
- [X] Change to use as Pip package for better use
- [X] Add Discord integration
- [ ] Add Lava Caster (request by @givenbakerad on Discord)
- [ ] Add Custom code runner (a way for users to test their own bot code in a nice and simple way)

## MineFlayer 🚀

Mineflayer is a complex library that allows you to control Minecraft accounts through a powerful, stable, and high-level JavaScript API

## Discord

https://discord.gg/Fa7HZgkczz

## Credits

<a href="https://github.com/PrismarineJS/mineflayer" target="_blank">MineFlayer</a>

---

Screenshots:
[Dashboard](https://imgur.com/a/Hceiwhp)
[Settings](https://imgur.com/a/9p1YbtE)

</file-attachment-contents>
