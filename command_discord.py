from discord.ext import commands
from utils import generate_audio, load_history, save_history, process_input, get_audio, process_speech
from discord import FFmpegPCMAudio
from config import BOT_NAME
import os
import asyncio

# for listening
listening = False

class CommandHandler:
    def __init__(self, bot):
        self.bot = bot
        self.register_commands()

    def register_commands(self):
        @self.bot.command()
        async def AIjoin(ctx):
            if ctx.author.voice:
                channel = ctx.author.voice.channel
                await channel.connect()
                await ctx.send(f"I have connected to the voice channel: {channel}, pretty cool, right?")
            else:
                await ctx.send("I need to be in a voice channel to use this command :)!")

        @self.bot.command()
        async def AIquit(ctx):
            global listening
            if ctx.voice_client:
                listening = False  # Disable listening
                await ctx.voice_client.disconnect()
                await ctx.send("I have been kicked from the voice channel! :(")
            else:
                await ctx.send("I am not connected to any voice channel.")

        @self.bot.command()
        async def AIanswer(ctx, *, message: str):
            history = load_history()
            user_name = ctx.author.name
            full_message = f"{user_name} says: {message}"
            history.append({"role": "user", "content": full_message})

            bot_response = process_input(history)
            history.append({"role": "assistant", "content": bot_response})
            save_history(history)

            await ctx.reply(bot_response)

        @self.bot.command()
        async def AIlisten(ctx):
            global listening
            if ctx.voice_client and ctx.voice_client.channel:
                await ctx.send("Listening enabled. Speak in the voice channel.")
                listening = True  # Enable listening
                
                while listening:
                    user_voice_text = get_audio()  # Listen to the user via speech recognition
                    if user_voice_text:
                        user_name = ctx.author.name 
                        full_message = f"{user_name} says: {user_voice_text}"  # Full message
                        
                        
                        history = load_history()
                        history.append({"role": "user", "content": full_message})
                        
                        
                        bot_response = process_speech(history)
                        
                        # Read the response aloud in the voice channel
                        if ctx.voice_client:
                            generate_audio(bot_response, "response.mp3")
                            ctx.voice_client.play(
                                FFmpegPCMAudio("response.mp3"), 
                                after=lambda e: os.remove("response.mp3")
                            )

                        history.append({"role": "assistant", "content": bot_response})
                        save_history(history)
                        
                        # Calculate the wait time based on the response length
                        response_length = len(bot_response)
                        
                        # Adjustable
                        base_sleep_time = 2  # Default value
                        extra_time = response_length // 100  # Adds one second for every 60 characters
                        sleep_time = base_sleep_time + extra_time  # Calculate the wait time
                        
                        # Ensure the sleep time is not too short or too long
                        sleep_time = max(sleep_time, 2)  # Minimum value
                        sleep_time = min(sleep_time, 8)  # Maximum value
                        
                        await asyncio.sleep(sleep_time)
                    else:
                        await asyncio.sleep(0.5)


            else:
                await ctx.send("The bot must be in a voice channel to listen.")

        @self.bot.command()
        async def AIstop(ctx):
            global listening
            if listening:
                listening = False  # Disable listening
                await ctx.send("Listening disabled.")
            else:
                await ctx.send("Listening is not enabled.")


        @self.bot.command()
        async def AIhelp(ctx):
            help_text = f"""
            Just mention {BOT_NAME} or reply to one of my messages to get a response.

            Here is a list of my commands:
            **/AIjoin**: Joins a voice channel.
            **/AIquit**: Leaves the voice channel.
            **/AIlisten**: Activates listening to discuss in voice.
            **/AIstop**: Deactivates listening.
            **/AIhelp**: Displays help.
            **/AIanswer**: Replies to a message.

            Use these commands to interact with me!
            """
            await ctx.send(help_text)

