from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.user.user_route import router as user_router
from routes.book.book_route import router as book_router
from database.mysql import engine
from models import create_all_tables
from middleware.exception_handlers import register_exception_handlers

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register exception handlers
register_exception_handlers(app)
# Auto create all tables in the database
create_all_tables(engine)

# Include the user router
app.include_router(user_router)
app.include_router(book_router)
