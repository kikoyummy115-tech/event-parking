import cloudinary
import cloudinary.uploader
import os

from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

result = cloudinary.uploader.upload(
    "./test.jpg",
    folder="test_upload"
)

print("UPLOAD SUCCESS!")
print(result["secure_url"])