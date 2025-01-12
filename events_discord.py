from discord import FFmpegPCMAudio
from utils import load_history, save_history, process_input, generate_audio
import os
from config import BOT_NAME

class EventHandler:
    def __init__(self, bot):
        self.bot = bot
        self.register_events()

    def register_events(self):
        @self.bot.event
        async def on_message(message):
            # Ignore bot messages to avoid infinite loops
            if message.author == self.bot.user:
                return

            # Check if it is a command
            if message.content.startswith(self.bot.command_prefix):
                await self.bot.process_commands(message)
                return

            # Check if the bot name is mentioned in the message
            if BOT_NAME in message.content:
               
                history = load_history()

                
                user_name = message.author.name  
                full_message = f"{user_name} : {message.content}"  

               
                history.append({"role": "user", "content": full_message})

             
                save_history(history)

            
                bot_response = process_input(history)

           
                history.append({"role": "assistant", "content": bot_response})

            
                save_history(history)

      
                await message.reply(bot_response)


                if message.guild.voice_client:
                    generate_audio(bot_response, "response.mp3")
                    message.guild.voice_client.play(FFmpegPCMAudio("response.mp3"), after=lambda e: os.remove("response.mp3"))


            if message.reference and message.reference.message_id:
                referenced_message = await message.channel.fetch_message(message.reference.message_id)
                if referenced_message.author == self.bot.user:  

                    history = load_history()


                    user_name = message.author.name  
                    full_message = f"{user_name} : {message.content}"


                    history.append({"role": "user", "content": full_message})


                    save_history(history)


                    bot_response = process_input(history)


                    history.append({"role": "assistant", "content": bot_response})


                    save_history(history)

                    await message.reply(bot_response)

                    # Read the response aloud in the voice channel
                    if message.guild.voice_client:
                        generate_audio(bot_response, "response.mp3")
                        message.guild.voice_client.play(FFmpegPCMAudio("response.mp3"), after=lambda e: os.remove("response.mp3"))

        @self.bot.event
        async def on_ready():
            print(f"Bot connected as {self.bot.user}")
