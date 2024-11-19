from telegram import Bot, InputFile
import asyncio

# Ganti dengan token bot Anda
TOKEN = '7456694718:AAFvfrrFrrNTdeq-O3k5CFgg_Klth5XnAyE'
# Ganti dengan ID chat Anda
CHAT_ID = '1871361462'
# Path ke foto yang akan dikirim
PHOTO_PATH = './1.jpg'

async def send_photo(bot_token, chat_id, photo_path):
    bot = Bot(token=bot_token)
    with open(photo_path, 'rb') as photo:
        await bot.send_photo(chat_id=chat_id, photo=InputFile(photo, filename='photo.jpg'))

async def main():
    await send_photo(TOKEN, CHAT_ID, PHOTO_PATH)

if __name__ == '__main__':
    # Use asyncio.run if no other event loop is running
    asyncio.run(main())
