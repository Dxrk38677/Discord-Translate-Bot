# Translator Bot


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

![Bot Permissions](https://via.placeholder.com/600x400?text=Permissions+Screenshot) <!-- Replace with actual permissions screenshot -->

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

For more details, visit the [GitHub repository](https://github.com/your-repo/translator-bot) or check the [Discord documentation](https://discord.com/developers/docs/intro).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
