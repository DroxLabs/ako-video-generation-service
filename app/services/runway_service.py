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
        image_data_list: bytes,
        content_types: str,
        prompt_text: str = 'generate a video',
        duration: int = 5
    ) -> dict:
        try:
            if len(image_data_list) == 0 or len(image_data_list) > 2:
                raise ValueError("You must provide one or two images.")
            
            # Convert images to base64 data URIs
            image_uris = [
                {"uri": f"data:{content_types[i]};base64,{base64.b64encode(image_data_list[i]).decode('utf-8')}",
                 "position": "first" if i == 0 else "last"}
                for i in range(len(image_data_list))
            ]
            
            # Create image-to-video task
            task = self.client.image_to_video.create(
                model='gen3a_turbo',
                prompt_image=image_uris if len(image_uris) > 1 else [image_uris[0]],
                prompt_text=prompt_text,
                duration=duration,
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