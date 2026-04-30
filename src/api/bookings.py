from fastapi import APIRouter

from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.api.dependencies import DBDep, UserIdDep

router = APIRouter(prefix="/bookings", tags=["Бронирования"])

@router.get(
    "",
    summary="Получение списка бронирований",
    description="Запрос на получение списка бронирований"
)
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()

@router.get("/me")
async def get_my_bookings(
        db: DBDep,
        user_id: UserIdDep
):
    booking = await db.bookings.get_filtered(user_id=user_id)
    return booking

@router.post("", summary="Добавление нового бронирования")
async def create_booking(
        db: DBDep,
        user_id: UserIdDep,
        booking_data: BookingAddRequest
):
    # получить цену номера
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price: int = room.price
    # создать схему данных BookingAdd
    _booking_data = BookingAdd(user_id=user_id, price=room_price, **booking_data.model_dump())
    # добавить бронирование конкретному пользователю
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "ok", "data": booking}