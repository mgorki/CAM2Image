import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import cairosvg 
from lxml import etree
from svgpathtools import svg2paths
#import svg_resize


### Opens Firefox, opens the local or web-adress (adress parameter) in the browser and sets the browsers download path (pathOut parameter)  
def initBrowser(adress, pathOut):
    try:
        ### Browser Settings###
        options = Options()
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.download.dir", pathOut)
        driver = webdriver.Firefox(options=options)  # Using Firefox. Use other browser that is supported by CAMEL if you want
        driver.get(adress)  # Opening CAMEL in the browser

        return driver
    except:
        print("Initializing browser failed! Crashing now,")
        return "fatal error"


### Creates SVGs from CAM files, takes as parameters (1.) the browser where CAMEL is opened and (2.) the CAM files
def createSVGs(driver, filesIn):
    for file in filesIn:
        ### Loading the CAM-file into CAMEL ###
        try:
            upDownButtons = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'hideResearcherButtonsTop')))  # Find the bar with the upload and download button (wait till propperly loaded, timeout=10sec)
            uploadButton = upDownButtons.find_element(by=By.ID, value='fileToLoad')  # Find the 'Upload CAM from file' button 
        except:
            print("Upload button could NOT be found!")

        try:
            uploadButton.send_keys(file)
            print("the file " + str(file) + " was loaded")
        except:
            print("There was an error loading " + str(file))

        ### Saving the vector graphic (svg) file of the CAM ###
        try:
            rightButtons = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'rightButton')))  # Find the bar that contains (among others) the download CAM as picture button (wait till propperly loaded, timeout=10sec)
            pictureButton = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((rightButtons.find_element(by=By.ID, value='saveCAMpicture'))))  # Find the 'Save CAM as picture' button 
        except:
            print("'Save CAM as picture' button could NOT be found!")  

        try:
            pictureButton.click()
        except Exception as error:
            print("there was an error clicking the 'Save CAM as picture' button for the following file: " + str(file) + " The error was" + str(error))


### Converts SVGs to PNGs, takes as parameters (1.) a dict with names and paths of SVG files (2.) the path of the folder where PNGs are saved
def convertSVGs(inputSVGsDict, pathOut):
    for fileName, filePath in inputSVGsDict.items():
        #print(fileName, " from ", filePath)
        try:
            fileOut = os.path.join(str(pathOut), str(str(fileName) + ".png"))
            cairosvg.svg2png(url=str(filePath), write_to=fileOut, dpi=1200, parent_height=1400, parent_width=2400, scale=3)
        except Exception as error: 
            print("There was an error converting ", (fileName), ": ", str(error))
        

"""def get_bbox(svg_file):
    paths, _ = svg2paths(svg_file)
    for i, path in enumerate(paths):
        if i == 0:
            # Initialise the overall min-max with the first path
            xmin, xmax, ymin, ymax = path.bbox()
        else:
            # Expand bounds to match path bounds if needed
            p_xmin, p_xmax, p_ymin, p_ymax = path.bbox()
            xmin = p_xmin if p_xmin < xmin else xmin
            xmax = p_xmax if p_xmax > xmax else xmax
            ymin = p_ymin if p_ymin < ymin else ymin
            ymax = p_ymax if p_ymax > ymax else ymax
    
    return(xmin, xmax, ymin, ymax)"""

def get_bbox(svg_file):
    paths, _ = svg2paths(svg_file)
    xmin = ymin = float("inf")
    xmax = ymax = float("-inf")

    for path in paths:
        p_xmin, p_xmax, p_ymin, p_ymax = path.bbox()
        xmin = min(xmin, p_xmin)
        xmax = max(xmax, p_xmax)
        ymin = min(ymin, p_ymin)
        ymax = max(ymax, p_ymax)

    return xmin, xmax, ymin, ymax

"""
def cropSVGs(inputSVGsDict, pathOut):
    for fileName, filePath in inputSVGsDict.items():
        #print(fileName, " from ", filePath)
        try:
            fileOut = os.path.join(str(pathOut), str(str(fileName) + ".svg"))
            tree = etree.parse(open(filePath, encoding='UTF-8'))
            toRemove = tree.xpath("/svg:svg/svg:rect[@id=\"background\"]",
                namespaces={"svg": "http://www.w3.org/2000/svg"})[0]
            parent = toRemove.getparent()
            parent.remove(toRemove)
            with open(fileOut, "wb") as out:
                out.write(etree.tostring(tree, pretty_print=True))
            bboxCoordinates = get_bbox(fileOut)
            rootElement = tree.getroot()
            '''
            print("TEST1")
            rootElement.set('width', (str(rootElement[1] - rootElement[0]) + "px"))       
            rootElement.set('height', (str(rootElement[3] - rootElement[2]) + "px"))
            print("TEST2")
            print(bboxCoordinates)
            with open(fileOut, "wb") as out:
                out.write(etree.tostring(tree, pretty_print=True))
            '''
        except Exception as error: 
            print("There was an error cropping ", (fileName), ": ", str(error))
"""

def cropSVGs(inputSVGsDict, pathOut):
    ns = {"svg": "http://www.w3.org/2000/svg"}

    for fileName, filePath in inputSVGsDict.items():
        try:
            fileOut = os.path.join(str(pathOut), f"{fileName}.svg")

            # Parse SVG and remove background rect
            tree = etree.parse(open(filePath, encoding="UTF-8"))
            root = tree.getroot()

            # Remove background rect
            background_rects = root.xpath(
                "/svg:svg/svg:rect[@id='background']",
                namespaces=ns
            )
            for r in background_rects:
                r.getparent().remove(r)

            # Save temp version w/o background (for bbox calculation)
            with open(fileOut, "wb") as out:
                out.write(etree.tostring(tree, pretty_print=True))

            # Get bbox of actual content (adjusted for any transformations)
            xmin, xmax, ymin, ymax = get_bbox(fileOut)
            print(xmin, xmax, ymin, ymax)
            width = xmax - xmin
            height = ymax - ymin

            # Create a <g> element to group all content
            SVG_NS = "http://www.w3.org/2000/svg"
            g = etree.Element("{%s}g" % SVG_NS)

            # Move all existing children into the group and apply translation
            for child in list(root):
                root.remove(child)
                g.append(child)

            # Add the <g> group back to the root
            root.append(g)

            # Apply the transformation (translate content to 0,0)
            g.set("transform", f"translate({-xmin}, {-ymin})")

            # Set new viewBox and width/height
            root.set("viewBox", f"0 0 {width} {height}")
            root.set("width", f"{width}")
            root.set("height", f"{height}")

            # Save final cropped SVG
            with open(fileOut, "wb") as out:
                out.write(etree.tostring(tree, pretty_print=True))

        except Exception as error:
            print(f"There was an error cropping {fileName}: {str(error)}")
