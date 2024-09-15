from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI()

# In-memory storage for cars
cars_db = []

# Define the Car model
class Car(BaseModel):
    id: int
    make: str
    model: str
    year: int

# Create: Add a new car
@app.post("/cars/", response_model=Car)
def create_car(car: Car):
    # Check if car with the same ID already exists
    for existing_car in cars_db:
        if existing_car.id == car.id:
            raise HTTPException(status_code=400, detail="Car with this ID already exists")
    cars_db.append(car)
    return car

# Read: Retrieve details of all cars
@app.get("/cars/", response_model=List[Car])
def get_all_cars():
    return cars_db

# Read: Retrieve details of a specific car by ID
@app.get("/cars/{car_id}", response_model=Car)
def get_car_by_id(car_id: int):
    for car in cars_db:
        if car.id == car_id:
            return car
    raise HTTPException(status_code=404, detail="Car not found")

# Update: Modify details of an existing car
@app.put("/cars/{car_id}", response_model=Car)
def update_car(car_id: int, car_update: Car):
    for index, car in enumerate(cars_db):
        if car.id == car_id:
            cars_db[index] = car_update
            return car_update
    raise HTTPException(status_code=404, detail="Car not found")

# Delete: Remove a car from the cars table by ID
@app.delete("/cars/{car_id}", response_model=Car)
def delete_car(car_id: int):
    for index, car in enumerate(cars_db):
        if car.id == car_id:
            deleted_car = cars_db.pop(index)
            return deleted_car
    raise HTTPException(status_code=404, detail="Car not found")
