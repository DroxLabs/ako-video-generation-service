from pydantic import BaseModel
from typing import Optional

class VideoRequest(BaseModel):
    prompt_text: str
    image_data: str  # Base64 encoded image

class VideoResponse(BaseModel):
    task_id: str
    status: str
    video_url: Optional[str] = None

class TaskStatus(BaseModel):
    task_id: str
    status: str
    video_url: Optional[str] = None 