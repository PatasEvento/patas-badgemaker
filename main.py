import menu
import os
import sys
sys.path.insert(0, 'badgemaker')
import loader
import template

def notifyNoData():
    submenu = menu.Menu(title="No Data File Loaded!")
    submenu.set_options([('Back', submenu.close)])
    submenu.open()

def notifyMissingInfo(info):
    submenu = menu.Menu(title=f"Missing {info} was not set!")
    submenu.set_options([('Back', submenu.close)])
    submenu.open()

def loadData():
    loader.data = loader.load_inputfile()
    submenu = menu.Menu(title=f"{loader.data}\n\nData Loaded Successfully!")
    submenu.set_options([('Back', submenu.close)])
    submenu.open()

def loadImages():
    if not len(loader.data.keys()):
        notifyNoData()
        return
    submenu = menu.Menu(title="Select a column to load images from:")
    options = []
    for column in loader.data.columns:
        options.append((column, lambda col=column: loader.loadImagesFromColumn(col, submenu)))
    submenu.set_options(options)
    submenu.open()

def loadFont():
    submenu = menu.Menu(title="Select a font to use:")
    options = []
    for fontfile in os.listdir('fonts'):
        if fontfile.endswith('.ttf'):
            options.append((fontfile, lambda font=fontfile: loader.set_font_name(font, submenu)))
    submenu.set_options(options)
    submenu.open()

def selectTextColumn():
    if not len(loader.data.keys()):
        notifyNoData()
        return
    submenu = menu.Menu(title="Select a column to use for badge text:")
    options = []
    for column in loader.data.columns:
        options.append((column, lambda col=column: loader.set_text_column(col, submenu)))
    submenu.set_options(options)
    submenu.open()

def selectTemplateColumn():
    if not len(loader.data.keys()):
        notifyNoData()
        return
    submenu = menu.Menu(title="Select a column to use for choosing a template:")
    options = []
    for column in loader.data.columns:
        options.append((column, lambda col=column: loader.set_template_column(col, submenu)))
    submenu.set_options(options)
    submenu.open()

def insertData():
    if not len(loader.data.keys()):
        notifyNoData()
        return
    newrow = {}
    for column in loader.data.columns:
        print(f"Enter a value for {column}:")
        value = input()
        newrow[column] = value
    loader.data.loc[len(loader.data)] = newrow
    submenu = menu.Menu(title=f"{loader.data}\n\nNew row inserted successfully!\nIf using a local image, don't forget to add it to the 'local_images' folder.")
    submenu.set_options([('Back', submenu.close)])
    submenu.open()

def genBadgesOption():
    if not len(loader.data.keys()):
        notifyNoData()
        return
    if not len(loader.text_column):
        notifyMissingInfo("text column")
        return
    if not len(loader.template_column):
        notifyMissingInfo("template column")
        return
    if not len(loader.font_name):
        notifyMissingInfo("font file")
        return
    if not len(loader.images.keys()):
        submenu = menu.Menu(title="No images are loaded, proceed anyway?")
        submenu.set_options([('Yes, only text will be customized', genBadges), ('Go back', submenu.close)])
        submenu.open()

def genBadges():
    submenu = menu.Menu(title="Generating Badges...")
    submenu.open()
    exit()

def exit():
    sys.exit()

mainmenu = menu.Menu(title="Mekhy's BadgeMaker",
                     options=[('Load Data', loadData), ('Insert Data', insertData), 
                              ('Load Images', loadImages), ('Select Text Column', selectTextColumn),
                              ('Select Template Column', selectTemplateColumn), ('Select Font', loadFont),
                              ('Generate Badges', genBadgesOption), 
                              ('Exit', exit)])
mainmenu.open()