from src.models.report import ReportIn, ReportOut


class ReportConverter:
    def to_document(self, model: ReportIn | ReportOut):
        return model.model_dump()

    
    def from_document(self, document: dict):
        return ReportOut(**document)

