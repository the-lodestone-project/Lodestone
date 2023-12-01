import lodestone

lodestone.get_plugins()

from __init__ import plugins

lodestone.createBot(
    host="2b2t.org",
    username="CustomCapes",
    ls_skip_checks=True,
)