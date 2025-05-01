from database.mysql import Base
from models.user.user_model import User
from models.book.book_model import Book
from models.profile.profile_model import Profile


def create_all_tables(engine):
    Base.metadata.create_all(bind=engine)
