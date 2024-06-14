from pydantic import BaseModel
from datetime import date


class WeatherSchema(BaseModel):
    id: int
    station_id: str
    date: date
    maximum_temp: float
    minimum_temp: float
    precipitation: float


class WeatherErrorSchema(BaseModel):
    message: str
