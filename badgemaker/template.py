import cv2
from PIL import ImageFont, ImageDraw, Image
import os

def insert_photo(template, photo):
    mask_green = cv2.inRange(template, (0, 250, 0), (5, 255, 5))
    contours_green, tree = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    x, y, w, h = cv2.boundingRect(contours_green[0])
    photo = cv2.resize(photo, (w, h), interpolation=cv2.INTER_CUBIC)
    mask_green_copy = mask_green[y:y+h, x:x+w]
    for i in range(y, y+h):
        for j in range(x, x+w):
            if mask_green_copy[i-y, j-x] == 255:
                template[i, j] = photo[i-y, j-x]
    return template

def insert_text(template, text, font_path):
    mask_red = cv2.inRange(template, (0, 0, 250), (5, 5, 255))
    contours_red, tree = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    x, y, w, h = cv2.boundingRect(contours_red[0])
    font_size = h / len(text.split(' '))  # This is a simple estimation
    font = ImageFont.truetype(font_path, font_size)
    text_box = Image.new('RGB', (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(text_box)
    bg_color = template[y+h//2, x+w//2]
    text_color = (255, 255, 255) if sum(bg_color) < 383 else (0, 0, 0)
    draw.text((0, 0), text, font=font, fill=text_color)
    text_box = text_box.resize((w, h))
    mask_red_copy = mask_red[y:y+h, x:x+w]
    for i in range(y, y+h):
        for j in range(x, x+w):
            if mask_red_copy[i-y, j-x] == 255:
                template[i, j] = bg_color
    template[y:y+h, x:x+w] = text_box
    return template

def generate_badge(data, photos, text_column, template_column, font_filename):
    for file in os.listdir('output'):
        if file != '.gitkeep':
            os.remove(f'output/{file}')
    for index, row in data.iterrows():
        filename = row[template_column].strip().lower().replace(' ', '_')
        try:
            template = cv2.imread(f'templates/{filename}.png')
        except FileNotFoundError:
            template = cv2.imread(f'templates/{filename}.jpg')
        template = insert_photo(template, photos[index])
        template = insert_text(template, row[text_column], f'fonts/{font_filename}')
        cv2.imwrite(f'output/{index}.png', template)