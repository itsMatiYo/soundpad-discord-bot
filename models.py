from peewee import *
from dotenv import load_dotenv
import os

load_dotenv()

db = SqliteDatabase(os.getenv('DB'))


class Command(Model):
    name = CharField()
    url = CharField()
    # birthday = DateField()
    server_id = BigIntegerField()

    class Meta:
        database = db  # This model uses the "people.db" database.


def validate_command_name(name, server_id):
    if Command.select().where(Command.name == name, Command.server_id == server_id):
        return False
    return True


def validate_command_url(url, server_id):
    if Command.select().where(Command.url == url, Command.server_id == server_id):
        return False
    return True


db.connect()
