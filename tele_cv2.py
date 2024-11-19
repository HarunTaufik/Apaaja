import cv2
import asyncio
import io
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Ganti dengan token bot Anda
BOT_TOKEN = '7456694718:AAFvfrrFrrNTdeq-O3k5CFgg_Klth5XnAyE'

# Inisialisasi kamera
camera = cv2.VideoCapture(0)  # 0 untuk kamera default, ubah jika menggunakan kamera lain

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hai! Tekan /takephoto untuk mengambil foto dan mengirimkannya.')

async def take_photo(update: Update, context: CallbackContext) -> None:
    # Ambil foto dari kamera
    ret, frame = camera.read()
    if not ret:
        await update.message.reply_text('Gagal mengambil foto.')
        return
    
    # Simpan foto ke buffer
    _, buffer = cv2.imencode('.jpg', frame)
    photo_buffer = io.BytesIO(buffer.tobytes())
    photo_buffer.seek(0)
    
    # Kirim foto ke Telegram
    try:
        await update.message.reply_photo(photo=InputFile(photo_buffer, filename='photo.jpg'))
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text('Terjadi kesalahan saat mengirim foto.')

async def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("takephoto", take_photo))

    await application.run_polling()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        # Jika event loop sudah berjalan, jangan panggil loop.run_until_complete
        if not loop.is_running():
            loop.run_until_complete(main())
        else:
            # Jika loop sudah berjalan, jalankan coroutine di dalam loop
            task = loop.create_task(main())
            loop.run_forever()
    except RuntimeError as e:
        print(f"RuntimeError: {e}")
    finally:
        # Pastikan tidak mencoba menutup loop yang sudah berjalan
        pass
