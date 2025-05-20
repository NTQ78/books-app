from celery_temp.celery_worker import celery_app
from utils.cloudinary import upload_image, delete_image
from database.mysql import SessionLocal
from models.book.book_model import Book
from loguru import logger

# from models.user.user_model import User
from models.profile.profile_model import Profile


def my_sink(message):
    record = message.record
    level = record["level"].name
    color_map = {
        "DEBUG": "\033[94m",  # Blue
        "INFO": "\033[92m",  # Green
        "WARNING": "\033[93m",  # Yellow
        "ERROR": "\033[91m",  # Red
        "CRITICAL": "\033[1;91m",
        "SUCCESS": "\033[92m",  # Green
    }
    reset = "\033[0m"
    colored = f"{color_map.get(level, '')}{record['message']}{reset}"
    print(colored)


logger.remove()
logger.add(my_sink)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@celery_app.task
def upload_image_and_update_book(book_id, image_bytes):
    try:
        url = upload_image(image_bytes)
        db = SessionLocal()
        book = db.query(Book).filter(Book.id == book_id).first()
        if book:
            book.cover_image = url if url else None
            db.commit()
            logger.success(f"Book {book_id} updated with new cover image.")
        else:
            logger.warning(f"Book {book_id} not found.")
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        db.close()


@celery_app.task
def update_profile_image(user_id, image_bytes):
    db = SessionLocal()
    try:
        profile = db.query(Profile).filter(Profile.profile_id == user_id).first()
        if not profile:
            logger.warning(f"Profile ID: {user_id} not found!")
            return

        old_image = profile.profile_Image
        if old_image is not None:
            delete_image(old_image)
            logger.info(f"Old profile image deleted!")

        url = upload_image(image_bytes)
        profile.profile_Image = url
        db.commit()
        db.refresh(profile)
        logger.success(f"Profile {user_id} updated with new image.")
    except Exception as e:
        logger.error(f"Error updating profile image for user {user_id}: {e}")
    finally:
        db.close()
