import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1.users import router as user_router
from src.api.v1.books import router as books_router
from src.api.v1.comments import router as comments_router
from src.api.v1.chapters import router as chapters_router
from src.api.v1.reports import router as reports_router
from src.api.v1.ratings import router as ratings_router
from src.api.v1.favorites import router as favorites_router


app = FastAPI(
    title="Books API",
    summary="API for SFEDU diploma project"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(user_router)
app.include_router(books_router)
app.include_router(comments_router)
app.include_router(chapters_router)
app.include_router(reports_router)
app.include_router(ratings_router)
app.include_router(favorites_router)


@app.get("/", tags=["general"])
async def health_check():
    return {"msg": "Healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
