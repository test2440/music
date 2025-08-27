import aiohttp
import aiofiles
import os
import re
import asyncio
from urllib.parse import urlparse, parse_qs
from pyrogram import Client, filters
from pyrogram.types import Message
from youtube_search import YoutubeSearch
from AnonXMusic import app

os.makedirs("downloads", exist_ok=True)

async def download_in_parts_with_clen(url: str, output_file: str, chunk_size=1_000_000):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    clen = query.get("clen", [None])[0]

    if not clen:
        raise Exception("❌ خطأ")
    
    file_size = int(clen)
    ranges = [(i, min(i + chunk_size - 1, file_size - 1)) for i in range(0, file_size, chunk_size)]
    part_files = []

    async def download_range(start, end, idx):
        headers = {"Range": f"bytes={start}-{end}"}
        part_file = f"{output_file}.part{idx}"
        part_files.append(part_file)

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status in [206, 200]:
                    async with aiofiles.open(part_file, mode='wb') as f:
                        await f.write(await resp.read())
                else:
                    raise Exception(f"❌ فشل تحميل الجزء {idx}، الحالة: {resp.status}")

    await asyncio.gather(*[
        download_range(start, end, idx) for idx, (start, end) in enumerate(ranges)
    ])

    async with aiofiles.open(output_file, mode='wb') as f_out:
        for part in part_files:
            async with aiofiles.open(part, mode='rb') as f_in:
                await f_out.write(await f_in.read())
            os.remove(part)

    return os.path.abspath(output_file)  


async def download_file(url: str, output_file: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                async with aiofiles.open(output_file, mode='wb') as f:
                    await f.write(await resp.read())
            else:
                raise Exception(f"❌ فشل تحميل الملف، الحالة: {resp.status}")

    return os.path.abspath(output_file)  

@app.on_message(filters.command(['نزل', 'حمل', 'تنزيل', 'يوت'], ""))
async def download_song(client: Client, msg: Message):
    try:
        if len(msg.text.split()) < 2:
            ask = await msg.reply("<b>≯︰شبدك تنزل؟</b>")
            try:
                response: Message = await client.listen(msg.chat.id, timeout=30)
                name = response.text.strip()
                await ask.delete()
                await response.delete()
            except asyncio.TimeoutError:
                return await ask.edit("<b>≯︰لم يتم تلقي أي رد، تم إلغاء العملية.</b>")
        else:
            name = msg.text.split(' ', 1)[1]

        x = await msg.reply("<b>جاري البحث على يوتيوب...</b>")

        results = YoutubeSearch(name, max_results=1).to_dict()
        if not results:
            return await x.edit("<b>⚠️ لم يتم العثور على نتائج.</b>")

        video_id = results[0]["id"]
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
        title = results[0]["title"][:40]

        api_url = "https://www.clipto.com/api/youtube"
        headers = {
            'authority': 'www.clipto.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://www.clipto.com',
            'referer': 'https://www.clipto.com/ar/media-downloader/free-youtube-video-to-mp4-0607',
            'user-agent': 'Mozilla/5.0'
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, headers=headers, json={"url": youtube_url}) as resp:
                if resp.status != 200:
                    return await x.edit("<b>⚠️ فشل الاتصال بـ Clipto.</b>")
                data = await resp.text()

        links = re.findall(r'https://[^\s"\\]+', data)
        image_url = next((l for l in links if "i.ytimg.com" in l), None)
        audio_links = [l for l in links if re.search(r"https://rr\d+---sn", l)]
        audio_url = audio_links[16] if len(audio_links) >= 17 else None

        if not audio_url or not image_url:
            return await x.edit("<b>⚠️ لم يتم العثور على روابط صوت أو صورة.</b>")

        os.makedirs("downloads", exist_ok=True)

        audio_path = f"downloads/{video_id}_audio.mp3"
        image_path = f"downloads/{video_id}_thumb.jpg"

        await x.edit("<b>جاري التحميل بأقصى سرعة...</b>")

        
        audio_path = await download_in_parts_with_clen(audio_url, audio_path)
        
        image_path = await download_file(image_url, image_path)

        await asyncio.sleep(1)

        bot_username = client.me.username
        caption = f"<b>≯︰uploader : @{bot_username}</b>"

        if msg.text.split()[0] in ['نزل', 'تنزيل', 'يوت']:
            await client.send_audio(
                chat_id=msg.chat.id,
                audio=audio_path,
                caption=caption,
                thumb=image_path,
                title=title
            )
        else:
            await client.send_video(
                chat_id=msg.chat.id,
                video=audio_path,
                caption=caption,
                thumb=image_path
            )

        await x.delete()

        os.remove(audio_path)
        os.remove(image_path)

    except Exception as e:
        await msg.reply(f"<b>⚠️ حدث خطأ:</b>\n<code>{str(e)}</code>")