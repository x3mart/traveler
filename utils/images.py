from io import BytesIO
from PIL import Image as PilImage
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
import os
from traveler.settings import BASE_DIR


def create_avatar(image, max_width=350, max_height=400):
    size = (max_width, max_height)
    memory_image = BytesIO(image.read())
    pil_image = PilImage.open(memory_image)
    img_format = os.path.splitext(image.name)[1][1:].upper()
    img_format = 'JPEG' if img_format == 'JPG' else img_format

    if pil_image.width > max_width or pil_image.height > max_height:
        pil_image.thumbnail(size)

    new_image = BytesIO()
    pil_image.save(new_image, format=img_format)

    new_image = ContentFile(new_image.getvalue())
    return InMemoryUploadedFile(new_image, None, image.name, image.content_type, None, None)

def crop_image(main_path, crop_width=1920, crop_heigth=640, tmb=False):
    relation = crop_width/crop_heigth
    img = PilImage.open(main_path)
    width, height = img.size
    # if width/height > 1:
    #     crop_width = crop_heigth
    #     crop_heigth = int(crop_width * relation)
    #     relation = 1/relation
    if round(height * relation) > width:
        h = round(width / relation)
        left = 0
        top = (height - h) / 2
        right = width
        bottom = top + h
        cropped_img = img.crop((left, top, right, bottom))
    elif round(height * relation) < width:
        w = round(height * relation)
        left = (width - w) / 2
        top = 0
        right = (left + w)
        bottom = height
        cropped_img = img.crop((left, top, right, bottom))
    else:
        cropped_img = img
    
    resized_img = cropped_img.resize((crop_width, crop_heigth))
    resized_img = resized_img.convert('RGB')
    if tmb:
        return resized_img
    resized_img.save(main_path) 


def make_tmb(main_path, width=200, height=200):
    tmb = crop_image(main_path, width, height, True)
    tmb_path = get_tmb_path(main_path)
    tmb_path = f'{BASE_DIR}/{tmb_path}'
    tmb.save(tmb_path)

def get_tmb_path(main_path):
    path, extension = os.path.splitext(main_path)
    path = path.split('/')
    filename = path.pop()
    path.append('tmb__' + filename)
    tmb_path = '/'.join(path) + extension
    tmb_path = tmb_path.replace(str(BASE_DIR), '')
    return tmb_path

def delete_image(image):
    storage = image.storage
    if storage.exists(image.name):
        storage.delete(image.name)
    delete_tmb(image)

def delete_tmb(image):
    tmb_path = get_tmb_path(image.path)
    if os.path.exists(f'{BASE_DIR}{tmb_path}'):
            os.remove(f'{BASE_DIR}{tmb_path}')

def image_processing(img, current_img=None, crop_width=1067, crop_height=800, tmb_width=350, tmb_height=270):
    if img and "/" not in img:
        crop_image(img.path, crop_width, crop_height)
        make_tmb(img.path, tmb_width, tmb_height)
        if current_img and current_img != img:
            delete_image(current_img)