
<h1 align="center">
  <br>
  <a href="https://github.com/SilkePilon/OpenDeliveryBot/"><img src="https://github.com/SilkePilon/OpenDeliveryBot/blob/main/logo.png?raw=true" alt="YouAgent" width="500"></a>
  <br>
  <br>
  Open Delivery Bot
  <br>
</h1>

<h4 align="center">🤖 Deliver anything, anywere! powered by <a href="https://github.com/PrismarineJS/mineflayer" target="_blank">MineFlayer</a>.</h4>

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

## About
YouAgent is an innovative AI tool that allows you to assemble, configure, and deploy autonomous AI agents using YouChat. With YouAgent, you can create and customize your own AI agent, and give it a unique name that suits its purpose. You can then set a goal for your agent to achieve, and watch as it uses its intelligent algorithms to execute tasks and learn from the results.

Whether you're looking to automate a process, improve efficiency, or simply explore the capabilities of AI, YouAgent offers an easy and intuitive way to do so. YouAgent gives you full control over your AI agent, allowing you to tailor it to your specific needs.

Whether you're a developer, a business owner, or just someone curious about the possibilities of AI, YouAgent is the perfect tool to help you get started. With its intuitive interface, powerful features, and endless customization options, YouAgent makes it easy to create, deploy, and manage your own autonomous AI agent. So why wait? Start exploring the possibilities of AI with YouAgent today!


## Getting Started

### 🐳 Docker Setup

The easiest way to run YouAgent locally is by using docker.
A convenient setup script is provided to help you get started.

```bash
./setup.sh --docker
```

### 👷 Local Development Setup

If you wish to develop YouAgent locally, the easiest way is to
use the provided setup script.

```bash
./setup.sh --local
```

### 🛠️ Manual Setup

> 🚧 You will need [Nodejs +18 (LTS recommended)](https://nodejs.org/en/) installed.

1. Fork this project:

- [Click here](https://github.com/SilkePilon/YouAgent/fork).

2. Clone the repository:

```bash
git clone git@github.com:YOU_USER/YouAgent.git
```

3. Install dependencies:

```bash
cd YouAgent
npm install
```

4. Create a **.env** file with the following content:

> 🚧 The environment variables must match the following [schema](https://github.com/SilkePilon/YouAgent/blob/main/src/env/schema.mjs).

```bash
# Deployment Environment:
NODE_ENV=development

# Next Auth config:
# Generate a secret with `openssl rand -base64 32`
NEXTAUTH_SECRET=changeme
NEXTAUTH_URL=http://localhost:3000
DATABASE_URL=file:./db.sqlite

# Your open api key
OPENAI_API_KEY=changeme
```

5. Modify prisma schema to use sqlite:

```bash
./prisma/useSqlite.sh
```

**Note:** This only needs to be done if you wish to use sqlite.

6. Ready 🥳, now run:

```bash
# Create database migrations
npx prisma db push
npm run dev
```

### 🚀 GitHub Codespaces

Set up YouAgent in the cloud immediately by using [GitHub Codespaces](https://github.com/features/codespaces).

1. From the GitHub repo, click the green "Code" button and select "Codespaces".
2. Create a new Codespace or select a previous one you've already created.
3. Codespaces opens in a separate tab in your browser.
4. In terminal, run `bash ./setup.sh --local`
5. Click "Open in browser" when the build process completes.

- To shut YouAgent down, enter Ctrl+C in Terminal.
- To restart YouAgent, run `npm run dev` in Terminal.

Run the project 🥳

```
npm run dev
```

---

## How To Use






## Discord
In addition to YouAgent, we also have an active [Discord server](https://discord.gg/SD7wZMFSvV) where you can chat with developers and get help with using the agent. Our Discord community is a great place to ask questions, share your projects, and get feedback from other developers.


## Credits
<a href="https://www.textstudio.com/">Text effect</a>
---
