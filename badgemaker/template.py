import cv2
from PIL import ImageFont, ImageDraw, Image
import os

def fit_text_in_box(font, bounding_box, text):
    x, y, w, h = bounding_box
    best_font_size = 1
    best_num_lines = float('inf')
    best_text_lines = []
    for font_size in range(1, h):
        current_font = ImageFont.truetype(font, font_size)
        draw = ImageDraw.Draw(Image.new('RGB', (1, 1)))
        text_width, text_height = draw.textbbox((0, 0), text, font=current_font)[2:]
        lines = []
        line = ''
        for word in text.split():
            if draw.textbbox((0, 0), line + word, font=current_font)[2] <= w:
                line += word + ' '
            else:
                lines.append(line.strip())
                line = word + ' '
        if line:
            lines.append(line.strip())
        num_lines = len(lines)
        if text_height * num_lines <= h and (num_lines < best_num_lines or (num_lines == best_num_lines and font_size > best_font_size)):
            best_font_size = font_size
            best_num_lines = num_lines
            best_text_lines = lines
    return best_font_size, best_text_lines

def insert_photo(template, photo):
    mask_green = cv2.inRange(template, (0, 180, 0), (100, 255, 100))
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours_green:
        print('No green rectangle found in template. Skipping photo insertion.')
        return template
    green_contour = max(contours_green, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(green_contour)
    height_ratio = h / photo.shape[0]
    width_ratio = w / photo.shape[1]
    scale = max(height_ratio, width_ratio)
    new_width = int(photo.shape[1] * scale)
    new_height = int(photo.shape[0] * scale)
    photo_resized = cv2.resize(photo, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
    offset_x = x + (w - new_width) // 2
    offset_y = y + (h - new_height) // 2
    start_x = offset_x
    start_y = offset_y
    for i in range(new_height):
        for j in range(new_width):
            try:
                if mask_green[start_y + i, start_x + j] == 255:
                    template[start_y + i, start_x + j] = photo_resized[i, j]
            except IndexError:
                continue
    return template


def insert_text(template, text, font_path):
    mask_red = cv2.inRange(template, (0, 0, 250), (5, 5, 255))
    contours_red, tree = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    x, y, w, h = cv2.boundingRect(contours_red[0])
    font_size, lines = fit_text_in_box(font_path, (x, y, w, h), text)
    text = '\n'.join(lines)
    font = ImageFont.truetype(font_path, font_size)
    bg_color = tuple(template[y+h//2, x+w//2])
    text_color = (255, 255, 255) if sum(bg_color) < 383 else (0, 0, 0)
    text_box = Image.new('RGB', (w, h), bg_color)
    draw = ImageDraw.Draw(text_box)
    draw.text((0, 0), text, font=font, fill=text_color)
    text_box = text_box.resize((w, h))
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