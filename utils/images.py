from io import BytesIO
from PIL import Image as PilImage
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
import os
from traveler.settings import BASE_DIR


def get_tmb_image_uri(self, obj):
        if hasattr(obj, 'avatar') and obj.tmb_avatar:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.tmb_avatar)
        elif hasattr(obj, 'image') and obj.tmb_image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.tmb_image)
        elif hasattr(obj, 'wallpaper') and obj.tmb_wallpaper:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.tmb_wallpaper)  
        return None 

def get_current_img(sender, instance):
    try:
        return sender.objects.get(pk=instance.id).image
    except:
        return ''

def resize_with_aspectratio(main_path, max_width=350, max_height=400):
    size = (max_width, max_height)
    pil_image = PilImage.open(main_path)

    if pil_image.width > max_width or pil_image.height > max_height:
        pil_image.thumbnail(size)
        pil_image.save(main_path)

def crop_image(main_path, crop_width=1920, crop_heigth=640, tmb=False):
    relation = crop_width/crop_heigth
    img = PilImage.open(main_path)
    width, height = img.size
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

def image_processing(img, current_img=None, crop_width=None, crop_height=None, tmb_width=None, tmb_height=None, aspectratio=None):
    if img and "/" not in img:
        if crop_width and crop_height and not aspectratio:
            crop_image(img.path, crop_width, crop_height)
        if crop_width and crop_height and aspectratio:
            resize_with_aspectratio(img.path, crop_width, crop_height)
        if tmb_width and tmb_height:
            make_tmb(img.path, tmb_width, tmb_height)
        if current_img and current_img != img:
            delete_image(current_img)