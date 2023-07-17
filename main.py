from pathlib import Path
import createImages
import cam2imageGUI as GUI
import fileHandling


##### General Settings #####
adress = None#"http://127.0.0.1:5500/"  # The (web/lokal) adress where CAMEL is deployed (-> check the adress bar in your browser. Adjust if needed). If chosen by GUI, this is set to None 
inputFileFormats = [".json", ".txt"]  # Allowed file formats for CAM-files


##### Main functions #####

### Creating SVGs from CAM-files ###
def cams2Images():
    try:
        if type(adress) is str and adress is not ("" or None):  # If The (web/lokal) adress where CAMEL is deployed is not already defined above 
            print("adress where CAMEL is deployed has been pre-defined in in main.py")
            pass
        else:
            adress = GUI.enterAdress()  # Open GUI for entering the (web/lokal) adress where CAMEL is deployed (-> check the adress bar in your browser.
    except:
        adress = GUI.enterAdress()  # Open GUI for entering the (web/lokal) adress where CAMEL is deployed (-> check the adress bar in your browser.

    ### Coosing folder of CAMs (input) and folder where images (SVGs) of CAMs shall be saved, both by GUIs ###
    try:
        files = fileHandling.inputFiles(patterns=inputFileFormats)
        saveDir = fileHandling.outputFolder()

        ### opening a browser and saving SVGs of all CAMs contained in the folder specified above ###
        browser = createImages.initBrowser(adress=adress, pathOut=saveDir)  # Initializing a browser window
        createImages.createSVGs(driver=browser, filesIn=files)  # Opening CAMEL in the browser Window, Loading CAMs into CAMEL ans saving a SVG of each CAM 

        browser.quit()  # Closing browser window(s) opened by the program
    except:
        print("There was a problem with getting the vector graphics. Returning to the main menue")
    

### Converting SVG files to PNG ###
def svgs2pngs():
    try:
        svgFileList = GUI.chooseFiles(msg=GUI.messages["msgLoadingSVGs"], fileTypes=[("SVG", ".svg")])
        svgFilePathNameDict = fileHandling.prepSVGsForConversion(svgFileList)
        saveDirConversion = GUI.chooseSavingFolder()
        createImages.convertSVGs(inputSVGsDict=svgFilePathNameDict, pathOut=saveDirConversion)
        print("Converted images saved to: ", str(saveDirConversion))
    except:
        print("There was an error at SVG conversion")


### Adding a prefix to chosen files ###
def prefix2Filenames():
    try:
        files = None  # Clearing the variable, to be sure
        files = GUI.chooseFiles(msg=GUI.messages["msgChooseFilesForRenamingPrefix"])
        prefix = GUI.enterPrefix()
        for file in files:
            fileHandling.addPrefix(file, prefix)
        GUI.completion("Adding prefix to 1 file") if len(files) == 1 else GUI.completion("Adding prefix to " + str(len(files)) + " files")
    except:
        print("There was an error at adding a prefix")



###############################
##### Running the program #####
###############################
while True:
    operation = GUI.decideWhichOperation()  # Show main menue for choosing which main function to perform

    if operation == "Exit":  # Exit the Program
        exit()

    elif operation == "btnGetSVGs":  # If user chooses do get vector graphics (SVGs) from CAM-files
        cams2Images()  # Creating SVGs from CAM-files 

    elif operation == "btnConvertSVG2PNG":  # If user chooses to convert images
        svgs2pngs()  # Converting SVG files to PNG
        
    elif operation == "btnAddPreffix":
        prefix2Filenames()  # Adding a prefix to chosen files
