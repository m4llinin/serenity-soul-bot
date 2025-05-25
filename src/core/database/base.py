from abc import (
    ABC,
    abstractmethod,
)
from datetime import datetime
from typing import Any

from loguru import logger
from sqlalchemy import (
    insert,
    select,
    update,
    delete,
    func,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), server_onupdate=func.now()
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}: {' '.join([f'{k}={v}' for k, v in self.to_dict().items()])}>"


class RepositoryABC(ABC):
    @abstractmethod
    async def get_one(self, data: dict[str, Any]) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, data: dict[str, Any]) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def insert(self, data: dict[str, Any]) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self,
        filters: dict[str, Any],
        data: dict[str, Any],
    ) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, data: dict[str, Any]) -> Any:
        raise NotImplementedError


class SqlAlchemyRepository(RepositoryABC):
    _model = None

    def __init__(self, session: AsyncSession):
        self._session = session

    async def insert(self, data: dict[str, Any]) -> Any:
        logger.debug(
            "Query for database from {model} with params: {params}",
            model=self._model.__tablename__,
            params=data,
        )
        stmt = insert(self._model).values(**data).returning(self._model)
        res = await self._session.execute(stmt)
        return res.scalar_one()

    async def get_one(self, filters: dict[str, Any]) -> Any | None:
        logger.debug(
            "Query for database from {model} with params: {params}",
            model=self._model.__tablename__,
            params=filters,
        )
        stmt = select(self._model).filter_by(**filters)
        res = await self._session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_all(self, filters: dict[str, Any]) -> list[Any]:
        logger.debug(
            "Query for database from {model} with params: {params}",
            model=self._model.__tablename__,
            params=filters,
        )
        stmt = select(self._model).filter_by(**filters)
        res = await self._session.execute(stmt)
        return [r[0] for r in res.all()]

    async def update(
        self,
        filters: dict[str, Any],
        data: dict[str, Any],
    ) -> Any | None:
        logger.debug(
            "Query for database from {model} with filters: {filters} and params: {params}",
            model=self._model.__tablename__,
            filters=filters,
            params=data,
        )
        stmt = (
            update(self._model)
            .values(**data)
            .filter_by(**filters)
            .returning(self._model)
        )
        res = await self._session.execute(stmt)
        return res.scalar_one_or_none()

    async def delete(self, filters: dict[str, Any]) -> Any | None:
        logger.debug(
            "Query for database from {model} with params: {params}",
            model=self._model.__tablename__,
            params=filters,
        )
        stmt = delete(self._model).filter_by(**filters).returning(self._model)
        res = await self._session.execute(stmt)
        return res.scalar_one_or_none()
