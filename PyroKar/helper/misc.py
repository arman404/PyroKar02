import asyncio
import shlex
import socket
from typing import Tuple

import heroku3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError

from config import BRANCH, HEROKU_API_KEY, HEROKU_APP_NAME
from PyroKar import LOGGER

HAPP = None

GIT_TOKEN = ""
REPO_URL = "https://github.com/ArmanGG01/PyroKar2-Userbot"

XCB = [
    "/",
    "@",
    ".",
    "com",
    ":",
    "git",
    "heroku",
    "push",
    str(HEROKU_API_KEY),
    "https",
    str(HEROKU_APP_NAME),
    "HEAD",
    "main",
]


def install_req(cmd: str) -> Tuple[str, str, int, int]:
    async def install_requirements():
        args = shlex.split(cmd)
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        return (
            stdout.decode("utf-8", "replace").strip(),
            stderr.decode("utf-8", "replace").strip(),
            process.returncode,
            process.pid,
        )

    return asyncio.get_event_loop().run_until_complete(install_requirements())
    

def _netcat(host, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(content.encode())
    s.shutdown(socket.SHUT_WR)
    while True:
        data = s.recv(4096).decode("utf-8").strip("\n\x00")
        if not data:
            break
        return data
    s.close()


async def user_input(input):
    if " " in input or "\n" in input:
        return str(input.split(maxsplit=1)[1].strip())
    return ""

async def paste_queue(content):
    loop = get_running_loop()
    link = await loop.run_in_executor(
        None, partial(_netcat, "ezup.dev", 9999, content)
    )
    return link


def git():
    REPO_LINK = REPO_URL
    if GIT_TOKEN:
        GIT_USERNAME = REPO_LINK.split("com/")[1].split("/")[0]
        TEMP_REPO = REPO_LINK.split("https://")[1]
        UPSTREAM_REPO = f"https://{GIT_USERNAME}:{GIT_TOKEN}@{TEMP_REPO}"
    else:
        UPSTREAM_REPO = REPO_URL
    try:
        repo = Repo()
        LOGGER("PyroKar").info(f"Git Client Found")
    except GitCommandError:
        LOGGER("PyroKar").info(f"Invalid Git Command")
    except InvalidGitRepositoryError:
        repo = Repo.init()
        if "origin" in repo.remotes:
            origin = repo.remote("origin")
        else:
            origin = repo.create_remote("origin", UPSTREAM_REPO)
        origin.fetch()
        repo.create_head(
            BRANCH,
            origin.refs[BRANCH],
        )
        repo.heads[BRANCH].set_tracking_branch(origin.refs[BRANCH])
        repo.heads[BRANCH].checkout(True)
        try:
            repo.create_remote("origin", REPO_URL)
        except BaseException:
            pass
        nrs = repo.remote("origin")
        nrs.fetch(BRANCH)
        try:
            nrs.pull(BRANCH)
        except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")
        install_req("pip3 install --no-cache-dir -U -r requirements.txt")
        LOGGER("PyroKar").info("Fetched Latest Updates")


def heroku():
    global HAPP
    if is_heroku:
        if HEROKU_API_KEY and HEROKU_APP_NAME:
            try:
                Heroku = heroku3.from_key(HEROKU_API_KEY)
                HAPP = Heroku.app(HEROKU_APP_NAME)
                LOGGER("PyroKar").info(f"Heroku App Configured")
            except BaseException as e:
                LOGGER("Heroku").error(e)
                LOGGER("Heroku").info(
                    f"Pastikan HEROKU_API_KEY dan HEROKU_APP_NAME anda dikonfigurasi dengan benar di config vars heroku."
                )
                
async def is_heroku():
    return "heroku" in socket.getfqdn()


async def create_botlog(client):
    if HAPP is None:
        return
    LOGGER("PyroKar").info(
        "TUNGGU SEBENTAR. SEDANG MEMBUAT GROUP LOG USERBOT UNTUK ANDA"
    )
    desc = "Group Log untuk PyroKar-UserBot.\n\nHARAP JANGAN KELUAR DARI GROUP INI.\n\n👑 Powered By ~ @Karc0de 👑"
    try:
        gruplog = await client.create_supergroup("PyroKar UserBot", desc)
        if await in_heroku():
            heroku_var = HAPP.config()
            heroku_var["BOTLOG_CHATID"] = gruplog.id
        else:
            path = dotenv.find_dotenv("config.env")
            dotenv.set_key(path, "BOTLOG_CHATID", gruplog.id)
    except Exception:
        LOGGER("PyroKar").warning(
            "var BOTLOG_CHATID kamu belum di isi. Buatlah grup telegram dan masukan bot @MissRose_bot lalu ketik /id Masukan id grup nya di var BOTLOG_CHATID"
        )

