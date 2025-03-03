import base64
import logging
from typing import Optional
import runwayml
from app.core.config import settings
import mimetypes

logger = logging.getLogger(__name__)

class RunwayService:
    def __init__(self):
        self.client = runwayml.RunwayML(api_key=settings.RUNWAY_API_KEY)

    async def create_video_from_image(
        self,
        image_data: bytes,
        content_type: str,
        prompt_text: str = 'generate a video',
    ) -> dict:
        try:
            # Convert bytes to base64 with proper data URI prefix
            base64_image = base64.b64encode(image_data).decode('utf-8')
            data_uri = f"data:{content_type};base64,{base64_image}"
            
            # Create image-to-video task
            # Note: Update these parameters according to Runway's actual API documentation
            task = self.client.image_to_video.create(
                model='gen3a_turbo',
                prompt_image=data_uri,
                prompt_text=prompt_text,
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
            task = self.client.tasks.retrieve(task_id)
            response = {
                "task_id": task_id,
                "status": task.status
            }
            
            if task.status == "SUCCEEDED":
                response["video_url"] = task.output[0]
                
            return response
        except Exception as e:
            logger.error(f"Error checking task status: {str(e)}, TASK: {task}")
            raise 