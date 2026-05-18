import asyncio
import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, filters
from handlers.handlers import (
    start_add, get_title, get_priority, get_deadline,
    list_tasks_handler, done_task_handler, delete_task_handler, start_bot, help_command,
    TITLE, PRIORITY, DEADLINE
)
async def schedule_reminders(context):
    from scheduler.reminder import check_deadlines
    await check_deadlines(context.bot)

def main():
    load_dotenv()
    token = os.getenv("TOKEN")
    app = Application.builder().token(token).build()
    conv_handler = ConversationHandler(
    entry_points=[CommandHandler("add", start_add)],
    states={
        TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_title)],
        PRIORITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_priority)],
        DEADLINE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_deadline)],
    },
    fallbacks=[]
        )
    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("start", start_bot))
    app.add_handler(CommandHandler("list", list_tasks_handler))
    app.add_handler(CommandHandler("done", done_task_handler))
    app.add_handler(CommandHandler("delete", delete_task_handler))
    app.add_handler(CommandHandler("help", help_command))
    app.job_queue.run_repeating(schedule_reminders, interval=3600, first=10)
    
    app.run_polling()
    
    
if __name__ == "__main__":
    main()