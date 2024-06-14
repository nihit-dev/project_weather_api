from sqlalchemy.orm import Session
from typing import Type, Any
from fastapi import HTTPException, status
from .models.weather import Weather
from .models.statistics import Statistics
from datetime import date

Model = {"weather": Weather, "statistics": Statistics}


def get_data_all(
    db: Session, model: str, offset: int, limit: int
) -> list[Type[Weather]]:
    """Fetches data from db without any filter"""
    model = Model.get(model)
    data = db.query(model).offset(offset).limit(limit).all()
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No data found at given offset"
        )

    return data


def get_data_by_date_and_station(
    db: Session,
    station_id: str,
    model: str,
    offset: int,
    limit: int,
    filter_date: date = None,
    year: int = None,
) -> Any:
    """Fetches data from given model based on filters: date/year and/or station_id"""
    print('dfafaf')
    model = Model.get(model)
    data = db.query(model)
    if filter_date or year:
        if model == Weather:
            data = data.filter(model.date == filter_date)
        else:
            print('+++++++++++uh ha')
            data = data.filter(model.year == year)
    if station_id:
        data = data.filter(model.station_id == station_id)
        
    total_data = data.all()
    data = data.offset(offset).limit(limit).all()
    
    if not data:
        if total_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No data found at the given offset.",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Station ID or date does not exist.",
            )
    
    return data
