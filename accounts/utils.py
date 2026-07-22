
import io
from PIL import Image
from django.core.files.base import ContentFile



def process_profile_picture(uploaded_file, size=500):
    """
    Center-crop the uploaded image to a square (using the shortest side),
    resize it to `size`x`size`, and return a Django ContentFile ready to
    assign directly to an ImageField.
    """
    image = Image.open(uploaded_file)

    # Flatten transparency (PNGs) onto a white background instead of
    # letting it turn black when we convert to RGB for JPEG output.
    if image.mode in ("RGBA", "P"):
        background = Image.new("RGB", image.size, (255, 255, 255))
        image = image.convert("RGBA")
        background.paste(image, mask=image.split()[-1])
        image = background
    else:
        image = image.convert("RGB")

    width, height = image.size
    shortest_side = min(width, height)

    left = (width - shortest_side) // 2
    top = (height - shortest_side) // 2
    right = left + shortest_side
    bottom = top + shortest_side

    image = image.crop((left, top, right, bottom))
    image = image.resize((size, size), Image.LANCZOS)

    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=90)
    buffer.seek(0)

    original_name = getattr(uploaded_file, "name", "profile.jpg")
    base_name = original_name.rsplit(".", 1)[0]
    new_name = f"{base_name}_cropped.jpg"

    return ContentFile(buffer.read(), name=new_name)
