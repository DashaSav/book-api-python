class PagingParams:
    def __init__(self, skip: int, limit: int) -> None:
        self.skip = skip
        self.limit = limit


def paging_params(skip: int = 0, limit: int = 100):
    return PagingParams(skip, limit)
