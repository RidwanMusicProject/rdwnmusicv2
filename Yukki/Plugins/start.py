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
                InlineKeyboardButton(text="📚 ᴄᴏᴍᴍᴀɴᴅꜱ 📚", url="https://telegra.ph/RidwanMusic-12-15-2")
            ],
            [ 
                InlineKeyboardButton(text="☕ ᴄʀᴇᴀᴛᴏʀ", url="https://t.me/rdwan_13"),
                InlineKeyboardButton(text="🔥 ꜱᴜᴘᴘᴏʀᴛ", url="https://t.me/anonymoustelegrm")
            ],
    ]
    return "⚡  **Welcome to rdwan music project bot.**", buttons

pstart_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔥 ᴀᴅᴅ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ 🔥", url="https://t.me/RdwanMsic_Bot?startgroup=true")
                ],[
                    InlineKeyboardButton(
                        "📚 ᴄᴏᴍᴍᴀɴᴅꜱ 📚", url="https://telegra.ph/RidwanMusic-12-15-2"),
                    InlineKeyboardButton(
                        "👑 ᴄʀᴇᴀᴛᴏʀ 👑", url="https://t.me/rdwan_13")
                ],[
                    InlineKeyboardButton(
                        "🔰 ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘꜱ 🔰", url="https://t.me/anonymoustelegrm"), 
                    InlineKeyboardButton(
                        "🔔 ᴄʜᴀɴɴᴇʟ 🔔", url="https://t.me/binalhot")
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
        await message.reply_text(f"❌ **not in allowed chat**\n\nridwan music is only for allowed chats, ask any sudo user to allow your chat.\n\ncheck sudo user list [From Here](https://t.me/{BOT_USERNAME}?start=sudolist)")
        return await app.leave_chat(chat_id)
    for member in message.new_chat_members:
        try:
            if member.id in OWNER:
                return await message.reply_text(f"💻 sᴀʏᴀ ᴅɪ ᴋᴇʟᴏʟᴀ ᴏʟᴇʜ ʙᴏs sᴀʏᴀ ʜᴀʟʙᴇʀᴛ, ᴍʏ ᴏᴡɴᴇʀ ʙᴏᴛ [{member.mention}] has joined this group.")
            if member.id in SUDOERS:
                return await message.reply_text(f"💡 sᴇʟᴀᴍᴀᴛ ᴅᴀᴛᴀɴɢ ᴀsɪssᴛᴀɴᴛ ᴢᴇᴜs, ᴛʜᴇ sᴜᴅᴏ ᴍᴇᴍʙᴇʀ [{member.mention}] has joined this group.")
            if member.id == ASSID:
                await remove_active_chat(chat_id)
            if member.id == BOT_ID:
                out = start_pannel()
                await message.reply_text(f"❤️ **Thanks for adding me to the group. Manager By HALBERT !**\n\n**Promote me as administrator of the group, otherwise I will not be able to work properly.", reply_markup=InlineKeyboardMarkup(out[1]))
                return
        except:
            return

@Client.on_message(filters.group & filters.command(["start", "help"]))
async def start(_, message: Message):
    chat_id = message.chat.id
    if not await is_served_chat(chat_id):
        await message.reply_text(f"❌ **not in allowed chat**\n\nridwan music is only for allowed chats, ask any sudo user to allow your chat.\n\ncheck sudo user list [From Here](https://t.me/{BOT_USERNAME}?start=sudolist)")
        return await app.leave_chat(chat_id)
    out = start_pannel()
    await message.reply_text(f"✨ Hello {message.from_user.mention}, i'm a Rdwn Music bot.\n\n💭 Make me admin in your group so I can play music, otherwise you can't use my service.", reply_markup=InlineKeyboardMarkup(out[1]))
    return
        
@Client.on_message(filters.private & filters.incoming & filters.command("start"))
async def play(_, message: Message):
    if len(message.command) == 1:
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        rpk = "["+user_name+"](tg://user?id="+str(user_id)+")" 
        await app.send_message(message.chat.id,
            text=f"""👋 Welcome **{rpk}** !\n\n 
💭 𝐈𝐧𝐢 𝐝𝐢 𝐤𝐞𝐥𝐨𝐥𝐚 𝐨𝐥𝐞𝐡 **[HALBERT](https://t.me/rdwan_13)**, 𝐝𝐚𝐧 𝐛𝐢𝐬𝐚 𝐦𝐞𝐦𝐛𝐚𝐧𝐭𝐮 𝐤𝐚𝐥𝐢𝐚𝐧 𝐮𝐧𝐭𝐮𝐤 𝐦𝐞𝐧𝐝𝐞𝐧𝐠𝐚𝐫 𝐤𝐚𝐧 𝐦𝐮𝐬𝐢𝐜 𝐦𝐞𝐥𝐚𝐥𝐮𝐢 𝐨𝐛𝐫𝐨𝐥𝐚𝐧 𝐬𝐮𝐚𝐫𝐚 𝐆𝐑𝐎𝐔𝐏 𝐭𝐞𝐥𝐞𝐠𝐫𝐚𝐦 (𝐕𝐂𝐆)
            
𝗗𝗮𝗻 𝗦𝗮𝘆𝗮 𝗠𝗲𝗺𝗶𝗹𝗶𝗸𝗶 𝗙𝗶𝘁𝘂𝗿 𝗦𝗲𝗽𝗲𝗿𝘁𝗶 :
• 𝗠𝗲𝗻𝗰𝗮𝗿𝗶 𝗗𝗮𝗻 𝗠𝗲𝗺𝘂𝘁𝗮𝗿 𝗟𝗮𝗴𝘂 𝗬𝗮𝗻𝗴 𝗞𝗮𝗺𝘂 𝗜𝗻𝗴𝗶𝗻𝗸𝗮𝗻.
• 𝗠𝗲𝗻𝗱𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝗟𝗮𝗴𝘂 𝗬𝗮𝗻𝗴 𝗜𝗻𝗴𝗶𝗻 𝗞𝗮𝗺𝘂 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱.
• 𝗠𝗲𝗻𝗱𝗼𝗻𝗮𝘀𝗶 𝗞𝗮𝗻 𝗞𝗲 𝗢𝘄𝗻𝗲𝗿 𝗕𝗼𝘁 𝗦𝗲 𝗜𝗸𝗵𝗹𝗮𝘀 𝗻𝘆𝗮,𝗝𝗶𝗸𝗮 𝗞𝗮𝗺𝘂 𝗞𝗲𝗹𝗲𝗯𝗶𝗵𝗮𝗻 𝗨𝗮𝗻𝗴.

🌹 𝐒𝐩𝐞𝐜𝐢𝐚𝐥 𝐓𝐡𝐚𝐧𝐤𝐬 𝐓𝐨 : **HALBERT** 🌹

👑 𝐎𝐰𝐧𝐞𝐫 : **[𝐇𝐚𝐥𝐛𝐞𝐫𝐭](https://t.me/rdwan_13)**

🚑 CARA PENGGUNAAN BOT KLIK » **COMMANDS**
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
💡 **Track Informations**

🏷 **Name:** {x["title"]}
⏱ **Duration:** {round(x["duration"] / 60)} min(s)
👀 **Views:** `{x["view_count"]}`
👍🏻 **Likes:** `{x["like_count"]}`
⭐️ **Ratings:** {x["average_rating"]}
📣 **Channel:** {x["uploader"]}
🔗 **Link:** {x["webpage_url"]}

⚡️ __Powered by Rdwan Music Project AI__"""
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
            text = "**💡 sudo users list:**\n\n"
            for count, user_id in enumerate(sudoers, 1):
                try:                     
                    user = await app.get_users(user_id)
                    user = user.first_name if not user.mention else user.mention
                except Exception:
                    continue                     
                text += f"➤ {user}\n"
            if not text:
                await message.reply_text("❌ no sudo users found")  
            else:
                await message.reply_text(text)
