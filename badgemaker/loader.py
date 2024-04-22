import pandas as pd
from PIL import Image
import requests
import tkinter
from tkinter import filedialog
import re
url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
data = {}
images = {}
text_column = ''
template_column = ''
font_name = ''

def load_inputfile():
    tkinter.Tk().withdraw()
    path = filedialog.askopenfilename()
    if path.endswith('.csv'):
        data = pd.read_csv(path)
    elif path.endswith('.xlsx'):
        data = pd.read_excel(path)
    else:
        raise ValueError(f'Unsupported file type: {path}! Only .csv and .xlsx are supported.')
    return data

def loadImagesFromColumn(col, submenu):
    global data, images
    images = {}
    try:
        for index, row in data.iterrows():
            if pd.notna(row[col]):
                print(row[col])
                if re.match(url_regex, row[col]):
                    im = Image.open(requests.get(row[col], stream=True).raw)
                else:
                    im = Image.open(f'local_images/{row[col]}')
                images[index] = im
        submenu.set_title(f"{images}\n\nImages loaded from column '{col}' successfully!")
        submenu.set_options([('Back', submenu.close)])
    except Exception as e:
        submenu.set_title(f"Error loading images: {e}")
        submenu.set_options([('Back', submenu.close)])

def set_text_column(col, submenu):
    global text_column
    text_column = col
    submenu.set_title(f"Text column set to '{col}'")
    submenu.set_options([('Back', submenu.close)])

def set_template_column(col, submenu):
    global template_column
    template_column = col
    submenu.set_title(f"Template column set to '{col}'")
    submenu.set_options([('Back', submenu.close)])

def set_font_name(name, submenu):
    global font_name
    font_name = name
    submenu.set_title(f"Font set to '{name}'")
    submenu.set_options([('Back', submenu.close)])