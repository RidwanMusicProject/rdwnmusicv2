import yt_dlp
from pyrogram import filters
from pyrogram import Client
from Yukki import app, SUDOERS, BOT_ID, BOT_USERNAME, OWNER
from Yukki import dbb, app, BOT_USERNAME, BOT_ID, ASSID, ASSNAME, ASSUSERNAME
from ..YukkiUtilities.helpers.inline import start_keyboard, personal_markup
from ..YukkiUtilities.helpers.thumbnails import down_thumb
from ..YukkiUtilities.helpers.ytdl import ytdl_opts 
from ..YukkiUtilities.helpers.filters import command
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
)
from Yukki.YukkiUtilities.database.chats import (get_served_chats, is_served_chat, add_served_chat, get_served_chats)
from Yukki.YukkiUtilities.database.queue import (is_active_chat, add_active_chat, remove_active_chat, music_on, is_music_playing, music_off)
from Yukki.YukkiUtilities.database.sudo import (get_sudoers, get_sudoers, remove_sudo)

def start_pannel():  
    buttons  = [
            [
                InlineKeyboardButton(text="๐ แดแดแดแดแดษดแด๊ฑ ๐", url="https://telegra.ph/RidwanMusic-12-15-2")
            ],
            [ 
                InlineKeyboardButton(text="โ ๐๐จ๐ง๐๐ฌ๐ข", url="https://t.me/rdwan13"),
                InlineKeyboardButton(text="๐ฅ ๊ฑแดแดแดแดสแด", url="https://t.me/anonymoustelegrm")
            ],
    ]
    return "โก  **Welcome to rdwan music project bot.**", buttons

pstart_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "๐ฅ แดแดแด แดแด สแดแดส ษขสแดแดแด ๐ฅ", url="https://t.me/RdwanMsic_Bot?startgroup=true")
                ],[
                    InlineKeyboardButton(
                        "๐ แดแดแดแดแดษดแด๊ฑ ๐", url="https://telegra.ph/RidwanMusic-12-15-2"),
                    InlineKeyboardButton(
                        "๐ ๐๐จ๐ง๐๐ฌ๐ข ๐", url="https://t.me/rdwan13")
                ],[
                    InlineKeyboardButton(
                        "๐ฐ ๊ฑแดแดแดแดสแด ษขสแดแดแด๊ฑ ๐ฐ", url="https://t.me/anonymoustelegrm"), 
                    InlineKeyboardButton(
                        "๐ แดสแดษดษดแดส ๐", url="https://t.me/rulesgrupp")
                ]
                # [
                #     InlineKeyboardButton(
                #         "Setup Guide", url="https://telegra.ph/RidwanMusic-12-15-2")
                # ]
            ]
        )

welcome_captcha_group = 2
@app.on_message(filters.new_chat_members, group=welcome_captcha_group)
async def welcome(_, message: Message):
    chat_id = message.chat.id
    if not await is_served_chat(chat_id):
        await message.reply_text(f"โ **not in allowed chat**\n\nridwan music is only for allowed chats, ask any sudo user to allow your chat.\n\ncheck sudo user list [From Here](https://t.me/{BOT_USERNAME}?start=sudolist)")
        return await app.leave_chat(chat_id)
    for member in message.new_chat_members:
        try:
            if member.id in OWNER:
                return await message.reply_text(f"๐ป sแดสแด แดษช แดแดสแดสแด แดสแดส สแดs sแดสแด สแดสสแดสแด, แดส แดแดกษดแดส สแดแด [{member.mention}] has joined this group.")
            if member.id in SUDOERS:
                return await message.reply_text(f"๐ก sแดสแดแดแดแด แดแดแดแดษดษข แดsษชssแดแดษดแด แดขแดแดs, แดสแด sแดแดแด แดแดแดสแดส [{member.mention}] has joined this group.")
            if member.id == ASSID:
                await remove_active_chat(chat_id)
            if member.id == BOT_ID:
                out = start_pannel()
                await message.reply_text(f"โค๏ธ **Thanks for adding me to the group. Manager By HALBERT !**\n\n**Promote me as administrator of the group, otherwise I will not be able to work properly.", reply_markup=InlineKeyboardMarkup(out[1]))
                return
        except:
            return

@Client.on_message(filters.group & filters.command(["start", "help"]))
async def start(_, message: Message):
    chat_id = message.chat.id
    if not await is_served_chat(chat_id):
        await message.reply_text(f"โ **not in allowed chat**\n\nridwan music is only for allowed chats, ask any sudo user to allow your chat.\n\ncheck sudo user list [From Here](https://t.me/{BOT_USERNAME}?start=sudolist)")
        return await app.leave_chat(chat_id)
    out = start_pannel()
    await message.reply_text(f"โจ Hello {message.from_user.mention}, i'm a Rdwn Music bot.\n\n๐ญ Make me admin in your group so I can play music, otherwise you can't use my service.", reply_markup=InlineKeyboardMarkup(out[1]))
    return
        
@Client.on_message(filters.private & filters.incoming & filters.command("start"))
async def play(_, message: Message):
    if len(message.command) == 1:
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        rpk = "["+user_name+"](tg://user?id="+str(user_id)+")" 
        await app.send_message(message.chat.id,
            text=f"""๐ Welcome **{rpk}** !\n\n 
๐ญ ๐๐ง๐ข ๐๐ข ๐ค๐๐ฅ๐จ๐ฅ๐ ๐จ๐ฅ๐๐ก **[HALBERT](https://t.me/rdwan13)**, ๐๐๐ง ๐๐ข๐ฌ๐ ๐ฆ๐๐ฆ๐๐๐ง๐ญ๐ฎ ๐ค๐๐ฅ๐ข๐๐ง ๐ฎ๐ง๐ญ๐ฎ๐ค ๐ฆ๐๐ง๐๐๐ง๐?๐๐ซ ๐ค๐๐ง ๐ฆ๐ฎ๐ฌ๐ข๐ ๐ฆ๐๐ฅ๐๐ฅ๐ฎ๐ข ๐จ๐๐ซ๐จ๐ฅ๐๐ง ๐ฌ๐ฎ๐๐ซ๐ ๐๐๐๐๐ ๐ญ๐๐ฅ๐๐?๐ซ๐๐ฆ (๐๐๐)
            
๐๐ฎ๐ป ๐ฆ๐ฎ๐๐ฎ ๐?๐ฒ๐บ๐ถ๐น๐ถ๐ธ๐ถ ๐๐ถ๐๐๐ฟ ๐ฆ๐ฒ๐ฝ๐ฒ๐ฟ๐๐ถ :
โข ๐?๐ฒ๐ป๐ฐ๐ฎ๐ฟ๐ถ ๐๐ฎ๐ป ๐?๐ฒ๐บ๐๐๐ฎ๐ฟ ๐๐ฎ๐ด๐ ๐ฌ๐ฎ๐ป๐ด ๐๐ฎ๐บ๐ ๐๐ป๐ด๐ถ๐ป๐ธ๐ฎ๐ป.
โข ๐?๐ฒ๐ป๐ฑ๐ผ๐๐ป๐น๐ผ๐ฎ๐ฑ ๐๐ฎ๐ด๐ ๐ฌ๐ฎ๐ป๐ด ๐๐ป๐ด๐ถ๐ป ๐๐ฎ๐บ๐ ๐๐ผ๐๐ป๐น๐ผ๐ฎ๐ฑ.
โข ๐?๐ฒ๐ป๐ฑ๐ผ๐ป๐ฎ๐๐ถ ๐๐ฎ๐ป ๐๐ฒ ๐ข๐๐ป๐ฒ๐ฟ ๐๐ผ๐ ๐ฆ๐ฒ ๐๐ธ๐ต๐น๐ฎ๐ ๐ป๐๐ฎ,๐๐ถ๐ธ๐ฎ ๐๐ฎ๐บ๐ ๐๐ฒ๐น๐ฒ๐ฏ๐ถ๐ต๐ฎ๐ป ๐จ๐ฎ๐ป๐ด.

๐น ๐๐ฉ๐๐๐ข๐๐ฅ ๐๐ก๐๐ง๐ค๐ฌ ๐๐จ : **HALBERT** ๐น

๐ ๐๐ฐ๐ง๐๐ซ : **[๐๐๐ฅ๐๐๐ซ๐ญ](https://t.me/rdwan13)**

๐ CARA PENGGUNAAN BOT KLIK ยป **COMMANDS**
            """,
            parse_mode="markdown",
            reply_markup=pstart_markup,
            reply_to_message_id=message.message_id
        )
    elif len(message.command) == 2:                                                           
        query = message.text.split(None, 1)[1]
        f1 = (query[0])
        f2 = (query[1])
        f3 = (query[2])
        finxx = (f"{f1}{f2}{f3}")
        if str(finxx) == "inf":
            query = ((str(query)).replace("info_","", 1))
            query = (f"https://www.youtube.com/watch?v={query}")
            with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
                x = ytdl.extract_info(query, download=False)
            thumbnail = (x["thumbnail"])
            searched_text = f"""
๐ก **Track Informations**

๐ท **Name:** {x["title"]}
โฑ **Duration:** {round(x["duration"] / 60)} min(s)
๐ **Views:** `{x["view_count"]}`
๐๐ป **Likes:** `{x["like_count"]}`
โญ๏ธ **Ratings:** {x["average_rating"]}
๐ฃ **Channel:** {x["uploader"]}
๐ **Link:** {x["webpage_url"]}

โก๏ธ __Powered by Rdwan Music Project AI__"""
            link = (x["webpage_url"])
            buttons = personal_markup(link)
            userid = message.from_user.id
            thumb = await down_thumb(thumbnail, userid)
            await app.send_photo(message.chat.id,
                photo=thumb,                 
                caption=searched_text,
                parse_mode="markdown",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        if str(finxx) == "sud":
            sudoers = await get_sudoers()
            text = "**๐ก sudo users list:**\n\n"
            for count, user_id in enumerate(sudoers, 1):
                try:                     
                    user = await app.get_users(user_id)
                    user = user.first_name if not user.mention else user.mention
                except Exception:
                    continue                     
                text += f"โค {user}\n"
            if not text:
                await message.reply_text("โ no sudo users found")  
            else:
                await message.reply_text(text)
