from src.models.comment import CommentOut


class CommentConverter:
    def to_document(self, model: CommentOut):
        return model.model_dump(by_alias=True)

    
    def from_document(self, document: dict):
        return CommentOut(**document)

