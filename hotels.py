from fastapi import Query, Body, APIRouter

from dependencies import PaginationDep
from schemas.hotels import Hotel, HotelPATCH

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
def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None, description="Идентификатор отеля"),
        title: str | None = Query(None, description = "Название отеля"),
        name: str | None = Query(None, description = "Наименование отеля"),
):
    hotels_=[]
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        if name and hotel["name"] != name:
            continue
        hotels_.append(hotel)
    if pagination.page and pagination.per_page:
        return hotels_[(pagination.page - 1) * pagination.per_page : pagination.per_page * pagination.page]
        #return hotels_[(pagination.page - 1) * pagination.per_page:][:pagination.per_page]
    return hotels_

@router.post("", summary="Добавление нового отеля")
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", "value":{
        "title": "Отель Сочи 5 звезд у моря",
        "name": "sochi_u_morya",
    }},
    "2": {"summary": "Дубай", "value":{
        "title": "Дубай 5 звезд оазис",
        "name": "dubai_oazis",
    }},
})
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
    })
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