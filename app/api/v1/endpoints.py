from fastapi import APIRouter, HTTPException, status
from app.services.bitrix_service import BitrixService
from app.schemas.bitrix_schemas import LeadCreate, LeadResponse, ErrorResponse
from app.core.config import settings

router = APIRouter(tags=["v1"])

bitrix_service = BitrixService(settings.BITRIX_URL)


@router.post(
    "/leads/",
    response_model=LeadResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Лид успешно создан"},
        500: {"model": ErrorResponse, "description": "Ошибка сервера или Bitrix API"}
    },
    summary="Создать нового лида",
    description="Создает нового лида в Bitrix24 CRM с указанными именем и телефоном.",
    )
async def create_lead(lead: LeadCreate):
    """
    Создание нового лида в Bitrix24

    - **name**: Имя клиента (обязательное)
    - **phone**: Номер телефона в любом формате (обязательное)

    Возвращает ID созданного лида в Bitrix24
    """
    try:
        lead_id = await bitrix_service.create_lead(lead.name, lead.phone)
        return LeadResponse(id=lead_id, status="created")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
            headers={"X-Error": "Bitrix API Error"}
        )


@router.get(
    "/leads/{phone}",
    responses={
        200: {"description": "Лид найден"},
        404: {"model": ErrorResponse, "description": "Лид не найден"},
        500: {"model": ErrorResponse, "description": "Ошибка сервера или Bitrix API"}
    },
    summary="Найти лида по телефону",
    description="Поиск лида в Bitrix24 по номеру телефона. Возвращает первый найденный лид.",
)
async def get_lead_by_phone(phone: str):
    """
    Поиск лида по номеру телефона

    - **phone**: Номер телефона (только цифры, без форматирования)

    Возвращает объект лида из Bitrix24 или ошибку 404 если лид не найден
    """
    try:
        lead = await bitrix_service.get_leads_by_phone(phone)
        return lead
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
            headers={"X-Error": "Lead Not Found"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
            headers={"X-Error": "Bitrix API Error"}
        )
