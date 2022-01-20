# Soundpad Discord Bot

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/itsMatiYo/soundpad-discord-bot/tree/master)

After cloning the project create a .env file which has following variables:

1. TOKEN (your bot token)
2. FIREBASE_API (So you can save commands in firebase real-time database)

Then run main.py

Be sure that you have ffmpeg.exe(for windows) in project directory. Later on if you wanted to run this bot heroku you should use add-ons for ffpmpeg.

> Pay attention that you need to set the rules of your firebase database to true.

## Instructions

Type `-sos` or `-help` for helping text

Type `-p <command>` to play a command

Type `-dc` to disconnect bot

### For administrators

Type `-del <command>` to delete command

Type `-add <command> <url>` to add command. Be sure that the url should end in .mp4 or mp3 or other video or audio file formats. You can copy the link of a file in discord and use it as a url.

#### This bot can also moderate (delete @everyone for members who can't mention everyone)

### Also added flask so your project does not go idle (use [https://uptimerobot.com/] to ping site)
