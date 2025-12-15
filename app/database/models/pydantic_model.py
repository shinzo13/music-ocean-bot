from typing import Optional

from pydantic import BaseModel
from sqlalchemy import TypeDecorator, JSON


class PydanticModel(TypeDecorator):
    impl = JSON
    cache_ok = True

    def __init__(self, pydantic_model):
        self.pydantic_model = pydantic_model
        super().__init__()

    def process_bind_param(self, value: Optional[BaseModel], dialect):
        if value is None:
            return None
        if isinstance(value, self.pydantic_model):
            return value.model_dump(mode='json')
        return value

    def process_result_value(self, value, dialect):
        if value is None:
            return self.pydantic_model()
        # Pydantic will automatically convert the string back to Engine enum
        # because of the type annotation in UserSettings
        return self.pydantic_model.model_validate(value)
