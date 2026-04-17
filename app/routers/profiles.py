from typing import Optional

from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
# from starlette import status

from app.database import get_db
from app.schemas.profile import ProfileResponse, ProfileCreate, ProfileListItem
from app.services.profile_service import create_profile, get_profile_by_id, get_all_profiles, delete_profile

router = APIRouter(prefix="/api/profiles", tags=["profiles"])


@router.post("", status_code=201)
async def handle_create_profile(payload: ProfileCreate, db: Session = Depends(get_db)):
    profile, already_existed = await create_profile(payload.name, db)

    profile_data = ProfileResponse.model_validate(profile).model_dump(mode="json")

    if already_existed:
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Profile already exists",
                "data": profile_data
            }
        )

    return JSONResponse(
        status_code=201,
        content={
            "status": "success",
            "data": profile_data
        }
    )


@router.get("/{profile_id}", status_code=200)
def handle_get_profile(
        profile_id: str,
        db: Session = Depends(get_db),
):
    profile = get_profile_by_id(profile_id, db)

    return {
        "status": "success",
        "data": ProfileResponse.model_validate(profile).model_dump(mode="json")
    }


@router.get("", status_code=200)
def handle_list_profiles(
        gender: Optional[str] = None,
        country_id: Optional[str] = None,
        age_group: Optional[str] = None,
        db: Session = Depends(get_db),
):
    profiles = get_all_profiles(db, gender, country_id, age_group)

    return {
        "status": "success",
        "count": len(profiles),
        "data": [
            ProfileListItem.model_validate(p).model_dump(mode="json") for p in profiles
        ]
    }


@router.delete("/{profile_id}", status_code=204)
def handle_delete_profile(
        profile_id: str,
        db: Session = Depends(get_db),
):
    delete_profile(profile_id, db)
    return Response(status_code=204)
