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

Welcome to the Open Delivery Bot project! This open-source initiative empowers users to deploy a self-hosted delivery bot, offering an array of advanced functionalities. Our command-line interface (CLI) or remote web GUI allows effortless control and management, ensuring a seamless experience. 🤖

Open Delivery Bot shines with its dynamic features, including pathfinding and optimized elytra flight, accelerating your delivery processes for utmost efficiency. Say goodbye to manual intervention and embrace automation! 📦

## Getting Started 🏁

> [!IMPORTANT]
> Some parts of the code are still in development and do not work!

All instalation instructons can be found [here](https://open-delivery-bot-documentation.vercel.app/)

### (6) Arguments & Options 📄

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

https://discord.gg/z8yRexNc3U

## Credits

<a href="https://github.com/PrismarineJS/mineflayer" target="_blank">MineFlayer</a>

---

Screenshots:
[Dashboard](https://imgur.com/a/Hceiwhp)
[Settings](https://imgur.com/a/9p1YbtE)

</file-attachment-contents>
