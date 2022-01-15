import asyncio
import os
import random
import shutil
from os import getenv, path

import yt_dlp
from pyrogram import Client, filters
from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidde
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, Voice
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputAudioStream, InputStream
from youtubesearchpython import VideosSearch

from Yukki import ASSID, ASSNAME, ASSUSERNAME, BOT_ID, BOT_USERNAME, app
from Yukki.YukkiUtilities.database.chats import is_served_chat
from Yukki.YukkiUtilities.database.onoff import is_on_off
from Yukki.YukkiUtilities.database.queue import (
    add_active_chat,
    is_active_chat,
    music_on,
    remove_active_chat,
)

from ..config import DURATION_LIMIT
from ..YukkiUtilities.helpers.chattitle import CHAT_TITLE
from ..YukkiUtilities.helpers.filters import command, other_filters
from ..YukkiUtilities.helpers.gets import get_url, themes
from ..YukkiUtilities.helpers.inline import (
    audio_markup,
    play_markup,
    playlist_markup,
    search_markup,
    search_markup2,
)
from ..YukkiUtilities.helpers.thumbnails import gen_thumb
from ..YukkiUtilities.helpers.ytdl import ytdl_opts
from ..YukkiUtilities.tgcallsrun import ASS_ACC, convert, download, put, yukki

flex = {}
chat_watcher_group = 3


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))

async def member_permissions(chat_id: int, user_id: int):
    perms = []
    member = await app.get_chat_member(chat_id, user_id)
    if member.can_manage_voice_chats:
        perms.append("can_manage_voice_chats")
    return perms


async def unauthorised(message):
    chatID = message.chat.id
    text = "**Anda harus menjadi admin untuk menggunakan perintah ini**"
    try:
        await message.reply_text(text)
    except ChatWriteForbidden:
        await app.send_messsge(chatID, "error")
    return 1


async def adminsOnly(permission, message):
    chatID = message.chat.id
    if not message.from_user:
        if message.sender_chat:
            return await authorised(message)
        return await unauthorised(message)
    userID = message.from_user.id
    permissions = await member_permissions(chatID, userID)
    if userID not in SUDOERS and permission not in permissions:
        return await unauthorised(message)


DISABLED_GROUPS = []
useer = "NaN"
que = {}


@app.on_message(filters.command(["player", f"player@{BOT_USERNAME}"])& ~filters.edited & ~filters.bot & ~filters.private)
async def music_onoff(_, message: Message):
    permission = "can_manage_voice_chats"
    m = await adminsOnly(permission, message)
    if m == 1:
        return
    global DISABLED_GROUPS
    try:
        message.from_user.id
    except:
        return
    if len(message.command) != 2:
        await message.reply_text("**• usage:**\n\n `/music on` & `/music off`")
        return
    status = message.text.split(None, 1)[1]
    message.chat.id
    if status in ("ON", "on", "On"):
        lel = await message.reply("`tunggu sebentar...`")
        if not message.chat.id in DISABLED_GROUPS:
            await lel.edit("» **Music Telah Aktif ✅**")
            return
        DISABLED_GROUPS.remove(message.chat.id)
        await lel.edit(
            f"**✅ Music Telah Di Diaktifkan Di {message.chat.title}**"
        )

    elif status in ("OFF", "off", "Off"):
        lel = await message.reply("`processing...`")

        if message.chat.id in DISABLED_GROUPS:
            await lel.edit("» **Music Tidak Aktif❌.**")
            return
        DISABLED_GROUPS.append(message.chat.id)
        await lel.edit(
            f"**✅ Music Telah Di Nonaktifkan Di {message.chat.title} !**"
        )
    else:
        await message.reply_text(
            "**• Penggunaan:**\n\n `/music on` & `/music off`"
        )


@Client.on_message(command(["play", "play@RdwanMsic_Bot"]) & other_filters)
async def play(_, message: Message):
    await message.delete()
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    global que
    global useer
    if chat_id in DISABLED_GROUPS:
        return await message.reply_text(
            f"😕 **Maaf kak {message.from_user.mention}, Musicnya sedang tidak aktif,tag Admin untuk mengaktifkan**" 
        )
    if not await is_served_chat(chat_id):
        await message.reply_text(
            f"❌ **not in allowed chat**\n\nhalbert music is only for allowed chats. ask any sudo user to allow your chat.\n\ncheck sudo user list [From Here](https://t.me/{BOT_USERNAME}?start=sudolist)"
        )
        return await app.leave_chat(chat_id)
    if message.sender_chat:
        return await message.reply_text(
            "you're an __Anonymous__ Admin !\n\n» revert back to user account from admin rights."
        )
    user_id = message.from_user.id
    chat_title = message.chat.title
    message.from_user.first_name
    checking = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    if await is_on_off(1):
        LOG_ID = "-1001306851903"
        if int(chat_id) != int(LOG_ID):
            return await message.reply_text(
                "» bot is under maintenance, sorry for the inconvenience!"
            )
        return await message.reply_text(
            "» bot is under maintenance, sorry for the inconvenience!"
        )
    a = await app.get_chat_member(message.chat.id, BOT_ID)
    if a.status != "administrator":
        await message.reply_text(
            f"💡 To use me, I need to be an Administrator with the following permissions:\n\n» ❌ __Delete messages__\n» ❌ __Add users__\n» ❌ __Manage video chat__\n\nData is **updated** automatically after you **promote me**"
        )
        return
    if not a.can_manage_voice_chats:
        await message.reply_text(
            "missing required permission:" + "\n\n» ❌ __Manage video chat__"
        )
        return
    if not a.can_delete_messages:
        await message.reply_text(
            "missing required permission:" + "\n\n» ❌ __Delete messages__"
        )
        return
    if not a.can_invite_users:
        await message.reply_text(
            "missing required permission:" + "\n\n» ❌ __Add users__"
        )
        return
    try:
        b = await app.get_chat_member(message.chat.id, ASSID)
        if b.status == "kicked":
            await message.reply_text(
                f"{ASSNAME}(@{ASSUSERNAME}) is banned in group **{chat_title}**\n\n» unban the userbot first to use this bot"
            )
            return
    except UserNotParticipant:
        if message.chat.username:
            try:
                await ASS_ACC.join_chat(f"{message.chat.username}")
                await remove_active_chat(chat_id)
            except Exception as e:
                await message.reply_text(
                    f"❌ **userbot failed to join**\n\n**reason**: `{e}`"
                )
                return
        else:
            try:
                invitelink = await app.export_chat_invite_link(message.chat.id)
                if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace(
                        "https://t.me/+", "https://t.me/joinchat/"
                    )
                await ASS_ACC.join_chat(invitelink)
                await remove_active_chat(chat_id)
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await message.reply_text(
                    f"❌ **userbot failed to join**\n\n**reason**: `{e}`"
                )
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    url = get_url(message)
    fucksemx = 0
    if audio:
        fucksemx = 1
        mystic = await message.reply_text("**🔄 ꜱᴇᴅᴀɴɢ ʟᴏᴀᴅɪɴɢ ᴋᴛʟ...**")
        if audio.file_size > 157286400:
            await mystic.edit_text("audio file size must be less than 150 mb.")
            return
        duration = round(audio.duration / 60)
        if duration > DURATION_LIMIT:
            return await mystic.edit_text(
                f"❌ **__Duration Error__**\n\n**Allowed Duration: **{DURATION_LIMIT} minute(s)\n**Received Duration:** {duration} minute(s)"
            )
        file_name = (
            audio.file_unique_id
            + "."
            + (
                (audio.file_name.split(".")[-1])
                if (not isinstance(audio, Voice))
                else "ogg"
            )
        )
        file_name = path.join(path.realpath("downloads"), file_name)
        file = await convert(
            (await message.reply_to_message.download(file_name))
            if (not path.isfile(file_name))
            else file_name,
        )
        title = "Telegram Audio"
        link = "https://t.me/levinachannel"
        thumb = "cache/audio.png"
        videoid = "smex1"
    elif url:
        query = " ".join(message.command[1:])
        mystic = await _.send_message(chat_id, "🔍 **ꜱᴇᴅᴀɴɢ ʟᴏᴀᴅɪɴɢ ᴋᴛʟ...**")
        ydl_opts = {"format": "bestaudio[ext=m4a]"}
        try:
            results = VideosSearch(query, limit=1)
            for result in results.result()["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"]
                link = result["link"]
                (result["id"])
                videoid = result["id"]
        except Exception as e:
            return await mystic.edit_text(f"song not found.\n\n**reason:** {e}")
        smex = int(time_to_seconds(duration))
        if smex > DURATION_LIMIT:
            return await mystic.edit_text(
                f"❌ **__Duration Error__**\n\n**Allowed Duration: **90 minute(s)\n**Received Duration:** {duration} minute(s)"
            )
        if duration == "None":
            return await mystic.edit_text("❌ live stream not supported")
        if views == "None":
            return await mystic.edit_text("❌ live stream not supported")
        semxbabes = f"📥 downloading: {title[:55]}"
        await mystic.edit(semxbabes)
        theme = random.choice(themes)
        ctitle = message.chat.title
        ctitle = await CHAT_TITLE(ctitle)
        userid = message.from_user.id
        thumb = await gen_thumb(thumbnail, title, userid, theme, ctitle)

        def my_hook(d):
            if d["status"] == "downloading":
                percentage = d["_percent_str"]
                per = (str(percentage)).replace(".", "", 1).replace("%", "", 1)
                per = int(per)
                eta = d["eta"]
                speed = d["_speed_str"]
                size = d["_total_bytes_str"]
                bytesx = d["total_bytes"]
                if str(bytesx) in flex:
                    pass
                else:
                    flex[str(bytesx)] = 1
                if flex[str(bytesx)] == 1:
                    flex[str(bytesx)] += 1
                    try:
                        if eta > 2:
                            mystic.edit(
                                f"Downloading {title[:50]}\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec"
                            )
                    except Exception:
                        pass
                if per > 250:
                    if flex[str(bytesx)] == 2:
                        flex[str(bytesx)] += 1
                        if eta > 2:
                            mystic.edit(
                                f"Downloading {title[:50]}..\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec"
                            )
                        print(
                            f"[{videoid}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                        )
                if per > 500:
                    if flex[str(bytesx)] == 3:
                        flex[str(bytesx)] += 1
                        if eta > 2:
                            mystic.edit(
                                f"Downloading {title[:50]}...\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec"
                            )
                        print(
                            f"[{videoid}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                        )
                if per > 800:
                    if flex[str(bytesx)] == 4:
                        flex[str(bytesx)] += 1
                        if eta > 2:
                            mystic.edit(
                                f"Downloading {title[:50]}....\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec"
                            )
                        print(
                            f"[{videoid}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                        )
            if d["status"] == "finished":
                try:
                    taken = d["_elapsed_str"]
                except Exception:
                    taken = "00:00"
                size = d["_total_bytes_str"]
                mystic.edit(
                    f"**Downloaded {title[:55]}...**\n\n**size:** `{size}`\n**time:** {taken} sec\n\n**Converting file** [ffmpeg process]"
                )
                print(f"[{videoid}] Downloaded | Elapsed: {taken} seconds")

        loop = asyncio.get_event_loop()
        x = await loop.run_in_executor(None, download, link, my_hook)
        file = await convert(x)
    else:
        if len(message.command) < 2:
            user_name = message.from_user.first_name
            thumb = "cache/playlist.png"
            buttons = playlist_markup(user_name, user_id)
            hmo = await message.reply_photo(
                photo=thumb,
                caption=(
                    "**usage:** /play (music name/youtube url/audio file)\n\nIf you want to play from playlist, select one from below."
                ),
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            return
        query = " ".join(message.command[1:])
        mystic = await _.send_message(chat_id, "🔍 **ꜱᴇᴅᴀɴɢ ʟᴏᴀᴅɪɴɢ ᴋᴛʟ...**")
        try:
            a = VideosSearch(query, limit=5)
            result = (a.result()).get("result")
            title1 = result[0]["title"]
            duration1 = result[0]["duration"]
            title2 = result[1]["title"]
            duration2 = result[1]["duration"]
            title3 = result[2]["title"]
            duration3 = result[2]["duration"]
            title4 = result[3]["title"]
            duration4 = result[3]["duration"]
            title5 = result[4]["title"]
            duration5 = result[4]["duration"]
            ID1 = result[0]["id"]
            ID2 = result[1]["id"]
            ID3 = result[2]["id"]
            ID4 = result[3]["id"]
            ID5 = result[4]["id"]
        except Exception:
            return await mystic.edit_text(
                f"😕 Sorry, we **couldn't** find the song you were looking for\n\n• Check that the **name is correct** or **try by searching the artist.**"
            )
        thumb = "cache/results.png"
        url = "https://www.youtube.com/watch?v={id}"
        await mystic.delete()
        buttons = search_markup(
            ID1,
            ID2,
            ID3,
            ID4,
            ID5,
            duration1,
            duration2,
            duration3,
            duration4,
            duration5,
            user_id,
            query,
        )
        hmo = await message.reply_text(
            text=f"1️⃣ <b>[{title1[:25]}...]({url})</b>\n ├ 💡 [More Information](https://t.me/{BOT_USERNAME}?start=info_{ID1})\n ├ ☕️ <b>Creator : [𝐇𝐀𝐋𝐁𝐄𝐑𝐓](https://t.me/rdwan_13)</b>\n └ ⚡ __Powered by : [𝐊𝐞𝐤𝐢𝐧𝐢𝐚𝐧 𝐫𝐚𝐬𝐚 𝐦𝐮𝐬𝐢𝐜](https://t.me/unclesamaja)__\n\n2️⃣ <b>[{title2[:25]}...]({url})</b>\n ├ 💡 [More Information](https://t.me/{BOT_USERNAME}?start=info_{ID2})\n ├ ☕️ <b>Creator : [𝐇𝐀𝐋𝐁𝐄𝐑𝐓](https://t.me/rdwan_13)</b>\n └ ⚡ __Powered by : [𝐊𝐞𝐤𝐢𝐧𝐢𝐚𝐧 𝐫𝐚𝐬𝐚 𝐦𝐮𝐬𝐢𝐜](https://t.me/unclesamaja)__\n\n3️⃣ <b>[{title3[:25]}...]({url})</b>\n ├ 💡 [More Information](https://t.me/{BOT_USERNAME}?start=info_{ID3})\n ├ ☕️ <b>Creator : [𝐇𝐀𝐋𝐁𝐄𝐑𝐓](https://t.me/rdwan_13)</b>\n └ ⚡ __Powered by : [𝐊𝐞𝐤𝐢𝐧𝐢𝐚𝐧 𝐫𝐚𝐬𝐚 𝐦𝐮𝐬𝐢𝐜](https://t.me/unclesamaja)__\n\n4️⃣ <b>[{title4[:25]}...]({url})</b>\n ├ 💡 [More Information](https://t.me/{BOT_USERNAME}?start=info_{ID4})\n ├ ☕️ <b>Creator : [𝐇𝐀𝐋𝐁𝐄𝐑𝐓](https://t.me/rdwan_13)</b>\n └ ⚡ __Powered by : [𝐊𝐞𝐤𝐢𝐧𝐢𝐚𝐧 𝐫𝐚𝐬𝐚 𝐦𝐮𝐬𝐢𝐜](https://t.me/unclesamaja)__\n\n5️⃣ <b>[{title5[:25]}...]({url})</b>\n ├ 💡 [More Information](https://t.me/{BOT_USERNAME}?start=info_{ID5})\n ├ ☕️ <b>Creator : [𝐇𝐀𝐋𝐁𝐄𝐑𝐓](https://t.me/rdwan_13)</b>\n └ ⚡ __Powered by : [𝐊𝐞𝐤𝐢𝐧𝐢𝐚𝐧 𝐫𝐚𝐬𝐚 𝐦𝐮𝐬𝐢𝐜](https://t.me/unclesamaja)__",
            reply_markup=InlineKeyboardMarkup(buttons),
        )

        return
    if await is_active_chat(chat_id):
        position = await put(chat_id, file=file)
        _chat_ = (str(file)).replace("_", "", 1).replace("/", "", 1).replace(".", "", 1)
        cpl = f"downloads/{_chat_}final.png"
        shutil.copyfile(thumb, cpl)
        f20 = open(f"search/{_chat_}title.txt", "w")
        f20.write(f"{title}")
        f20.close()
        f111 = open(f"search/{_chat_}duration.txt", "w")
        f111.write(f"{duration}")
        f111.close()
        f27 = open(f"search/{_chat_}username.txt", "w")
        f27.write(f"{checking}")
        f27.close()
        if fucksemx != 1:
            f28 = open(f"search/{_chat_}videoid.txt", "w")
            f28.write(f"{videoid}")
            f28.close()
            buttons = play_markup(videoid, user_id)
        else:
            f28 = open(f"search/{_chat_}videoid.txt", "w")
            f28.write(f"{videoid}")
            f28.close()
            buttons = audio_markup(videoid, user_id)
        checking = (
            f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
        )
        await message.reply_photo(
            photo=thumb,
            caption=(
                f"💡 **Track added to queue »** {position}\n\n🏷 <b>𝐍𝐚𝐦𝐚:</b> [{title[:35]}...]({link}) \n⏱ <b>𝐃𝐮𝐫𝐚𝐬𝐢:</b> `{duration}` \n🎧 <b>𝐑𝐞𝐪𝐮𝐞𝐬𝐭 𝐛𝐲:</b> {checking}"
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        return await mystic.delete()
    else:
        await music_on(chat_id)
        await add_active_chat(chat_id)
        await yukki.pytgcalls.join_group_call(
            chat_id,
            InputStream(
                InputAudioStream(
                    file,
                ),
            ),
            stream_type=StreamType().local_stream,
        )
        _chat_ = (str(file)).replace("_", "", 1).replace("/", "", 1).replace(".", "", 1)
        checking = (
            f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
        )
        if fucksemx != 1:
            f28 = open(f"search/{_chat_}videoid.txt", "w")
            f28.write(f"{videoid}")
            f28.close()
            buttons = play_markup(videoid, user_id)
        else:
            f28 = open(f"search/{_chat_}videoid.txt", "w")
            f28.write(f"{videoid}")
            f28.close()
            buttons = audio_markup(videoid, user_id)
        await message.reply_photo(
            photo=thumb,
            reply_markup=InlineKeyboardMarkup(buttons),
            caption=(
                f"🏷 <b>𝐍𝐚𝐦𝐚:</b> [{title[:75]}]({link})\n⏱ <b>𝐃𝐮𝐫𝐚𝐬𝐢:</b> `{duration}`\n💡 **Status:** `Playing`\n🎧 <b>𝐑𝐞𝐪𝐮𝐞𝐬𝐭 𝐛𝐲:</b> {checking}"
            ),
        )
        return await mystic.delete()


@Client.on_callback_query(filters.regex(pattern=r"yukki"))
async def startyuplay(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    chat_id = CallbackQuery.message.chat.id
    CallbackQuery.message.chat.title
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id
    try:
        id, duration, user_id = callback_request.split("|")
    except Exception as e:
        return await CallbackQuery.message.edit(f"an error occured\n\n**reason**:{e}")
    if duration == "None":
        return await CallbackQuery.message.reply_text(f"❌ live stream not supported")
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer(
            "💡 sorry this not your request", show_alert=True
        )
    await CallbackQuery.message.delete()
    checking = f"[{CallbackQuery.from_user.first_name}](tg://user?id={userid})"
    url = f"https://www.youtube.com/watch?v={id}"
    videoid = id
    smex = int(time_to_seconds(duration))
    if smex > DURATION_LIMIT:
        await CallbackQuery.message.reply_text(
            f"❌ **__Duration Error__**\n\n**Allowed Duration: **90 minute(s)\n**Received Duration:** {duration} minute(s)"
        )
        return
    try:
        with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
            x = ytdl.extract_info(url, download=False)
    except Exception as e:
        return await CallbackQuery.message.reply_text(
            f"❌ failed to download video.\n\n**reason**: `{e}`"
        )
    title = x["title"]
    mystic = await CallbackQuery.message.reply_text(f"📥 downloading: {title[:55]}")
    thumbnail = x["thumbnail"]
    (x["id"])
    videoid = x["id"]

    def my_hook(d):
        if d["status"] == "downloading":
            percentage = d["_percent_str"]
            per = (str(percentage)).replace(".", "", 1).replace("%", "", 1)
            per = int(per)
            eta = d["eta"]
            speed = d["_speed_str"]
            size = d["_total_bytes_str"]
            bytesx = d["total_bytes"]
            if str(bytesx) in flex:
                pass
            else:
                flex[str(bytesx)] = 1
            if flex[str(bytesx)] == 1:
                flex[str(bytesx)] += 1
                try:
                    if eta > 2:
                        mystic.edit(
                            f"Downloading {title[:50]}\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec"
                        )
                except Exception:
                    pass
            if per > 250:
                if flex[str(bytesx)] == 2:
                    flex[str(bytesx)] += 1
                    if eta > 2:
                        mystic.edit(
                            f"Downloading {title[:50]}..\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec"
                        )
                    print(
                        f"[{videoid}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                    )
            if per > 500:
                if flex[str(bytesx)] == 3:
                    flex[str(bytesx)] += 1
                    if eta > 2:
                        mystic.edit(
                            f"Downloading {title[:50]}...\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec"
                        )
                    print(
                        f"[{videoid}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                    )
            if per > 800:
                if flex[str(bytesx)] == 4:
                    flex[str(bytesx)] += 1
                    if eta > 2:
                        mystic.edit(
                            f"Downloading {title[:50]}....\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec"
                        )
                    print(
                        f"[{videoid}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds"
                    )
        if d["status"] == "finished":
            try:
                taken = d["_elapsed_str"]
            except Exception:
                taken = "00:00"
            size = d["_total_bytes_str"]
            mystic.edit(
                f"**Downloaded: {title[:55]}...**\n\n**size:** `{size}`\n**time:** `{taken}` sec\n\n**Converting file [ffmpeg process]"
            )
            print(f"[{videoid}] Downloaded | Elapsed: {taken} seconds")

    loop = asyncio.get_event_loop()
    x = await loop.run_in_executor(None, download, url, my_hook)
    file = await convert(x)
    theme = random.choice(themes)
    ctitle = CallbackQuery.message.chat.title
    ctitle = await CHAT_TITLE(ctitle)
    thumb = await gen_thumb(thumbnail, title, userid, theme, ctitle)
    await mystic.delete()
    if await is_active_chat(chat_id):
        position = await put(chat_id, file=file)
        buttons = play_markup(videoid, user_id)
        _chat_ = (str(file)).replace("_", "", 1).replace("/", "", 1).replace(".", "", 1)
        cpl = f"downloads/{_chat_}final.png"
        shutil.copyfile(thumb, cpl)
        f20 = open(f"search/{_chat_}title.txt", "w")
        f20.write(f"{title}")
        f20.close()
        f111 = open(f"search/{_chat_}duration.txt", "w")
        f111.write(f"{duration}")
        f111.close()
        f27 = open(f"search/{_chat_}username.txt", "w")
        f27.write(f"{checking}")
        f27.close()
        f28 = open(f"search/{_chat_}videoid.txt", "w")
        f28.write(f"{videoid}")
        f28.close()
        await mystic.delete()
        m = await CallbackQuery.message.reply_photo(
            photo=thumb,
            caption=(
                f"💡 **Track added to queue »** `{position}`\n\n🏷 <b>𝐍𝐚𝐦𝐚:</b> [{title[:35]}...]({url})\n⏱ <b>𝐃𝐮𝐫𝐚𝐬𝐢:</b> `{duration}`\n🎧 <b>𝐑𝐞𝐪𝐮𝐞𝐬𝐭 𝐛𝐲:</b> {checking}"
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        os.remove(thumb)
        await CallbackQuery.message.delete()
    else:
        await music_on(chat_id)
        await add_active_chat(chat_id)
        await yukki.pytgcalls.join_group_call(
            chat_id,
            InputStream(
                InputAudioStream(
                    file,
                ),
            ),
            stream_type=StreamType().local_stream,
        )
        buttons = play_markup(videoid, user_id)
        await mystic.delete()
        m = await CallbackQuery.message.reply_photo(
            photo=thumb,
            reply_markup=InlineKeyboardMarkup(buttons),
            caption=(
                f"🏷 <b>𝐍𝐚𝐦𝐚:</b> [{title[:75]}]({url}) \n⏱ <b>𝐃𝐮𝐫𝐚𝐬𝐢:</b> `{duration}`\n💡 **𝐌𝐚𝐧𝐚𝐠𝐞:** `HALBERT`\n🎧 **𝐑𝐞𝐪𝐮𝐞𝐬𝐭 𝐛𝐲:** {checking}"
            ),
        )
        os.remove(thumb)
        await CallbackQuery.message.delete()


@Client.on_callback_query(filters.regex(pattern=r"popat"))
async def popat(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    print(callback_request)
    CallbackQuery.from_user.id
    try:
        id, query, user_id = callback_request.split("|")
    except Exception as e:
        return await CallbackQuery.message.edit(f"an error occured\n\n**reason**: {e}")
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer(
            "💡 sorry this not your request", show_alert=True
        )
    i = int(id)
    query = str(query)
    try:
        a = VideosSearch(query, limit=10)
        result = (a.result()).get("result")
        title1 = result[0]["title"]
        duration1 = result[0]["duration"]
        title2 = result[1]["title"]
        duration2 = result[1]["duration"]
        title3 = result[2]["title"]
        duration3 = result[2]["duration"]
        title4 = result[3]["title"]
        duration4 = result[3]["duration"]
        title5 = result[4]["title"]
        duration5 = result[4]["duration"]
        title6 = result[5]["title"]
        duration6 = result[5]["duration"]
        title7 = result[6]["title"]
        duration7 = result[6]["duration"]
        title8 = result[7]["title"]
        duration8 = result[7]["duration"]
        title9 = result[8]["title"]
        duration9 = result[8]["duration"]
        title10 = result[9]["title"]
        duration10 = result[9]["duration"]
        ID1 = result[0]["id"]
        ID2 = result[1]["id"]
        ID3 = result[2]["id"]
        ID4 = result[3]["id"]
        ID5 = result[4]["id"]
        ID6 = result[5]["id"]
        ID7 = result[6]["id"]
        ID8 = result[7]["id"]
        ID9 = result[8]["id"]
        ID10 = result[9]["id"]
    except Exception:
        return await mystic.edit_text(
            "😕 Sorry, we **couldn't** find the song you were looking for\n\n• Check that the **name is correct** or **try by searching the artist.**"
        )
    if i == 1:
        url = "https://www.youtube.com/watch?v={id}"
        buttons = search_markup2(
            ID6,
            ID7,
            ID8,
            ID9,
            ID10,
            duration6,
            duration7,
            duration8,
            duration9,
            duration10,
            user_id,
            query,
        )
        await CallbackQuery.edit_message_text(
            f"6️⃣ <b>[{title6[:25]}...]({url})</b>\n ├ 💡 [More Information](https://t.me/{BOT_USERNAME}?start=info_{ID6})\n ├ ☕️ <b>Creator : [𝙃𝘼𝙇𝘽𝙀𝙍𝙏](https://t.me/rdwan_13)</b>\n └ ⚡ __Powered by : [𝐊𝐞𝐤𝐢𝐧𝐢𝐚𝐧 𝐫𝐚𝐬𝐚 𝐦𝐮𝐬𝐢𝐜](https://t.me/unclesamaja)__\n\n7️⃣ <b>[{title7[:25]}...]({url})</b>\n ├ 💡 [More Information](https://t.me/{BOT_USERNAME}?start=info_{ID7})\n ├ ☕️ <b>Creator : [𝙃𝘼𝙇𝘽𝙀𝙍𝙏](https://t.me/rdwan_13)</b>\n └ ⚡ __Powered by : [𝐊𝐞𝐤𝐢𝐧𝐢𝐚𝐧 𝐫𝐚𝐬𝐚 𝐦𝐮𝐬𝐢𝐜](https://t.me/unclesamaja)__\n\n8️⃣ <b>[{title8[:25]}...]({url})</b>\n ├ 💡 [More Information](https://t.me/{BOT_USERNAME}?start=info_{ID8})\n ├ ☕️ <b>Creator : [𝙃𝘼𝙇𝘽𝙀𝙍𝙏](https://t.me/rdwan_13)</b>\n └ ⚡ __Powered by : [𝐊𝐞𝐤𝐢𝐧𝐢𝐚𝐧 𝐫𝐚𝐬𝐚 𝐦𝐮𝐬𝐢𝐜](https://t.me/unclesamaja)__\n\n9️⃣ <b>[{title9[:25]}...]({url})</b>\n ├ 💡 [More Information](https://t.me/{BOT_USERNAME}?start=info_{ID9})\n ├ ☕️ <b>Creator : [𝙃𝘼𝙇𝘽𝙀𝙍𝙏](https://t.me/rdwan_13)</b>\n └ ⚡ __Powered by : [𝐊𝐞𝐤𝐢𝐧𝐢𝐚𝐧 𝐫𝐚𝐬𝐚 𝐦𝐮𝐬𝐢𝐜](https://t.me/unclesamaja)__\n\n🔟 <b>[{title10[:25]}...]({url})</b>\n ├ 💡 [More Information](https://t.me/{BOT_USERNAME}?start=info_{ID10})\n ├ ☕️ <b>Creator : [𝙃𝘼𝙇𝘽𝙀𝙍𝙏](https://t.me/rdwan_13)</b>\n └ ⚡ __Powered by : [𝐊𝐞𝐤𝐢𝐧𝐢𝐚𝐧 𝐫𝐚𝐬𝐚 𝐦𝐮𝐬𝐢𝐜](https://t.me/unclesamaja)__",
            reply_markup=InlineKeyboardMarkup(buttons),
        )

        return
    if i == 2:
        url = "https://www.youtube.com/watch?v={id}"
        buttons = search_markup(
            ID1,
            ID2,
            ID3,
            ID4,
            ID5,
            duration1,
            duration2,
            duration3,
            duration4,
            duration5,
            user_id,
            query,
        )
        await CallbackQuery.edit_message_text(
            f"1️⃣ <b>[{title1[:25]}...]({url})</b>\n ├ 💡 [More Information](https://t.me/{BOT_USERNAME}?start=info_{ID1})\n ├ ☕️ <b>Creator : [𝙃𝘼𝙇𝘽𝙀𝙍𝙏](https://t.me/rdwan_13)</b>\n └ ⚡ __Powered by : [𝐊𝐞𝐤𝐢𝐧𝐢𝐚𝐧 𝐫𝐚𝐬𝐚 𝐦𝐮𝐬𝐢𝐜](https://t.me/unclesamaja)__\n\n2️⃣ <b>[{title2[:25]}...]({url})</b>\n ├ 💡 [More Information](https://t.me/{BOT_USERNAME}?start=info_{ID2})\n ├ ☕️ <b>Creator : [𝙃𝘼𝙇𝘽𝙀𝙍𝙏](https://t.me/rdwan_13)</b>\n └ ⚡ __Powered by : [𝐊𝐞𝐤𝐢𝐧𝐢𝐚𝐧 𝐫𝐚𝐬𝐚 𝐦𝐮𝐬𝐢𝐜](https://t.me/unclesamaja)__\n\n3️⃣ <b>[{title3[:25]}...]({url})</b>\n ├ 💡 [More Information](https://t.me/{BOT_USERNAME}?start=info_{ID3})\n ├ ☕️ <b>Creator : [𝙃𝘼𝙇𝘽𝙀𝙍𝙏](https://t.me/rdwan_13)</b>\n └ ⚡ __Powered by : [𝐊𝐞𝐤𝐢𝐧𝐢𝐚𝐧 𝐫𝐚𝐬𝐚 𝐦𝐮𝐬𝐢𝐜](https://t.me/unclesamaja)__\n\n4️⃣ <b>[{title4[:25]}...]({url})</b>\n ├ 💡 [More Information](https://t.me/{BOT_USERNAME}?start=info_{ID4})\n ├ ☕️ <b>Creator : [𝙃𝘼𝙇𝘽𝙀𝙍𝙏](https://t.me/rdwan_13)</b>\n └ ⚡ __Powered by : [𝐊𝐞𝐤𝐢𝐧𝐢𝐚𝐧 𝐫𝐚𝐬𝐚 𝐦𝐮𝐬𝐢𝐜](https://t.me/unclesamaja)__\n\n5️⃣ <b>[{title5[:25]}...]({url})</b>\n ├ 💡 [More Information](https://t.me/{BOT_USERNAME}?start=info_{ID5})\n ├ ☕️ <b>Creator : [𝙃𝘼𝙇𝘽𝙀𝙍𝙏](https://t.me/rdwan_13)</b>\n └ ⚡ __Powered by : [𝐊𝐞𝐤𝐢𝐧𝐢𝐚𝐧 𝐫𝐚𝐬𝐚 𝐦𝐮𝐬𝐢𝐜](https://t.me/unclesamaja)__",
            reply_markup=InlineKeyboardMarkup(buttons),
        )

        return


@Client.on_message(
    command(["playplaylist", "playplaylist@RdwanMsic_Bot"]) & other_filters
)
async def play_playlist_cmd(_, message):
    thumb = "cache/playlist.png"
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    buttons = playlist_markup(user_name, user_id)
    await message.reply_photo(
        photo=thumb,
        caption=("**❓ Which playlist do you want to play ?**"),
        reply_markup=InlineKeyboardMarkup(buttons),
    )
    return
