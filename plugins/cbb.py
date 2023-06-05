#(©)Codexbotz

from pyrogram import __version__
from bot import Bot
from config import OWNER_ID
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text = f"<b>â—‹ Creator : <a href='tg://user?id={OWNER_ID}'>This Person</a>\n\nâ—‹ Language : <code>Python3</code>\n\nâ—‹ Library : <a href='https://docs.pyrogram.org/'>Pyrogram asyncio {__version__}</a>\n\nâ—‹ Auto group : <a href='https://t.me/+siOFt_rvsnJkNjY9'>Click here</a>\n\nâ—‹ Channel : @The_Silent_Teams\n\nâ—‹ Support Group : @Robo_5_0</b>",
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔒 Close", callback_data = "close")
                    ]
                ]
            )
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
