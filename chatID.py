import nest_asyncio
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Apply nest_asyncio to support running in environments with existing event loops
nest_asyncio.apply()

async def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    await update.message.reply_text(f'Chat ID Anda adalah: {chat_id}')

async def main():
    application = Application.builder().token('7456694718:AAFvfrrFrrNTdeq-O3k5CFgg_Klth5XnAyE').build()
    application.add_handler(CommandHandler('start', start))
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
