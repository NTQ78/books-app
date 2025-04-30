from database.mysql import Base
from models.user.model import User
from models.book.model import Book
from models.profile.model import Profile


def create_all_tables(engine):
    Base.metadata.create_all(bind=engine)
