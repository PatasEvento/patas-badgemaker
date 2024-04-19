import menu
import pandas as pd
from PIL import Image
import requests
import tkinter
from tkinter import filedialog
import re
url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
data = {}
images = {}

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