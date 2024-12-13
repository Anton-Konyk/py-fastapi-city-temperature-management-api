from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from city.models import DBCity
from dependencies import get_db
from temperature import crud, models, schemas


router = APIRouter()


@router.post(
    "/temperatures/update",
    response_model=schemas.TemperatureUpdateResponse
)
async def update_temperatures(db: Session = Depends(get_db)):

    cities = db.query(DBCity).all()
    print(f"Cities: {cities}")
    if not cities:
        raise HTTPException(status_code=404, detail="No cities found in the database.")

    temperatures = []

    for city in cities:
        try:
            temperature = await crud.fetch_temperature(city.name)
            new_temperature = models.DBTemperature(
                city_id=city.id,
                date_time=datetime.utcnow(),
                temperature=temperature
            )
            db.add(new_temperature)
            temperatures.append(schemas.TemperatureCreate(
                city_id=city.id,
                city=city.name,
                date_time=new_temperature.date_time,
                temperature=new_temperature.temperature
            ))
        except HTTPException as e:
            print(e.detail)

    db.commit()

    return schemas.TemperatureUpdateResponse(
        message="Temperatures updated successfully",
        updated_records=len(temperatures),
        temperatures=temperatures
    )
