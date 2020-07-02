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
        
        
        self.team = Frame(self.mainFrame, borderwidth=0, highlightthickness=0, height = self.heightBox, width = self.widthBox, bg=self.backgroundColor)
        self.team.grid(row=3, column = 0, sticky = N)
        self.teamItems = []
        self.init_team()

        self.box = Frame(self.mainFrame, borderwidth=0, highlightthickness=0, height = self.heightBox, width = self.widthBox, bg=self.backgroundColor)
        self.box.grid(row=3, column = 2)
        self.box.grid_propagate(0)
        self.boxItems = []
        self.init_box()

        
        
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
            config["widthBox"] = 224
            config["heightBox"] = 224
            config["widthGraveyard"] = 224
            config["heightGraveyard"] = 224
            config["player1Name"] = "Player1"
            config["player2Name"] = "Player2"
            config["defaultSize"] = 56
            config["spaceBetweenGroups"] = 20
            config["windowWidth"] = 1200
            config["windowHeight"] = 400
            config["windowPosX"] = 0
            config["windowPosY"] = 0
            config["imageFolder"] = "Path To The Folder Containing The Images You Want To Use"
            config["missingPicture"] = "Path to the Image which gets displayed if the image wasn't found"
            config["enforceUniqueNames"] = False
            config["usePainedPicture"] = True
            config["inputPlaceCaught"] = True
            config["enforceUniquePlaceCaught"] = True
            config["soullinkMode"] = True
            config["displaySoul"] = True
            config["soulImagePath"] = "Path To The Image Between Team Pokemon Of Player1 and Player2"
            

            
            self.data = {
                            "config":config,
                            "team" : [],
                            "box" : [],
                            "graveyard" : []
                        }
            self.save(False)
            
    #Create the main layout
    def init_main_frame(self):
        self.mainFrame = Frame(self.master, bg = self.backgroundColor)

        self.mainFrame.grid_columnconfigure(1, minsize = self.spaceBetweenGroups)
        self.mainFrame.grid_columnconfigure(3, minsize = self.spaceBetweenGroups)
        self.mainFrame.grid_columnconfigure(5, minsize = self.spaceBetweenGroups)

        self.mainFrame.grid_rowconfigure(0, minsize = self.spaceBetweenGroups)
        self.mainFrame.grid_rowconfigure(2, minsize = self.spaceBetweenGroups)

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


        self.menuItems.append(Button(self.teamMenuFrame, text = "Add to team", command = self.addPokemonToTeam))
        self.menuItems[0].grid(row = 0, column = 0)

        self.menuItems.append(Button(self.teamMenuFrame, text = "Kill Pokemon", command = self.killPokemon))
        self.menuItems[1].grid(row = 0, column = 1)

        self.menuItems.append(Button(self.teamMenuFrame, text = "Evolve Pokemon", command = self.evolvePokemon))
        self.menuItems[2].grid(row = 0, column = 2)
        
        self.menuItems.append(Button(self.boxMenuFrame, text = "Swap to Team", command = self.swapPokemonToTeam))
        self.menuItems[3].grid(row = 0, column = 0)
        
        self.menuItems.append(Button(self.boxMenuFrame, text = "Add to Box", command = self.addPokemonToBox))
        self.menuItems[4].grid(row = 0, column = 1)        
        
        self.menuItems.append(Button(self.graveyardMenuFrame, text = "Add to Graveyard", command = self.addToGraveyardDirectly))
        self.menuItems[5].pack()

        
        self.menuItems.append(Button(self.sideMenuFrame, text = "refresh", command = self.manualRefresh))
        self.menuItems[6].pack(fill=BOTH, expand=True)
        
        self.menuItems.append(Checkbutton(self.sideMenuFrame, text = "Disable Automatic Refresh?", variable = self.automaticRefresh))
        self.menuItems[7].pack(fill=BOTH, expand=True)
        
        self.menuItems.append(Button(self.sideMenuFrame, text = "export data", command = self.exportData))
        self.menuItems[8].pack(fill=BOTH, expand=True)

        self.menuItems.append(Button(self.sideMenuFrame, text = "import data", command = self.changeDataFile))
        self.menuItems[9].pack(fill=BOTH, expand=True)

        self.menuItems.append(Entry(self.sideMenuFrame, textvar = self.searchValueVar))
        self.menuItems[10].pack(fill=BOTH, expand=True)
        
        self.menuItems.append(Button(self.sideMenuFrame, text = "Search by pokemon name", command = self.searchByName))
        self.menuItems[11].pack(fill=BOTH, expand=True)

        if self.inputPlaceCaught == 1: 
            self.menuItems.append(Button(self.sideMenuFrame, text = "Search by place caught", command = self.searchByLocation))
            self.menuItems[12].pack(fill=BOTH, expand=True)
                              

    #initializes Config Values
    def init_customizable_values(self):
        self.backgroundColor = self.data["config"]["backgroundColor"]
        self.widthBox = self.data["config"]["widthBox"]
        self.heightBox = self.data["config"]["heightBox"]
        self.widthGraveyard = self.data["config"]["widthGraveyard"]
        self.heightGraveyard = self.data["config"]["heightGraveyard"]
        self.player1 = self.data["config"]["player1Name"]
        self.player2 = self.data["config"]["player2Name"]
        self.defaultSize = self.data["config"]["defaultSize"]
        self.spaceBetweenGroups = self.data["config"]["spaceBetweenGroups"]
        self.imageFolder = self.data["config"]["imageFolder"]
        self.missingPicture = self.data["config"]["missingPicture"]
        self.usePainedPicture = self.data["config"]["usePainedPicture"]
        self.enforceUniqueNames = self.data["config"]["enforceUniqueNames"]
        self.inputPlaceCaught = self.data["config"]["inputPlaceCaught"]
        self.enforceUniquePlaceCaught = self.data["config"]["enforceUniquePlaceCaught"]
        self.soullinkMode = self.data["config"]["soullinkMode"]
        self.displaySoul = self.data["config"]["displaySoul"]
        self.soulImagePath = self.data["config"]["soulImagePath"]
        self.windowWidth = self.data["config"]["windowWidth"]
        self.windowHeight = self.data["config"]["windowHeight"]
        self.windowPosX = self.data["config"]["windowPosX"]
        self.windowPosY = self.data["config"]["windowPosY"]

        if self.soullinkMode:
            self.boxMultiplier = 2
            if self.displaySoul:
                self.teamMultiplier = 3
            else:
                self.teamMultiplier = 2
        else:
            self.boxMultiplier = 1
            self.teamMultiplier = 1

    #initializes some internal values
    def init_internal_values(self):
        self.nameVar = StringVar()
        self.nameVar2 = StringVar()
        self.placeCaughtVar  = StringVar()
        self.searchValueVar = StringVar()
        self.name   = ""
        self.link   = ""
        self.name2  = ""
        self.link2  = ""
        self.popUp  = ""
        self.target = ""
        self.placeCaught = ""
        self.searchValue = ""
        self.automaticRefresh = IntVar()
        
        self.columncount = 2
        self.columncountTeam = 2



    def init_team(self):
        self.teamItems = []
        self.size = self.defaultSize
        for pair in self.data["team"]:
            position = len(self.teamItems)
            self.teamItems.append(Canvas(self.team, width= self.defaultSize*self.teamMultiplier+2, height = self.defaultSize+2, borderwidth=0, highlightthickness=0, bg=self.backgroundColor))
            self.teamItems[position].grid(row = (position//self.columncountTeam)+1, column = position%self.columncountTeam)

            for pokemon in enumerate(pair):
                if(pokemon[0]==0):
                    self.create_canvas(pokemon[1], False, False, self.teamItems, position, 0)

                else:
                    if self.soullinkMode == 1:
                        i = 1
                        if self.displaySoul:
                            self.create_canvas(self.soulImagePath, False, False, self.teamItems, position, 1)
                            i = 2

                        if len(pair)==1:
                            self.create_canvas(self.missingPicture, True, False, self.teamItems, position, i)
                        else:
                            self.create_canvas(pokemon[1], True, False, self.teamItems, position, i)
                
                
        

    def init_box(self):
        self.boxItems = []
        self.calculateSizes(len(self.data["box"]), "box")
        for pair in self.data["box"]:
            position = len(self.boxItems)
            self.boxItems.append(Canvas(self.box, width= self.size*self.boxMultiplier, height = self.size, borderwidth=0, highlightthickness=0, bg=self.backgroundColor))
            self.boxItems[position].grid(row = (position//self.columncount)+1, column = position%self.columncount)

            for pokemon in enumerate(pair):
                if(pokemon[0]==0):
                    self.create_canvas(pokemon[1], False, False, self.boxItems, position, 0)
                else:
                    if self.soullinkMode == 1:
                        if(len(pair)==1):
                            self.create_canvas(self.missingPicture, True, False, self.boxItems, position, 1)
                        else:
                            self.create_canvas(pokemon[1], True, False, self.boxItems, position, 1)

                    
        



    def init_graveyard(self):
        self.graveyardItems = []

        self.calculateSizes(len(self.data["graveyard"]),"graveyard")
        
        for pair in self.data["graveyard"]:
            
            position = len(self.graveyardItems)     
            self.graveyardItems.append(Canvas(self.graveyard, width= self.size*self.boxMultiplier, height = self.size, borderwidth=0, highlightthickness=0, bg = self.backgroundColor))
            self.graveyardItems[position].grid(row = (position//self.columncount)+1, column = position%self.columncount)
            
            for pokemon in enumerate(pair):
                if(pokemon[0]==0):
                        self.create_canvas(pokemon[1], False, True, self.graveyardItems, position, 0)
                else:
                    if self.soullinkMode == 1:
                        if(len(pair)==1):
                            self.create_canvas(self.missingPicture, True, True, self.graveyardItems, position, 1)
                        else:
                            self.create_canvas(pokemon[1], True, True, self.graveyardItems, position, 1)
    

    def create_canvas(self, pokemon, mirrored, greyscale, imageArray, position, canvasPos):
        try:
            link = pokemon["link"]
        except KeyError:
            self.displayMessage(pokemon["name"]+" is missing a link.")
            link = self.missingPicture
        except TypeError:
            link = pokemon

        img = Image.open(link).resize((self.size,self.size), Image.ANTIALIAS)
        
        if mirrored == True and not link == self.missingPicture:
            img = ImageOps.mirror(img)


        if greyscale == True:
            img = img.convert('LA')
            
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
        return self.normalize_caseless(left) == self.normalize_caseless(right)




    #Calculates the ideal sizes for the images.
    #https://stackoverflow.com/questions/1575589/resizing-n-of-squares-to-be-as-big-as-possible-while-still-fitting-into-box-of
    def calculateSizes(self, n, place):
        if(place=="graveyard"):
            self.width = self.widthGraveyard
            self.height = self.heightGraveyard
        else:
            self.width = self.widthBox
            self.height = self.heightBox
        
        try:
            area = self.width * self.height
            idealArea = area//(n*self.boxMultiplier)
            idealLength = math.sqrt(idealArea)
            numberHorizontal = math.ceil(self.width/idealLength)
            if numberHorizontal%self.boxMultiplier!=0:
                numberHorizontal+=1
            numberVertical = math.ceil(self.height/idealLength)

            self.size = min(self.width//numberHorizontal, self.height//numberVertical)
            self.columncount = numberHorizontal//self.boxMultiplier
            self.rowcount = numberVertical
        except:
            self.size = self.defaultSize
            self.rowcount = 2
            self.columncount = 2


        if(self.size>self.defaultSize):
            self.size = self.defaultSize



    #checks if the name given as a parameter is unique
    def isNameUnique(self, name):
        try:
            return name not in self.getAllNames()
        except:
            return true
    
    #checks if the place given as a parameter is unique
    def isPlaceUnique(self, place):
        return place not in self.getAllPlaces()
        
    #gets all the names that a pokemon has
    def getAllNames(self):
        names = []
        for place in self.data["team"], self.data["box"], self.data["graveyard"]:
            for pair in place:
                for pokemon in pair:
                    names.append(pokemon["name"])

        return names

    #gets all the place that a pokemon has
    def getAllPlaces(self):
        places = []
        for array in self.data["team"], self.data["box"], self.data["graveyard"]:
            for pair in array:
                for pokemon in pair:
                    try:
                        if not pokemon["place"] in places:
                            places.append(pokemon["place"])
                    except KeyError:
                        pass

        return places


        
            
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
            self = Window(Tk(className="Geenes Pokemon Team Visualiser"))

    def recreatePopUp(self):
        try:
            self.popUp.destroy()
        except:
            pass

        self.popUp = Toplevel(self.master)

    #creates a pop up with numberOfInputs inputs
    def entryDialogue(self, numberOfInputs, message1, message2=""):
        self.recreatePopUp()

        if numberOfInputs >=1:
            nameEntryLabel = Label(self.popUp, text = message1)
            nameEntryLabel.grid(row = 0, column = 0)
            
            nameEntryField = Entry(self.popUp, textvariable = self.nameVar)
            nameEntryField.grid(row = 0, column = 1)

        if self.inputPlaceCaught == 1 and numberOfInputs >=2:
            routeEntryLabel = Label(self.popUp, text = "Place Caught: ")
            routeEntryLabel.grid(row = 2, column = 0)

            routeEntryField = Entry(self.popUp, textvariable = self.placeCaughtVar)
            routeEntryField.grid(row = 2, column = 1)

        if numberOfInputs >=2 and not message2=="":
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
        self.name2 = self.nameVar2.get()
        
        if(self.enforceUniqueNames==1):
            if not self.isNameUnique(self.name):
                duplicateText = "Name is already in use"

                nameDuplicate = Label(self.popUp, text = duplicateText, fg="red")
                nameDuplicate.grid(row=4, column = 0)

                return
                
                
            if self.soullinkMode and (self.name==self.name2 or not self.isNameUnique(self.name2)):
                duplicateText =""

                if(self.name == self.name2):
                    duplicateText = "Names can't be equal"
                
                elif not self.isNameUnique(self.name) and self.isNameUnique(self.name2):
                    duplicateText = "Name 1 is not unique"
                elif self.isNameUnique(self.name) and not self.isNameUnique(self.name2):
                    duplicateText = "Name 2 is not unique"
                
                
                statusMessage = Label(self.popUp, text = duplicateText, fg="red")
                statusMessage.grid(row=4, column = 0, sticky = "we")

                return

            
        if(self.name =="" or (self.name2=="" and self.soullinkMode == 1)):
            return

        self.confirmPlace()

    def confirmPlace(self):
        if self.inputPlaceCaught == True:
            self.placeCaught = self.placeCaughtVar.get()
            if self.enforceUniquePlaceCaught == True:
                if not self.isPlaceUnique(self.placeCaught):
                    statusMessage = Label(self.popUp, text = "Place isn't unique", fg = "red")
                    statusMessage.grid(row=4, column = 0, sticky = "we")

                    return
        
        if self.inputPlaceCaught == False:
            self.placeCaught = ""

        self.selectLink()

    #let's the user select the path to up to two image files
    def selectLink(self):
        self.link = filedialog.askopenfilename(initialdir = self.imageFolder, title = "Auswahl Bild Pokemon " + self.player1, filetypes = (("png files","*.png"),("all files","*.*")))
        if(self.soullinkMode ==1):
            self.link2 = filedialog.askopenfilename(initialdir = self.imageFolder, title = "Auswahl Bild Pokemon "+ self.player2, filetypes = (("png files","*.png"),("all files","*.*")))

        if self.link =="" or (self.link2 == "" and self.soullinkMode ==1):
            return

        pair = []

        if(self.target=="graveyard"):
            self.replacePartOfLink(self.link, "Pained")

            

        pair.append({"name":self.name, "link":self.link, "place":self.placeCaught})


        if(self.soullinkMode ==1):
            if(self.target == "graveyard"):
                self.replacePartOfLink(self.link2, "Pained")
            pair.append({"name":self.name2, "link":self.link2, "place":self.placeCaught})

        self.data[self.target].append(pair)

        self.save()

                
#------------------------------------------------
#------------Search Methods----------------------
#------------------------------------------------ 
    
    def searchByName(self):
        self.searchValue = self.searchValueVar.get()
        for place in self.data["team"], self.data["box"], self.data["graveyard"]:
            for pair in place:
                for pokemon in pair:
                    if pokemon["name"]==self.searchValue:
                        self.displaySearchResult(pair)
                        return
        self.displayMessage("No Pokemon with found with that name")
        return
    
    #Searches for a pair based on the place that they were caught.
    #Really disgusting so it works even with missing places
    def searchByLocation(self):
        self.searchValue = self.searchValueVar.get()
        i = 0
        for place in self.data["team"], self.data["box"], self.data["graveyard"]:
            for pair in place:
                try:
                    if pair[0]["place"]==self.searchValue or pair[1]["place"]==self.searchValue:
                        self.displaySearchResult(pair)
                        return
                except:
                    if i==0:
                        self.displayMessage("The Catch place isn't set for some pokemon\nYou should add them manually to data.json file")
                        i+=1
                    try:
                        if(self.soullinkMode == 1):
                            if pair[1]["place"]==self.searchValue:
                                self.displaySearchResult(pair)
                                return
                    except:
                        pass

    #searches for the pair
    def searchPair(self, name, searchplace):
        for pair in self.data[searchplace]:
            if(self.caseless_equal(pair[0]["name"],name)):
                return pair
            elif(self.caseless_equal(pair[1]["name"],name)):
                return pair

    #searches for the pokemon
    def searchPokemon(self, name, searchplace):
        for pair in self.data[searchplace]:
            if(self.caseless_equal(pair[0]["name"],name)):
                return pair[0]
            elif(self.caseless_equal(pair[1]["name"],name)):
                return pair[1]
        
#------------------------------------------------
#------------PopUp Methods-----------------------
#------------------------------------------------                     
    def displaySearchResult(self, pair):
        try:
            self.popUp.destroy
        except:
            pass
        self.popUp = Toplevel(self.master)

        
        pokemon1Image = Canvas(self.popUp, width = self.defaultSize, height = self.defaultSize, borderwidth = 0, highlightthickness = 0, bg = self.backgroundColor)
        pokemon1Image.grid(row = 0, column = 0)
        
        img = ImageTk.PhotoImage(Image.open(pair[0]["link"]).resize((self.defaultSize, self.defaultSize), Image.ANTIALIAS))
        pokemon1Image.create_image(0, 0, anchor = NW, image = img)
        
        self.usedImages.append(img)

        pokemon1Name = Label(self.popUp, text = "Name: "+pair[0]["name"])
        pokemon1Name.grid(row = 1, column = 0)
        
        if(self.inputPlaceCaught == 1):
            try:
                pokemon1Place = Label(self.popUp, text = "Place: "+pair[0]["place"])
                pokemon1Place.grid(row = 2, column = 0)
            except:
                pokemon1Place = Label(self.popUp, text = "No Place Found")
                pokemon1Place.grid(row = 2, column = 0)
        if self.soullinkMode == 1:
            pokemon2Image = Canvas(self.popUp, width = self.defaultSize, height = self.defaultSize, borderwidth = 0, highlightthickness = 0, bg = self.backgroundColor)
            pokemon2Image.grid(row = 0, column = 1)
            
            img = ImageTk.PhotoImage(Image.open(pair[1]["link"]).resize((self.defaultSize, self.defaultSize), Image.ANTIALIAS))
            pokemon2Image.create_image(0, 0, anchor = NW, image = img)
            
            self.usedImages.append(img)

            pokemon2Name = Label(self.popUp, text = "Name: "+pair[1]["name"])
            pokemon2Name.grid(row = 1, column = 1)

            if(self.inputPlaceCaught == 1):
                try:
                    pokemon2Place = Label(self.popUp, text = "Place: "+pair[1]["place"])
                    pokemon2Place.grid(row = 2, column = 1)
                except:
                    pokemon1Place = Label(self.popUp, text = "No Place Found")
                    pokemon1Place.grid(row = 2, column = 1)
            

        confirm = Button(self.popUp, text = "OK", command=self.popUp.destroy)
        confirm.grid(row = 3, column = 0)




#------------------------------------------------
#------------Functionality Methods---------------
#------------------------------------------------        
            
        
#------------------------------------------------
#------------Graveyard---------------------------
#------------------------------------------------
                
    #Configures the input pop up for killing a pokemon
    def killPokemon(self):
        if len(self.data["team"])!=0:
            self.entryDialogue(1, "Name des gestorbenen Pokemons: ")
            confirm = Button(self.popUp, text="Enter", command = self.handlePokemonKill)
            confirm.grid(row=1, column = 1)
        
        else:
            self.displayMessage("Es sind keine Pokemon im Team.")

    

    #Handles the killing of the pokemon / pair
    def handlePokemonKill(self):
        pair = self.searchPair(self.nameVar.get(), "team")
        if(self.usePainedPicture):
            pair[0]["link"] = self.replacePartOfLink(pair[0]["link"], "Pained")
            if(self.soullinkMode ==1):
                pair[1]["link"] = self.replacePartOfLink(pair[1]["link"],"Pained")
        self.data["team"].remove(pair)
        self.data["graveyard"].append(pair)
        self.save()
        
    #Allows to either add a pair or a single pokemon to the graveyard, for first time setup
    def addToGraveyardDirectly(self):
        if(self.soullinkMode ==1):
            self.entryDialogue(2+self.inputPlaceCaught, self.player1+"s Pokemon Name: ", self.player2+"s Pokemon Name: ")
        else:
            self.entryDialogue(1+self.inputPlaceCaught, "Pokemon Name: ")

        self.target="graveyard"
        confirm = Button(self.popUp, text="Enter", command = self.confirmName)
        confirm.grid(row=2+self.inputPlaceCaught, column = 1)


#------------------------------------------------
#------------Team--------------------------------
#------------------------------------------------

        
    #Configures the input pop up for evolving a pokemon
    def evolvePokemon(self):
        if len(self.data["team"])!=0:
            self.entryDialogue(1,"Name entwickelte pokemon: ")
            confirm = Button(self.popUp, text="Enter", command = self.handlePokemonEvolution)
            confirm.grid(row = 1, column = 1)

        else:
            self.displayMessage("Es sind keine Pokemon im Team.")

    #searches for the pokemon with the given name and let's the user select a new picture for it
    def handlePokemonEvolution(self):
        self.link = filedialog.askopenfilename(title = "Select the pokemon",filetypes = (("png files","*.png"),("all files","*.*")))
        pokemonToEvolve = self.nameVar.get()
        pokemon = self.searchPokemon(pokemonToEvolve, "team")
        pokemon["link"] = self.link

        self.save()

    #Configures the input pop up for adding a new pair or single pokemon to the team
    def addPokemonToTeam(self):        
        if len(self.data["team"])==6:
            self.displayMessage("Es sind schon 6 Pokemon im Team.")
        else:
            if(self.soullinkMode ==1):
                self.entryDialogue(2+self.inputPlaceCaught, "Name Pokemon von "+self.player1+": ", "Name Pokemon von "+self.player2+": ")
            else:
                self.entryDialogue(1+self.inputPlaceCaught, "Pokemon Name: ")
                
            self.target="team"

            confirm = Button(self.popUp, text="Enter", command = self.confirmName)
            confirm.grid(row = 2+self.inputPlaceCaught, column = 1)
    






        
#------------------------------------------------
#------------Swapping----------------------------
#------------------------------------------------
        
    #Configures the input pop up for swapping
    def swapPokemonToTeam(self):
        if len(self.data["box"])!=0:
            if len(self.teamItems)==6:
                self.entryDialogue(2, "Name Pokemon in der Box: ", "Name Pokemon im Team: ")
                
                confirm = Button(self.popUp, text="Enter", command = self.handleSwap)
                confirm.grid(row = 2, column = 1)
            else:
                self.entryDialogue(1, "Name Pokemon in der Box: ")
                
                confirm = Button(self.popUp, text="Enter", command = self.handleAddToTeam)
                confirm.grid(row = 2, column = 1)
        else:
            self.displayMessage("Es sind keine Pokemon in der Box.")

    #calls the swap method, needed since button commands can't have parameters
    def handleSwap(self):
        self.swapPair(self.searchPair(self.nameVar.get(),"box"),self.searchPair(self.nameVar2.get(),"team"))

    
    #Removes the pairs from their places and adds them to the other place
    def swapPair(self, toTeam, toBank):
        self.data["team"].remove(toBank)
        self.data["team"].append(toTeam)
        self.data["box"].remove(toTeam)
        self.data["box"].append(toBank)

        self.save()

    #Used if swapping isn't necessary since there is an open space in the team
    def handleAddToTeam(self):
        pair = self.searchPair(self.nameVar.get(),"box")
        self.data["box"].remove(pair)
        self.data["team"].append(pair)

        self.save()
		














#------------------------------------------------
#------------Box---------------------------------
#------------------------------------------------        

        

    #adds a pokemon or pair directly to the box
    def addPokemonToBox(self):
        if(self.soullinkMode ==1):
            self.entryDialogue(2+self.inputPlaceCaught, self.player1+"s Pokemon Name: ", self.player2+"s Pokemon Name: ")
        else:
            self.entryDialogue(1+self.inputPlaceCaught, "Pokemon Name: ")

        self.target="box"
        confirm = Button(self.popUp, text="Enter", command = self.confirmName)
        confirm.grid(row=2+self.inputPlaceCaught, column = 1)


#------------------------------------------------
#------------Config Menu-------------------------
#------------------------------------------------        




    def displayOptionsMenu(self):
        self.recreatePopUp()
        items = {}
        items["backgroundColor"] = self.createConfigTuple(self.popUp, "Background color", self.backgroundColor, "text", 0)
        items["widthBox"] = self.createConfigTuple(self.popUp, "Width of Box display", self.widthBox, "number", 1)
        items["heightBox"] = self.createConfigTuple(self.popUp, "Height of Box display", self.heightBox, "number", 2)
        items["widthGraveyard"] = self.createConfigTuple(self.popUp, "Width of Graveyard display", self.widthGraveyard, "number", 3)
        items["heightGraveyard"] = self.createConfigTuple(self.popUp, "Height of Graveyard display", self.heightGraveyard, "number", 4)
        items["player1Name"] = self.createConfigTuple(self.popUp, "Name of Player 1", self.player1, "text", 5)
        items["player2Name"] = self.createConfigTuple(self.popUp, "Name of Player 2", self.player2, "text", 6)
        items["defaultSize"] = self.createConfigTuple(self.popUp, "Max./Team image size (in px)", self.defaultSize, "number", 7)
        items["spaceBetweenGroups"] = self.createConfigTuple(self.popUp, "Space between the groups", self.spaceBetweenGroups, "number", 8)
        items["windowWidth"] = self.createConfigTuple(self.popUp, "Window start width (in px)", self.windowWidth, "number", 9)
        items["windowHeight"] = self.createConfigTuple(self.popUp, "Window start height (in px)", self.windowHeight, "number", 10)
        items["windowPosX"] = self.createConfigTuple(self.popUp, "Window position x", self.windowPosX, "number", 11)
        items["windowPosY"] = self.createConfigTuple(self.popUp, "Window position y", self.windowPosY, "number", 12)
        items["imageFolder"] = self.createConfigTuple(self.popUp, "Images Folder", self.imageFolder, "folderSelection", 13)
        items["missingPicture"] = self.createConfigTuple(self.popUp, "Path to Missing Picture", self.missingPicture, "folderSelection", 14)
        items["usePainedPicture"] = self.createConfigTuple(self.popUp, "Pained Picture for Graveyard?", self.usePainedPicture, "checkbox", 15)
        items["enforceUniqueNames"] = self.createConfigTuple(self.popUp, "Enforce Unique Names?", self.enforceUniqueNames, "checkbox", 16)
        items["inputPlaceCaught"] = self.createConfigTuple(self.popUp, "Input Place Caught?", self.inputPlaceCaught, "checkbox", 17)
        items["enforceUniquePlaceCaught"] = self.createConfigTuple(self.popUp, "Enforce Unique Place Caught?", self.enforceUniquePlaceCaught, "checkbox", 18)
        items["soullinkMode"] = self.createConfigTuple(self.popUp, "Enable Soullink Mode?", self.soullinkMode, "checkbox", 19)
        items["displaySoul"] = self.createConfigTuple(self.popUp, "Display Soul?", self.displaySoul, "checkbox", 20)
        items["soulImagePath"] = self.createConfigTuple(self.popUp, "Path to Soul Image", self.soulImagePath, "folderSelection", 21)

        self.popUp.grid_rowconfigure(22, minsize = 20)
        
        cancelButton = Button(self.popUp, text="cancel", command = self.popUp.destroy)
        cancelButton.grid(row = 23, column = 0)
        
        confirmButton = Button(self.popUp, text="save", command = partial(self.saveConfigValues,items))
        confirmButton.grid(row = 24, column = 1)
        


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








    
        
        
            
        
root = Tk(className="Geenes Pokemon Team Visualiser")
app = Window(root)
root.mainloop()
