from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from src.database import Base

class HotelsOrm(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True) #в скобках можно указать желаемый тип столбца для БД, например, BigInteger
    title: Mapped[str] = mapped_column(String(100))
    location: Mapped[str] = mapped_column()