# Translator Bot

![Translator Bot Banner]([[https://media.discordapp.net/attachments/1280552587724324895/1280553693875408947/IMG_3980.png?ex=66d88010&is=66d72e90&hm=754c79a2a40d35715658664cfc5e3b33e098bd4c241aa33af5376eb149cf1b29&=&quality=lossless]])) 

## Created By

**Dxrk3867Bot** & **Dxrk3867**

## Overview

The Translator Bot is a Discord bot designed to translate messages from a specific user into a selected language in real time. Built using Python and Google Translate, it allows server members to seamlessly communicate across different languages by setting their preferred language through emoji reactions.

## Features

- **Automatic Translation**: Translates messages from a specific user into a chosen language.
- **Easy Control**: Start or stop translation services with simple commands.
- **Interactive Language Selection**: Users select their preferred language by reacting with emojis.
- **Multi-Language Support**: Supports languages like German, French, Spanish, English, Russian, and more.

## Prerequisites

### Software Requirements

- **Python 3.8 or Higher**: [Download Python](https://www.python.org/downloads/)
- **Discord Bot Token**: Create a bot on the [Discord Developer Portal](https://discord.com/developers/applications) to obtain your token.
- **Python Libraries**: Install the required libraries using the `requirements.txt` file.

### Bot Permissions

To ensure the bot functions correctly, grant the following permissions when adding it to your Discord server:

1. **Read Messages**: Allows the bot to read messages.
2. **Send Messages**: Allows the bot to send messages.
3. **Add Reactions**: Enables the bot to add emoji reactions.
4. **Read Message History**: Necessary for translating previous messages.

![Bot Permissions](https://cdn.discordapp.com/attachments/1224724172954013748/1280611864148967546/image.png?ex=66d8b63d&is=66d764bd&hm=74df6ba45e35ab01d477520237191265a8266e2c8c39a9f0869fd3a2bda4c4b4&) 

## Setup Instructions

Follow these steps to set up and run the Translator Bot:

### 1. Clone the Repository

First, download the bot’s source code to your local machine.

```bash
git clone https://github.com/your-repo/translator-bot.git
cd translator-bot
```

### 2. Install Required Libraries

Install all necessary Python libraries listed in `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 3. Configure Your Bot Token

Open the `Translator.py` file and replace `'YOUR_BOT_TOKEN'` with your actual Discord bot token.

```python
bot.run('YOUR_BOT_TOKEN')
```

### 4. Start the Program

To launch the bot, run the `Start.bat` file provided in the repository.

```bash
Open Start.bat
```

After starting, go to your Discord server and initiate the bot with the following command:

```bash
.support start (channel_id) (user_id)
```

Replace `(channel_id)` and `(user_id)` with the specific Discord channel ID and user ID.

## Usage

1. **Start the Bot**: Use the `.support start` command followed by the channel ID and user ID where you want translations.
2. **Select Language**: The bot will prompt users to select their preferred language by reacting with an emoji.
3. **Stop the Bot**: Use the `.support stop` command to stop the translation service.

## Troubleshooting

- **Bot Not Responding**: Ensure the bot has the necessary permissions and that the token is correctly inserted in the `Translator.py` file.
- **Dependencies**: Make sure all dependencies are installed by running `pip install -r requirements.txt`.

## Additional Information

For more details, visit the [GitHub repository]([https://github.com/your-repo/translator-bot)] or check the [Discord documentation](https://discord.com/developers/docs/intro).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
