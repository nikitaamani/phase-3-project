from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db import conn, cursor




from models.tickets import Ticket
from models.hire import Hire
from models.bus import Buses
from front import PrivateModel, PublicModel,TicketModel


app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=[
    "*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/hire")
def get_cars():
    cars = Hire.find_all()

    return cars


@app.post("/hire")
def save(data: PrivateModel):
    hire = Hire(data.name, data.car_brand, data.image,
                data.hire_fee, data.date_hire)
    hire.save()
    return hire.to_dict()


@app.get("/bus")
def get_buses():
    buses = Buses.find_all_buses()

    return buses


@app.post("/bus")
def save(data: PublicModel):
    bus = Buses(data.name, data.location_from,
                data.location_to, data.passengers, data.price)
   

    return bus.to_dict()


@app.post("/tickets")
async def book_ticket(request: TicketModel):
    try:
        bus = Buses.find_one(request.bus_id)
        if not bus:
            raise HTTPException(status_code=404, detail="Bus not found")
        
        if bus.passengers <= 0:
            raise HTTPException(status_code=400, detail="No available seats")
        
        ticket = Ticket(request.location_from, request.location_to,  request.bus_id)
        ticket.save()

        # Reduce the number of available seats
        cursor.execute("UPDATE buses SET passengers = passengers - 1 WHERE id = ?", (request.bus_id,))
        conn.commit()

        bus = Buses.find_one(request.bus_id)
        
        return {"message": "Ticket booked successfully", "available_seats": bus.passengers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    

    
        

        

       
        
       
    