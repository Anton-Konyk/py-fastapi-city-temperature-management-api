from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from city import schemas, crud
from dependencies import get_db

router = APIRouter()


@router.post("/cities/", response_model=schemas.City)
def create_city(
    city: schemas.CityCreate,
    db: Session = Depends(get_db),
):
    db_city = crud.get_city_by_name_additional_info(
        db=db,
        city_name=city.name,
        city_additional_info=city.additional_info
    )

    if db_city:
        raise HTTPException(
            status_code=400,
            detail="Such city with such additional info already exists"
        )

    return crud.create_city(db=db, city=city)


@router.get("/cities/", response_model=List[schemas.City])
def list_cities(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    return crud.get_cities(db, skip=skip, limit=limit)


@router.get("/cities/{city_id}/", response_model=schemas.City)
def read_single_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return db_city
