from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/users", tags=["users"])

USERS = [
    {"id": 1, "name": "Ada"},
    {"id": 2, "name": "Alan"},
]


@router.get("")
def list_users():
    return {"users": USERS}


@router.get("/{user_id}")
def get_user(user_id: int):
    for user in USERS:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")
