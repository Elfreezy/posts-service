from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from app.settings import settings

engine = create_async_engine(url=settings.DATABASE_URL, echo=True)
sessionmaker_local = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
