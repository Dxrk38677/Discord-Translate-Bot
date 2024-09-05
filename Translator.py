import discord
from discord.ext import commands
from googletrans import Translator
import json
from colorama import Fore, Style, init
import logging
import asyncio

init(autoreset=True)

# Configure logging with colorama
logger = logging.getLogger('discord')
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(name)s: %(message)s')

class ColoredFormatter(logging.Formatter):
    def format(self, record):
        log_fmt = {
            'INFO': Fore.YELLOW + formatter._fmt + Style.RESET_ALL,
            'ERROR': Fore.RED + formatter._fmt + Style.RESET_ALL,
            'WARNING': Fore.RED + formatter._fmt + Style.RESET_ALL,
            'DEBUG': Fore.CYAN + formatter._fmt + Style.RESET_ALL,
        }.get(record.levelname, formatter._fmt)
        formatter._fmt = log_fmt
        return super().format(record)

handler.setFormatter(ColoredFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Load configuration from config.json
def load_config():
    with open('config.json', 'r') as file:
        return json.load(file)

# Save configuration to config.json
def save_config(config):
    with open('config.json', 'w') as file:
        json.dump(config, file, indent=4)

# Define the necessary intents for your bot
intents = discord.Intents.default()
intents.message_content = True  # Enables access to message content
intents.reactions = True        # Enables access to reactions
intents.members = True          # Enables access to guild members

# Initialize the bot with the specified intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Define the global variables
translator = Translator()
translator_task = None
translation_active = False
selected_language = None
selected_flag = None
monitor_channel_id = None
target_user_id = None
starting_user_id = None

@bot.event
async def on_ready():
    print(f"{Fore.GREEN}Bot is ready.{Style.RESET_ALL}")

@bot.command(name="support")
async def support(ctx, action=None, channel_id: int = None, user_id: int = None):
    global translator_task, translation_active, selected_language, selected_flag, monitor_channel_id, target_user_id, starting_user_id

    if action not in ["start", "stop"]:
        await ctx.send("Invalid action. Use `!support start (channel_id) (user_id)` to begin translating and `!support stop` to stop the translation.")
        return

    if action == "start":
        if not channel_id or not user_id:
            await ctx.send("Please provide both a channel ID and a user ID.")
            return

        if translation_active:
            await ctx.send("Translation is already active.")
            return

        lang_emojis = {
            "🇺🇸": "en",  # English
            "🇪🇸": "es",  # Spanish
            "🇧🇷": "pt",  # Portuguese
            "🇨🇳": "zh-cn",  # Chinese (Simplified)
            "🇯🇵": "ja",  # Japanese
            "🇰🇷": "ko",  # Korean
            "🇷🇺": "ru",  # Russian
            "🇫🇷": "fr",  # French
            "🇩🇪": "de",  # German
            "🇮🇹": "it",  # Italian
            "🇳🇱": "nl",  # Dutch
            "🇳🇵": "ne",  # Nepali
            "🇮🇳": "hi",  # Hindi
            "🇧🇩": "bn",  # Bengali
            "🇵🇰": "ur",  # Urdu
            "🇲🇲": "my",  # Burmese
            "🇸🇦": "ar",  # Arabic
            "🇹🇷": "tr",  # Turkish
            "🇵🇱": "pl",  # Polish
            "🇭🇺": "hu",  # Hungarian
            "🇹🇭": "th",  # Thai
            "🇦🇪": "fa",  # Persian
            "🇲🇨": "ms",  # Malay
            # Add more languages and their respective flags here
        }

        embed = discord.Embed(
            title="Language Selection",
            description="Hello! Please select your language by reacting to the emoji that represents it.",
            color=discord.Color.blue()
        )

        message = await ctx.send(embed=embed)

        # Add reactions for each language, up to a maximum of 20 to avoid hitting the reaction limit
        for emoji in list(lang_emojis.keys())[:20]:
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
                starting_user_id = ctx.author.id  # Set the ID of the user who started the translation

                target_user = await bot.fetch_user(target_user_id)
                if target_user:
                    embed = discord.Embed(
                        title="Translation Activated",
                        description=f"Made By Dxrk3867. Current User: **{target_user.name}**. Messages from this user will now be translated.",
                        color=discord.Color.green()
                    )
                    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1279830220488183834/1280874742785642518/3c09f2f84f8e91389943839e754f92a5.jpg?ex=66d9ab10&is=66d85990&hm=f8426e1ee81bf1c46fdfbeb8712b5ee080cb2ac69346e0c0a6903a979f33facd&")
                    await ctx.send(embed=embed)
                    logger.info(f"Connected. Current User: {target_user.name}")
                else:
                    await ctx.send("Could not fetch the user. Please ensure the User ID is correct.")
                    logger.error("Could not fetch the user.")

                translation_active = True

                # Start translating messages in real-time
                translator_task = bot.loop.create_task(translate_messages(ctx, monitor_channel_id))
                await ctx.send("Translations started.")
                logger.info("Static is working. Translations started.")
            else:
                await ctx.send("No language was selected. Please react again.")
        except asyncio.TimeoutError:
            await ctx.send("Timed out waiting for a language reaction.")
            logger.error("Timed out waiting for a language reaction.")

    elif action == "stop":
        if not translation_active:
            await ctx.send("Active Translation not found.")
            logger.warning("Active Translation not found.")
            return

        if translator_task and not translator_task.done():
            translator_task.cancel()
            translation_active = False
            selected_language = None
            selected_flag = None
            monitor_channel_id = None
            target_user_id = None
            starting_user_id = None  # Reset the starting user ID
            await ctx.send("Thanks for using Dxrk3867's Translation bot!")
            logger.info("Static is working. Translation task has been stopped.")
            await bot.close()  # Close the bot connection
            print(f"{Fore.YELLOW}Bot stopped and going offline.{Style.RESET_ALL}")
        else:
            await ctx.send("Active Translation not found.")
            logger.warning("Active Translation not found.")

async def translate_messages(ctx, channel_id):
    global translation_active, selected_language, target_user_id
    channel = bot.get_channel(channel_id)
    if not channel:
        await ctx.send("Invalid channel ID.")
        logger.error("Invalid channel ID.")
        return

    try:
        while translation_active:
            await asyncio.sleep(1)  # Small delay to prevent flooding

            # Fetch recent messages to translate
            messages = await channel.history(limit=10).flatten()
            for message in messages:
                if message.author.id == target_user_id and selected_language:
                    detected_language = translator.detect(message.content).lang
                    if detected_language != selected_language:  # Translate if the detected language is not the selected language
                        translated_text = translator.translate(message.content, dest=selected_language).text
                        await message.reply(f"**Translated message**: {translated_text}")

    except asyncio.CancelledError:
        await ctx.send("Translation process was canceled.")
        logger.error("Translation process was canceled.")

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
                starting_user_id = None
                logger.info("Static is working. Translation task has been stopped as requested.")
                return

            detected_language = translator.detect(message.content).lang
            if detected_language != selected_language:  # Translate if the detected language is not the selected language
                translated_text = translator.translate(message.content, dest=selected_language).text
                await message.channel.send(f"**Translated message**: {translated_text}")

# Load the bot token from the configuration file
config = load_config()
bot_token = config.get('bot_token')

if bot_token:
    bot.run(bot_token)
else:
    print(f"{Fore.RED}Bot token not found in configuration file.{Style.RESET_ALL}")
