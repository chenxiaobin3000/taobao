from pathlib import Path

from django.conf import settings


IMAGE_ROOT = Path(settings.BASE_DIR) / 'static' / 'good_images'
IMAGE_URL = '/static/good_images'
IMAGE_EXTS = ['.jpg', '.jpeg', '.png', '.webp']


def get_good_image_url(shop_id, origin):
    path = find_good_image_path(shop_id, origin)
    if not path:
        return ''
    if path.parent.name == str(shop_id):
        return IMAGE_URL + '/' + str(shop_id) + '/' + path.name
    return IMAGE_URL + '/' + path.name


def find_good_image_path(shop_id, origin):
    origin = str(origin or '').strip()
    if not origin:
        return None
    for folder in [IMAGE_ROOT / str(shop_id), IMAGE_ROOT]:
        if not folder.exists():
            continue
        for ext in IMAGE_EXTS:
            path = folder / (origin + ext)
            if path.exists():
                return path
    return None
