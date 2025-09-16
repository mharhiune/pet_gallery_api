def serialize_pet(pet):
    return {
        "id": str(pet["_id"]),
        "image_url": pet["image_url"],
        "animal_type": pet["animal_type"],
        "user_comment": pet["user_comment"],
        "votes": pet.get("votes", {"up": 0, "down": 0}),
    }