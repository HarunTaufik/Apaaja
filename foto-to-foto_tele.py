import nest_asyncio
import asyncio
import cv2
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Apply nest_asyncio
nest_asyncio.apply()

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('Bot is online!')

async def capture_and_send_photo(update: Update, context: CallbackContext):
    # Capture photo
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    camera.release()
    
    if not ret:
        await update.message.reply_text('Failed to capture photo.')
        return

    # Save the photo
    photo_path = 'photo.jpg'
    cv2.imwrite(photo_path, frame)
    
    # Send photo
    with open(photo_path, 'rb') as photo_file:
        await update.message.reply_photo(photo=InputFile(photo_file, filename='photo.jpg'))

async def main():
    application = Application.builder().token('7456694718:AAFvfrrFrrNTdeq-O3k5CFgg_Klth5XnAyE').build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.PHOTO, capture_and_send_photo))

    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
