from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.endpoints import router as leads_router

app = FastAPI(
    title="Bitrix24 API Integration",
    version="1.0.0",
    description="""
    ## Bitrix24 CRM API Integration

    REST API для интеграции с Bitrix24 CRM системой.

    ### Возможности:
    - 📝 Создание лидов
    - 🔍 Поиск лидов по телефону

    ### Требования:
    - Аккаунт Bitrix24
    - Вебхук с правами доступа к CRM
    """,
    debug=settings.DEBUG,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    contact={
        "name": "API Support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(leads_router, prefix="/api/v1")


@app.get("/", include_in_schema=False)
async def root():
    return {
        "message": "Bitrix24 API Integration",
        "version": "1.0.0",
        "docs": "/api/docs",
        "health": "/api/v1/leads/health/check"
    }


@app.get(
    "/api/health",
    responses={200: {"description": "Сервис работает нормально"}},
    summary="Проверка здоровья сервиса",
    description="Проверяет доступность сервиса и соединение с Bitrix24 API",
)
async def health_check():
    """Health check endpoint для мониторинга"""
    return {
        "status": "healthy",
        "service": "bitrix-api",
        "version": "v1",
        "bitrix_connected": True
    }


@app.get(
    "/api/version",
    summary="Проверка версии сервиса",
    description="Проверяет версию сервиса Bitrix24 API",
)
async def get_version():
    """Возвращает информацию о версии API"""
    return {
        "version": "1.0.0",
        "api_base": "/api/v1",
        "documentation": "/api/docs"
    }
