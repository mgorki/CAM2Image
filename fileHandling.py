
import os
from pathlib import Path
import cam2imageGUI as GUI


### Returns a list of all files in a folder and (recursively) all its subfolders. 
## If a list is given as the pattterns argument only files ending on the pattern will be returned (e.g., only table files of the json, txt, csv, xlsx format if patterns = [".json", ".csv", ".xlsx", ".txt"])
def listFilesInFolder(folderPath: str, patterns = None) -> list:  
    #patterns = [".json", ".csv", ".xlsx", ".txt"]
    filepaths = []
    if not patterns == None:
        for pattern in patterns:
            folder = Path(folderPath) 
            for filename in map(str, list(folder.rglob("*"))): 
                if filename.endswith(pattern):
                    filepaths.append(filename)
    else:
        folder = Path(folderPath) 
        for filename in map(str, list(folder.rglob("*"))): 
            filepaths.append(filename)

    return filepaths   


### Choosing a folder from which all CAM-files are loaded ###
def inputFiles(patterns):
    return listFilesInFolder(folderPath=str(GUI.chooseLoadingFolder()), patterns=patterns)


### Coosing a folder, where resulting images are saved ###
def outputFolder():
    while True:
        saveDir = GUI.chooseSavingFolder()  # The user has to choose where to save the results
        if os.path.isdir(saveDir):  # Checking if chosen folder is valid (if not user has to choose again)
            return str(Path(saveDir))  # Path module is called to make sure formating is correct
        elif saveDir == None:  # This is the case if the user clicks on "Cancel"
            print("Operation canceled. No images are saved. Crashing now.")
            saveDir = "placeholder"
            return saveDir
        else:
            GUI.invalidFolder()
            pass
    
    
def prepSVGsForConversion(filePaths):
    namePathDict = {}
    for filePath in filePaths:
        try:
            namePathDict[Path(filePath).stem] = Path(filePath)
        except Exception as error:
            print("There was an error with ", str(filePath), ": ", str(error))
    
    return namePathDict


def addPrefix(filePath, prefix):
    dirName = os.path.dirname(filePath)
    originalFileName = str(os.path.basename(filePath))
    newFileName = prefix + originalFileName
    newFilePath = os.path.join(dirName, newFileName) 
    os.rename(filePath, newFilePath)

    return originalFileName, newFileName, dirName