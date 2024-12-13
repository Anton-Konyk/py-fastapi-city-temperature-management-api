from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    UniqueConstraint,
    Float
)
from sqlalchemy.orm import relationship

from database import Base


class DBTemperature (Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    date_time = Column(DateTime, nullable=False)
    temperature = Column(Float, nullable=False)

    city = relationship("DBCity", back_populates="temperatures")

    __table_args__ = (
        UniqueConstraint('city_id', 'date_time', name='_city_date_uc'),
    )
