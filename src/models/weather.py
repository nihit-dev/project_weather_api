from sqlalchemy import Float, Column, Date, Integer, String
from sqlalchemy import UniqueConstraint
from ..database import Base


class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(String)
    date = Column(Date)
    maximum_temp = Column(Float)
    minimum_temp = Column(Float)
    precipitation = Column(Float)
    UniqueConstraint("station_id", "date")
