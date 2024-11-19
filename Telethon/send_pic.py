from telethon import TelegramClient
from telethon.tl.types import InputFile

# Ganti dengan API ID dan API Hash dari my.telegram.org
api_id = '25450488'
api_hash = 'acbb7918c2adedd458de3b64c4bac34f'

# Ganti dengan nomor telepon Anda yang terhubung dengan Telegram
phone_number = '+6285944608131'

# Inisialisasi client Telethon
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    # Login atau autentikasi jika diperlukan
    await client.start(phone_number)

    # Ganti dengan username atau ID penerima pesan
    receiver = '@Zfty_bot'  # Username atau chat ID penerima

    # Ganti dengan path file foto yang ingin dikirim
    photo_path = '../1.jpg'

    # Mengirim foto
    await client.send_file(receiver, photo_path) #, caption='Ini foto dari akun Telegram biasa!')

# Menjalankan client dengan event loop
with client:
    client.loop.run_until_complete(main())
