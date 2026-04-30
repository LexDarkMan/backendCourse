from fastapi import APIRouter, Query, Body

from src.schemas.rooms import RoomAddRequest, RoomPatchRequest, RoomPatch
from src.schemas.rooms import RoomAdd
from src.repositories.rooms import RoomsRepository
from src.database import async_session_maker

router = APIRouter(prefix="/hotels", tags=["Номера"])

@router.get(
    "/{hotel_id}/rooms",
    summary="Получение списка номеров в отеле",
    description="Запрос на получение списка номеров в отеле"
)
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_filtered(hotel_id=hotel_id)

@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение конкретного номера"
)
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)

@router.post("/{hotel_id}/rooms", summary="Добавление нового номера")
async def create_room(hotel_id: int, room_data: RoomAddRequest = Body(openapi_examples={
    "1": {"summary": "стандарт", "value":{
        "title": "Стандарт (Standard, STD)",
        "description": "То что называется «дёшево и сердито»: спальное место, ванная и всё самое необходимое.",
        "price": "50",
        "quantity": "20",
    }},
    "2": {"summary": "улучшенный", "value":{
        "title": "Улучшенный номер (Superior, SUP)",
        "description": "Это стандарт, в котором либо лучше вид из окна, либо недавно делали ремонт. Минимум на 10% дороже.",
        "price": "60",
        "quantity": "15",
    }},
    "3": {"summary": "делюкс", "value":{
        "title": "Делюкс (Deluxe, DLX)",
        "description": "Просторный однокомнатный номер с телевизором, сейфом, мини-холодильником и мини-баром. Свежий ремонт, лучше мебель, уборка каждый день. Дороже стандарта на четверть суммы или вдвое.",
        "price": "100",
        "quantity": "12",
    }},
    "4": {"summary": "семейный", "value": {
        "title": "Семейный (Family, или Family Studio)",
        "description": "Обычно состоит минимум из двух комнат, рассчитан на семью с несколькими детьми. Обстановка — как в стандарте, улучшенном номере или делюксе.",
        "price": "150",
        "quantity": "10",
    }},
    "5": {"summary": "апартаменты", "value": {
        "title": "Апартаменты (APT)",
        "description": "Несколько спален с кухней. Отличается от Family тем, что рассчитан на компанию друзей.",
        "price": "200",
        "quantity": "8",
    }},
    "6": {"summary": "полулюкс", "value": {
        "title": "Полулюкс (Junior Suite, J.Suite)",
        "description": "Ещё не люкс, но вариант тоже может включать минимум две комнаты — спальню и гостиную. Отличается более дорогой отделкой.",
        "price": "250",
        "quantity": "5",
    }},
    "7": {"summary": "люкс", "value": {
        "title": "Люкс (Suite)",
        "description": "Полный набор: две или три комнаты (со столовой), дорогой интерьер, вид из окна, может быть джакузи, два туалета.",
        "price": "300",
        "quantity": "3",
    }},
    "8": {"summary": "президентский", "value": {
        "title": "Президентский (President, Presidential Suite, Royal Suite)",
        "description": "Самая дорогая категория номеров в гостинице. Несколько спален и ванных комнат, гостиная, кабинет, минимум два балкона. Расположен обычно на верхних этажах, откуда открывается лучший вид на город или море.",
        "price": "500",
        "quantity": "1",
    }},
})
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(_room_data)
        await session.commit()
    return {"status": "ok", "data": room}

@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера")
async def delete_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"status": "ok"}

@router.put("/{hotel_id}/rooms/{room_id}", summary="Изменение номера")
async def update_room(hotel_id: int, room_id: int, room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).update(_room_data, id=room_id)
        await session.commit()
    return {"status": "ok"}

@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное изменение данных о номере")
async def update_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest,
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        await RoomsRepository(session).update(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"status": "ok"}