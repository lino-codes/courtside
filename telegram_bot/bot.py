from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
)
import datetime
from config import bot_token
from domain.auto_booker import lesson_booker
from utils.time_utils import format_time_ampm

CHOOSING_LEVEL, ASK_START_TIME = range(2)


async def class_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
        [
            InlineKeyboardButton("Advanced", callback_data="Advanced"),
            InlineKeyboardButton("Intermediate", callback_data="Intermediate"),
            InlineKeyboardButton("Beginner", callback_data="Beginner"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Choose your class level:", reply_markup=reply_markup
    )
    return CHOOSING_LEVEL


async def choose_level(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    # Save chosen class level in context.user_data
    context.user_data["class_level"] = query.data

    keyboard = [
        [
            InlineKeyboardButton("Yes", callback_data="yes"),
            InlineKeyboardButton("No", callback_data="no"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Exclude classes starting before 5pm on weekdays?", reply_markup=reply_markup
    )
    return ASK_START_TIME

def extract_url(markdown_url):
    # "[text](url)" - returns: text, url
    import re
    match = re.match(r"\[(.+?)\]\((.+?)\)", markdown_url)
    if match:
        return match.group(1), match.group(2)
    return markdown_url, ""

def format_results(df):
    messages = []
    for _, row in df.iterrows():
        # Extract title, url
        title = row["title"]
        url = row["url"]
        # Location: only up to first comma
        location = str(row['location']).split(",")[0]
        # Start/end time in am/pm
        start = format_time_ampm(row['start_time'])
        end = format_time_ampm(row['end_time'])
        # Day, dates
        day = row.get("day", "")
        dates = row.get("dates", "")
        msg = (f'<a href="{url}">{title}</a>\n'
               f"Location: {location}\n"
               f"Date: {dates}\n"
               f"Time: {start} - {end}")
        messages.append(msg)
    return "\n\n".join(messages)

async def ask_start_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    start_after_5pm = query.data == "yes"
    lesson_start = 17 if start_after_5pm else 0
    class_level = context.user_data.get("class_level")

    # Your lesson_booker is assumed to return a pandas DataFrame
    # This is where the booking function
    result_df = lesson_booker(
        class_level=class_level,
        exclude_days=[],
        full_days=["Sat", "Sun"],
        lesson_start=lesson_start,
    )

    if result_df is not None and not result_df.empty:
        formatted_message = format_results(result_df)
        await query.edit_message_text(formatted_message, parse_mode="HTML")
    else:
        await query.edit_message_text("Sorry, there is no class available.")

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END


def main():
    application = ApplicationBuilder().token(bot_token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("class_query", class_query)],
        states={
            CHOOSING_LEVEL: [CallbackQueryHandler(choose_level)],
            ASK_START_TIME: [CallbackQueryHandler(ask_start_time)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == "__main__":
    main()
