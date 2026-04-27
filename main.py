import os
import base64
import requests
from pyrogram import Client, filters

# ====== إعدادات ======
API_ID = 7706053
API_HASH = "a87b492b8fe379c5fd63793d29ca7a27"
BOT_TOKEN = "7703260297:AAGhND4ti2mPpbV0gFYDvS6GEBGHFSpuVH0"

GITHUB_TOKEN = "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"
REPO = "alaan1/DataBase"  # مثال: alaan1/myproject

# =====================

app = Client("github-uploader-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


def upload_to_github(filename, file_bytes):
    url = f"https://api.github.com/repos/{REPO}/contents/{filename}"

    content = base64.b64encode(file_bytes).decode()

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    # تحقق إذا الملف موجود
    get_resp = requests.get(url, headers=headers)

    data = {
        "message": f"Upload {filename} via bot",
        "content": content
    }

    if get_resp.status_code == 200:
        sha = get_resp.json()["sha"]
        data["sha"] = sha  # تحديث الملف

    response = requests.put(url, json=data, headers=headers)
    return response.json()


# استقبال الملفات
@app.on_message(filters.document | filters.photo)
async def handle_files(client, message):
    try:
        if message.document:
            file_name = message.document.file_name
            file_path = await message.download()
        elif message.photo:
            file_name = f"photo_{message.photo.file_unique_id}.jpg"
            file_path = await message.download()
        else:
            return

        # قراءة الملف
        with open(file_path, "rb") as f:
            file_bytes = f.read()

        # رفع إلى GitHub
        result = upload_to_github(file_name, file_bytes)

        # حذف الملف المؤقت
        os.remove(file_path)

        if "content" in result:
            await message.reply(f"✅ تم رفع: {file_name}")
        else:
            await message.reply(f"❌ خطأ:\n{result}")

    except Exception as e:
        await message.reply(f"⚠️ صار خطأ:\n{str(e)}")


print("Bot is running...")
app.run()
