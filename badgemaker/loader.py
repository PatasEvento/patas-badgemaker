import pandas as pd
import tkinter
from tkinter import filedialog

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

def loadImagesFromColumn(column):
    pass