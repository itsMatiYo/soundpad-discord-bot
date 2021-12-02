from bot import bot
from peewee import *
import os
from dotenv import load_dotenv
from models import db, Command

if __name__ == "__main__":
    load_dotenv()
    bot.run(os.getenv('TOKEN'))
    db.create_tables([Command, ])


# git pull heroku master
