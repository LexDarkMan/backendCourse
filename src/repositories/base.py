from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update

class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model, from_attributes=True)

    async def add(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        # print(add_data_stmt.compile(engine, compile_kwargs={"literal_binds": True})) # скомпилировать и распечатать запрос в БД
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        return self.schema.model_validate(model, from_attributes=True)

    async def update(self, data: BaseModel, exclude_unset: bool=False, **filter_by) -> None:
        query = update(self.model).filter_by(**filter_by).values(**data.model_dump(exclude_unset=exclude_unset)) # exclude_unset - исключает из запроса пропущенные (непереданные) параметры
        await self.session.execute(query)

    async def delete(self, **filter_by) -> None:
        query = delete(self.model).filter_by(**filter_by)
        await self.session.execute(query)