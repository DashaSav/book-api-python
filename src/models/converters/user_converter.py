from src.models.user import UserInDB, UserUpdate, UserUpsert


class UserConverter:
    def to_document(self, model: UserUpdate | UserUpsert | UserInDB):
        return model.model_dump()

    
    def from_document(self, document: dict):
        return UserInDB(**document)

