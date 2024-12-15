from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import httpx

from temperature import schemas, models

OPENWEATHER_API_KEY = "dc41438b531b4d89df81363c55dad4e4"
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


async def fetch_temperature(city_name: str) -> float:
    params = {
        "q": city_name,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(OPENWEATHER_URL, params=params)
        if response.status_code != 200:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch temperature for city: {city_name}. "
                       f"Error: {response.json().get('message', 'Unknown error')}"
            )
        data = response.json()
        return data["main"]["temp"]


async def get_temperatures(db: AsyncSession, skip: int = 0, limit: int | None = 10):
    query = await db.execute(
        select(models.DBTemperature).offset(skip).limit(limit)
    )
    return query.scalars().all()


async def get_temperature_by_city_id(db: AsyncSession, city_id: int):
    query = select(models.DBTemperature).where(models.DBTemperature.city_id ==
                                               city_id)
    result = await db.execute(query)

    return result.scalars().all()
