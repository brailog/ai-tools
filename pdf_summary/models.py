from sqlalchemy import Column, Integer, String, Text
from database import Base

class PDFContent(Base):
    __tablename__ = "pdf_contents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    content = Column(Text, index=True)
