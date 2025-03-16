from typing import TypeVar
import json

from pydantic import BaseModel

from app.database import Base


ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class DataMapper:
    model = ModelType | None
    schema = SchemaType | None

    @classmethod
    def map_to_domain_entity(cls, data):
        return cls.schema.model_validate(data, from_attributes=True)


class RedisDataMapper:
    schema = SchemaType | None

    @classmethod
    def serialize_data_to_schema(cls, data):
        new_data = json.loads(data)
        return cls.schema.model_validate(new_data, from_attributes=True)
