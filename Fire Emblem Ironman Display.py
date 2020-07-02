from tkinter import filedialog
from tkinter import *
from PIL import ImageTk,Image, ImageOps
from functools import partial
import json
import math
import unicodedata

class Window(Frame):

    def __init__(self, master = None, datafileName = "data.json"):
        self.master = master
        self.datafile = datafileName
        self.init_window()
        

#------------------------------------------------
#------------Initialization Methods--------------
#------------------------------------------------ 

    def init_window(self):
        self.init_internal_values()
        self.init_data()
        self.usedImages = []
        self.init_customizable_values()

        self.master.configure(background=self.backgroundColor)
        self.master.geometry(str(self.windowWidth)+"x"+str(self.windowHeight)+"+"+str(self.windowPosX)+"+"+str(self.windowPosY))
        

        self.init_main_frame()
        self.init_menu()    
        
        self.graveyard = Frame(self.mainFrame, borderwidth=0, highlightthickness=0, height = self.heightGraveyard, width = self.widthGraveyard, bg=self.backgroundColor)
        self.graveyard.grid(row=3, column = 4)
        self.graveyard.grid_propagate(0)
        self.graveyardItems = []
        self.init_graveyard()

        self.mainFrame.pack()
    
    def init_data(self):
        try: 
            with open(self.datafile) as f:
                self.data = json.load(f)
        #Data file not found, create a new one with default values. Then refresh the window
        except FileNotFoundError:
            config = {}
            config["backgroundColor"] = "#0047bb"
            config["widthGraveyard"] = 224
            config["heightGraveyard"] = 224
            config["defaultSize"] = 56
            config["windowWidth"] = 1200
            config["windowHeight"] = 400
            config["windowPosX"] = 0
            config["windowPosY"] = 0
            config["imageFolder"] = "Path To The Folder Containing The Images You Want To Use"
            config["missingPicture"] = "Path to the Image which gets displayed if the image wasn't found"
            config["automaticNameCreation"] = True
            config["useFilenameForName"] = True
            

            
            self.data = {
                            "config":config,
                            "graveyard" : []
                        }
            self.save(False)
            
    #Create the main layout
    def init_main_frame(self):
        self.mainFrame = Frame(self.master, bg = self.backgroundColor)

        self.mainFrame.grid_columnconfigure(1, minsize = 20)
        self.mainFrame.grid_columnconfigure(3, minsize = 20)
        self.mainFrame.grid_columnconfigure(5, minsize = 20)

    #Create the menu buttons
    def init_menu(self):
        self.teamMenuFrame = Frame(self.mainFrame, bg = self.backgroundColor)
        self.teamMenuFrame.grid(row = 1, column = 0, sticky = "w")
        self.menuItems = []

        self.boxMenuFrame = Frame(self.mainFrame, bg = self.backgroundColor)
        self.boxMenuFrame.grid(row = 1, column = 2, sticky = "w")

        self.graveyardMenuFrame = Frame(self.mainFrame, bg = self.backgroundColor)
        self.graveyardMenuFrame.grid(row = 1, column = 4, sticky = "w")

        self.optionsButton = Button(self.mainFrame,text = "config", command = self.displayOptionsMenu)
        self.optionsButton.grid(row = 1, column = 6, sticky = "e")

        self.sideMenuFrame = Frame(self.mainFrame, bg = self.backgroundColor)
        self.sideMenuFrame.grid(row = 3, column = 6, sticky = "w")

        self.menuItems.append(Button(self.sideMenuFrame, text = "refresh", command = self.manualRefresh))
        self.menuItems[0].pack(fill=BOTH, expand=True)
        
        self.menuItems.append(Checkbutton(self.sideMenuFrame, text = "Disable Automatic Refresh?", variable = self.automaticRefresh))
        self.menuItems[1].pack(fill=BOTH, expand=True)
        
        self.menuItems.append(Button(self.sideMenuFrame, text = "export data", command = self.exportData))
        self.menuItems[2].pack(fill=BOTH, expand=True)

        self.menuItems.append(Button(self.sideMenuFrame, text = "import data", command = self.changeDataFile))
        self.menuItems[3].pack(fill = BOTH, expand = True)

        self.menuItems.append(Button(self.sideMenuFrame, text = "Reset Characters", command = self.confirmReset))
        self.menuItems[4].pack(fill=BOTH, expand=True)

        self.menuItems.append(Button(self.graveyardMenuFrame, text = "Add Character", command = self.addToGraveyardDirectly))
        self.menuItems[5].grid(row = 0, column = 0, sticky = "we")

        self.menuItems.append(Button(self.graveyardMenuFrame, text = "Swap Characters", command = self.swapCharacters))
        self.menuItems[6].grid(row = 0, column = 1, sticky = "we")

        self.menuItems.append(Button(self.graveyardMenuFrame, text = "Change Character Name", command = self.changeName))
        self.menuItems[7].grid(row = 0, column = 2, sticky = "we")

        self.menuItems.append(Button(self.graveyardMenuFrame, text = "Remove Character", command = self.removeCharacter))
        self.menuItems[8].grid(row = 1, column = 0, sticky = "we")

        self.menuItems.append(Button(self.graveyardMenuFrame, text = "Change Image", command = self.changeImage))
        self.menuItems[9].grid(row = 1, column = 1, sticky = "we")

        

                              

    #initializes Config Values
    def init_customizable_values(self):
        self.backgroundColor = self.data["config"]["backgroundColor"]
        self.widthGraveyard = self.data["config"]["widthGraveyard"]
        self.heightGraveyard = self.data["config"]["heightGraveyard"]
        self.defaultSize = self.data["config"]["defaultSize"]
        self.imageFolder = self.data["config"]["imageFolder"]
        self.missingPicture = self.data["config"]["missingPicture"]

        self.windowWidth = self.data["config"]["windowWidth"]
        self.windowHeight = self.data["config"]["windowHeight"]
        self.windowPosX = self.data["config"]["windowPosX"]
        self.windowPosY = self.data["config"]["windowPosY"]
        self.automaticNameCreation = self.data["config"]["automaticNameCreation"]
        self.useFilenameForName = self.data["config"]["useFilenameForName"]
        self.boxMultiplier = 1
        self.teamMultiplier = 1

    #initializes some internal values
    def init_internal_values(self):
        self.nameVar = StringVar()
        self.nameVar2 = StringVar()
        self.searchValueVar = StringVar()
        self.name   = ""
        self.link   = ""
        self.name2  = ""
        self.link2  = ""
        self.popUp  = ""
        self.placeCaught = ""
        self.searchValue = ""
        self.automaticRefresh = IntVar()
        
        self.columncount = 2
        self.columncountTeam = 2


    def init_graveyard(self):
        self.graveyardItems = []

        self.calculateSizes(len(self.data["graveyard"]),"graveyard")
        
        for character in self.data["graveyard"]:
            
            position = len(self.graveyardItems)     
            self.graveyardItems.append(Canvas(self.graveyard, width= self.size+2, height = self.size+2, borderwidth=0, highlightthickness=0, bg = self.backgroundColor))
            self.graveyardItems[position].grid(row = (position//self.columncount)+1, column = position%self.columncount)
 
            self.create_canvas(character, False, True, self.graveyardItems, position, 0)
    

    def create_canvas(self, character, mirrored, greyscale, imageArray, position, canvasPos):
        try:
            link = character["link"]
        except KeyError:
            self.displayMessage(character["name"]+" is missing a link.")
            link = self.missingPicture
        except TypeError:
            link = character

        img = Image.open(link).resize((self.size,self.size), Image.ANTIALIAS)
            
        tkImage = ImageTk.PhotoImage(img)
        imageArray[position].create_image(canvasPos * self.size, 0, anchor = NW, image = tkImage)
        
        self.usedImages.append(tkImage)
            


#------------------------------------------------
#------------Utility Methods---------------------
#------------------------------------------------


    #compare the names without caring about capitalization
    #https://stackoverflow.com/questions/319426/how-do-i-do-a-case-insensitive-string-comparison
    def normalize_caseless(self,text):
        return unicodedata.normalize("NFKD", text.casefold())

    def caseless_equal(self,left, right):
        return self.normalize_caseless(str(left)) == self.normalize_caseless(str(right))




    #Calculates the ideal sizes for the images.
    #https://stackoverflow.com/questions/1575589/resizing-n-of-squares-to-be-as-big-as-possible-while-still-fitting-into-box-of
    def calculateSizes(self, n, place):
        if(place=="graveyard"):
            self.width = self.widthGraveyard
            self.height = self.heightGraveyard
        
        try:
            area = self.width * self.height
            idealArea = area/n
            idealLength = math.sqrt(idealArea)

            if self.width / idealLength % 1 > self.height / idealLength % 1:
                numberHorizontal = math.ceil(self.width/idealLength)
                numberVertical = math.ceil(self.height/idealLength)   
                self.size = math.floor(self.height / numberVertical)
            else:
                numberHorizontal = math.floor(self.width/idealLength)
                numberVertical = math.ceil(self.height/idealLength)   
                self.size = math.floor(self.height / numberVertical)

            self.columncount = numberHorizontal//1
            self.rowcount = numberVertical
        except:
            self.size = self.defaultSize
            self.rowcount = 2
            self.columncount = 2


        if(self.size>self.defaultSize):
            self.size = self.defaultSize



        
            
    #saves the changes to the data.json file
    def save(self, refresh = True):
        self.name1 = ""
        self.name2 = ""
        self.link1 = ""
        self.link2 = ""
        
        with open(self.datafile,'w+') as json_file:
            json.dump(self.data, json_file, indent = 4)
            json_file.close()
        if(refresh):
            self.refresh()


    #Allows the user to export the data to a file. Should always be the same as the data.json, but why not
    def exportData(self):
        path = filedialog.asksaveasfilename(initialdir = "/",title = "Choose location",filetypes = (("json files","*.json"),("all files","*.*")))
        
        if path[-5:] == ".json":
            
            with open(path,'w') as json_file:
                json.dump(self.data, json_file, indent = 4)
        else:
            with open(path+".json",'w') as json_file:
                json.dump(self.data, json_file, indent = 4)

    def changeDataFile(self):
        self.datafile = filedialog.askopenfilename(initialdir = "/",title = "Choose location",filetypes = (("json files","*.json"),("all files","*.*")))
        self.refresh()


#------------------------------------------------
#------------UI Methods--------------------------
#------------------------------------------------ 
    #automatic refresh after each action, can be disabled
    def refresh(self):
        if self.automaticRefresh.get()==0:
            self.manualRefresh()

    #allows the user to refresh the screen manually
    def manualRefresh(self):
        self.master.destroy()   
        self = Window(Tk(className="Geenes Ironman display"), self.datafile)

    def recreatePopUp(self):
        try:
            self.popUp.destroy()
        except:
            pass

        self.popUp = Toplevel(self.master)

    def confirmReset(self):
        self.recreatePopUp()

        confirmationMessage = Label(self.popUp, text="Are you sure you want to reset the Death Counter? This action can not be reversed.")
        confirmationMessage.grid(row = 0, column = 0, columnspan = 9)
    
        yesButton = Button(self.popUp, text="Yes", command=self.resetCharacters)
        yesButton.grid(row = 1, column = 4)
        noButton = Button(self.popUp, text="No", command= self.popUp.destroy)
        noButton.grid(row = 1, column = 6)

    def resetCharacters(self):
        self.data["graveyard"] = []
        self.save()
    
    

        
        
        

    #creates a pop up with numberOfInputs inputs
    def entryDialogue(self, numberOfInputs, message1, message2=""):
        self.recreatePopUp()

        if numberOfInputs >0:
            nameEntryLabel = Label(self.popUp, text = message1)
            nameEntryLabel.grid(row = 0, column = 0)
            
            nameEntryField = Entry(self.popUp, textvariable = self.nameVar)
            nameEntryField.grid(row = 0, column = 1)

        if numberOfInputs >1:
            nameEntryLabel2 = Label(self.popUp, text = message2)
            nameEntryLabel2.grid(row = 1, column = 0)
            
            nameEntryField2 = Entry(self.popUp, textvariable = self.nameVar2)
            nameEntryField2.grid(row = 1, column = 1)
                
            return

    #dispalys a given message in a pop up
    def displayMessage(self, message):
        self.recreatePopUp()
        message= Label(self.popUp, text = message)
        message.pack()

        confirm = Button(self.popUp, text = "OK", command=self.popUp.destroy)
        confirm.pack()



    #replaces a part of the link with the newContent.
    def replacePartOfLink(self, link, newContent):
        try:
            index1 = link.rindex("/")+1
        except:
            index1 = link.rindex("\\")+1

        index2 = link.rindex(".")

        return link.replace(link[index1:index2], newContent)



#------------------------------------------------
#------------User Input Methods------------------
#------------------------------------------------ 

    #Checks the names that the user input. 
    def confirmName(self):
        self.name = self.nameVar.get()
        
        if(self.name ==""):
            return

        self.selectLink()


    #let's the user select the path to up to two image files
    def selectLink(self):
        self.link = filedialog.askopenfilename(initialdir = self.imageFolder, title = "Select Image", filetypes = (("png files","*.png"),("all files","*.*")))

        if self.link =="":
            return

        self.data["graveyard"].append({"name":self.name, "link":self.link})

        self.save()

                
#------------------------------------------------
#------------Search Methods----------------------
#------------------------------------------------ 

    #searches for the character
    def getCharacter(self, name):
        for character in self.data["graveyard"]:
            if(self.caseless_equal(character["name"], name)):
                return character

    def getCharacterIndex(self, name):
        for character in self.data["graveyard"]:
            if(self.caseless_equal(character["name"], name)):
                return self.data["graveyard"].index(character)  




#------------------------------------------------
#------------Functionality Methods---------------
#------------------------------------------------        

        
    #Allows to add a character to the graveyard
    def addToGraveyardDirectly(self):
        if self.automaticNameCreation:
            self.link = filedialog.askopenfilename(initialdir = self.imageFolder, title = "Select Image", filetypes = (("png files","*.png"),("all files","*.*")))
            if not self.link == "":
                self.name = self.getNameToUse(self.link)
                self.data["graveyard"].append({"name":self.name, "link":self.link})
                self.save()

        else:
            self.entryDialogue(1, "Name: ")

            confirm = Button(self.popUp, text="Enter", command = self.confirmName)
            confirm.grid(row=2, column = 1)

    def getNameToUse(self, link = ""):
        if self.useFilenameForName:
            return link[link.rfind("/")+1:link.find(".")]
        else:
            return str(len(self.data["graveyard"])+1)
                

        
        
        

    #Allows to swap two characters positions in the graveyard.
    def swapCharacters(self):
        self.entryDialogue(2, "Name: ", "Name: ")
        confirm = Button(self.popUp, text="Enter", command = self.handleSwap)
        confirm.grid(row=2, column = 1)

    def removeCharacter(self):
        self.entryDialogue(1, "Name: ")

        confirm = Button(self.popUp, text="Enter", command = self.handleRemoval)
        confirm.grid(row=2, column = 1)

    def changeImage(self):
        self.entryDialogue(1, "Name: ")

        confirm = Button(self.popUp, text="Enter", command = self.handleImageChange)
        confirm.grid(row=2, column = 1)

    def handleSwap(self):
        name1 = self.nameVar.get()
        name2 = self.nameVar2.get()

        char1 = self.getCharacterIndex(name1)
        char2 = self.getCharacterIndex(name2)

        self.data["graveyard"][char1], self.data["graveyard"][char2] = self.data["graveyard"][char2], self.data["graveyard"][char1]

        self.save()

    def handleImageChange(self):
        name = self.nameVar.get()
        self.link = filedialog.askopenfilename(initialdir = self.imageFolder, title = "Select Image", filetypes = (("png files","*.png"),("all files","*.*")))

        if self.link =="":
            return

        character = self.getCharacter(name)
        character["link"] = self.link

        self.save()

    def handleRemoval(self):
        name = self.nameVar.get()
        character = self.getCharacter(name)

        self.data["graveyard"].remove(character)
        self.save()

    def changeName(self):
        self.entryDialogue(2, "Current Name: ", "New Name: ")

        confirm = Button(self.popUp, text="Enter", command = self.handleNameChange)
        confirm.grid(row=2, column = 1)

    def handleNameChange(self):
        name = self.nameVar.get()
        newName = self.nameVar2.get()
        character = self.getCharacter(name)
        character["name"] = newName
        self.save()
        
        

        
#------------------------------------------------
#------------Config Menu-------------------------
#------------------------------------------------        




    def displayOptionsMenu(self):
        self.recreatePopUp()
        items = {}
        items["backgroundColor"] = self.createConfigTuple(self.popUp, "Background color", self.backgroundColor, "text", 0)
        items["widthGraveyard"] = self.createConfigTuple(self.popUp, "Width of Graveyard display", self.widthGraveyard, "number", 1)
        items["heightGraveyard"] = self.createConfigTuple(self.popUp, "Height of Graveyard display", self.heightGraveyard, "number", 2)
        items["defaultSize"] = self.createConfigTuple(self.popUp, "Max./Team image size (in px)", self.defaultSize, "number", 3)
        items["windowWidth"] = self.createConfigTuple(self.popUp, "Window start width (in px)", self.windowWidth, "number", 4)
        items["windowHeight"] = self.createConfigTuple(self.popUp, "Window start height (in px)", self.windowHeight, "number", 5)
        items["windowPosX"] = self.createConfigTuple(self.popUp, "Window position x", self.windowPosX, "number", 6)
        items["windowPosY"] = self.createConfigTuple(self.popUp, "Window position y", self.windowPosY, "number", 7)
        items["imageFolder"] = self.createConfigTuple(self.popUp, "Images Folder", self.imageFolder, "folderSelection", 8)
        items["missingPicture"] = self.createConfigTuple(self.popUp, "Path to Missing Picture", self.missingPicture, "folderSelection", 9)
        items["automaticNameCreation"] = self.createConfigTuple(self.popUp, "Create Name automatically", self.automaticNameCreation, "checkbox", 11)
        items["useFilenameForName"] = self.createConfigTuple(self.popUp, "Use File Name For Name", self.useFilenameForName, "checkbox", 12)


        self.popUp.grid_rowconfigure(13, minsize = 20)
        
        cancelButton = Button(self.popUp, text="cancel", command = self.popUp.destroy)
        cancelButton.grid(row = 14, column = 0)
        
        confirmButton = Button(self.popUp, text="save", command = partial(self.saveConfigValues,items))
        confirmButton.grid(row = 14, column = 1)
    


    def saveConfigValues(self, configValues):
        for configValue in configValues:
            self.data["config"][configValue] = configValues[configValue][2].get()
        self.save()
            

    def createConfigTuple(self, parent, name, currentValue, inputType, gridRow):
        #create the tuple as a list and convert it before returning
        returnValue = []
        if not "?" in name:
            name += ": "
        returnValue.append(Label(parent, text = name))
        var = None
        if inputType == "text":
            var = StringVar()
            var.set(currentValue)
            returnValue.append(Entry(parent, textvariable = var))
            
        elif inputType == "number":
            var = IntVar()
            var.set(currentValue)
            returnValue.append(Entry(parent, textvariable = var))

        elif inputType == "checkbox":
            var = IntVar()
            var.set(currentValue)
            returnValue.append(Checkbutton(parent, variable = var))
            
        elif inputType == "folderSelection":
            var = StringVar()
            var.set(currentValue)
            returnValue.append(Button(parent, text="change", command = partial(self.handleFolderSelection, var)))
            
        else:
            print("ERROR - wrong input type when creating config tuple " + name)
            return
        returnValue[0].grid(row = gridRow, column = 0)
        returnValue[1].grid(row = gridRow, column = 1)
        returnValue.append(var)


        return tuple(returnValue)
        
    def handleFolderSelection(self, var):
        var.set(filedialog.askdirectory())








    
        
        
            
        
root = Tk(className="Geenes ironman display")
app = Window(root)
root.mainloop()
