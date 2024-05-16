from src.models.report import UserReportIn, UserReportOut, BookReportIn, BookReportOut


class UserReportConverter:
    def to_document(self, model: UserReportIn | UserReportOut):
        return model.model_dump()

    
    def from_document(self, document: dict):
        return UserReportOut(**document)


class BookReportConverter:
    def to_document(self, model: BookReportIn | BookReportOut):
        return model.model_dump()

    
    def from_document(self, document: dict):
        return BookReportOut(**document)


