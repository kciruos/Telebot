import os
import whisper
from telegram import Update
from telegram.ext import Application, MessageHandler, CallbackContext, filters
from pydub import AudioSegment

# Initialize Whisper model
model = whisper.load_model("base")  # You can use "small", "medium", or "large" for better accuracy

# Function to respond to "hello"
async def reply_to_hello(update: Update, context: CallbackContext) -> None:
    if "hello" in update.message.text.lower():
        await update.message.reply_text("Hi there!")

# Function to process voice messages
async def handle_voice_message(update: Update, context: CallbackContext) -> None:
    file_id = update.message.voice.file_id
    file = await context.bot.get_file(file_id)
    file_path = "voice_message.ogg"

    # Download the voice message
    await file.download_to_drive(file_path)

    # Convert the .ogg file to .wav for Whisper
    audio = AudioSegment.from_file(file_path, format="ogg")
    wav_path = "voice_message.wav"
    audio.export(wav_path, format="wav")

    # Transcribe the audio using Whisper
    try:
        result = model.transcribe(wav_path)
        transcription = result["text"]
        await update.message.reply_text(f"Transcription: {transcription}")
    except Exception as e:
        await update.message.reply_text(f"An error occurred while transcribing: {str(e)}")

    # Clean up temporary files
    os.remove(file_path)
    os.remove(wav_path)

def main():
    # Fetch the bot token from the environment variable
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN environment variable not set!")
    
    # Build the bot application
    application = Application.builder().token(token).build()

    # Add handlers for text and voice messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_to_hello))
    application.add_handler(MessageHandler(filters.VOICE, handle_voice_message))

    # Start the bot
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()


'''
import os
import whisper
from telegram import Update
from telegram.ext import Application, MessageHandler, CallbackContext, filters
from pydub import AudioSegment

# Initialize Whisper model
model = whisper.load_model("base")  # You can use "small", "medium", or "large" for better accuracy

# Function to respond to "hello"
async def reply_to_hello(update: Update, context: CallbackContext) -> None:
    if "hello" in update.message.text.lower():
        await update.message.reply_text("Hi there!")

# Function to process voice messages
async def handle_voice_message(update: Update, context: CallbackContext) -> None:
    file_id = update.message.voice.file_id
    file = await context.bot.get_file(file_id)
    file_path = "voice_message.ogg"

    # Download the voice message
    await file.download_to_drive(file_path)

    # Convert the .ogg file to .wav for Whisper
    audio = AudioSegment.from_file(file_path, format="ogg")
    wav_path = "voice_message.wav"
    audio.export(wav_path, format="wav")

    # Transcribe the audio using Whisper
    try:
        result = model.transcribe(wav_path)
        transcription = result["text"]
        await update.message.reply_text(f"Transcription: {transcription}")
    except Exception as e:
        await update.message.reply_text(f"An error occurred while transcribing: {str(e)}")

    # Clean up temporary files
    os.remove(file_path)
    os.remove(wav_path)

def main():
    # Replace 'YOUR_BOT_TOKEN' with your bot's token
    application = Application.builder().token("7620304429:AAEXpiCvdSweuCIGl4YZsBUcDIvH9XS5v_Y").build()

    # Add handlers for text and voice messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_to_hello))
    application.add_handler(MessageHandler(filters.VOICE, handle_voice_message))

    # Start the bot
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
'''