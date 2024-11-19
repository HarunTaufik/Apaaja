from telethon import TelegramClient, events

# Ganti dengan API ID dan API Hash dari my.telegram.org
api_id = '25450488'
api_hash = 'acbb7918c2adedd458de3b64c4bac34f'

# Ganti dengan nomor telepon Anda yang terhubung dengan Telegram
phone_number = '+6285944608131'

# Inisialisasi client Telethon
client = TelegramClient('session_name', api_id, api_hash)

# Path folder untuk menyimpan foto yang diterima
PHOTO_SAVE_PATH = './'

# Buat folder jika belum ada
import os
if not os.path.exists(PHOTO_SAVE_PATH):
    os.makedirs(PHOTO_SAVE_PATH)

@client.on(events.NewMessage(from_users='@Zfty_bot'))  # Ganti dengan username bot
async def handle_new_message(event):
    if event.photo:  # Mengecek apakah pesan berisi foto
        print("Foto diterima dari bot!")

        # Mendapatkan informasi file
        photo = await event.download_media(file=PHOTO_SAVE_PATH)
        print(f"Foto berhasil disimpan di: {photo}")
    else:
        print("Pesan bukan foto.")

async def main():
    # Mulai client
    await client.start(phone_number)
    
    print("Menunggu pesan dari bot...")
    await client.run_until_disconnected()

# Menjalankan client
with client:
    client.loop.run_until_complete(main())
