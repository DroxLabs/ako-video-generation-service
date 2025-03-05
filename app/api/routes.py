from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from app.schemas.video import VideoRequest, VideoResponse, TaskStatus
from app.services.runway_service import RunwayService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
runway_service = RunwayService()

@router.post("/videos", response_model=VideoResponse)
async def create_video(
    first_frame: UploadFile = File(..., description="First frame image"),
    last_frame: UploadFile = File(None, description="Last frame image"),
    prompt_text: str = Form("generate a video"),
    duration: int = Form(5)
):
    try:
        image_data_list = []
        content_types = []
        
        if first_frame:
            image_data_list.append(await first_frame.read())
            content_types.append(first_frame.content_type)

        if last_frame:
            image_data_list.append(await last_frame.read())
            content_types.append(last_frame.content_type)
        
        if not image_data_list:
            raise HTTPException(status_code=400, detail="At least one image must be provided.")
        
        result = await runway_service.create_video_from_image(
            image_data_list=image_data_list,
            content_types=content_types,
            prompt_text=prompt_text,
            duration=duration
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