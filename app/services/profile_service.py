from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.integrations.external_apis import fetch_profile_data
from app.models.profile import PersonProfile


async def create_profile(name: str, db: Session) -> PersonProfile:
    # 1. Idempotency check -- same name, return existing record
    existing = db.query(PersonProfile).filter(PersonProfile.name == name.lower()).first()
    if existing:
        return existing, True # True = already existing

    # 2. Call the three external APIs concurrently
    data = await fetch_profile_data(name)

    # 3. Build and store the new record
    profile = PersonProfile(
        name=name.lower(),
        gender=data.gender,
        gender_probability=data.gender_probability,
        sample_size=data.sample_size,
        age=data.age,
        age_group=data.age_group,
        country_id=data.country_id,
        country_probability=data.country_probability,
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile, False

def get_profile_by_id(profile_id: str, db: Session) -> PersonProfile:
    profile = db.query(PersonProfile).filter(PersonProfile.id == str(profile_id)).first()

    if not profile:
        raise HTTPException(
            status_code=404,
            detail={"status": "error", "message": "Profile not found"},
        )

    return profile

def get_all_profiles(
        db: Session,
        gender: Optional[str] = None,
        country_id: Optional[str] = None,
        age_group: Optional[str] = None,
) -> list[PersonProfile]:
    query = db.query(PersonProfile)

    if gender:
        query = query.filter(func.lower(PersonProfile.gender) == gender.lower())

    if country_id:
        query = query.filter(func.lower(PersonProfile.country_id) == country_id.lower())

    if age_group:
        query = query.filter(func.lower(PersonProfile.age_group) == age_group.lower())

    return query.all()

def delete_profile(profile_id: str, db: Session) -> None:
    profile = db.query(PersonProfile).filter(PersonProfile.id == str(profile_id)).first()

    if not profile:
        raise HTTPException(
            status_code=404,
            detail={"status": "error", "message": "Profile not found"},
        )

    db.delete(profile)
    db.commit()
