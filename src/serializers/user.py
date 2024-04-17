from src.models.user import UserOut


def to_user_out(db_user) -> UserOut:
    return UserOut(_id=str(db_user["_id"]), name=db_user["name"], email=db_user["email"])
