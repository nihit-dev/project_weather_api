"""Ingests the data to database"""

import os
from datetime import datetime
from sqlalchemy.orm import Session

from .models.weather import Weather
from .models.statistics import Statistics
from .exceptions import IngestException


def read_data(file: str, db: Session):
    """Reads the data from file and add to db"""
    try:
        station_id = file.split("/")[-1].split(".")[0]
    except Exception as e:
        raise e
    try:
        with open(file, "r", encoding="utf-8") as f:
            avg_min_temp = 0
            avg_max_temp = 0
            count = 0
            total_precipitation = 0
            year = datetime.strptime(f.readline().split()[0], "%Y%m%d").date().year
            f.seek(0)
            for line in f:
                data = line.split()
                # File format: date maximum_temp minimum_temp precipitation
                date = datetime.strptime(data[0], "%Y%m%d").date()
                max_temp = data[1] if data[1] != -9999 else None
                min_temp = data[2] if data[2] != -9999 else None
                precipitation = data[3] if data[3] != -9999 else None
                weather = Weather(
                    station_id=station_id,
                    date=date,
                    maximum_temp=max_temp,
                    minimum_temp=min_temp,
                    precipitation=precipitation,
                )
                db.add(weather)
                if year != date.year:
                    # calculate the averages
                    avg_min_temp = avg_min_temp / count
                    avg_max_temp = avg_max_temp / count
                    statistics = Statistics(
                        year=year,
                        station_id=station_id,
                        avg_max_temp=avg_max_temp,
                        avg_min_temp=avg_min_temp,
                        total_precipitation=total_precipitation,
                    )
                    db.add(statistics)

                    # reset the counters
                    avg_min_temp = 0
                    avg_max_temp = 0
                    total_precipitation = 0
                    count = 0
                    year = date.year
                count += 1
                avg_max_temp += int(max_temp)
                avg_min_temp += int(min_temp)
                total_precipitation += int(precipitation)
    except Exception as e:
        raise e


def ingest_data(path: str, db: Session):
    """Ingests the data to db from each file in path"""

    # Check if db already has entries
    weather = db.query(Weather).offset(0).limit(10).all()
    if len(weather) > 0:
        raise IngestException("Data is already ingested")
    files = [
        entry for entry in os.listdir(path) if os.path.isfile(os.path.join(path, entry))
    ]

    try:
        for file in files:
            read_data(os.path.join(path, file), db)
            db.commit()
    except Exception as e:
        raise e
