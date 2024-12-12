from fastapi import HTTPException
from sqlalchemy.orm import Session

from city import schemas, models


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.DBCity(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def get_city_by_id(db: Session, city_id: int):
    return (
        db.query(models.DBCity).filter(models.DBCity.id == city_id).first()
    )


def get_city_by_name_additional_info(
        db: Session,
        city_name: str,
        city_additional_info: str
):
    return (
        db.query(models.DBCity).
        filter((models.DBCity.name == city_name) &
               (models.DBCity.additional_info == city_additional_info)).
        first()
    )


def get_cities(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.DBCity).offset(skip).limit(limit).all()


def update_city(db: Session, city_id: int, city: schemas.CityUpdate):
    db_city = db.query(models.DBCity).filter(models.DBCity.id == city_id).first()

    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")

    db_city.name = city.name
    db_city.additional_info = city.additional_info

    db.commit()
    db.refresh(db_city)

    return db_city
