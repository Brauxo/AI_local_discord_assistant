from config import bot  # Import the configured bot
from command_discord import CommandHandler  # Import commands
from events_discord import EventHandler  # Import events
from config import DISCORD_TOKEN
from utils import init_system_prompt

def setup_bot():
    CommandHandler(bot)  
    EventHandler(bot)    

if __name__ == "__main__":
    setup_bot()
    init_system_prompt()
    try:
        bot.run(DISCORD_TOKEN)  
    except Exception as e:
        print(f"Error starting the bot: {e}")


