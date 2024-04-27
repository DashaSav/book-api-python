from src.models.user import UserInDB


class UserConverter:
    def to_document(self, model: UserInDB):
        return model.model_dump(by_alias=True)

    
    def from_document(self, document: dict):
        return UserInDB(**document)

