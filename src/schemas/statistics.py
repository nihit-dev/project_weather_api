from pydantic import BaseModel


class StatisticsSchema(BaseModel):
    id: int
    station_id: str
    year: int
    avg_max_temp: float
    avg_min_temp: float
    total_precipitation: float


class StatisticsErrorSchema(BaseModel):
    message: str
