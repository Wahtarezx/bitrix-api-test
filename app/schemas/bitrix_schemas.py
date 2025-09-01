from pydantic import BaseModel, Field, validator
import re


class LeadCreate(BaseModel):
    """Схема для создания лида"""
    name: str = Field(..., min_length=1, max_length=100, description="Имя клиента")
    phone: str = Field(..., max_lengh=15, description="Номер телефона")

    @validator('phone')
    def validate_phone(cls, v):
        cleaned_phone = re.sub(r'\D', '', v)
        if len(cleaned_phone) < 10:
            raise ValueError('Неверный формат телефона')
        return cleaned_phone


class LeadResponse(BaseModel):
    """Схема ответа при создании лида"""
    id: int
    status: str
