# import the package
from .mineflayer import createBot
 

bot = createBot(
  host='localhost',          # minecraft server ip
  username='Bot',            # username or email, switch if you want to change accounts
  auth='microsoft'           # for offline mode servers, you can set this to 'offline'
  # port: 25565,             # only set if you need a port that isn't 25565
  # version: false,          # only set if you need a specific version or snapshot (ie: "1.8.9" or "1.16.5"), otherwise it's set automatically
  # password: '12345678'     # set if you want to use password-based auth (may be unreliable). If specified, the `username` must be an email
)

