from fastapi import APIRouter, HTTPException, File, UploadFile
from app.schemas.video import VideoRequest, VideoResponse, TaskStatus
from app.services.runway_service import RunwayService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
runway_service = RunwayService()

@router.post("/videos", response_model=VideoResponse)
async def create_video(prompt_text: str, image_file: UploadFile = File(...)):
    try:
        image_data = await image_file.read()
        result = await runway_service.create_video_from_image(
            image_data=image_data,
            prompt_text=prompt_text,
            content_type=image_file.content_type
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

@router.get("/health", status_code=200)
async def health_check():
    return {"status": "healthy"} 