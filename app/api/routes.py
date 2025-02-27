from fastapi import APIRouter, HTTPException
from app.schemas.video import VideoRequest, VideoResponse, TaskStatus
from app.services.runway_service import RunwayService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
runway_service = RunwayService()

@router.post("/videos", response_model=VideoResponse)
async def create_video(request: VideoRequest):
    try:
        result = await runway_service.create_video_from_image(
            image_data=request.image_data,
            prompt_text=request.prompt_text
        )
        return VideoResponse(**result)
    except Exception as e:
        logger.error(f"Error in create_video: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to create video"
        )

@router.get("/videos/{task_id}", response_model=TaskStatus)
async def get_video_status(task_id: str):
    try:
        result = await runway_service.get_task_status(task_id)
        return TaskStatus(**result)
    except Exception as e:
        logger.error(f"Error in get_video_status: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to get video status"
        ) 