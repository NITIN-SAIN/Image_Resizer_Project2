from pathlib import Path
from uuid import uuid4

from PIL import Image

from app.services.s3_service import upload_file


BASE_UPLOAD_DIR = Path("uploads")

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def resize_image(
    input_file,
    username,
    width=800,
    height=800
):
    original_filename = Path(input_file.filename).name

    if not original_filename:
        raise ValueError("No filename provided.")

    extension = Path(original_filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            "Unsupported image format. Allowed formats: JPG, JPEG, PNG."
        )

    unique_name = f"{uuid4().hex}{extension}"

    user_dir = BASE_UPLOAD_DIR / username

    original_dir = user_dir / "original"
    resized_dir = user_dir / "resized"

    original_dir.mkdir(parents=True, exist_ok=True)
    resized_dir.mkdir(parents=True, exist_ok=True)

    original_path = original_dir / unique_name
    resized_path = resized_dir / unique_name

    # Save original image temporarily
    input_file.save(original_path)

    # Resize image
    with Image.open(original_path) as image:
        image.thumbnail((width, height))
        image.save(resized_path)

    # S3 object paths
    original_s3_key = f"users/{username}/original/{unique_name}"
    resized_s3_key = f"users/{username}/resized/{unique_name}"

    # Upload both images to S3
    upload_file(original_path, original_s3_key)
    upload_file(resized_path, resized_s3_key)

    return {
        "original": original_s3_key,
        "resized": resized_s3_key
    }
