import logging
import time
from typing import List

from sqlalchemy.orm import Session
import datetime
from fastapi import (
    Depends,
    HTTPException,
    status,
    Response,
)

from .database import get_db, app
from .ingest import ingest_data
from .schemas.weather import WeatherSchema, WeatherErrorSchema
from .schemas.statistics import StatisticsSchema, StatisticsErrorSchema
from .schemas.ingest import IngestSchema, IngestErrorSchema
from .exceptions import IngestException
from .crud import get_data_all, get_data_by_date_and_station


logger = logging.Logger(name="api_logger", level=logging.DEBUG)


@app.get(
    "/weather",
    summary="Get the weather data for stations",
    response_model=List[WeatherSchema] | WeatherErrorSchema,
    status_code=status.HTTP_200_OK,
)
async def get_weather(
    response: Response,
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = 50,
    station_id: str = None,
    date: datetime.date | str = None,
):
    """Get the weather data for stations"""
    try:
        if date or station_id:
            if isinstance(date, str):
                date = datetime.datetime.strptime(date, "%Y%m%d").date()
            data = get_data_by_date_and_station(
                db,
                station_id,
                "weather",
                offset=offset,
                limit=limit,
                filter_date=date,
            )
        else:
            data = get_data_all(db, "weather", offset, limit)
        return data
    except HTTPException as he:
        response.status_code = status.HTTP_404_NOT_FOUND
        logger.error(he)
        return {"message": f"Couldn't fetch data: {he.detail}"}
    except Exception as e:
        logger.error(e)
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "Unknown error"}


@app.get(
    "/weather/stats",
    summary="Get the statistic data for stations",
    response_model=List[StatisticsSchema] | StatisticsErrorSchema,
    status_code=status.HTTP_200_OK,
)
async def get_statistics(
    response: Response,
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = 50,
    year: int = None,
    station_id: str = None,
):
    """Get the statistic data for stations"""
    try:
        if station_id or year:
            data = get_data_by_date_and_station(
                db,
                station_id,
                "statistics",
                offset,
                limit,
                year=year,
            )
        else:
            data = get_data_all(db, "statistics", offset, limit)
        return data
    except HTTPException as he:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"Couldn't fetch data: {he.detail}"}
    except Exception as e:
        logger.error(e)
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "Unknown error"}


@app.get(
    "/ingest",
    summary="Ingests the data to db",
    status_code=status.HTTP_200_OK,
    response_model=IngestSchema | IngestErrorSchema
)
def ingest(
        response: Response,
        db: Session = Depends(get_db)
):
    """API Endpoint to ingest data to db"""
    try:
        start_time = time.time()
        logger.info(f"start time: {start_time}")
        ingest_data("wx_data/", db)
        end_time = time.time()
        logger.info("Total time: ", end_time - start_time)
        return {"status": "Success"}
    except IngestException as ie:
        return {"message": ie.message}
    except Exception as e:
        logger.error(e)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "Failed"}
