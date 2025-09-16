from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bson import ObjectId
from db import pets_collection
# import os

# --- FastAPI App ---
app = FastAPI(title="😸🐶 RHIUNNE'S Pet Gallery API")

# --- Models ---
class FavouritePets(BaseModel):
    image_url: str
    animal_type: str
    user_comment: str

class VotePet(BaseModel):
    vote: str

# --- Utility Function ---
def serialize_pet(pet):
    return {
        "id": str(pet["_id"]),
        "image_url": pet["image_url"],
        "animal_type": pet["animal_type"],
        "user_comment": pet["user_comment"],
        "votes": pet["votes"]
    }

# --- Endpoints ---

@app.get("/pets/random")
def get_random_pet(animal_type: str = "dog"):
    if animal_type == "dog":
        res = requests.get("https://dog.ceo/api/breeds/image/random")
        image_url = res.json()["message"]
    else:
        res = requests.get("https://api.thecatapi.com/v1/images/search")
        image_url = res.json()[0]["url"]

    return {"animal_type": animal_type, "image_url": image_url}

@app.post("/pets/favorites")
def add_favorite(pet: FavouritePets):
    pet_data = pet.dict()
    pet_data["votes"] = {"up": 0, "down": 0}
    result = pets_collection.insert_one(pet_data)
    return {"id": str(result.inserted_id), **pet_data}

@app.get("/pets/favorites")
def list_favorites():
    pets = list(pets_collection.find())
    return {"favorites": [serialize_pet(p) for p in pets]}

@app.post("/pets/favorites/{pet_id}/vote")
def vote_pet(pet_id: str, vote: VotePet):
    if vote.vote not in ["up", "down"]:
        return {"error": "vote must be 'up' or 'down'"}

    try:
        result = pets_collection.update_one(
            {"_id": ObjectId(pet_id)},
            {"$inc": {f"votes.{vote.vote}": 1}}
        )

        if result.matched_count == 0:
            return {"error": "Pet not found"}

        pet = pets_collection.find_one({"_id": ObjectId(pet_id)})
        return serialize_pet(pet)

    except Exception as e:
        return {"error": str(e)}
