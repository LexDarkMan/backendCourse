from fastapi import FastAPI, Query, Body
import uvicorn

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubay"},
]

@app.get("/hotels")
def get_hotels(
        id: int | None = Query(None, description="Идентификатор отеля 2"),
        title: str | None = Query(None, description = "Название отеля")
):
    hotels_=[]
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_

@app.post("/hotels")
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

@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "ok"}

@app.put("/hotels/{hotel_id}")
def update_hotel(
        hotel_id: int,
        title: str = Body(embed = True),
        name: str = Body(embed = True),
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
    return {"status": "ok"}

@app.patch("/hotels/{hotel_id}")
def update_hotel(
        hotel_id: int,
        title: str | None = Body(None, embed = True), #Query(None, description = "Название отеля"),
        name: str | None = Body(None, embed = True), #Query(None, description = "Наименование отеля"),
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title:
                hotel["title"] = title
            if name:
                hotel["name"] = name
    return {"status": "ok"}

if __name__ == "__main__":
  uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)