from fastapi import Query, Body, APIRouter

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubay"},
]



@router.get(
    "",
    summary="Получение списка отелей",
    description="Запрос на получение списка отелей согласно фильтру"
)
def get_hotels(
        id: int | None = Query(None, description="Идентификатор отеля"),
        title: str | None = Query(None, description = "Название отеля"),
        name: str | None = Query(None, description = "Наименование отеля")
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
    return hotels_

@router.post("", summary="Добавление нового отеля")
def create_hotel(
        title: str = Body(embed = True),
        name: str = Body(embed = True),
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title,
        "name": name
    })
    return {"status": "ok"}

@router.delete("/{hotel_id}", summary="Удаление отеля")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "ok"}

@router.put("/{hotel_id}", summary="Изменение отеля")
def update_hotel(
        hotel_id: int,
        title: str = Body(embed = True),
        name: str = Body(embed = True),
):
    global hotels
    #hotels = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
    return {"status": "ok"}

@router.patch("/hotels/{hotel_id}", summary="Частичное изменение данных об отеле")
def update_hotel(
        hotel_id: int,
        title: str | None = Body(None, embed = True),
        name: str | None = Body(None, embed = True),
):
    global hotels
    # hotels = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title:
                hotel["title"] = title
            if name:
                hotel["name"] = name
    return {"status": "ok"}