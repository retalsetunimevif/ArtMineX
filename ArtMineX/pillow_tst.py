from random import randint
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile


def make_picture():
    """Function: Generates a random image and returns it as an InMemoryUploadedFile."""
    image = Image.new(mode='RGB', size=(450, 450),
                      color=(randint(0, 255),
                             randint(0, 255),
                             randint(0, 255)))
    image_buffer = BytesIO()
    image.save(image_buffer, format='JPEG')
    image_data = image_buffer.getvalue()
    image_file = SimpleUploadedFile(
        'example.jpg',
        image_data,
        content_type='image/jpeg'
    )
    return image_file
