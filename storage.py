from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import create_engine


engine = create_engine("sqlite:///project.db", echo=True)


class Base(DeclarativeBase):
     pass


class User(Base):
     __tablename__ = "user"
     word: Mapped[str] = mapped_column(String(30), primary_key=True)
     user_id: Mapped[int] = mapped_column(primary_key=True)
     meaning: Mapped[str] = mapped_column(String(30))


Base.metadata.create_all(engine)
