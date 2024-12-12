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
