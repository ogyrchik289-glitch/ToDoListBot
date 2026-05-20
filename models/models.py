from dataclasses import dataclass

@dataclass
class Task:
    id: int
    title: str
    status: str
    priority: str
    deadline: str
    user_id: int
    remind_before: int
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "priority": self.priority,
            "deadline": self.deadline,
            "user_id": self.user_id,
            "remind_before": self.remind_before
                    }
   
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            title=data["title"],
            status=data["status"],
            priority=data["priority"],
            deadline=data["deadline"],
            user_id=data["user_id"],
            remind_before=data["remind_before"]
            )