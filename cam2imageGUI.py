import PySimpleGUI as sg


### Messages (dictionary) ###
messages = {
    "msgLoadingFolder": """Select Folder that contains all CAM-files.
        -> CAM-files can be contained in sub-folders.
        -> Each CAM must be saved as a separate (json/txt) file.""",

    "msgLoadingSVGs": """Select SVG files that should be converted to png format""",

    "msgSavingFolder": """Select Folder where results should be saved.
        -> Please mind that only folders (not the files they may contain) are shown on this screen, so make sure you do not overwrite existing files""",

    "msgEnterAdress": """Please enter the exact adress where CAMEL is deployed with researcher buttons (the variable "ShowResearcherButtons" must be set to "true" in the respective config file).
        -> This might be a web-adress (like e.g., https://weblab.uni-xyz.edu/publix/123...) if deployed on a web server or a local adress (like e.g., http://123.0.0.1:5500/), if you are running CAMEL locally on your machine""",

    "msgDecideCAMs2SVG": """Do you want to create vector graphics (SVGs) from CAM-files?""",

    "msgDecideSVGsConversion": """Do you want to convert SVG vector graphics (like the CAM-graphics) into PNG formate?"""
}



### Error Windows ###

def missingPath():
    layout = [[sg.Text("Path not propperly chosen")], [sg.Button("OK")]]
    window = sg.Window("Error", layout)  # Create the window

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if event == "OK" or event == sg.WIN_CLOSED:
            break

    window.close()


def invalidFolder():
    layout = [[sg.Text("The folder you specified does not exist/is not valid!")], [sg.Button("OK")]]  
    window = sg.Window("Error", layout)# Create the window

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if event == "OK" or event == sg.WIN_CLOSED:
            break

    window.close()


def MissingInput():
    layout = [[sg.Text("You entered no input!")], [sg.Button("OK")]]
    window = sg.Window("Error", layout)  # Create the window

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if event == "OK" or event == sg.WIN_CLOSED:
            break

    window.close()


def chooseFiles(fileTypes=None, msg=messages["msgLoadingSVGs"]):
    fileTypes = ("Any type", "*") if fileTypes == None else tuple([("Any type", "*"), *fileTypes])
    files = sg.popup_get_file(msg, multiple_files=True, file_types=(fileTypes), title="Select files")
    print(files.split(';'))
    if files == "" or None:
        missingPath()
        chooseFiles(fileTypes=fileTypes)
    else:
        return files.split(';')


### Yes/No decisions ###

def decideCAMs2SVG():
    layout = [[sg.Text((messages["msgDecideCAMs2SVG"]))], 
        [sg.Button("Yes"), sg.Button("No")],] 
    window = sg.Window("Convert images?", layout) # Create the window

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if (event == "Yes") or (event == "No") or (event == sg.WIN_CLOSED):
            break
    window.close()
    if event == "Yes":
        return True
    else:
        return False


def decideImageConversion():
    layout = [[sg.Text((messages["msgDecideSVGsConversion"]))], 
        [sg.Button("Yes"), sg.Button("No")],] 
    window = sg.Window("Convert images?", layout) # Create the window

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if (event == "Yes") or (event == "No") or (event == sg.WIN_CLOSED):
            break
    window.close()
    if event == "Yes":
        return True
    else:
        return False


### Text-input windows ###

def enterAdress():
    adress = sg.popup_get_text(messages["msgEnterAdress"], title="Enter column-names")
    if adress == "" or None:
        MissingInput()
        enterAdress()
    else:
        print("The chosen adress where CAMEL is deployed is: " + str(adress))
        return str(adress)


### Folder/File selection windows ###

def chooseLoadingFolder():
    msg = messages["msgLoadingFolder"]
    folder = sg.popup_get_folder(msg, title="Loading all from folder")
    if folder == "" or None:
        missingPath()
        chooseLoadingFolder()
    else:
        print(folder)
        return folder


def chooseSavingFolder():
    folder = sg.popup_get_folder(messages["msgSavingFolder"], title="Saving to folder")
    if folder == "" or None:
        missingPath()
        chooseSavingFolder()
    else:
        print(folder)
        return folder




