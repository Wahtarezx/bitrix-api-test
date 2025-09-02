import re
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class LeadCreate(BaseModel):
    """Схема для создания лида в Bitrix24"""
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Имя клиента",
        examples=["Иван Иванов"]
    )
    phone: str = Field(
        ...,
        description="Номер телефона в любом формате",
        examples=["+79161234567", "89161234567", "9161234567"]
    )

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        """Валидация номера телефона"""
        cleaned_phone = re.sub(r'\D', '', v)
        if len(cleaned_phone) < 10:
            raise ValueError('Номер телефона должен содержать не менее 10 цифр')
        return cleaned_phone

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Иван Иванов",
                "phone": "+79161234567"
            }
        }
    }


class LeadResponse(BaseModel):
    """Схема ответа при создании лида"""
    id: int = Field(..., description="ID созданного лида в Bitrix24", examples=[123])
    status: str = Field(..., description="Статус операции", examples=["created"])

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 123,
                "status": "created"
            }
        }
    }


class ErrorResponse(BaseModel):
    """Схема для ошибок API"""
    detail: str = Field(..., description="Описание ошибки", examples=["Лид не найден"])
    error_code: Optional[str] = Field(None, description="Код ошибки", examples=["LEAD_NOT_FOUND"])

    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "Лид не найден",
                "error_code": "LEAD_NOT_FOUND"
            }
        }
    }
