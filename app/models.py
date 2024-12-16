from sqlalchemy import Column, Integer, String, DateTime

from database import Base

class ImageDB(Base):
    __tablename__ = "imagesdb"
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(150), unique=True)
    prediction = Column(String(50))
    upload_time = Column(DateTime)