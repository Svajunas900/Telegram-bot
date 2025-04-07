from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import os
from dotenv import load_dotenv
import logging
import json

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

API_TOKEN=os.getenv("TELEGRAM_API_KEY")


async def start(update: Update, context):
    await update.message.reply_text("Hello! Send me any message, and I will echo it back.")


async def echo(update: Update, context):
    text = update.message.text
    await update.message.reply_text(f"You said: {text}")


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

    
async def lambda_handler(event, context):

    body = json.loads(event['body'])
    update = Update.de_json(body, None)

    app = ApplicationBuilder().token(API_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    await app.process_update(update)

    return {
        'statusCode': 200,
        'body': json.dumps('OK')
    }