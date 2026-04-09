from fastapi import Query, Body, APIRouter

from database import async_session_maker
from repositories.hotels import HotelsRepository
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
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=(pagination.page - 1) * per_page
        )

@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)
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
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    return {"status": "ok", "data": hotel}

@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "ok"}

@router.put("/{hotel_id}", summary="Изменение отеля")
async def update_hotel(hotel_id: int, hotel_data: Hotel):
    # global hotels
    # #hotels = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    # for hotel in hotels:
    #     if hotel["id"] == hotel_id:
    #         hotel["title"] = hotel_data.title
    #         hotel["name"] = hotel_data.name
    async with async_session_maker() as session:
        await HotelsRepository(session).update(hotel_data, id=hotel_id)
        await session.commit()
    return {"status": "ok"}

@router.patch("/hotels/{hotel_id}", summary="Частичное изменение данных об отеле")
async def update_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH
):
    # global hotels
    # # hotels = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    # for hotel in hotels:
    #     if hotel["id"] == hotel_id:
    #         if hotel_data.title:
    #             hotel["title"] = hotel_data.title
    #         if hotel_data.name:
    #             hotel["name"] = hotel_data.name
    async with async_session_maker() as session:
        await HotelsRepository(session).update(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()
    return {"status": "ok"}