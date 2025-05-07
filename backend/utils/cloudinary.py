import cloudinary
import cloudinary.uploader

from dotenv import load_dotenv
import os

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)


def upload_image(image_bytes):
    try:
        result = cloudinary.uploader.upload(
            image_bytes,
            folder="Books_Project",
            transformation=[
                {"width": 800, "height": 800, "crop": "limit"},
                {"quality": "auto:good"},
                {"fetch_format": "auto"},
            ],
            resource_type="image",
        )

        # Optimize the image for web
        optimized_image_url = cloudinary.CloudinaryImage(result["public_id"]).build_url(
            transformation=[
                {"width": 800, "height": 800, "crop": "limit"},
                {"quality": "auto"},
                {"fetch_format": "auto"},
            ]
        )

        return optimized_image_url

    except Exception as e:
        print(f"Error uploading image: {e}")
        return None


def delete_image(cloudinary_url):
    try:
        public_id = extract_public_id(cloudinary_url)
        print(f"public_id: {public_id}")
        if not public_id:
            return False
        response = cloudinary.uploader.destroy(public_id)

        return response["result"] == "ok"

    except Exception as e:
        print(f"Error deleting image: {e}")
        return False


def extract_public_id(cloudinary_url):

    if not cloudinary_url or "cloudinary.com" not in cloudinary_url:
        return None

    parts = cloudinary_url.split("/v1/")
    if len(parts) < 2:
        return None

    return parts[1]
