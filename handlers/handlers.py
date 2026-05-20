
from turtle import update

from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, CommandHandler, ConversationHandler, filters
from models.models import Task
from storage.storage import add_task, get_task_by_user, delete_task, save_tasks

TITLE, PRIORITY, DEADLINE, REMIND_BEFORE = range(4)

async def start_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Отлично! Введите название задачи:")
    return TITLE

async def get_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["title"] = update.message.text
    await update.message.reply_text("Введите приоритет задачи (низкий, средний, высокий):")
    return PRIORITY

async def get_priority(update: Update, context: ContextTypes.DEFAULT_TYPE):
    priority_map = {
    "низкий": "low",
    "средний": "medium",
    "высокий": "high"
}
    priority = update.message.text.lower()
    if priority not in priority_map:
        await update.message.reply_text("Пожалуйста, введите корректный приоритет (низкий, средний, высокий):")
        return PRIORITY
    context.user_data["priority"] = priority_map[priority]
    await update.message.reply_text("Введите срок выполенения задачи. Формат: ДД.ММ.ГГГГ ЧЧ:ММ:")
    return DEADLINE

async def get_deadline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    deadline = update.message.text
    try:
        date_part, hour_part = deadline.split(" ")
        day, month, year = map(int, date_part.split("."))
        hour = int(hour_part)
        deadline_date = f"{year:04d}-{month:02d}-{day:02d} {hour:02d}:00"
    except ValueError:
        await update.message.reply_text("Пожалуйста введите правильный срок. Формат: ДД.ММ.ГГГГ ЧЧ")
        return DEADLINE
    
    context.user_data["deadline"] = deadline_date
    await update.message.reply_text("За сколько часов напомнить? Введите число (например: 1, 3, 24):")
    return REMIND_BEFORE

async def get_remind_before(update: Update, context: ContextTypes.DEFAULT_TYPE):
    time = update.message.text
    try:
        hour = int(time)
        
    except ValueError:
        await update.message.reply_text("Пожалуйста укажите верное время. Формат(ЧЧ)")
        return REMIND_BEFORE
    context.user_data["remind_before"] = hour
    task = Task(
        id=len(get_task_by_user(update.effective_user.id)) + 1,
        title=context.user_data["title"],
        status="Невыполнено",
        priority=context.user_data["priority"],
        deadline=context.user_data["deadline"],
        user_id=update.effective_user.id,
        remind_before=context.user_data["remind_before"]
    )
    add_task(task)
    return ConversationHandler.END    

async def list_tasks_handler(update: Update, context:ContextTypes.DEFAULT_TYPE):
    tasks = get_task_by_user(update.effective_user.id)
    if not tasks:
        await update.message.reply_text("Вы ещё не добавили задачи")
        return
    response = "Ваши задачи:\n"
    for task in tasks:
        response += f"{task.id}. Название: {task.title}, Приоритет: {task.priority}, Срок: {task.deadline}, Статус: {task.status}\n"
    await update.message.reply_text(response)
    
async def done_task_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        task_id = int(update.message.text.split()[1])
    except (IndexError, ValueError):
        await update.message.reply_text("Пожалуйства, укажите ID задачи после команды /done. Пример: /done 2")
        return
    tasks = get_task_by_user(update.effective_user.id)
    if not any(task.id == task_id for task in tasks):
        await update.message.reply_text(f"Задача с ID {task_id} не найдена.")
        return
    for task in tasks:
        if task.id == task_id:
            task.status = "Выполнено"
            break
    save_tasks(tasks)
    await update.message.reply_text("Статус задачи успешно изменён на 'Выволено' ")
            
    
async def delete_task_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        task_id = int(update.message.text.split()[1])
    except (IndexError, ValueError):
        await update.message.reply_text("Пожалуйста, укажите ID задачи после команды /delete. Пример: /delete 2")
        return
    tasks = get_task_by_user(update.effective_user.id)
    if not any(task.id == task_id for task in tasks):
        await update.message.reply_text(f"Задача с ID {task_id} не найдена.")
        return
    delete_task(task_id, update.effective_user.id)
    await update.message.reply_text(f"Задача {task_id} успешно удалена!")
    
async def start_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"""Привет {update.effective_user.full_name} !
    Я твой личный менеджер задач в Telegram
    Организуй свои дела, держи фокус и перестань забывать о важном.
    Бот поможет тебе:
    ✅ планировать задачи и цели
    ⏰ получать напоминания вовремя        
    📈 сохранять продуктивность каждый день
    🧠 разгружать голову от лишнего хаоса
    🔥 вырабатывать дисциплину и привычку действовать
    Минималистично. Быстро. Без лишнего.
    Просто добавляй задачи — и двигайся вперед. 🚀""")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""                     
    Вот список доступный команд:\n
        
    start - Запустить бота
    add - Добавить задачу
    list - Показать все задачи
    done - Отметить задачу выполненной
    delete - Удалить задачу
    """)    
    
    




    
     