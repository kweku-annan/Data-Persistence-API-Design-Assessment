from datetime import datetime

from pydantic import BaseModel, field_validator



class ProfileCreate(BaseModel):
    name: str

    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('name must not be empty')
        if not v.strip().replace(" ", "").replace("-", "").isalpha():
            raise ValueError('name must be a valid string (only letters, spaces, and hyphens allowed)')
        return v.strip().lower()


class ProfileResponse(BaseModel):
    id: str
    name: str
    gender: str
    gender_probability: float
    sample_size: int
    age: int
    age_group: str
    country_id: str
    country_probability: float
    created_at: datetime

    model_config = {
        "from_attributes": True,
        "json_encoders": {datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%SZ")}
    }


class ProfileListItem(BaseModel):
    id: str
    name: str
    gender: str
    age: int
    age_group: str
    country_id: str

    model_config = {"from_attributes": True}