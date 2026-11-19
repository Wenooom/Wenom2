import asyncio
import os
from telethon import TelegramClient
from telethon.sessions import StringSession

# ========================================================
# 🎛️ تنظیمات اصلی و اختصاصی
START_LINE = 20000     
END_LINE = 30000        

API_ID = 35220615
API_HASH = "6d9f1eeebf4255c3f4fd25a4442b0f4f"

# خواندن رشته سشن از فایل متنی مخصوص هر اکانت
SESSION_FILE = "session2.text"

TEXT_FILE_PATH = "Number1text" 
TARGET_CHAT = "Havij_robot"
# ========================================================

async def send_messages():
    try:
        # خواندن سشن از فایل متنی
        with open(SESSION_FILE, "r", encoding="utf-8") as sf:
            session_string = sf.read().strip()
    except FileNotFoundError:
        print(f"❌ خطا: فایل سشن '{SESSION_FILE}' پیدا نشد!")
        return

    client = TelegramClient(StringSession(session_string), API_ID, API_HASH)
    print("⏳ در حال اتصال به تلگرام روی Render...")
    await client.start()
    print("🔓 یوزربات با موفقیت متصل شد و آماده ارسال است!")
    
    try:
        if not os.path.exists(TEXT_FILE_PATH):
            print(f"❌ خطا: فایل متنی '{TEXT_FILE_PATH}' پیدا نشد!")
            await client.disconnect()
            return

        with open(TEXT_FILE_PATH, "r", encoding="utf-8") as f:
            print(f"🚀 شروع ارسال از خط {START_LINE} تا {END_LINE} به مقصد {TARGET_CHAT} (با وقفه دقیق ۳ ثانیه)...")
            
            for line_number, line in enumerate(f, start=1):
                if line_number < START_LINE:
                    continue
                if line_number > END_LINE:
                    print(f"🛑 به خط {END_LINE} رسیدیم. توقف ارسال.")
                    break
                    
                text = line.strip()
                if text:
                    try:
                        await client.send_message(TARGET_CHAT, text)
                        print(f"✅ [خط {line_number}] ارسال شد: {text}")
                    except Exception as e:
                        print(f"❌ خطا در ارسال خط {line_number}: {e}")
                        
                    # وقفه دقیق ۳ ثانیه بین هر ارسال
                    await asyncio.sleep(3)
                    
        print("🏁 ارسال تمام خطوط با موفقیت تمام شد.")
    except Exception as e:
        print(f"❌ خطای ناخواسته در خواندن فایل: {e}")
        
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(send_messages())
