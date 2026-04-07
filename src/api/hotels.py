from fastapi import Query, Body, APIRouter

from sqlalchemy import insert, select, func

from database import async_session_maker, engine
from models.hotels import HotelsOrm
from src.api.dependencies import PaginationDep
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Сочи", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubay"},
    {"id": 3, "title": "Мальдивы", "name": "maldiv"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
    {"id": 8, "title": "Кипр", "name": "cyprus"},
]

@router.get(
    "",
    summary="Получение списка отелей",
    description="Запрос на получение списка отелей согласно фильтру"
)
async def get_hotels(
        pagination: PaginationDep,
        #id: int | None = Query(None, description="Идентификатор отеля"),
        title: str | None = Query(None, description = "Название отеля"),
        location: str | None = Query(None, description = "Адрес отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower())) # like(f"%{location.strip().lower()}%"))
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower())) # like(f"%{title.strip().lower()}%"))
        query = (
            query
            .limit(per_page)
            .offset((pagination.page - 1) * per_page)
        )
        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels
    # if pagination.page and pagination.per_page:
    #     return hotels_[(pagination.page - 1) * pagination.per_page : pagination.per_page * pagination.page]
    #     #return hotels_[(pagination.page - 1) * pagination.per_page:][:pagination.per_page]

@router.post("", summary="Добавление нового отеля")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", "value":{
        "title": "Отель Сочи 5 звезд у моря",
        "location": "Сочи, ул. Моря, 1",
    }},
    "2": {"summary": "Дубай", "value":{
        "title": "Дубай 5 звезд оазис",
        "location": "Дубай, ул. Шейха, 2",
    }},
})
):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        #print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True})) # скомпилировать и распечатать запрос в БД
        await session.execute(add_hotel_stmt)
        await session.commit()
    return {"status": "ok"}

@router.delete("/{hotel_id}", summary="Удаление отеля")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "ok"}

@router.put("/{hotel_id}", summary="Изменение отеля")
def update_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    #hotels = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
    return {"status": "ok"}

@router.patch("/hotels/{hotel_id}", summary="Частичное изменение данных об отеле")
def update_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH
):
    global hotels
    # hotels = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title:
                hotel["title"] = hotel_data.title
            if hotel_data.name:
                hotel["name"] = hotel_data.name
    return {"status": "ok"}