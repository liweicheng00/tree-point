from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import uuid4


class User(BaseModel):
    id: str
    username: str
    total_points: int
    create_time: datetime
    update_time: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str

    class Config:
        schema_extra = {
            "example": {"username": "Happy User"}
        }


class PointRecord(BaseModel):
    record_id: str
    user_id: str
    timestamp: datetime
    transaction_points: int
    point_source_id: Optional[str] = Field(description="Foreign key for source of received points like another platform.")
    consumed_package_id: Optional[str] = Field(description="Foreign key for package of products that user purchased.")

    class Config:
        orm_mode = True


class CreatePointReceivedRecord(BaseModel):
    user_id: str
    transaction_points: int = Field(ge=0)
    point_source_id: str = Field(description="Foreign key for source of received points like another platform.")

    class Config:
        schema_extra = {
            "example": {
                "user_id": uuid4(),
                "transaction_points": 200,
                "point_source_id": uuid4()
            },
        }


class CreatePointConsumedRecord(BaseModel):
    user_id: str
    transaction_points: int = Field(ge=0)
    consumed_package_id: str = Field(description="Foreign key for package of products that user purchased.")

    class Config:
        schema_extra = {
            "example": {
                "user_id": uuid4(),
                "transaction_points": 23,
                "consumed_package_id": uuid4()
            },
        }
