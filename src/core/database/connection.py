from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

from src.core.utils.singleton import singleton


@singleton
class DBConnection:
    def __init__(self, url: str = None) -> None:
        if url is None:
            raise ValueError("URL cannot be None")

        self._engine = create_async_engine(url)
        self._async_sessionmaker = async_sessionmaker(
            self._engine,
            expire_on_commit=False,
        )

    @property
    def async_sessionmaker(self):
        return self._async_sessionmaker
