import logging

import telebot
from telebot.async_telebot import AsyncTeleBot

from altlinker import config
from altlinker.core import has_alt_urls, replace_alternate_url_in_text

logger = logging.getLogger(__name__)
bot = AsyncTeleBot(config.TELEGRAM_BOT_TOKEN)


@bot.message_handler(func=lambda message: True, content_types=["text"])
async def msg_handler(message) -> None:
    """handle messages received from telegram bot api"""
    text_html = message.html_text

    try:
        if has_alt_urls(text_html):
            alt_text = await replace_alternate_url_in_text(text_html)
            logger.info(
                "success:\nmsg_id: {}\nmsg_txt: {}\nalternate text: {}".format(
                    message.message_id, message.text, alt_text
                )
            )
            await bot.reply_to(
                message,
                alt_text,
                disable_notification=True,
                parse_mode="html",
            )
    except Exception as e:
        logger.error(
            "telegram msg handler error:\nmsg_id[{}]\nmsg_txt: {}\nerror: {}".format(
                message.message_id, message.text, e
            )
        )


async def update_data_handler(update_data: dict) -> None:
    update = telebot.types.Update.de_json(update_data)
    await bot.process_new_updates([update])
