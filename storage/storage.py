import json
import os
from models.models import Task

FILE_PATH = "storage/tasks.json"

def load_tasks():
    tasks = []
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        loaded = json.load(f)
        if not loaded:
            return []
    
        
        for t in loaded:
            task = Task.from_dict(t)
            tasks.append(task)
    return tasks

def save_tasks(tasks: list[Task]) -> None:
    d_tasks = []
    for task in tasks:
        task_dict = task.to_dict()
        d_tasks.append(task_dict)
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(d_tasks, f, indent=2)
        
        
def add_task(new_task: Task) -> None:
    tasks = load_tasks()
    tasks.append(new_task)
    save_tasks(tasks)    
    
def get_task_by_user(target_id: int) -> list[Task]:
    tasks = load_tasks()
    users_tasks = []
    for task in tasks:
        if task.user_id == target_id:
            users_tasks.append(task)
    return users_tasks

def delete_task(task_id: int, user_id: int):
    tasks = load_tasks()
    updated_tasks = [task for task in tasks if not (task_id == task.id and user_id == task.user_id)]
    save_tasks(updated_tasks)