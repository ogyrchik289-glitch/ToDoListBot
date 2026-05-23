import datetime
from storage.storage import load_tasks

async def check_deadlines(bot):
    tasks = load_tasks()
    now_time = datetime.datetime.now()
    for task in tasks:
        if task.status == "Выполнено":
            continue
        parsed_deadline = datetime.datetime.strptime(task.deadline, "%Y-%m-%d. %H:%M" )
        diff = parsed_deadline - now_time
        hours_left = diff.total_seconds() / 3600
        if 0 < hours_left <= task.remind_before:
            await bot.send_message(
                chat_id = task.user_id,
                text=f"⚠️ Задача '{task.title}' должна быть выполнена до {task.deadline}!")
        