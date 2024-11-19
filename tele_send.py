import nest_asyncio
import asyncio
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, CallbackContext

# Terapkan nest_asyncio
nest_asyncio.apply()

# Ganti dengan token bot Anda
BOT_TOKEN = '7456694718:AAFvfrrFrrNTdeq-O3k5CFgg_Klth5XnAyE'

# Fungsi untuk menangani perintah /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hai! Ketik /kirimfoto untuk menerima foto esp-cam.')

# Fungsi untuk menangani perintah /kirimfoto
async def kirim_foto(update: Update, context: CallbackContext) -> None:
    foto_path = '1.jpg'
    await update.message.reply_photo(photo=InputFile(foto_path))

# Fungsi utama untuk menjalankan bot
async def main() -> None:
    # Buat aplikasi bot
    application = Application.builder().token(BOT_TOKEN).build()

    # Tambahkan handler untuk perintah /start
    application.add_handler(CommandHandler("start", start))
    
    # Tambahkan handler untuk perintah /kirimfoto
    application.add_handler(CommandHandler("kirimfoto", kirim_foto))

    # Jalankan polling untuk bot
    await application.run_polling()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
