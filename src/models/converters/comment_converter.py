from src.models.comment import CommentIn, CommentOut


class CommentConverter:
    def to_document(self, model: CommentIn | CommentOut):
        return model.model_dump()

    
    def from_document(self, document: dict):
        return CommentOut(**document)

