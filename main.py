import menu
import sys
sys.path.insert(0, 'badgemaker')
import loader
data = None
images = None

def notifyNoData():
    submenu = menu.Menu(title="No Data File Loaded!")
    submenu.set_options([('Back', submenu.close)])
    submenu.open()

def loadData():
    global data
    data = loader.load_inputfile()
    submenu = menu.Menu(title=f"{data}\n\nData Loaded Successfully!")
    submenu.set_options([('Back', submenu.close)])
    submenu.open()

def insertData():
    global data
    if data is None:
        notifyNoData()
        return
    newrow = {}
    for column in data.columns:
        print(f"Enter a value for {column}:")
        value = input()
        newrow[column] = value
    data.loc[len(data)] = newrow
    submenu = menu.Menu(title=f"{data}\n\nNew row inserted successfully!\nIf using a local image, don't forget to add it to the 'images' folder.")
    submenu.set_options([('Back', submenu.close)])
    submenu.open()

def genBadgesOption():
    if data is None:
        notifyNoData()
        return
    if images is None:
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
                     options=[('Load Data', loadData), ('Insert Data', insertData), ('Generate Badges', genBadgesOption), ('Exit', exit)])
mainmenu.open()