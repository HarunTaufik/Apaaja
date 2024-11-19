from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from PIL import Image, ImageFilter
import io

# Ganti dengan token bot Anda
BOT_TOKEN = '7456694718:AAFvfrrFrrNTdeq-O3k5CFgg_Klth5XnAyE'

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hai! Kirimkan foto dan saya akan memprosesnya.')

async def handle_photo(update: Update, context: CallbackContext) -> None:
    # Ambil file foto
    photo_file = await update.message.photo[-1].get_file()
    
    # Unduh foto ke buffer
    photo_buffer = io.BytesIO()
    await photo_file.download_to_memory(photo_buffer)
    
    # Proses gambar dengan Pillow
    photo_buffer.seek(0)
    image = Image.open(photo_buffer)
    processed_image = image.filter(ImageFilter.CONTOUR)  # Contoh pemrosesan, ubah sesuai kebutuhan

    # Simpan gambar yang diproses ke buffer
    processed_buffer = io.BytesIO()
    processed_image.save(processed_buffer, format='PNG')
    processed_buffer.seek(0)

    # Kirim gambar yang telah diproses
    await update.message.reply_photo(photo=InputFile(processed_buffer, filename='processed_photo.png'))

async def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

