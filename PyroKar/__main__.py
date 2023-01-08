import importlib

from pyrogram import idle
from uvloop import install

from config import BOT_VER, CMD_HANDLER
from PyroKar import BOTLOG_CHATID, LOGGER, LOOP, aiosession, clients, app, ids
from PyroKar.helper.misc import create_botlog, heroku
from PyroKar.modules import ALL_MODULES

MSG_ON = """
💢 **PyroKar-Userbot Udah Aktif** 💢
╼┅━━━━━━━━━━╍━━━━━━━━━━┅╾
❍▹ **Userbot Version -** `{}`
❍▹ **Ketik** `{}alive` **untuk Mengecheck Bot**
╼┅━━━━━━━━━━╍━━━━━━━━━━┅╾
"""


async def main():
    for all_module in ALL_MODULES:
        importlib.import_module("PyroKar.modules" + all_module)
        print(f"Successfully Imported {all_module} ✔")
    for cli in clients:
        try:
            await cli.start()
            bot.me = await cli.get_me()
            await client.join_chat("StoryMan01")
            await client.join_chat("Karc0de")
            try:
                await bot.send_message(
                    BOTLOG_CHATID, MSG_ON.format(BOT_VER, CMD_HANDLER)
                )
            except BaseException:
                pass
            LOGGER("PyroKar").info(
                f"Logged in as {bot.me.first_name} | [ {bot.me.id} ]"
            )
        except Exception as a:
            LOGGER("main").warning(a)
    LOGGER("PyroKar").info(f"PyroKar-UserBot v{BOT_VER} [👑 BERHASIL DIAKTIFKAN YA KONTOL! 👑]")
    if not str(BOTLOG_CHATID).startswith("-100"):
        await create_botlog(bot1)
    await idle()
    await aiosession.close()


if __name__ == "__main__":
    LOGGER("PyroKar").info("Starting PyroKar-UserBot")
    install()
    heroku()
    LOOP.run_until_complete(main())
