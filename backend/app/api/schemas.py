from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class JobStartRequest(BaseModel):
    proxy: str = Field(min_length=1, max_length=500)
    platform: Literal["windows", "android"]
    target_profiles: int = Field(ge=1, le=1000)


class JobResponse(BaseModel):
    id: int; proxy: str; platform: str; target_profiles: int; passed_profiles: int; attempts: int; status: str; message: Optional[str]; created_at: datetime
    model_config = {"from_attributes": True}


class ProfileResponse(BaseModel):
    id: int; job_id: int; octo_profile_id: str; platform: str; proxy: str; status: str; created_at: datetime
    model_config = {"from_attributes": True}


class ResultResponse(BaseModel):
    id: int; job_id: int; profile_id: Optional[int]; score: int; status: str; reason: str; screenshot_path: Optional[str]; created_at: datetime
    model_config = {"from_attributes": True}
