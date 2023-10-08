import lodestone
mcbot = lodestone.createBot(
  host='connect.2b2t.org',
  username='silke2007minecraft@gmail.com',
  auth='microsoft',
  disableLogs=False,
  enableChatLogging=False,# makes a database for the server and logs all the messages
  skipChecks=True
)

@lodestone.Event(mcbot.bot, 'messagestr')
def chat(this, message, messagePosition, jsonMsg, sender, *args):
    message = str(message).replace("\n\n","")
    print(f"{sender}: {message}")

# print(mcbot.chatHistory(username="idk xD"))# prints all the messages from this player