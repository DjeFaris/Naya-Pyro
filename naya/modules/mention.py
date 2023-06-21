import asyncio

from pyrogram import filters

from . import *

chatQueue = []

stopProcess = False


@bots.on_message(filters.command(["all"], cmd) & filters.me)
async def everyone(client, message):
    global stopProcess
    await client.get_chat_member(message.chat.id, message.from_user.id)
    if len(chatQueue) > 100:
        return await message.reply(
          "-› Saya sudah mengerjakan jumlah maksimum 500 obrolan saat ini. Coba sebentar lagi."
        )
    if message.chat.id in chatQueue:
        return await message.reply(
          f"-› Sudah ada proses yang sedang berlangsung dalam obrolan ini. Silakan ketik `{cmd}batal` untuk memulai yang baru."
            )
    else:
        chatQueue.append(message.chat.id)
        if message.reply_to_message:
            inputText = message.reply_to_message.text
        else:
            inputText = message.text.split(None, 1)[1]
            membersList = []
            async for member in client.get_chat_members(message.chat.id):
                if member.user.is_bot == True:
                  pass
                elif member.user.is_deleted == True:
                  pass
                else:
                    membersList.append(member.user)
                    i = 0
                    lenMembersList = len(membersList)
                    if stopProcess:
                        stopProcess = False
                    while len(membersList) > 0 and not stopProcess:
                        j = 0
                        text1 = f"{inputText}\n\n"
                    try:
                        while j < 10:
                            user = membersList.pop(0)
                            if user.username == None:
                                text1 += f"👤 {user.mention}\n"
                                j += 1
                            else:
                                text1 += f"👤 @{user.username}\n"
                                j += 1
                            try:
                                await client.send_message(message.chat.id, text1)
                            except Exception:
                                pass
                            await asyncio.sleep(3)
                            i += 10
                    except IndexError:
                        try:
                            await client.send_message(message.chat.id, text1)
                        except Exception:
                            pass
                            i = i + j
                    chatQueue.remove(message.chat.id)


@bots.on_message(filters.command(["batal", "cancel"], cmd) & filters.me)
async def stop(client, message):
    global stopProcess
    try:
        try:
            await client.get_chat_member(message.chat.id, message.from_user.id)
        except:
            pass
        if not message.chat.id in chatQueue:
            await message.reply(
                "-› Tidak ada proses yang berkelanjutan untuk dihentikan."
            )
        else:
            stopProcess = True
            return await message.reply("-› Stopped.")
    except FloodWait as e:
        await asyncio.sleep(e.value)


__MODULE__ = "mention"
__HELP__ = f"""
✘ Bantuan Untuk Mention

๏ Perintah: <code>{cmd}all</code> [balas pesan]
◉ Penjelasan: Untuk menandai anggota dengan pesan.

๏ Perintah: <code>{cmd}batal</code>
◉ Penjelasan: Untuk membatalkan mention all.
"""
