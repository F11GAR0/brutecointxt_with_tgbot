import telebot
import asyncio
from telebot.async_telebot import AsyncTeleBot
from brutecointxt import check_passphrase, _check_passphrase, file_check
from config import TG_BOT_TOKEN


bot = AsyncTeleBot(TG_BOT_TOKEN, parse_mode="HTML")


@bot.message_handler(commands=['start', 'help'])
async def send_start_message(message: telebot.types.Message):

    await bot.reply_to(message, "Usage: send file in .txt format which is contains passwords (passphrase)., or by sending text single password (passphrase).")

@bot.message_handler()
async def send_start_message(message: telebot.types.Message):

    result = _check_passphrase(message.text, True)

    await bot.reply_to(message, result)
    
@bot.message_handler(content_types=['document'])
async def upload_data(message: telebot.types.Message):

    if message.document:

        await bot.reply_to(message, "Loading data...")

        file_id_info = await bot.get_file(message.document.file_id)
        downloaded_file = str(await bot.download_file(file_id_info.file_path))

        await bot.reply_to(message, "Uploaded. Wait til check.")

        result = file_check(downloaded_file)

        if result == "":
            await bot.reply_to(message, "Nothing.")
        else:
            await bot.reply_to(message, result)
    
    else:

        await bot.reply_to(message, "Does not see document! Check /help")

asyncio.run(bot.infinity_polling())