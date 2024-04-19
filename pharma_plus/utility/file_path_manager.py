import os
import uuid
from datetime import datetime


def generate_unique_filename(original_filename):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # use the first 6 characters of a random uuid
    # this ensure no file name collision occurs
    random_string = str(uuid.uuid4().hex)[:6]

    original_name, file_extension = os.path.splitext(original_filename)
    unique_filename = (
        f"{original_name}_saved_at_{timestamp}_{random_string}{file_extension}"
    )

    return unique_filename


def save_image_to_static_folder(img_file, folder_name):
    if img_file and img_file.filename:
        filename = generate_unique_filename(img_file.filename)

        target_directory = os.path.join("pharma_plus", "static", "media", folder_name)
        os.makedirs(target_directory, exist_ok=True)

        file_path = os.path.join(target_directory, filename)
        img_file.save(file_path)

        return filename
    return None
