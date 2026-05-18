import datetime
from storage.storage import load_tasks

async def check_deadlines(bot):
    tasks = load_tasks()
    now_time = datetime.datetime.now()
    for task in tasks:
        if task.status == "Выполнено":
            continue
        parsed_deadline = datetime.datetime.strptime(task.deadline, "%Y-%m-%d" )
        diff = parsed_deadline - now_time
        if 0 < diff.total_seconds() / 3600 <= 24: 
            await bot.send_message(
                chat_id = task.user_id,
                text=f"⚠️ Задача '{task.title}' должна быть выполнена до {task.deadline}!")
        