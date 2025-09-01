import aiohttp
from typing import Dict, Any


class BitrixController:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = aiohttp.ClientSession()

    async def create_lead(self, name: str, phone: str) -> int:
        """Создание лида в Bitrix24"""
        url = f"{self.base_url}crm.lead.add"
        payload = {
            "fields": {
                "TITLE": f"Лид от {name}",
                "NAME": name,
                "PHONE": [{"VALUE": phone, "VALUE_TYPE": "WORK"}]
            }
        }

        async with self.session.post(url, json=payload) as response:
            if response.status == 200:
                data = await response.json()
                return data.get('result')
            else:
                raise Exception(f"Ошибка создания лида: {response.status}")

    async def get_leads_by_phone(self, phone: str) -> Dict[str, Any]:
        """Получение лида по номеру телефона"""
        cleaned_phone = ''.join(filter(str.isdigit, phone))

        url = f"{self.base_url}crm.lead.list"
        params = {
            "filter[SEARCH_PHONE]": cleaned_phone,
             "select[0]": "ID",
                "select[1]": "NAME",
                "select[2]": "PHONE",
                "select[3]": "TITLE",
                "select[4]": "DATE_CREATE"
        }

        async with self.session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                print(data)
                leads = data.get('result', [])

                if not leads:
                    raise Exception("Лид не найден")

                for lead in leads:
                    print(lead)
                    phone_entries = lead.get('PHONE')
                    if isinstance(phone_entries, list):
                        for phone_entry in phone_entries:
                            phone_value = phone_entry.get('VALUE', '')
                            if phone_value:
                                entry_digits = ''.join(filter(str.isdigit, str(phone_value)))
                                if entry_digits == cleaned_phone:
                                    return lead

                return leads[0]

            else:
                raise Exception(f"Ошибка поиска лида: {response.status}")

    async def close(self):
        """Закрытие сессии"""
        await self.session.close()
