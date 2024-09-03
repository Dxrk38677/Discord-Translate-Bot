import discord
from discord.ext import commands
import asyncio
from googletrans import Translator  # Import Google Translate library
#Made By Dxrk3867,Dxrk3867Bot
# Define the necessary intents for your bot
intents = discord.Intents.default()
intents.message_content = True  # Enables access to message content
intents.reactions = True        # Enables access to reactions

# Initialize the bot with the specified intents
bot = commands.Bot(command_prefix='.', intents=intents)
translator = Translator()

# Global variables to manage the translation state
translator_task = None
translation_active = False
selected_language = None
selected_flag = None  # To store the selected flag emoji
monitor_channel_id = None  # Channel ID where messages will be monitored
target_user_id = None      # User ID whose messages will be translated

@bot.command(name="support")
async def support(ctx, action=None, channel_id: int = None, user_id: int = None):
    global translator_task, translation_active, selected_language, selected_flag, monitor_channel_id, target_user_id

    if action not in ["start", "stop"]:
        await ctx.send("Invalid action. Use `.support start (channel_id) (user_id)` to begin translating and `.support stop` to stop the translation.")
        return

    if action == "start":
        if not channel_id or not user_id:
            await ctx.send("Please provide both a channel ID and a user ID.")
            return

        if translation_active:
            await ctx.send("Translation is already active.")
            return

        lang_emojis = {
            "🇩🇪": "de",  # German
            "🇫🇷": "fr",  # French
            "🇪🇸": "es",  # Spanish
            "🇬🇧": "en",  # English
            "🇷🇺": "ru",  # Russian
            # Add more languages and their respective flags here
        }

        message = await ctx.send(
            "Hello! Please select your language by reacting to the emoji that represents it."
        )

        # Add reactions for each language
        for emoji in lang_emojis.keys():
            await message.add_reaction(emoji)

        def check_reaction(reaction, user):
            return user != bot.user and str(reaction.emoji) in lang_emojis

        try:
            # Wait for a reaction to be added with a count of 2
            reaction, _ = await bot.wait_for('reaction_add', timeout=60.0, check=check_reaction)
            if reaction.count >= 2:
                selected_flag = str(reaction.emoji)
                selected_language = lang_emojis[selected_flag]
                monitor_channel_id = channel_id
                target_user_id = user_id

                target_user = bot.get_user(target_user_id)
                if target_user:
                    await ctx.send(f"Your language: {selected_flag}. Messages from **{target_user.name}** will now be translated.")
                else:
                    await ctx.send(f"Your language: {selected_flag}. Messages from the specified user will now be translated.")

                translation_active = True

                # Start translating messages in real-time
                translator_task = bot.loop.create_task(translate_messages(ctx, monitor_channel_id))
                await ctx.send("Translations started.")
            else:
                await ctx.send("No language was selected. Please react again.")
        except asyncio.TimeoutError:
            await ctx.send("Timed out waiting for a language reaction.")

    elif action == "stop":
        if not translation_active:
            await ctx.send("Translation is not active.")
            return

        if translator_task and not translator_task.done():
            translator_task.cancel()
            translation_active = False
            selected_language = None
            selected_flag = None
            monitor_channel_id = None
            target_user_id = None
            await ctx.send("Translation task has been stopped.")
        else:
            await ctx.send("No active translation task found.")

async def translate_messages(ctx, channel_id):
    global translation_active, selected_language, target_user_id
    channel = bot.get_channel(channel_id)
    if not channel:
        await ctx.send("Invalid channel ID.")
        return

    try:
        while translation_active:
            await asyncio.sleep(1)  # Small delay to prevent flooding

            # Fetch recent messages to translate
            messages = await channel.history(limit=10).flatten()
            for message in messages:
                if message.author.id == target_user_id and selected_language:
                    detected_language = translator.detect(message.content).lang
                    if detected_language == 'en':  # Only translate if detected language is English
                        translated_text = translator.translate(message.content, dest=selected_language).text
                        await message.reply(f"**Translated message**: {translated_text}")

    except asyncio.CancelledError:
        await ctx.send("Translation process was canceled.")

@bot.event
async def on_message(message):
    global translation_active, selected_language, target_user_id

    # Process commands and translations
    await bot.process_commands(message)

    # Check if translation is active and if the message is from the specific user
    if translation_active and message.author.id == target_user_id:
        if selected_language:
            if message.content.lower() == "stop translating":
                await message.channel.send("Stopping translation as requested.")
                if translator_task and not translator_task.done():
                    translator_task.cancel()
                translation_active = False
                selected_language = None
                selected_flag = None
                monitor_channel_id = None
                target_user_id = None
                return

            detected_language = translator.detect(message.content).lang
            if detected_language == 'en':  # Only translate if detected language is English
                translated_text = translator.translate(message.content, dest=selected_language).text
                await message.channel.send(f"**Translated message**: {translated_text}")

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot.run('Your Bot token ')
