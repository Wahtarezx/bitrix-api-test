from fastapi import FastAPI, HTTPException
from app.controllers.bitrix_controller import BitrixController
from app.schemas.bitrix_schemas import LeadCreate, LeadResponse
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Bitrix API", version="1.0.0")

# Инициализация контроллера
bitrix = BitrixController(os.getenv("BITRIX_URL"))

@app.post("/leads/", response_model=LeadResponse)
async def create_lead(lead: LeadCreate):
    """Создание нового лида в Bitrix24"""
    try:
        lead_id = await bitrix.create_lead(lead.name, lead.phone)
        return {"id": lead_id, "status": "created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/leads/{phone}")
async def get_lead_by_phone(phone: str):
    """Поиск лида по номеру телефона"""
    try:
        lead = await bitrix.get_leads_by_phone(phone)
        return lead
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Bitrix API работает"}
