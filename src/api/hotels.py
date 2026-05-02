from datetime import date

from fastapi import Query, Body, APIRouter


from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import HotelPatch, HotelAdd

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    "",
    summary="Получение списка отелей",
    description="Запрос на получение списка отелей согласно фильтру"
)
async def get_hotels(
        db: DBDep,
        pagination: PaginationDep,
        title: str | None = Query(None, description = "Название отеля"),
        location: str | None = Query(None, description = "Адрес отеля"),
        date_from: date = Query(example = "2026-05-01"),
        date_to: date = Query(example = "2026-05-10"),
):
    per_page = pagination.per_page or 5
    # return await db.hotels.get_all(
    #     location=location,
    #     title=title,
    #     limit=per_page,
    #     offset=(pagination.page - 1) * per_page
    #     )
    return await db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
        )

@router.get("/{hotel_id}")
async def get_hotel(db: DBDep, hotel_id: int):
    return await db.hotels.get_one_or_none(id=hotel_id)

@router.post("", summary="Добавление нового отеля")
async def create_hotel(db: DBDep, hotel_data: HotelAdd = Body(openapi_examples={
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
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "ok", "data": hotel}

@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(db: DBDep, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "ok"}

@router.put("/{hotel_id}", summary="Изменение отеля")
async def update_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):
    await db.hotels.update(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "ok"}

@router.patch("/{hotel_id}", summary="Частичное изменение данных об отеле")
async def update_hotel(
        db: DBDep,
        hotel_id: int,
        hotel_data: HotelPatch
):
    await db.hotels.update(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": "ok"}