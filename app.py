from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import uuid4, UUID
from datetime import datetime
import motor.motor_asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.ECSE3038

app = FastAPI()

# CORS for the lab tester site
origins = ["https://ecse3038-lab3-tester.netlify.app"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class ProfileIn(BaseModel):
    username: str
    role: str
    color: str

class ProfileOut(ProfileIn):
    id: str
    last_updated: str

class TankIn(BaseModel):
    location: str
    lat: float
    long: float

class TankOut(TankIn):
    id: str

class TankUpdate(BaseModel):
    location: Optional[str] = None
    lat: Optional[float] = None
    long: Optional[float] = None

# Profile Routes
@app.get("/profile", response_model=Optional[ProfileOut])
async def get_profile():
    profile = await db.profile.find_one()
    if profile:
        profile["id"] = str(profile["_id"])
        del profile["_id"]
        return profile
    return {}

@app.post("/profile", response_model=ProfileOut, status_code=201)
async def create_profile(profile: ProfileIn):
    existing = await db.profile.find_one()
    if existing:
        raise HTTPException(status_code=400, detail="Profile already exists")

    profile_data = profile.model_dump()
    profile_data["last_updated"] = datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")
    result = await db.profile.insert_one(profile_data)
    profile_data["id"] = str(result.inserted_id)
    return profile_data

async def update_last_updated():
    await db.profile.update_one({}, {
        "$set": {"last_updated": datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")}
    })

# Tank Routes
@app.get("/tank", response_model=List[TankOut])
async def get_all_tanks():
    tanks = await db.tanks.find().to_list(1000)
    for tank in tanks:
        tank["id"] = str(tank["_id"])
        del tank["_id"]
    return tanks

@app.post("/tank", response_model=TankOut, status_code=201)
async def create_tank(tank: TankIn):
    tank_data = tank.model_dump()
    tank_data["_id"] = str(uuid4())
    await db.tanks.insert_one(tank_data)
    await update_last_updated()
    return {
        "id": tank_data["_id"],
        "location": tank_data["location"],
        "lat": tank_data["lat"],
        "long": tank_data["long"]
    }

@app.patch("/tank/{id}", response_model=TankOut)
async def update_tank(id: str, tank: TankUpdate):
    update_data = {k: v for k, v in tank.model_dump().items() if v is not None}
    result = await db.tanks.find_one_and_update(
        {"_id": id},
        {"$set": update_data},
        return_document=True
    )
    if not result:
        raise HTTPException(status_code=404, detail="Tank not found")
    await update_last_updated()
    result["id"] = result["_id"]
    del result["_id"]
    return result

@app.delete("/tank/{id}", status_code=204)
async def delete_tank(id: str):
    result = await db.tanks.delete_one({"_id": id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Tank not found")
    await update_last_updated()
    return Response(status_code=204)
