import discord
from discord.ext import commands

# Config of the bot
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="/", intents=intents)

# Model name used by your ollama
MODEL_NAME = "Mistral"

# PATH FOR THE ffmpeg.exe file that need to be installed for audio
HISTORY_FILE = "chat_history.json"
FFMPEG_EXECUTABLE = "ffmpeg.exe"

# System prompt of your bot
SYSTEM_PROMPT = "You are a Discord BOT that interact with users.  Keep your answers short"

#DISCORD TOKEN OF YOUR BOT
DISCORD_TOKEN = ""

#BOT NAME (will be used so that when the bot is mentionned it answer to your message)
BOT_NAME = "BOT"