from fastapi import HTTPException
from sqlalchemy.orm import Session

import schemas
import models


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.DBCity(
        name=city.name,
        bio=city.additional_info,
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def get_city_by_id(db: Session, city_id: int):
    return (
        db.query(models.DBCity).filter(models.DBCity.id == city_id).first()
    )


def update_city(db: Session, city_id: int, city: schemas.CityUpdate):
    db_city = db.query(models.DBCity).filter(models.DBCity.id == city_id).first()

    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")

    db_city.name = city.name
    db_city.additional_info = city.additional_info

    db.commit()
    db.refresh(db_city)

    return db_city
