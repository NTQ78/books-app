from celery_temp.celery_worker import celery_app
from services.cloudinary import upload_image, delete_image
from database.mysql import SessionLocal
from models.book.model import Book
from models.user.model import User
from models.profile.model import Profile


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@celery_app.task
def upload_image_and_update_book(book_id, image_bytes):
    import logging

    logger = logging.getLogger(__name__)
    try:
        url = upload_image(image_bytes)
        db = SessionLocal()
        book = db.query(Book).filter(Book.id == book_id).first()
        if book:
            book.cover_image = url if url else None
            db.commit()
            logger.info(f"Book {book_id} updated with new cover image.")
        else:
            logger.warning(f"Book {book_id} not found.")
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        db.close()


@celery_app.task
def update_profile_image(user_id, image_bytes):
    import logging

    logger = logging.getLogger(__name__)
    db = SessionLocal()
    try:
        profile = db.query(Profile).filter(Profile.profile_id == user_id).first()
        if not profile:
            logger.warning(f"Profile ID: {user_id} not found!")
            return

        old_image = profile.profile_Image
        if old_image:
            delete_image(old_image)
            logger.info(f"Old profile image deleted!")

        url = upload_image(image_bytes)
        profile.profile_Image = url
        db.commit()
        db.refresh(profile)
        logger.info(f"Profile {user_id} updated with new image.")
    except Exception as e:
        logger.error(f"Error updating profile image for user {user_id}: {e}")
    finally:
        db.close()
