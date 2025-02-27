import base64
import logging
from typing import Optional
import runwayml
from app.core.config import settings

logger = logging.getLogger(__name__)

class RunwayService:
    def __init__(self):
        self.client = runwayml.RunwayML(api_key=settings.RUNWAY_API_KEY)

    async def create_video_from_image(
        self,
        image_data: str,
        prompt_text: str
    ) -> dict:
        try:
            # Create image-to-video task
            task = await self.client.imageToVideo.create(
                model='gen3a_turbo',
                promptImage=image_data,
                promptText=prompt_text,
            )
            
            return {
                "task_id": task.id,
                "status": "PROCESSING"
            }
        except Exception as e:
            logger.error(f"Error creating video: {str(e)}")
            raise

    async def get_task_status(self, task_id: str) -> dict:
        try:
            task = await self.client.tasks.retrieve(task_id)
            
            response = {
                "task_id": task_id,
                "status": task.status
            }
            
            if task.status == "SUCCEEDED":
                response["video_url"] = task.output.url
                
            return response
        except Exception as e:
            logger.error(f"Error checking task status: {str(e)}")
            raise 