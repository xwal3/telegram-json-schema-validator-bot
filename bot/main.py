
import json

from telegram import Update, ForceReply, BotCommand
from telegram.ext import (Application, ApplicationBuilder, ContextTypes, CommandHandler,MessageHandler, filters, ConversationHandler)

from bot.LLMConversationValidator import LLMConversationValidator

from config.settings import TELEGRAM_BOT_TOKEN







SCHEMA_STATE, DATA_STATE, REVIEW_STATE = range(3)

async def post_init(application: Application):

    bot_commands = [
        BotCommand("start", "Starts the bot and shows a welcome message"),
        BotCommand("validate", "Starts the JSON validation process"),
        BotCommand("review", "Review a complete AI tool call conversation"),
        BotCommand("cancel", "Cancels the current operation"),
    ]
    await application.bot.set_my_commands(bot_commands)

def clean_json_string(input_text: str) -> str:

    replacements = {
        "\u00A0": " ",    
        "\u201C": '"',    
        "\u201D": '"',    
        "\u2018": "'",    
        "\u2019": "'",    
    }
    for bad, good in replacements.items():
        input_text = input_text.replace(bad, good)
    return input_text.strip()
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}! I'm a JSON schema validator bot. "
        "Use the menu to start a new validation or get help.",
        reply_markup=ForceReply(selective=True),
    )

async def validate_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    await update.message.reply_text("Please paste your JSON Schema now. You can use /cancel to stop at any time.")
    return SCHEMA_STATE




async def get_schema(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        raw_text = update.message.text
        cleaned_text = clean_json_string(raw_text)
        schema = json.loads(cleaned_text)
        context.user_data['schema'] = schema
        await update.message.reply_text("Schema received. Now, please paste your JSON data.")
        return DATA_STATE
    except json.JSONDecodeError:
        await update.message.reply_text(
            "That doesn't look like valid JSON. Please send a valid JSON Schema."
        )
        return SCHEMA_STATE



async def get_data_and_validate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        raw_text = update.message.text
        cleaned_text = clean_json_string(raw_text)
        data = json.loads(cleaned_text)
        schema = context.user_data.get('schema')

        if not schema:
            await update.message.reply_text(
                "I've lost the schema. Please start over with /validate."
            )
            return ConversationHandler.END

        validator = LLMConversationValidator(schema)

        result = validator.validate_schema(data)

        if result["valid"]:
            await update.message.reply_text("✅ Validation successful! No issues found.")

        else:
            message = "❌ Validation failed. Issues found:\n\n"
            for error in result["errors"]:
                message += f"Error Type: {error.get('type', 'Unknown')}\n"
                message += f"Description: {error.get('description', 'No description')}\n"
                message += f"Path: {error.get('path', 'None')}\n"
                message += f"Context: {error.get('context', 'None')}\n"
            await update.message.reply_html(message)

    except json.JSONDecodeError:
        await update.message.reply_text(
            "That doesn't look like valid JSON. Please send a valid JSON data document."
        )
    finally:

        context.user_data.clear()
        return ConversationHandler.END

async def review_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Please paste the full review payload now. The JSON should contain a 'schema' and a 'data' object.")
    return REVIEW_STATE


async def review_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        raw_text = update.message.text
        cleaned_text = clean_json_string(raw_text)
        payload = json.loads(cleaned_text)
        schema = payload.get('schema')
        data = payload.get('data')

        if not schema or not data:
            await update.message.reply_text(
                "❌ Invalid payload. The JSON must contain a 'schema' and a 'data' object. Please try again."
            )
            return REVIEW_STATE  


        validator = LLMConversationValidator(schema)
        
        result = validator.validate_schema(data)
        

        if result["valid"]:
            await update.message.reply_text("✅ Review complete. No issues found in this conversation.")
        else:
            message = "❌ Review complete. Issues found:\n\n"
            for error in result["errors"]:
                message += f"Error Type: {error.get('type', 'Unknown')}\n"
                message += f"Description: {error.get('description', 'No description')}\n"
                message += f"Path: {error.get('path', 'None')}\n"
                message += f"Context: {error.get('context', 'None')}\n"
            await update.message.reply_html(message)
    except json.JSONDecodeError:
        await update.message.reply_text(
        "That doesn't look like valid JSON. Please send a valid JSON payload."
        )
    finally:
        context.user_data.clear()
        return ConversationHandler.END



async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Validation process canceled. Send /validate or /review to start again.")
    context.user_data.clear()
    return ConversationHandler.END





async def run_bot():


    application = Application.builder().token(TELEGRAM_BOT_TOKEN).post_init(post_init).build()


    application.add_handler(CommandHandler("start", start))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("validate", validate_command), CommandHandler("review", review_command)],
        states={
            SCHEMA_STATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_schema)],
            DATA_STATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_data_and_validate)],
            REVIEW_STATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, review_conversation)],
        },
        fallbacks=[ CommandHandler("cancel", cancel)],
    )
    
    application.add_handler(conv_handler)
    print("Bot is now running and polling for updates...")
    await application.run_polling(allowed_updates=["message"])

