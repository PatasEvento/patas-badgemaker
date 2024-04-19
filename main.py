import menu
import sys
sys.path.insert(0, 'badgemaker')
import loader

def notifyNoData():
    submenu = menu.Menu(title="No Data File Loaded!")
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
        options.append((column, options.append((column, lambda col=column: loader.loadImagesFromColumn(col, submenu)))))
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
                     options=[('Load Data', loadData), ('Insert Data', insertData), ('Load Images', loadImages), ('Generate Badges', genBadgesOption), ('Exit', exit)])
mainmenu.open()