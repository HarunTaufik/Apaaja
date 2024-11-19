import nest_asyncio
import asyncio
import os
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Terapkan nest_asyncio untuk menghindari masalah event loop yang sudah berjalan
nest_asyncio.apply()

# Path ke folder yang berisi foto
PHOTO_FOLDER = './'

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('Bot sudah online! Kirimkan nama file foto untuk menerima foto dari folder.')

async def send_photo_by_filename(update: Update, context: CallbackContext):
    # Ambil nama file dari pesan teks
    filename = update.message.text.strip()
    
    # Periksa apakah nama file kosong
    if not filename:
        await update.message.reply_text('Silakan kirimkan nama file foto yang ingin Anda terima.')
        return
    
    # Buat path file foto
    photo_path = os.path.join(PHOTO_FOLDER, filename)
    
    # Periksa apakah file ada di folder
    if not os.path.isfile(photo_path):
        await update.message.reply_text(f'Foto dengan nama "{filename}" tidak ditemukan di folder.')
        return
    
    # Kirim foto
    with open(photo_path, 'rb') as photo:
        await update.message.reply_photo(photo=InputFile(photo, filename=filename))

async def main():
    # Ganti dengan token bot Telegram Anda
    application = Application.builder().token('7456694718:AAFvfrrFrrNTdeq-O3k5CFgg_Klth5XnAyE').build()
    
    # Menambahkan handler untuk perintah /start
    application.add_handler(CommandHandler('start', start))
    
    # Menambahkan handler untuk pesan teks (nama file)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_photo_by_filename))
    
    # Jalankan polling untuk menerima pembaruan
    await application.run_polling()

if __name__ == '__main__':
    # Jalankan fungsi utama
    asyncio.run(main())
