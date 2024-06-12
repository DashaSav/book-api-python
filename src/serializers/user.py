from src.models.user import UserInDB, UserOut


def to_user_out(db_user) -> UserOut:
    return UserOut(_id=str(db_user["_id"]), name=db_user["name"], email=db_user["email"])


def to_db_user(db_user) -> UserInDB:
    return UserInDB(_id=str(db_user["_id"]), name=db_user["name"], email=db_user["email"], hash_pass=db_user["password"])
