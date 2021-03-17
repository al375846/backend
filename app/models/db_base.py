from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field
from odmantic import Model


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class DbBase(Model):
    id: Optional[PyObjectId] = Field(alias="_id")

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }