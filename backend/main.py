from fastapi import FastAPI


from routes.user.route import router as user_router
from routes.book.route import router as book_router
from database.mysql import engine
from models import create_all_tables
from services.exception_handlers import register_exception_handlers

app = FastAPI()
# Register exception handlers
register_exception_handlers(app)
# Auto create all tables in the database
create_all_tables(engine)

# Include the user router
app.include_router(user_router)
app.include_router(book_router)
