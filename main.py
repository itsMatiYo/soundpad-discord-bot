import os

from dotenv import load_dotenv

# import app
from bot import bot

# import threading


if __name__ == "__main__":
    load_dotenv()
    # threading.Thread(target=app.app.run).start()
    bot.run(os.getenv("TOKEN"))

# git pull heroku master
