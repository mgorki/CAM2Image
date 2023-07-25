# CAM2Image
Tools for the creation and the handling of images from Cognitive Affective Map (CAM) files created with the [*C.A.M.E.L.*](https://github.com/Camel-app/DataCollection/tree/main) software.

## How to run the program? ##
Run main.py for running the program. Follow the instructions on the graphical user Interface (GUI)

## Main functionalities ##
1. Automating the creation of svg vector graphics from whole folders of CAM files 
2. Converting svg vector graphics (from 1.) to png.
3. Adding a prefix to filenames of several files
4. Splitting a file that contains data from several CAMs into several files (one file per CAM) -> prerequisite for 1. in some cases

## Frequently encountered errors ##
- *I get an error when trying to create svg vector graphics from CAM files, why/what can I do?*
    - Make sure you are using the most recent version of [*C.A.M.E.L.*](https://github.com/Camel-app/DataCollection/tree/main) and make sure to set *surpressSaveCAMpopup* in the *configfile* of to *true*.
    - Make sure data from one and *only one CAM is contained in each CAM file*. If this is not the case: Split the file into multiple files using the respective function in this program (see above).

(***Readme to be expanded soon***)
