from pydantic import BaseModel
from typing import Optional


class VideoRequest(BaseModel):
    prompt_text: str
    
    class Config:
        arbitrary_types_allowed = True


class VideoResponse(BaseModel):
    task_id: str
    status: str
    video_url: Optional[str] = None


class TaskStatus(BaseModel):
    task_id: str
    status: str
    video_url: Optional[str] = None 