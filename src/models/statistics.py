from sqlalchemy import Float, Column, Integer, String

from ..database import Base


class Statistics(Base):
    __tablename__ = "statistics"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer)
    station_id = Column(String)
    avg_max_temp = Column(Float)
    avg_min_temp = Column(Float)
    total_precipitation = Column(Float)
