from datetime import datetime
from sqlalchemy import BigInteger, ForeignKey, Boolean, String, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncEngine

from config_data.config import load_config, DBSettings


db: DBSettings = load_config().database

DATABASE_URL = f"postgresql+asyncpg://{db.user}:{db.password}@{db.host}/{db.name}"

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger, unique=True)
    created_on: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    feedbacks: Mapped[list["Feedback"]] = relationship('Feedback', back_populates='user', cascade='all, delete-orphan')


class Feedback(Base):
    __tablename__ = 'feedbacks'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    is_bot: Mapped[bool] = mapped_column(Boolean(), default=False)
    tg_nickname: Mapped[str] = mapped_column(String(50))
    name: Mapped[str] = mapped_column(String(50))
    mail: Mapped[str] = mapped_column(String(50))
    phone: Mapped[str] = mapped_column(String(11))
    created_on: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    appeal: Mapped[str] = mapped_column()

    user: Mapped["User"] = relationship('User', back_populates='feedbacks')


class Advantages(Base):
    __tablename__ = 'advantages'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column()
    image_name: Mapped[str] = mapped_column(String(50), nullable=True)


class Contacts(Base):
    __tablename__ = 'contacts'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column()
    image_name: Mapped[str] = mapped_column(String(50), nullable=True)


class Opportunities(Base):
    __tablename__ = 'opportunities'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column()
    image_name: Mapped[str] = mapped_column(String(50), nullable=True)


class Functionalities(Base):
    __tablename__ = 'functionalities'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column()
    image_name: Mapped[str] = mapped_column(String(50), nullable=True)


class Interface(Base):
    __tablename__ = 'interface'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column()
    image_name: Mapped[str] = mapped_column(String(50), nullable=True)


async def config_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
