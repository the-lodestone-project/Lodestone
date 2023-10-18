import lodestone

import sys
import re


if len(sys.argv) < 3 or len(sys.argv) > 5:
    print("Usage : python bee.py <host> <port> [<name>] [<password>]")
    quit(1)

bot = lodestone.Bot(host=sys.argv[1], port=int(sys.argv[2]), password=sys.argv[4] if len(sys.argv) > 4 else '',
                    username=sys.argv[3] if len(sys.argv) > 3 else 'book')

pages = [
  'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
  'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
  'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.',
  'Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
]

def transform_page(page):
    words = page.split(' ')
    transformed_words = []

    for i, word in enumerate(words):
        formatted_word = f'§{(i % 13 + 1):x}'
        if i % 2 != 0:
            formatted_word += '§l'
        formatted_word += word
        transformed_words.append(formatted_word)

    return ' '.join(transformed_words)

transformed_pages = [transform_page(page) for page in pages]

@bot.on("chat")
def chat(_, username, message, *args):
    if username == bot.username: return
    match message:
        case "print":
            print_book()
        case "write":
            write_book()
        case "toss":
            toss_book()

def toss_book():
    items = bot.inventory.items()
    for item in items:
        if item.name == "writable_book":
            found_item = item
            break
    else:
        bot.chat("I don't have a book!")
        return
    bot.bot.tossStack(found_item)

def write_book():
    items = bot.inventory.items()
    for item in items:
        if item.name == "writable_book":
            found_item = item
            break
    else:
        bot.chat("I don't have a book!")
        return
    bot.bot.writeBook(found_item.slot, transformed_pages, timeout=100)

def print_book():
    items = bot.inventory.items()
    for item in items:
        if item.name == "writable_book":
            found_item = item
            break
    else:
        bot.chat("I don't have a book!")
        return
    for i, page in enumerate(found_item.nbt.value.pages.value.value):
        bot.chat(f"Page {i + 1}: {re.sub('§[a-z0-9]', '', page)}")
