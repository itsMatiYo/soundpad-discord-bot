from bot import bot
import os
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    bot.run(os.getenv('TOKEN'))


# git pull heroku master
