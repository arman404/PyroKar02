from pyrogram.types import InlineKeyboardButton

class Data:

    text_help_menu = (
        "**Command List & Help**\n**— Prefixes:** `.`, `?`, `-`, `!`"
        .replace(",", "")
        .replace("[", "")
        .replace("]", "")
        .replace("'", "")
    )
    reopen = [[InlineKeyboardButton("Re-Open", callback_data="reopen")]]
