from datetime import date

from sqlalchemy import select, func

from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm

def rooms_ids_for_booking(
    date_from,
    date_to,
    hotel_id: int | None = None,
):
    rooms_count = (
        select(
            BookingsOrm.room_id,
            func.count("*").label("rooms_booked"),
        )
        .select_from(BookingsOrm)
        .filter(
            BookingsOrm.date_from <= date_to,
            BookingsOrm.date_to >= date_from
        )
        .group_by(BookingsOrm.room_id)
        .cte(name="rooms_count")
    )

    free_rooms = (
        select(
            RoomsOrm.id.label("room_id"),
            (RoomsOrm.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("rest_rooms")
        )
        .select_from(RoomsOrm)
        .outerjoin(rooms_count, RoomsOrm.id == rooms_count.c.room_id)
        .cte(name="free_rooms")
    )


    rooms_ids_for_hotel = (
        select(RoomsOrm.id)
        .select_from(RoomsOrm)
    )
    if hotel_id is not None:
        rooms_ids_for_hotel = rooms_ids_for_hotel.filter_by(hotel_id=hotel_id)

    rooms_ids_for_hotel = rooms_ids_for_hotel.subquery(name="rooms_ids_for_hotel")


    rooms_ids_to_get = (
        select(free_rooms.c.room_id)
        .select_from(free_rooms)
        .filter(
            free_rooms.c.rest_rooms > 0,
            free_rooms.c.room_id.in_(rooms_ids_for_hotel)
        )
    )

    return rooms_ids_to_get