#region IMPORTS
'''
This is where I put all my imports.
'''
from importlib.resources import path
from importlib.resources import path
import os
import pygame
from pygame.locals import *
from pygame import mixer
import csv
import re
import copy
import time
import random
import webbrowser
pygame.font.init()
pygame.init()
pygame.mixer.init()
#endregion

#---------------------------------------------------------------------------------------------------------------------------

#region PATHS AND FILES
'''
This is where I store all the paths and folders, for easier acess.

'''
base_path = os.path.dirname(__file__) #This is to get the path of the current .py file
background_folder = os.path.join(base_path, "Backgrounds")
config_folder = os.path.join(base_path, "Config")
image_folder = os.path.join(base_path, "Images")
sprites_folder = os.path.join(base_path, 'Sprites')

ConfigFile = os.path.join(config_folder, "Config.txt")

Image_Folders = [f for f in os.listdir(image_folder) 
                if os.path.isdir(os.path.join(image_folder, f)) and f.endswith("Deck")] #this is a list of STR, getting the name of the folders inside the image folder
#endregion

#---------------------------------------------------------------------------------------------------------------------------

#region FIXED VALUES 
'''
This is where I store all values that are FIXED.
Generally, most variables are either variables (as the name suggests) or read from the settings
'''

#VARIABLES
CardWidth, CardHeight = 64, 89
CardScale = 2
CS = 18 #CardSpace between cards
CW, CH = CardScale*CardWidth, CardScale*CardHeight
#.
WSIncrement = 26 #21 for small font, + 5 for in lines. Used for Window Settings increments between lines of text.
InitialOffset = 17 #initial offset for text
Centralizer = 2.5 #adjuster for text
Corrector = 5 #adjuster for text
TutorialPage = 1 #for changing the page in the tutorial

#PREDEFINED - COLORS
BLUE  = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_ORANGE = (255, 200, 0)
ORANGE = (255, 165, 0)
DARK_ORANGE = (255, 140, 0)
PINK = (255, 192, 203)
PURPLE = (128, 0, 128)
LIGHT_GRAY = (211, 211, 211)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)

#PREDEFINED - DELAYS
Delay1000MS = 1000 #this is used for the timer, and it is in milliseconds. 1000 ms = 1 second
Delay500MS = 500 #500 ms = 0.5 seconds
Delay300MS = 300 #300 ms = 0.3 seconds
Delay100MS = 100 #100 ms = 0.1 seconds
button_clicked_time = None
action_pending = False
action_pending1, action_pending2, action_pending3, action_pending4, action_pending5 = False, False, False, False, False
action_pending6, action_pending7, action_pending8, action_pending9, action_pending10 = False, False, False, False, False 

#TIMER FOR LIFEGAIN
DamageTimer = 0
LifegainTimer = 0
DLTimer = 1.5 #This is the timer the Damage/Lifegain pop-up lingers on
DamageValue = 0
LifegainValue = 0

#ALTERNATIVE BACKGROUNDS
'''
This is a list of Backgrounds, in case I want to do different backgrounds for each screen.
For now, I'm not using it.
'''
BGTitle = None
BGSettings = None
BGScoreboard = None
BGPlay = None
BGCredits = None

#INITIAL STATS
StartingHealthPoints = 20
HealthPoints = StartingHealthPoints
StartingScore = 0
PotionCounter = 0
Score = StartingScore
DButtonLock = 0
Score = 0
Flag = 0
DrawingEachTurn = True
PlayerName = ''

#endregion

#---------------------------------------------------------------------------------------------------------------------------

#region WIDTH, HEIGHT & FONTS
'''This is for defining the WIDTH and HEIGHT of the game. Normally, it
reads the ConfigFile and draws the WIDTH and HEIGHT from there.
A function was created for, later on, update the WIDTH and HEIGHT when the user changes
'''
with open(ConfigFile,'r', encoding='utf-8') as f:
    for line in f:
        if "WIDTH" in line:
            WIDTH = int(line.split('=')[1].strip())
        elif "HEIGHT" in line:
            HEIGHT = int(line.split('=')[1].strip())

'''WIDTH, HEIGHT = 1200, 700 #if reset, the WIDTH and HEIGHT are 1200 x 700''' #CREATE A RESET
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Scoundrel")

#just a placeholder for some fonts I liked
fonts_type = [
'agencyfbnegrito',
'arialblack',
'bookantiqua', #too thin
'castellar',
'comicsans',
'felixtitling',
'franklingothicheavy', #cartoonish
'freensansbold',
'gilsanscondensed',
'hightowertext',
'swiss721outline', #bad transparency
'impact'
]

font_type_classic = fonts_type[4] #comicsans
font_type_outline =  fonts_type[11] 
font_type_arial = fonts_type[1] 

#this is the default font, for buttons or texts
BIGFONT = pygame.font.SysFont(font_type_classic, 50)
FONT = pygame.font.SysFont(font_type_classic, 30)
SMALLFONT = pygame.font.SysFont(font_type_classic, 15)

#this is the outline font, used for reminder texts and more visibility
BIGFONT2 = pygame.font.SysFont(font_type_outline, 50)
FONT2 = pygame.font.SysFont(font_type_outline, 30)
SMALLFONT2 = pygame.font.SysFont(font_type_outline, 15)

#this is arial, a little more impactful and clear, good for titles
BIGFONT3 = pygame.font.SysFont(font_type_arial, 50)
FONT3 = pygame.font.SysFont(font_type_arial, 30)
SMALLFONT3 = pygame.font.SysFont(font_type_arial, 15)

WindowsSizeOptions = [
'800 x 600', 
'1024 x 768', 
'1152 x 864', 
'1280 x 600',
'1280 x 800',
'1280 x 960',
'1280 x 1024',
'1360 x 768',
'1400 x 1050', 
'1600 x 900', 
'1680 x 1050', 
'1920 x 1080']
#endregion

#---------------------------------------------------------------------------------------------------------------------------

#region GAME STATE
'''The existing game states are:'''
game_state = "Main_Menu" 
#game_state = "Settings"
#game_state = "Scoreboard"
#game_state = "Credits"
#game_state = "Play"
#game_state = "Game_Over"
#game_state = "Tutorial"
#endregion

#---------------------------------------------------------------------------------------------------------------------------

#region CLASSES
'''
This is where I set up the classes. General speaking, we're using Buttons and cards.
In retrospect, I could build more classes and functions to create all of this, but
it is what it is.
'''

class Button:
    def __init__(self, text, x_pos, y_pos,enabled,height,length,color):
        self.text = text
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.enabled = enabled
        self.height = height
        self.length = length
        self.color = color

class Card:
    def __init__ (self, name, value, suit, type, cardimage):
        self.name = name
        self.value = value
        self.suit = suit
        self.type = type
        self.cardimage = cardimage

    def __str__(self):
        return f"{self.name} of {self.suit}"
#endregion

#---------------------------------------------------------------------------------------------------------------------------

#region SAVE FILES
'''
This is where anything save-file related is stored, loaded or changed.
'''
#Saves have the following indexes: 'SaveIndex', 'Name', 'Score'. 
# EX: ('Slot2', 'BRU', 15)
#Check the example below to understand
'''
Save1=[]
Save2=[]
Save3=[]
Save4=[]
Save5=[]
Save6=[]
Save7=[]
Save8=[]
Save9=[]
Save10=[]
Saves=[Save1,Save2,Save3,Save4,Save5,Save6,Save7,Save8,Save9,Save10] -> which actually becomes
Saves=[["Slot1", "Name1", "Score1"],["Slot2", "Name2", "Score2"], ... ,["Slot10", "Name10", "Score10"]]
'''
rows = [] #row is a temporary list used to save the variables "Slot", "Name" and "Score"
Saves = [] #this is the list of lists of saves, just like the example above.
SaveFile = os.path.join(config_folder, "SaveFiles.csv")

#This is opening .csv file, reordering the saves, saving on the Saves List and putting it back organized into the .csv file.
with open(SaveFile, newline='') as file:
    reader = csv.reader(file)
    header = next(reader) #skips the header
    for row in reader:
            #row = [Slot2', 'BRU', '20']
            if row[2] == '-inf' or row[2] == 'inf':
                savescore = float('-inf')
            else:
                savescore = int(row[2])
            Saves.append([row[0], row[1], savescore]) #this is creating a list with 3 values as STR, called Slot, Name and Score.
            #Score null is assigned as infinite negative for ordering reasons

Saves.sort(key=lambda x: (-x[2], x[1])) #sorts by score (desc), then name (asc)

for i, row in enumerate(Saves, start= 1): #Reassignes values
    row[0] = f"Save{i}" 

with open(SaveFile, 'w', newline='') as file: #Writes back save files
    writer = csv.writer(file)
    writer.writerow(["Slot", "Name", "Score"])

    for row in Saves:
        if row[2] == float("-inf"):
            savescore = '-inf'
        else:
            savescore = str(row[2])
        writer.writerow([row[0], row[1], savescore])
#endregion

#---------------------------------------------------------------------------------------------------------------------------

#region FUNCTIONS
'''
All functions that do not need to be specifically inside a part of the code are grouped here.
In retrospect, more of the code should be done with functions, but it's something I'm still not 100% used to do.
'''

def DrawBackground(): #this function gets the current background in the config file and saves it in variables
    global BGName,BGNameCropped, BGImage, background_folder, ConfigFile
    BGName = next((line.split('=')[1].strip() for line in open(ConfigFile, 'r') if line.startswith('BACKGROUND =')), "1-Dice.png") #this fetches the exact name of the '.png' currently being used in the config file, default to 1-Dice.png if not found or empty
    BGNameCropped = BGName.split("-")[1].split(".")[0] #this is just the name of the image file. EX: 'Dice'
    print(f"Current Background (variable 'BGNameCropped'): {BGNameCropped}")
    BGImage = os.path.join(background_folder, BGName) #this is the default BG

DrawBackground()

def get_backgrounds(folder_path): #this function gets all the images in the backgrounds folder and sorts it in a nice list of dictionaries
    global backgrounds
    print(f"DEBUG: Searching for backgrounds in: {folder_path}")
    print(f"DEBUG: Folder exists: {os.path.exists(folder_path)}")
    '''
    This function is getting a list of dictionaries such as:
    [
        {"path": "C:\\your\\folder\\1-Dice.png", "name": "Dice"},
        {"path": "C:\\your\\folder\\2-Castle.png", "name": "Castle"},
        {"path": "C:\\your\\folder\\3-Dungeon.png", "name": "Dungeon"}
    ]
    '''
    backgrounds = []
    BGReversedName = '' #I ended up not using this, as I can reverse names and lists with functions. Nevertheless, it's here.

    for file in os.listdir(folder_path):
        if file.lower().endswith(".png") or file.lower().endswith(".jpg"):
            full_path = os.path.join(folder_path, file)

            #Split filename
            name_part = file.rsplit(".", 1)[0] #removes the extension
            try:
                number, name = name_part.split("-", 1) #splits into number and name
                print(f"DEBUG: Found background - number: {number}, name: {name}")
            except ValueError:
                #Skips files that don't match the pattern
                print(f"DEBUG: Skipped file (wrong format): {file}")
                continue
        
            backgrounds.append({
                "path": full_path,
                "name": name
            })
    
    print(f"DEBUG: Total backgrounds found: {len(backgrounds)}")
    return backgrounds

get_backgrounds(background_folder)

def capturingindex():
    global backgrounds, BGNameCropped, BGIndex
    '''
    The index is the position it has in the backgrounds' folder.
    Remember that a 3 len list has the indexes 0, 1 and 2.
    '''
    capturingindex_counter = 0
    for i in backgrounds:
        capturingindex_counter += 1
        if i["name"] == BGNameCropped:
            BGIndex = backgrounds.index(i) 
            print(f"Match found. Current background is:{i["name"]}")
            '''
            this is the index of the current background in the list of backgrounds,
            it is used to move between backgrounds in the settings menu
            '''
        else:
            print(f"Iteration {capturingindex_counter}. Name used: {i["name"]}. Not a match with Current Background.")

capturingindex()

def BuildDeckImage():
    global DI, DeckImage, DeckName, DeckTitle, Current_Deck, deck_image1, deck_image2, image_folder, ConfigFile, Image_Folders
    
    DeckName = next((line.split('=')[1].strip() for line in open(ConfigFile, 'r') if line.startswith('DECK IMAGE =')), "MonstersDeck") #this fetches the current deck name in the config file, default to "RedDeck" if not found or empty
    DeckTitle = DeckName #this is used later on to change the type of deck
    Current_Deck = os.path.join(image_folder, DeckName) #this fetches the current Deck FOLDER from the txt
    deck_image1 = os.path.join(Current_Deck,'cardback.png') #this is the image that is shown in the change deck image menu. This is the Back
    deck_image2 = os.path.join(Current_Deck,'ace_of_spades.png') #this is the image that is shown in the change deck image menu. This is the Ace
    DeckImage = os.path.join(Current_Deck, "cardback.png")
    DI = pygame.transform.scale(pygame.image.load(DeckImage), (CW, CH)) #Despite I normally build images in the #IMAGES, this is here
    #cause I need to rebuild the deck image after running the function. 

BuildDeckImage()

def ReadHUD():
    #reads the config file for HUD. saves it on HUDToggle, that can be "ON" or "OFF"
    global HUDToggle, ConfigFile
    with open(ConfigFile, 'r') as file:
        for line in file:
            line = line.strip()
            
            if line.startswith("HUD"):
                # Split at '=' and clean spaces
                _, HUDToggle = line.split('=')
                HUDToggle = HUDToggle.strip()
                
                # Convert to boolean
                if HUDToggle == "ON":
                    return True
                elif HUDToggle == "OFF":
                    return False

ReadHUD()

def ToggleHUD():
    #toggles the HUD from ON to OFF, changing a local variable called HUDToggle
    global HUDToggle, ConfigFile
    lines = []

    with open(ConfigFile, 'r') as file:
        for line in file:
            stripped = line.strip()

            if stripped.startswith("HUD"):
                key, value = stripped.split('=')
                value = value.strip()

                # Toggle value
                if value == "ON":
                    new_line = f"{key.strip()} = OFF\n"
                elif value == "OFF":
                    new_line = f"{key.strip()} = ON\n"
                else:
                    new_line = line  # unexpected value, keep as is
            else:
                new_line = line

            lines.append(new_line)

    # Rewrite file with updated content
    with open(ConfigFile, 'w') as file:
        file.writelines(lines)

def ReadTEXT():
    #reads the config file for TEXT. saves it on TEXTToggle, that can be "ON" or "OFF"
    global TEXTToggle, ConfigFile
    with open(ConfigFile, 'r') as file:
        for line in file:
            line = line.strip()
            
            if line.startswith("TEXT"):
                # Split at '=' and clean spaces
                _, TEXTToggle = line.split('=')
                TEXTToggle = TEXTToggle.strip()
                
                # Convert to boolean
                if TEXTToggle == "ON":
                    return True
                elif TEXTToggle == "OFF":
                    return False

ReadTEXT()

def ToggleTEXT():
    #toggles the TEXT from ON to OFF, changing a local variable called TEXTToggle
    global TEXTToggle, ConfigFile
    lines = []

    with open(ConfigFile, 'r') as file:
        for line in file:
            stripped = line.strip()

            if stripped.startswith("TEXT"):
                key, value = stripped.split('=')
                value = value.strip()

                # Toggle value
                if value == "ON":
                    new_line = f"{key.strip()} = OFF\n"
                elif value == "OFF":
                    new_line = f"{key.strip()} = ON\n"
                else:
                    new_line = line  # unexpected value, keep as is
            else:
                new_line = line

            lines.append(new_line)

    # Rewrite file with updated content
    with open(ConfigFile, 'w') as file:
        file.writelines(lines)

def Build_WS_Arrows():
    global WSArrow1, WSArrow2, WSArrow3, WSArrow4, WSArrow5, WSArrow6, WSArrow7, WSArrow8, WSArrow9, WSArrow10, WSArrow11, WSArrow12
    global WSArrowSlots
    global HEIGHT
    global WSIncrement, InitialOffset, Centralizer, Corrector

    WSArrow1  = [1,(240+Corrector),(0.10*HEIGHT + 10+17.5),800,600] #y:orangebox.y + padding (10) + half the arrow (17.5)
    WSArrow2  = [2,(240+Corrector),(0.10*HEIGHT + 10+17.5+WSIncrement*1),1024,768]
    WSArrow3  = [3,(240+Corrector),(0.10*HEIGHT + 10+17.5+WSIncrement*2),1152,864]
    WSArrow4  = [4,(240+Corrector),(0.10*HEIGHT + 10+17.5+WSIncrement*3),1280,600]
    WSArrow5  = [5,(240+Corrector),(0.10*HEIGHT + 10+17.5+WSIncrement*4),1280,800]
    WSArrow6  = [6,(240+Corrector),(0.10*HEIGHT + 10+17.5+WSIncrement*5),1280,960]
    WSArrow7  = [7,(240+Corrector),(0.10*HEIGHT + 10+17.5+WSIncrement*6),1280,1024]
    WSArrow8  = [8,(240+Corrector),(0.10*HEIGHT + 10+17.5+WSIncrement*7),1360,768]
    WSArrow9  = [9,(240+Corrector),(0.10*HEIGHT + 10+17.5+WSIncrement*8),1400,1050]
    WSArrow10  = [10,(240+Corrector),(0.10*HEIGHT + 10+17.5+WSIncrement*9),1600,900]
    WSArrow11  = [11,(240+Corrector),(0.10*HEIGHT + 10+17.5+WSIncrement*10),1680,1050]
    WSArrow12 = [12,(240+Corrector),(0.10*HEIGHT + 10+17.5+WSIncrement*11),1920,1080]

    WSArrowSlots = [WSArrow1,
                    WSArrow2,
                    WSArrow3,
                    WSArrow4,
                    WSArrow5,
                    WSArrow6,
                    WSArrow7,
                    WSArrow8,
                    WSArrow9,
                    WSArrow10,
                    WSArrow11,
                    WSArrow12]

Build_WS_Arrows()

def toggle_sound():
    global sound_enabled
    
    sound_enabled = not sound_enabled #this is a toggle that switches between TRUE and FALSE

    if sound_enabled:
        mixer.music.set_volume(1.0) #full volume
        mixer.set_num_channels(8) #opens all sound effects
    elif not sound_enabled:
        mixer.music.set_volume(0.0) #mute music
        mixer.set_num_channels(0) #mutes all sound effects

def RebuildHeightDimensions():
    global WIDTH, HEIGHT
    pass

def decrement_first_index(expression):
    '''
    This function only works (so far) with the DiscardPileSlot, and aims to find the position
    of the index and substract it by one.
    '''
    global DiscardPileSlot

    counter = 0

    for i in DiscardPileSlot:
        if expression == i.cardimage:
            index = counter
            break
        else:
            counter += 1
            continue

    try:
        new_expression = DiscardPileSlot[index-1].cardimage
    except:
        print("Error: could not decrement the index.")

    return new_expression

def increment_first_index(expression):
    '''
    This function only works (so far) with the DiscardPileSlot, and aims to find the position
    of the index and adds it by one.
    '''
    global DiscardPileSlot

    counter = 0
    
    for i in DiscardPileSlot:
        if expression == i.cardimage:
            index = counter
            break
        else:
            counter += 1
            continue

    try:
        new_expression = DiscardPileSlot[index+1].cardimage
    except:
        print("Error: could not decrement the index.")

    return new_expression

def drawlink(surface, text, url, pos, hovered):
    global BLUE, LIGHT_BLUE, DARK_BLUE
    color = LIGHT_BLUE if hovered else BLUE
    link_text = SMALLFONT.render(text, True, color)
    rect = link_text.get_rect(topleft=pos)

    #draw underline
    underline_y = rect.bottom - 2
    pygame.draw.line(surface, color, (rect.left, underline_y), (rect.right, underline_y), 1)

    surface.blit(link_text, pos)
    return rect

#endregion

#---------------------------------------------------------------------------------------------------------------------------

#region SOUND
'''
This is where I store anything sound/music related.
It's also where we use the mixer
'''
mixer.music.set_volume(1.0)
mixer.set_num_channels(8) #these are all channels for sound effects
sound_enabled = True
#endregion

#---------------------------------------------------------------------------------------------------------------------------

#region BUTTONS, ICONS, FLAGS AND SCREENS

'''
This is where we store all the buttons, icons, screens and some flags.
Most of the code is done by activating and deactivating flags and buttons.
We also store some key values, some of them fixed, some of them based on WIDTH and HEIGHT
'''

#General
ArrowCondition = False
ArrowSlot = None
ShowDamage = False
ShowLifegain = False

#Deck Image
DIArrowCondition = False
DISelectorMode = False
DIOrangeBoxSet_Enabled = False
DIConfirmationBox_Enabled = False

DISpacing = 24
DIOrangeBoxWIDTH = 0.25*WIDTH
DIOrangeBoxHEIGHT = 0.25*HEIGHT
DeckImageWidth = 0.125*WIDTH
DeckImageHeight = DeckImageWidth*(7/5)
DIApplyButton = Button("Apply",(0.50*WIDTH-DISpacing-DeckImageWidth/2-CW/2),(0.75*HEIGHT-20),True,20,CW,ORANGE)
DICancelButton = Button("Cancel",(0.50*WIDTH+DISpacing+DeckImageWidth/2-CW/2),(0.75*HEIGHT-20),True,20,CW,ORANGE)
Button_Rect_AR, Button_Rect_AL = None, None

DIConfirmationBox_Width = 328
DIConfirmationBox_Height = 220
DIOKButton = Button("OK",((0.5*WIDTH-DIConfirmationBox_Width/2)+DISpacing),(0.5*HEIGHT+0.5*DIConfirmationBox_Height-20),True,20,CW,ORANGE)

#Window Settings
WSSelectorMode = False
WSArrowCondition = False
WSOrangeBoxSet_Enabled = False
WSArrowSlot = None

WSConfirmationBox_Width = 328
WSConfirmationBox_Height = 220
WSSpacing = 24
WSOKButton = Button("OK",((0.5*WIDTH-WSConfirmationBox_Width/2)+WSSpacing),(0.5*HEIGHT+0.5*WSConfirmationBox_Height-20),True,20,CW,ORANGE)
WSCancelButton = Button("Cancel",((0.5*WIDTH-WSConfirmationBox_Width/2)+2*WSSpacing+CW),(0.5*HEIGHT+0.5*WSConfirmationBox_Height-20),True,20,CW,ORANGE)
WSConfirmationBox_Enabled = False

#Background
BGSelectorMode = False
BGConfirmationBox_Width = 328
BGConfirmationBox_Height = 220
BGSpacing = 24
BGOKButton = Button("OK",((0.5*WIDTH-BGConfirmationBox_Width/2)+BGSpacing),(0.5*HEIGHT+0.5*BGConfirmationBox_Height-20),True,20,CW,ORANGE)
BGConfirmationBox_Enabled = False

BGOrangeBoxWIDTH = 0.25*WIDTH
BGOrangeBoxHEIGHT = 0.25*HEIGHT
BGImage_Width = 0.30*WIDTH
BGImage_Height = BGImage_Width *(9/16)
BGApplyButton = Button("Apply",(0.3750*WIDTH-CW/2),(0.75*HEIGHT-20),True,20,CW,ORANGE)
BGCancelButton = Button("Cancel",(0.6250*WIDTH-CW/2),(0.75*HEIGHT-20),True,20,CW,ORANGE)
Button_Rect_AR, Button_Rect_AL = None, None
BGOrangeBoxSet_Enabled = False
BGNameBackground = None
BGArrowCondition = False

#PlayScreen
PSsound_enabled = True
PStips_enabled = True
PShud_enabled = True
PlayGameTexts_Enabled = False
PlaySettingsBox_Enabled = False
PlayMenuConfirmationBox_Enabled = False
PlayMenuConfirmationBox_Text = ''
PSHUDText = ''
PlayMenuConfirmationFlag = ''
DrawingCardsButton = Button("Draw",80,(60+CH+20),True,20,CW,ORANGE) #1 from the top
PlaySettingsButton = Button("Settings",80,(60+CH+20+30),True,20,CW,ORANGE) #2 from the top
SeeDiscardPileButton = Button("See Discard Pile",(WIDTH - CW - 20), HEIGHT-100-CH + 35, True, 20, CW, ORANGE) #on the bottom-right
#The difference between buttons is 30, which is the height of the buttons (20) + the space between them (10)

PlayingSettingsBoxWIDTH = 10 + CW + 10
PlayingSettingsBoxHEIGHT = 6*(10+20)+10

ReturntoGameButton = Button("Return to Game",((WIDTH/2)-PlayingSettingsBoxWIDTH/2+10),(HEIGHT/2-PlayingSettingsBoxHEIGHT/2+10+0*(20+10)),True,20,CW,ORANGE) #1 button
MainMenuPlayButton = Button("Main Menu",((WIDTH/2)-PlayingSettingsBoxWIDTH/2+10),(HEIGHT/2-PlayingSettingsBoxHEIGHT/2+10+1*(20+10)),True,20,CW,ORANGE) #2 button
HUDToggleButton = Button("HUD",((WIDTH/2)-PlayingSettingsBoxWIDTH/2+10),(HEIGHT/2-PlayingSettingsBoxHEIGHT/2+10+2*(20+10)),True,20,CW,ORANGE) #3 button
TipsToggleButton = Button("Tips",((WIDTH/2)-PlayingSettingsBoxWIDTH/2+10),(HEIGHT/2-PlayingSettingsBoxHEIGHT/2+10+3*(20+10)),True,20,CW,ORANGE) #4 button
SoundToggleButton = Button("Sound",((WIDTH/2)-PlayingSettingsBoxWIDTH/2+10),(HEIGHT/2-PlayingSettingsBoxHEIGHT/2+10+4*(20+10)),True,20,CW,ORANGE) #5 button
QuitGamePlayButton = Button("Quit",((WIDTH/2)-PlayingSettingsBoxWIDTH/2+10),(HEIGHT/2-PlayingSettingsBoxHEIGHT/2+10+5*(20+10)),True,20,CW,ORANGE) #6 button

PSSpacing = 24
PlayingConfirmationBoxWIDTH = 0.25*WIDTH
PlayingConfirmationBoxHEIGHT = 0.25*HEIGHT
PlayMenuConfirmationBox_YesButton = Button("Yes",(0.50*WIDTH-(PlayingConfirmationBoxWIDTH/4)-CW/2),(0.625*HEIGHT-20),True,20,CW,ORANGE)
PlayMenuConfirmationBox_NoButton = Button("No",(0.50*WIDTH+(PlayingConfirmationBoxWIDTH/4)-CW/2),(0.625*HEIGHT-20),True,20,CW,ORANGE)

#Game Over
GOMainMenuButton = Button("Main Menu",((WIDTH/2)-(CW/2)-15),(HEIGHT*0.65)+20,False,20,CW,ORANGE)
GOScoreboardButton = Button("Scoreboard",((WIDTH/2)-(CW/2)-15),((HEIGHT*0.65)+45),False,20,CW,ORANGE)
GOQuitButton = Button("Quit",((WIDTH/2)-(CW/2)-15),((HEIGHT*0.65)+70),False,20,CW,ORANGE)   

#Discard Pile 
DiscardPileSeeBox_Enabled = False
DiscardPileSeeBoxWIDTH = CW *3 + 10 * 4 + 40 * 2 #10 is the spacing between card-card and card-arrow, 40 is the arrow width (2 of those) and CW is for the 3 cards that appear
DiscardPileSeeBoxHEIGHT = 10 + CH + 10
DiscardImage1 = None
DiscardImage2 = None
DiscardImage3 = None

#Scoreboard
'''
This is the scoreboard after finishing a game. It's different than the scoreboard you
access trough the settings. That one is above, called 'Settings Scoreboard'
'''
SC_MainMenuButton = Button("Main Menu",(((0.075*WIDTH)-(CW/2))),(0.15*HEIGHT),True,20,CW,ORANGE)    
SC_SaveGameButton = Button("Save Game",(((0.075*WIDTH)-(CW/2))),((0.15*HEIGHT)+25*1),True,20,CW,ORANGE)    
SC_DeleteGameButton = Button("Delete Save",(((0.075*WIDTH)-(CW/2))),((0.15*HEIGHT)+25*2),True,20,CW,ORANGE)    
SC_QuitButton = Button("Quit",(((0.075*WIDTH)-(CW/2))),((0.15*HEIGHT)+25*3),True,20,CW,ORANGE)

DeleteConfirmationBox_Width = 328
DeleteConfirmationBox_Height = 220
DeleteSpacing = 24
DeleteYesButton = Button("Apply",(0.50*WIDTH-(DeleteConfirmationBox_Width/4)-CW/2),(0.50*HEIGHT+(DeleteConfirmationBox_Height/2)-20),True,20,CW,ORANGE)
DeleteNoButton = Button("Cancel",(0.50*WIDTH+(DeleteConfirmationBox_Width/4)-CW/2),(0.50*HEIGHT+(DeleteConfirmationBox_Height/2)-20),True,20,CW,ORANGE)
DeleteConfirmationBoxEnabled = False

WritingMode = False
SaveSelectorMode = False
SaveDeleteMode = False
DeleteMode = False

#Settings Scoreboard
STSC_MainMenuButton = Button("Main Menu",(((0.075*WIDTH)-(CW/2))),(0.15*HEIGHT),True,20,CW,ORANGE)

#Tutorial

#Settings
#Button Positions: these are the X and Y of the Buttons from the settings menu (ST)
ButtonPosition1 = [50, 50]  #Go Back
ButtonPosition2 = [50, 80]  #Controls
ButtonPosition3 = [50, 110] #Window Size
ButtonPosition4 = [50, 140] #Sound
ButtonPosition5 = [50, 170] #Background
ButtonPosition6 = [50, 200] #Deck
ButtonPosition7 = [50, 230] #Extra Button 1: not used
ButtonPosition8 = [50, 270] #Extra Button 2: not used

STEscapeButton = Button("Go Back",ButtonPosition1[0], ButtonPosition1[1],True,20,CW,ORANGE)
STControlsButton = Button("Controls",ButtonPosition2[0], ButtonPosition2[1],True,20,CW,ORANGE)
STWindowSizeButton = Button("Window Size",ButtonPosition3[0], ButtonPosition3[1],True,20,CW,ORANGE)
STSoundButton = Button("Sound",ButtonPosition4[0], ButtonPosition4[1],True,20,CW,ORANGE)
STBackgroundButton = Button("Background",ButtonPosition5[0], ButtonPosition5[1],True,20,CW,ORANGE)
STDeckImageButton = Button("Deck Image",ButtonPosition6[0], ButtonPosition6[1],True,20,CW,ORANGE)

OrangeBoxSet_Enabled = False #this is the first orange box ever used, and it's used for the controls part of the game; that's why it is the original/does not have a control in the variable name

#endregion

#---------------------------------------------------------------------------------------------------------------------------

#region CARDS AND SLOTS
'''
This is where we save the cards, decks and basic slots
'''
Suits = ("Clubs","Diamond","Hearts","Spades")
Value = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14) #11, 12, 13 and 14 are Jack, Queen, King and Ace respectively
Type = ("Monster", "Weapon", "Potion") #Spades and Clubs are Monsters, Diamondss are Weapons and Hearts are Potions

Deck = [
    Card("2", 2, "Diamonds", "Weapon","2_of_diamonds.png"),
    Card("2", 2, "Spades", "Monster", "2_of_spades.png"),
    Card("2", 2, "Clubs", "Monster","2_of_clubs.png"),
    Card("2", 2, "Hearts", "Potion","2_of_hearts.png"),

    Card("3", 3, "Diamonds", "Weapon","3_of_diamonds.png"),
    Card("3", 3, "Spades", "Monster", "3_of_spades.png"),
    Card("3", 3, "Clubs", "Monster","3_of_clubs.png"),
    Card("3", 3, "Hearts", "Potion","3_of_hearts.png"),   

    Card("4", 4, "Diamonds", "Weapon","4_of_diamonds.png"),
    Card("4", 4, "Spades", "Monster","4_of_spades.png"),
    Card("4", 4, "Clubs", "Monster","4_of_clubs.png"),
    Card("4", 4, "Hearts", "Potion","4_of_hearts.png" ),   

    Card("5", 5, "Diamonds", "Weapon","5_of_diamonds.png"),
    Card("5", 5, "Spades", "Monster","5_of_spades.png"),
    Card("5", 5, "Clubs", "Monster","5_of_clubs.png"),
    Card("5", 5, "Hearts", "Potion","5_of_hearts.png"),  

    Card("6", 6, "Diamonds", "Weapon","6_of_diamonds.png"),
    Card("6", 6, "Spades", "Monster","6_of_spades.png"),
    Card("6", 6, "Clubs", "Monster","6_of_clubs.png"),
    Card("6", 6, "Hearts", "Potion","6_of_hearts.png"), 

    Card("7", 7, "Diamonds", "Weapon","7_of_diamonds.png"),
    Card("7", 7, "Spades", "Monster","7_of_spades.png"),
    Card("7", 7, "Clubs", "Monster","7_of_clubs.png"),
    Card("7", 7, "Hearts", "Potion","7_of_hearts.png"),   

    Card("8", 8, "Diamonds", "Weapon","8_of_diamonds.png"),
    Card("8", 8, "Spades", "Monster","8_of_spades.png"),
    Card("8", 8, "Clubs", "Monster","8_of_clubs.png"),
    Card("8", 8, "Hearts", "Potion","8_of_hearts.png"),   

    Card("9", 9, "Diamonds", "Weapon","9_of_diamonds.png"),
    Card("9", 9, "Spades", "Monster","9_of_spades.png"),
    Card("9", 9, "Clubs", "Monster","9_of_clubs.png"),
    Card("9", 9, "Hearts", "Potion","9_of_hearts.png"),   

    Card("10", 10, "Diamonds", "Weapon","10_of_diamonds.png"),
    Card("10", 10, "Spades", "Monster","10_of_spades.png"),
    Card("10", 10, "Clubs", "Monster","10_of_clubs.png"),
    Card("10", 10, "Hearts", "Potion","10_of_hearts.png"),  

    Card("Jack", 11, "Clubs", "Monster","jack_of_clubs.png"),
    Card("Jack", 11, "Spades", "Monster","jack_of_spades.png"),   

    Card("Queen", 12, "Clubs", "Monster","queen_of_clubs.png"),
    Card("Queen", 12, "Spades", "Monster","queen_of_spades.png"),   

    Card("King", 13, "Clubs", "Monster", "king_of_clubs.png"),
    Card("King", 13, "Spades", "Monster", "king_of_spades.png"),  

    Card("Ace", 14, "Clubs", "Monster", "ace_of_clubs.png"),
    Card("Ace", 14, "Spades", "Monster", "ace_of_spades.png"),  
]

OriginalDeck = copy.deepcopy(Deck) #this is to make sure we always have a 'default' deck to go back to

Slot1 = []
Slot2 = []
Slot3 = []
Slot4 = []
Slots = [Slot1, Slot2, Slot3, Slot4]
SlotCounter = 0 #this is to move from one slot to another

DiscardPileSlot = []
EquipSlot = []
ExperienceSlots = []
ReversedES =[]
#endregion

#---------------------------------------------------------------------------------------------------------------------------

#region IMAGES
HPImage = os.path.join(image_folder, "Heart.jpg") 
HP = pygame.transform.scale(pygame.image.load(HPImage), (80, 80))
TestImage1 = os.path.join(Current_Deck, 'ace_of_spades.png')
TI1 = pygame.transform.scale(pygame.image.load(TestImage1), (80, 80))
#endregion

#---------------------------------------------------------------------------------------------------------------------------

#MAIN MENU SCREEN
def draw_menu(mouse_pos, LeftClick):
    global game_state, HealthPoints, Score, Flag, elapsed_time, start_time, SlotCounter, PotionCounter, DButtonLock, BGImage, PlayGameTexts_Enabled
    global HUDToggle, ConfigFile, ReadHUD, HUDToggle, ReadTEXT, TEXTToggle, TutorialPage

    #BGImage is being set in the beginning of the code
    BG = pygame.transform.scale(pygame.image.load(BGImage).convert(), (WIDTH, HEIGHT))
    WIN.blit(BG, (0, 0)) 

    TitleImage = os.path.join(image_folder,"Title.jpg")
    TI = pygame.transform.scale(pygame.image.load(TitleImage), (WIDTH*0.50, HEIGHT*0.5))
    WIN.blit(TI, (WIDTH*0.25, HEIGHT*0.20))

    #BUTTONS
    PlayButton = Button("Play",((WIDTH/2)-(CW/2)),(HEIGHT*0.60),True,20,CW,ORANGE)
    SettingsButton = Button("Settings",((WIDTH/2)-(CW/2)),((HEIGHT*0.60)+25*1),True,20,CW,ORANGE)
    ScoreboardButton = Button("Scoreboard",((WIDTH/2)-(CW/2)),((HEIGHT*0.60)+25*2),True,20,CW,ORANGE)
    TutorialButton = Button("Tutorial",((WIDTH/2)-(CW/2)),((HEIGHT*0.60)+25*3),True,20,CW,ORANGE)
    CreditsButton = Button("Credits",((WIDTH/2)-(CW/2)),((HEIGHT*0.60)+25*4),True,20,CW,ORANGE)
    QuitButton = Button("Quit",((WIDTH/2)-(CW/2)),((HEIGHT*0.60)+25*5),True,20,CW,ORANGE)

    #PlayButton
    button_text = SMALLFONT.render(PlayButton.text, True, BLACK) #text
    text_rect = button_text.get_rect(center=(PlayButton.x_pos + PlayButton.length//2, PlayButton.y_pos + PlayButton.height//2))
    button_rect = pygame.rect.Rect((PlayButton.x_pos,PlayButton.y_pos),(PlayButton.length,PlayButton.height))
    bcolor = PlayButton.color
    if button_rect.collidepoint(mouse_pos):
        if LeftClick:
            bcolor = DARK_ORANGE
            HealthPoints = StartingHealthPoints
            Deck[:] = OriginalDeck[:]
            random.shuffle(Deck)
            Slot1.clear()
            Slot2.clear()
            Slot3.clear()
            Slot4.clear()
            DiscardPileSlot.clear()
            EquipSlot.clear()
            ExperienceSlots.clear()
            ReversedES.clear()
            ReadHUD()
            ReadTEXT()
            #.
            SlotCounter = 0
            PotionCounter = 0
            DButtonLock = 0
            Score = 0
            Flag = 0
            #.
            DrawingEachTurn = True
            DrawingCardsButton.enabled = True
            PlaySettingsButton.enabled = True
            #.
            HUDToggleButton.enabled = False
            MainMenuPlayButton.enabled = False
            HUDToggleButton.enabled = False
            TipsToggleButton.enabled = False 
            SoundToggleButton.enabled = False
            QuitGamePlayButton.enabled = False
            #.
            GOMainMenuButton.enabled = False
            GOScoreboardButton.enabled = False
            GOQuitButton.enabled = False
            elapsed_time = 0
            start_time = time.time()
            game_state = "Play"
        else:
            bcolor = LIGHT_ORANGE
    pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
    pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
    WIN.blit(button_text, text_rect) #text and position

    #SettingsButton    
    button_text = SMALLFONT.render(SettingsButton.text, True, BLACK)
    text_rect = button_text.get_rect(center=(SettingsButton.x_pos + SettingsButton.length//2, SettingsButton.y_pos + SettingsButton.height//2))
    button_rect = pygame.rect.Rect((SettingsButton.x_pos,SettingsButton.y_pos),(SettingsButton.length,SettingsButton.height))
    bcolor = SettingsButton.color
    if button_rect.collidepoint(mouse_pos):
        if LeftClick:
            bcolor = DARK_ORANGE
            game_state = "Settings"
        else:
            bcolor = LIGHT_ORANGE
    pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
    pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
    WIN.blit(button_text, text_rect)

    #ScoreboardButton
    button_text = SMALLFONT.render(ScoreboardButton.text, True, BLACK)
    text_rect = button_text.get_rect(center=(ScoreboardButton.x_pos + ScoreboardButton.length//2, ScoreboardButton.y_pos + ScoreboardButton.height//2))
    button_rect = pygame.rect.Rect((ScoreboardButton.x_pos,ScoreboardButton.y_pos),(ScoreboardButton.length,ScoreboardButton.height))
    bcolor = ScoreboardButton.color
    if button_rect.collidepoint(mouse_pos):
        if LeftClick:
            bcolor = DARK_ORANGE
            game_state = "Settings Scoreboard"           
        else:
            bcolor = LIGHT_ORANGE
    pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
    pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
    WIN.blit(button_text, text_rect)

    #TutorialButton    
    button_text = SMALLFONT.render(TutorialButton.text, True, BLACK)
    text_rect = button_text.get_rect(center=(TutorialButton.x_pos + TutorialButton.length//2, TutorialButton.y_pos + TutorialButton.height//2))
    button_rect = pygame.rect.Rect((TutorialButton.x_pos,TutorialButton.y_pos),(TutorialButton.length,TutorialButton.height))
    bcolor = TutorialButton.color
    if button_rect.collidepoint(mouse_pos):
        if LeftClick:
            bcolor = DARK_ORANGE
            game_state = "Tutorial"
            TutorialPage = 1
        else:
            bcolor = LIGHT_ORANGE
    pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
    pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
    WIN.blit(button_text, text_rect)

    #CreditsButton
    button_text = SMALLFONT.render(CreditsButton.text, True, BLACK)
    text_rect = button_text.get_rect(center=(CreditsButton.x_pos + CreditsButton.length//2, CreditsButton.y_pos + CreditsButton.height//2))
    button_rect = pygame.rect.Rect((CreditsButton.x_pos,CreditsButton.y_pos),(CreditsButton.length,CreditsButton.height))
    bcolor = CreditsButton.color
    if button_rect.collidepoint(mouse_pos):
        if LeftClick:
            bcolor = DARK_ORANGE
            game_state = "Credits"
        else:
            bcolor = LIGHT_ORANGE
    pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
    pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
    WIN.blit(button_text, text_rect)

    #QuitButton
    button_text = SMALLFONT.render(QuitButton.text, True, BLACK)
    text_rect = button_text.get_rect(center=(QuitButton.x_pos + QuitButton.length//2, QuitButton.y_pos + QuitButton.height//2))
    button_rect = pygame.rect.Rect((QuitButton.x_pos,QuitButton.y_pos),(QuitButton.length,QuitButton.height))
    bcolor = QuitButton.color
    if button_rect.collidepoint(mouse_pos):
        if LeftClick:
            bcolor = DARK_ORANGE
            quit()
        else:
            bcolor = LIGHT_ORANGE
    pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
    pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
    WIN.blit(button_text, text_rect)

    #UPDATE
    pygame.display.update()
    return game_state

#---------------------------------------------------------------------------------------------------------------------------

#PLAY SCREEN
def draw_play(BG, elapsed_time, mouse_pos, LeftClick, RightClick):
    global HealthPoints, game_state, SlotCounter, PotionCounter, DButtonLock, Score, Flag, BGImage, PlayGameTexts_Enabled
    global PlayMenuConfirmationBox_Enabled, padding_y, padding_x, PlayMenuConfirmationFlag, PlayMenuConfirmationBox_YesButton, PlayMenuConfirmationBox_NoButton, QuitGamePlayButton
    global MainMenuPlayButton, TipsToggleButton, SoundToggleButton, HUDToggleButton, PShud_enabled, PStips_enabled, PSsound_enabled, PSHUDText, PlaySettingsBox_Enabled, PlaySettingsButton,PlayMenuConfirmationBox_Text
    global PlayingConfirmationBox, PlayingConfirmationBoxWIDTH, PlayingConfirmationBoxHEIGHT, PSSpacing, PlayMenuConfirmationBox_YesButton, PlayMenuConfirmationBox_NoButton
    global DrawingEachTurn, HUDToggle, ReadHUD, TEXTToggle, ReadTEXT, ShowDamage, ShowLifegain, LifegainTimer, DamageTimer, DLTimer, DamageValue, LifegainValue, DiscardPileSeeBox_Enabled, DiscardPileSeeBoxWIDTH, DiscardPileSeeBoxHEIGHT 
    global decrement_first_index, increment_first_index, DiscardImage1, DiscardImage2, DiscardImage3

    #BACKGROUND
    #BGImage = os.path.join(background_folder, "1-Dice.png") 
    BG = pygame.transform.scale(pygame.image.load(BGImage).convert(), (WIDTH, HEIGHT))
    WIN.blit(BG, (0, 0)) #Py Game starts the scren at top left as '0,0' and increasing the numbers in proportion with the width and heigth

    #CLOCK
    time_text = FONT.render(f"Time: {(round(elapsed_time))}s", 1, "white") #can use a ",1" or ",2" after the elapsed_time to round with the
    WIN.blit(time_text, ((WIDTH - 180), 20))

    #IMAGES AND TEXT
        
    #   Heart
    #HP is a 80, 80 image
    WIN.blit(HP, (40, (HEIGHT-100)))
    HealthValue = FONT.render(str(HealthPoints), True, WHITE)
    text_rect = HealthValue.get_rect(center=(80, (HEIGHT-65)))
    WIN.blit(HealthValue, text_rect)

    #   Texts
    TextsColor = WHITE

    DeckText = SMALLFONT3.render('Deck', True, TextsColor)
    SlotText = SMALLFONT3.render('Slots', True, TextsColor)
    ReminderText1 = SMALLFONT3.render('LEFT CLICK: Fight bare-handed OR find weapon/potion.', True, TextsColor)
    ReminderText2 = SMALLFONT3.render('RIGHT CLICK: Use weapon.', True, TextsColor)
    EquipText = SMALLFONT3.render('Equipment', True, TextsColor)
    GraveyardText = SMALLFONT3.render('Discard Pile', True, TextsColor)

    if TEXTToggle == "ON":
        WIN.blit(DeckText, ((80 + 0*(CW)+0*(CS)), (60-30)))
        WIN.blit(SlotText, ((80 + 1*(CW)+1*(CS) + 80),60-30))
        #.
        WIN.blit(ReminderText1, ((80 + 1*(CW)+1*(CS) + 80), 60+CH+30))
        WIN.blit(ReminderText2, ((80 + 1*(CW)+1*(CS) + 80), 60+CH+60))
        #.
        WIN.blit(EquipText, ((80 + 1*(CW)+1*(CS) + 60), (HEIGHT-CH-120-30)))
        #.
        WIN.blit(GraveyardText, ((WIDTH-CW-20), (80+CH)-30))

    if ShowDamage == True:
        if str(DamageValue) == "No Damage!":
            DamageText = FONT.render(str(DamageValue), True, WHITE)
            WIN.blit(DamageText, (40+80+5, HEIGHT-85))  
        else:
            DamageText = FONT.render(f" - {str(DamageValue)}", True, WHITE)
            WIN.blit(DamageText, (40+80+5, HEIGHT-85))
        #.
        if time.time() - DamageTimer >= DLTimer:
                ShowDamage = False

    if ShowLifegain == True:
        LifegainText = FONT.render(f"+ {str(LifegainValue)}", True, WHITE)
        WIN.blit(LifegainText, (40+80+5, HEIGHT-85))
        if time.time() - LifegainTimer >= DLTimer:
            ShowLifegain = False

    #DECK AND CARDS SLOTS
    CardOutline = os.path.join(image_folder, 'CardOutline.png')
    CardBorder = pygame.transform.scale(pygame.image.load(CardOutline), (CW, CH))

    if PShud_enabled == True:
        WIN.blit(CardBorder, ((80 + 1*(CW)+1*(CS) + 80), (60))) 

    if Slot1:
        Slot1Image = os.path.join(Current_Deck, Slot1[0].cardimage) 
        S1 = pygame.transform.scale(pygame.image.load(Slot1Image), (CW, CH))
        WIN.blit(S1, ((80 + 1*(CW)+1*(CS) + 80), (60))) 
        S1REC = S1.get_rect(topleft=((80 + 1*(CW)+1*(CS) + 80), (60)))
        if LeftClick and S1REC.collidepoint(mouse_pos) and HealthPoints > 0 and len(Slots) >= 2 and SlotCounter < 3:
            SlotCounter = SlotCounter + 1
            if Slot1[0].type == "Monster":
                DamageValue = Slot1[0].value
                DamageTimer = time.time()
                ShowDamage = True
                if HealthPoints - DamageValue > 0:
                    HealthPoints = HealthPoints - DamageValue
                elif DamageValue >= HealthPoints:
                    HealthPoints = 0
                DiscardPileSlot.append(Slot1.pop(0))
            elif Slot1[0].type == "Potion":
                if PotionCounter < 1:
                    LifegainValue = Slot1[0].value
                    LifegainTimer = time.time()
                    ShowLifegain = True
                    HealthPoints = HealthPoints + Slot1[0].value
                    PotionCounter = PotionCounter + 1
                    if HealthPoints > StartingHealthPoints:
                        HealthPoints = StartingHealthPoints
                elif PotionCounter == 1:
                    pass
                DiscardPileSlot.append(Slot1.pop(0))
            elif Slot1[0].type == "Weapon":
                if EquipSlot:
                    DiscardPileSlot.append(EquipSlot.pop(0))
                    EquipSlot.append(Slot1.pop(0))
                    if len(ExperienceSlots) > 0:
                        while ExperienceSlots:
                            DiscardPileSlot.append(ExperienceSlots.pop(0))                 
                else:
                    EquipSlot.append(Slot1.pop(0))
        if RightClick and S1REC.collidepoint(mouse_pos) and HealthPoints > 0 and len(Slots) >= 2 and SlotCounter < 3:
            if Slot1[0].type =="Monster":
                SlotCounter = SlotCounter + 1
                if EquipSlot:
                    if len(ExperienceSlots) == 0:
                        if Slot1[0].value >= EquipSlot[0].value: #if the monster is bigger than the weapon
                            DamageValue = Slot1[0].value - EquipSlot[0].value
                            DamageTimer = time.time()
                            ShowDamage = True
                            HealthPoints = HealthPoints - DamageValue
                            ExperienceSlots.append(Slot1.pop(0))
                        elif Slot1[0].value < EquipSlot[0].value: #if the monster is weaker than the weapon
                            DamageValue = "No Damage!"
                            DamageTimer = time.time()
                            ShowDamage = True
                            HealthPoints = HealthPoints
                            ExperienceSlots.append(Slot1.pop(0))
                    elif len(ExperienceSlots) >= 1:
                        ReversedES = list(reversed(ExperienceSlots))
                        if ReversedES[0].value > Slot1[0].value:
                            if Slot1[0].value >= EquipSlot[0].value: #if the monster is bigger than the weapon
                                DamageValue = Slot1[0].value - EquipSlot[0].value
                                DamageTimer = time.time()
                                ShowDamage = True
                                HealthPoints = HealthPoints - DamageValue
                                ExperienceSlots.append(Slot1.pop(0))
                            elif Slot1[0].value < EquipSlot[0].value: #if the monster is weaker than the weapon
                                DamageValue = "No Damage!"
                                DamageTimer = time.time()
                                ShowDamage = True
                                HealthPoints = HealthPoints
                                ExperienceSlots.append(Slot1.pop(0))
                        elif ReversedES[0].value <= Slot1[0].value:
                            pass
            elif not EquipSlot:
                pass
            elif Slot1[0].type == "Potion":
                pass
            elif Slot1[0].type == "Weapon":
                pass    

    if PShud_enabled == True:
        WIN.blit(CardBorder, ((80 + 2*(CW)+2*(CS) + 80), (60))) 

    if Slot2:
        Slot2Image = os.path.join(Current_Deck, Slot2[0].cardimage) 
        S2 = pygame.transform.scale(pygame.image.load(Slot2Image), (CW, CH))
        WIN.blit(S2, ((80 + 2*(CW)+2*(CS) + 80), (60))) 
        S2REC = S2.get_rect(topleft=((80 + 2*(CW)+2*(CS) + 80), (60)))
        if LeftClick and S2REC.collidepoint(mouse_pos) and HealthPoints > 0 and len(Slots) >= 2 and SlotCounter < 3:
            SlotCounter = SlotCounter + 1
            if Slot2[0].type == "Monster":
                DamageValue = Slot2[0].value
                DamageTimer = time.time()
                ShowDamage = True
                if HealthPoints - DamageValue > 0:
                    HealthPoints = HealthPoints - DamageValue
                elif DamageValue >= HealthPoints:
                    HealthPoints = 0
                DiscardPileSlot.append(Slot2.pop(0))
            elif Slot2[0].type == "Potion":
                if PotionCounter < 1:
                    LifegainValue = Slot2[0].value
                    LifegainTimer = time.time()
                    ShowLifegain = True
                    HealthPoints = HealthPoints + Slot2[0].value
                    PotionCounter = PotionCounter + 1
                    if HealthPoints > StartingHealthPoints:
                        HealthPoints = StartingHealthPoints
                elif PotionCounter == 1:
                    pass
                DiscardPileSlot.append(Slot2.pop(0))
            elif Slot2[0].type == "Weapon":
                if EquipSlot:
                    DiscardPileSlot.append(EquipSlot.pop(0))
                    EquipSlot.append(Slot2.pop(0))
                    if len(ExperienceSlots) > 0:
                        while ExperienceSlots:
                            DiscardPileSlot.append(ExperienceSlots.pop(0))                 
                else:
                    EquipSlot.append(Slot2.pop(0))
        if RightClick and S2REC.collidepoint(mouse_pos) and HealthPoints > 0 and len(Slots) >= 2 and SlotCounter < 3:
            if Slot2[0].type =="Monster":
                SlotCounter = SlotCounter + 1
                if EquipSlot:
                    if len(ExperienceSlots) == 0:
                        if Slot2[0].value >= EquipSlot[0].value: #if the monster is bigger than the weapon
                            DamageValue = Slot2[0].value - EquipSlot[0].value
                            DamageTimer = time.time()
                            ShowDamage = True
                            HealthPoints = HealthPoints - DamageValue
                            ExperienceSlots.append(Slot2.pop(0))
                        elif Slot2[0].value < EquipSlot[0].value: #if the monster is weaker than the weapon
                            DamageValue = "No Damage!"
                            DamageTimer = time.time()
                            ShowDamage = True
                            HealthPoints = HealthPoints
                            ExperienceSlots.append(Slot2.pop(0))
                    elif len(ExperienceSlots) >= 1:
                        ReversedES = list(reversed(ExperienceSlots))
                        if ReversedES[0].value > Slot2[0].value:
                            if Slot2[0].value >= EquipSlot[0].value: #if the monster is bigger than the weapon
                                DamageValue = Slot2[0].value - EquipSlot[0].value
                                DamageTimer = time.time()
                                ShowDamage = True
                                HealthPoints = HealthPoints - DamageValue
                                ExperienceSlots.append(Slot2.pop(0))
                            elif Slot2[0].value < EquipSlot[0].value: #if the monster is weaker than the weapon
                                DamageValue = "No Damage!"
                                DamageTimer = time.time()
                                ShowDamage = True
                                HealthPoints = HealthPoints
                                ExperienceSlots.append(Slot2.pop(0))
                        elif ReversedES[0].value <= Slot2[0].value:
                            pass
            elif not EquipSlot:
                pass
            elif Slot2[0].type == "Potion":
                pass
            elif Slot2[0].type == "Weapon":
                pass    
        
    if PShud_enabled == True:
        WIN.blit(CardBorder, ((80 + 3*(CW)+3*(CS) + 80), (60)))

    if Slot3:
        Slot3Image = os.path.join(Current_Deck, Slot3[0].cardimage) 
        S3 = pygame.transform.scale(pygame.image.load(Slot3Image), (CW, CH))
        WIN.blit(S3, ((80 + 3*(CW)+3*(CS) + 80), (60))) 
        S3REC = S3.get_rect(topleft=((80 + 3*(CW)+3*(CS) + 80), (60)))
        if LeftClick and S3REC.collidepoint(mouse_pos) and HealthPoints > 0 and len(Slots) >= 2 and SlotCounter < 3:
            SlotCounter = SlotCounter + 1
            if Slot3[0].type == "Monster":
                DamageValue = Slot3[0].value
                DamageTimer = time.time()
                ShowDamage = True
                if HealthPoints - DamageValue > 0:
                    HealthPoints = HealthPoints - DamageValue
                elif DamageValue >= HealthPoints:
                    HealthPoints = 0
                DiscardPileSlot.append(Slot3.pop(0))
            elif Slot3[0].type == "Potion":
                if PotionCounter < 1:
                    LifegainValue = Slot3[0].value
                    LifegainTimer = time.time()
                    ShowLifegain = True
                    HealthPoints = HealthPoints + Slot3[0].value
                    PotionCounter = PotionCounter + 1
                    if HealthPoints > StartingHealthPoints:
                        HealthPoints = StartingHealthPoints
                elif PotionCounter == 1:
                    pass
                DiscardPileSlot.append(Slot3.pop(0))
            elif Slot3[0].type == "Weapon":
                if EquipSlot:
                    DiscardPileSlot.append(EquipSlot.pop(0))
                    EquipSlot.append(Slot3.pop(0))
                    if len(ExperienceSlots) > 0:
                        while ExperienceSlots:
                            DiscardPileSlot.append(ExperienceSlots.pop(0))                 
                else:
                    EquipSlot.append(Slot3.pop(0))
        if RightClick and S3REC.collidepoint(mouse_pos) and HealthPoints > 0 and len(Slots) >= 2 and SlotCounter < 3:
            if Slot3[0].type =="Monster":
                SlotCounter = SlotCounter + 1
                if EquipSlot:
                    if len(ExperienceSlots) == 0:
                        if Slot3[0].value >= EquipSlot[0].value: #if the monster is bigger than the weapon
                            DamageValue = Slot3[0].value - EquipSlot[0].value
                            DamageTimer = time.time()
                            ShowDamage = True
                            HealthPoints = HealthPoints - DamageValue
                            ExperienceSlots.append(Slot3.pop(0))
                        elif Slot3[0].value < EquipSlot[0].value: #if the monster is weaker than the weapon
                            DamageValue = "No Damage!"
                            DamageTimer = time.time()
                            ShowDamage = True
                            HealthPoints = HealthPoints
                            ExperienceSlots.append(Slot3.pop(0))
                    elif len(ExperienceSlots) >= 1:
                        ReversedES = list(reversed(ExperienceSlots))
                        if ReversedES[0].value > Slot3[0].value:
                            if Slot3[0].value >= EquipSlot[0].value: #if the monster is bigger than the weapon
                                DamageValue = Slot3[0].value - EquipSlot[0].value
                                DamageTimer = time.time()
                                ShowDamage = True
                                HealthPoints = HealthPoints - DamageValue
                                ExperienceSlots.append(Slot3.pop(0))
                            elif Slot3[0].value < EquipSlot[0].value: #if the monster is weaker than the weapon
                                DamageValue = "No Damage!"
                                DamageTimer = time.time()
                                ShowDamage = True
                                HealthPoints = HealthPoints
                                ExperienceSlots.append(Slot3.pop(0))
                        elif ReversedES[0].value <= Slot3[0].value:
                            pass
            elif not EquipSlot:
                pass
            elif Slot3[0].type == "Potion":
                pass
            elif Slot3[0].type == "Weapon":
                pass    

    if PShud_enabled == True:
        WIN.blit(CardBorder, ((80 + 4*(CW)+4*(CS) + 80), (60)))      

    if Slot4:
        Slot4Image = os.path.join(Current_Deck, Slot4[0].cardimage) 
        S4 = pygame.transform.scale(pygame.image.load(Slot4Image), (CW, CH))
        WIN.blit(S4, ((80 + 4*(CW)+4*(CS) + 80), (60))) 
        S4REC = S4.get_rect(topleft=((80 + 4*(CW)+4*(CS) + 80), (60)))
        if LeftClick and S4REC.collidepoint(mouse_pos) and HealthPoints > 0 and len(Slots) >= 2 and SlotCounter < 3:
            SlotCounter = SlotCounter + 1
            if Slot4[0].type == "Monster": 
                DamageValue = Slot4[0].value
                DamageTimer = time.time()
                ShowDamage = True
                if HealthPoints - DamageValue > 0:
                    HealthPoints = HealthPoints - DamageValue
                elif DamageValue >= HealthPoints:
                    HealthPoints = 0
                DiscardPileSlot.append(Slot4.pop(0))
            elif Slot4[0].type == "Potion":
                if PotionCounter < 1:
                    LifegainValue = Slot4[0].value
                    LifegainTimer = time.time()
                    ShowLifegain = True
                    HealthPoints = HealthPoints + Slot4[0].value
                    PotionCounter = PotionCounter + 1
                    if HealthPoints > StartingHealthPoints:
                        HealthPoints = StartingHealthPoints
                elif PotionCounter == 1:
                    pass
                DiscardPileSlot.append(Slot4.pop(0))
            elif Slot4[0].type == "Weapon":
                if EquipSlot:
                    DiscardPileSlot.append(EquipSlot.pop(0))
                    EquipSlot.append(Slot4.pop(0))
                    if len(ExperienceSlots) > 0:
                        while ExperienceSlots:
                            DiscardPileSlot.append(ExperienceSlots.pop(0))                 
                else:
                    EquipSlot.append(Slot4.pop(0))
        if RightClick and S4REC.collidepoint(mouse_pos) and HealthPoints > 0 and len(Slots) >= 2 and SlotCounter < 3:
            if Slot4[0].type =="Monster":
                SlotCounter = SlotCounter + 1
                if EquipSlot:
                    if len(ExperienceSlots) == 0:
                        if Slot4[0].value >= EquipSlot[0].value: #if the monster is bigger than the weapon
                            DamageValue = Slot4[0].value - EquipSlot[0].value
                            DamageTimer = time.time()
                            ShowDamage = True
                            HealthPoints = HealthPoints - DamageValue
                            ExperienceSlots.append(Slot4.pop(0))
                        elif Slot4[0].value < EquipSlot[0].value: #if the monster is weaker than the weapon
                            DamageValue = "No Damage!"
                            DamageTimer = time.time()
                            ShowDamage = True
                            HealthPoints = HealthPoints
                            ExperienceSlots.append(Slot4.pop(0))
                    elif len(ExperienceSlots) >= 1:
                        ReversedES = list(reversed(ExperienceSlots))
                        if ReversedES[0].value > Slot4[0].value:
                            if Slot4[0].value >= EquipSlot[0].value: #if the monster is bigger than the weapon
                                DamageValue = Slot4[0].value - EquipSlot[0].value
                                DamageTimer = time.time()
                                ShowDamage = True
                                HealthPoints = HealthPoints - DamageValue
                                ExperienceSlots.append(Slot4.pop(0))
                            elif Slot4[0].value < EquipSlot[0].value: #if the monster is weaker than the weapon
                                DamageValue = "No Damage!"
                                DamageTimer = time.time()
                                ShowDamage = True
                                HealthPoints = HealthPoints
                                ExperienceSlots.append(Slot4.pop(0))
                        elif ReversedES[0].value <= Slot4[0].value:
                            pass
            elif not EquipSlot:
                pass
            elif Slot4[0].type == "Potion":
                pass
            elif Slot4[0].type == "Weapon":
                pass    

    #   DECK IMAGE
    WIN.blit(DI, ((80 + 0*(CW)+0*(CS)), (60))) #Adding 64 per card + 12 per space
    DeckCounter = len(Deck)
    DC = FONT.render(str(DeckCounter),True, WHITE)
    WIN.blit(DC,(30, 60))

    #   DISCARD PILE
    if PShud_enabled == True:
        WIN.blit(CardBorder, ((80 + 1*(CW)+1*(CS) + 60), (HEIGHT-CH-120))) #surface, PosX, PosY

    if not DiscardPileSlot:
        pass
    else:
        Discard_unit = len(DiscardPileSlot)-1
        DiscardImage = os.path.join(Current_Deck, DiscardPileSlot[Discard_unit].cardimage)
        DisImg = pygame.transform.scale(pygame.image.load(DiscardImage), (CW, CH))
        WIN.blit(DisImg,((WIDTH-CW-20), (80+CH)))

    #   WEAPON ZONE

    if PShud_enabled == True:
        WIN.blit(CardBorder, ((WIDTH-CW-20), (80+CH)))     

    if len(ExperienceSlots)>8 and ExperienceSlots[8]:
        ExperienceImage9 = os.path.join(Current_Deck, ExperienceSlots[8].cardimage) 
        EI9 = pygame.transform.scale(pygame.image.load(ExperienceImage9), (CW, CH))
        WIN.blit(EI9, ((0 + 3*(CW)+3*(CS) + 60), (HEIGHT-CH-40)))   
  
    if  len(ExperienceSlots)>7 and ExperienceSlots[7]:
        ExperienceImage8 = os.path.join(Current_Deck, ExperienceSlots[7].cardimage) 
        EI8 = pygame.transform.scale(pygame.image.load(ExperienceImage8), (CW, CH))
        WIN.blit(EI8, ((20 + 3*(CW)+3*(CS) + 60), (HEIGHT-CH-60)))

    if len(ExperienceSlots)>6 and ExperienceSlots[6]:
        ExperienceImage7 = os.path.join(Current_Deck, ExperienceSlots[6].cardimage) 
        EI7 = pygame.transform.scale(pygame.image.load(ExperienceImage7), (CW, CH))
        WIN.blit(EI7, ((40 + 3*(CW)+3*(CS) + 60), (HEIGHT-CH-80)))

    if len(ExperienceSlots)>5 and ExperienceSlots[5]:
        ExperienceImage6 = os.path.join(Current_Deck, ExperienceSlots[5].cardimage) 
        EI6 = pygame.transform.scale(pygame.image.load(ExperienceImage6), (CW, CH))
        WIN.blit(EI6, ((60 + 3*(CW)+3*(CS) + 60), (HEIGHT-CH-100)))  

    if len(ExperienceSlots)>4 and ExperienceSlots[4]:
        ExperienceImage5 = os.path.join(Current_Deck, ExperienceSlots[4].cardimage) 
        EI5 = pygame.transform.scale(pygame.image.load(ExperienceImage5), (CW, CH))
        WIN.blit(EI5, ((80 + 3*(CW)+3*(CS)+ 60), (HEIGHT-CH-120))) 

    if len(ExperienceSlots)>3 and ExperienceSlots[3]:
        ExperienceImage4 = os.path.join(Current_Deck, ExperienceSlots[3].cardimage) 
        EI4 = pygame.transform.scale(pygame.image.load(ExperienceImage4), (CW, CH))
        WIN.blit(EI4, ((0 + 1*(CW)+1*(CS) + 60), (HEIGHT-CH-40)))

    if len(ExperienceSlots)>2 and ExperienceSlots[2]:
        ExperienceImage3 = os.path.join(Current_Deck, ExperienceSlots[2].cardimage) 
        EI3 = pygame.transform.scale(pygame.image.load(ExperienceImage3), (CW, CH))
        WIN.blit(EI3, ((20 + 1*(CW)+1*(CS) + 60), (HEIGHT-CH-60)))  

    if len(ExperienceSlots)>1 and ExperienceSlots[1]:
        ExperienceImage2 = os.path.join(Current_Deck, ExperienceSlots[1].cardimage) 
        EI2 = pygame.transform.scale(pygame.image.load(ExperienceImage2), (CW, CH))
        WIN.blit(EI2, ((40 + 1*(CW)+1*(CS) + 60), (HEIGHT-CH-80))) 

    if len(ExperienceSlots)>0 and ExperienceSlots[0]:
        ExperienceImage1 = os.path.join(Current_Deck, ExperienceSlots[0].cardimage) 
        EI1 = pygame.transform.scale(pygame.image.load(ExperienceImage1), (CW, CH))
        WIN.blit(EI1, ((60 + 1*(CW)+1*(CS) + 60), (HEIGHT-CH-100)))

    if EquipSlot:
        WeaponImage = os.path.join(Current_Deck, EquipSlot[0].cardimage) 
        WP = pygame.transform.scale(pygame.image.load(WeaponImage), (CW, CH))
        WIN.blit(WP, ((80 + 1*(CW)+1*(CS) + 60), (HEIGHT-CH-120)))

    #SCREENS
    if PlayMenuConfirmationBox_Enabled == True:
        if PlayMenuConfirmationFlag == "Main Menu":
            PlayMenuConfirmationBox_Text = "Return to Main Menu?"
        elif PlayMenuConfirmationFlag == "Quit Game":
            PlayMenuConfirmationBox_Text = "Quit Game?"
        else:       
            PlayMenuConfirmationBox_Text = "Error not found"
            print(PlayMenuConfirmationBox_Text)

    padding_x = 10
    padding_y = 10
    lines_spacing = 5

    if PlayMenuConfirmationBox_Enabled == True:
        PlayingConfirmationBox = pygame.Rect(0.50*WIDTH-PlayingConfirmationBoxWIDTH/2, 0.50*HEIGHT-PlayingConfirmationBoxHEIGHT/2, PlayingConfirmationBoxWIDTH, PlayingConfirmationBoxHEIGHT) #pygame.rect(pos.x, pos.y, width, height)
        pygame.draw.rect(WIN,ORANGE,PlayingConfirmationBox,border_top_left_radius=12,border_bottom_left_radius=12, border_top_right_radius=12,border_bottom_right_radius=12) #pygame.draw.rect(surface, color, figure, bordertopleft [optional], borderbottomleft [optional])
        pygame.draw.rect(WIN,BLACK, PlayingConfirmationBox, 1, border_top_left_radius=12,border_bottom_left_radius=12, border_top_right_radius=12,border_bottom_right_radius=12)
        y_offset = PlayingConfirmationBox.y + padding_y #y its the y_pos, padding_y = padding_x = 10
            
        text_surface = SMALLFONT.render(PlayMenuConfirmationBox_Text, True, BLACK)
        text_rect =text_surface.get_rect(topleft=(PlayingConfirmationBox.x + padding_x, y_offset))        
        WIN.blit(text_surface, text_rect)

    if PlaySettingsBox_Enabled == True:
        PlayingSettingsBox = pygame.Rect(0.50*WIDTH-PlayingSettingsBoxWIDTH/2, 0.50*HEIGHT-PlayingSettingsBoxHEIGHT/2, PlayingSettingsBoxWIDTH, PlayingSettingsBoxHEIGHT) #pygame.rect(pos.x, pos.y, width, height)
        pygame.draw.rect(WIN,ORANGE,PlayingSettingsBox,border_top_left_radius=12,border_bottom_left_radius=12, border_top_right_radius=12,border_bottom_right_radius=12) #pygame.draw.rect(surface, color, figure, bordertopleft [optional], borderbottomleft [optional])
        pygame.draw.rect(WIN,BLACK, PlayingSettingsBox, 1, border_top_left_radius=12,border_bottom_left_radius=12, border_top_right_radius=12,border_bottom_right_radius=12)
    
    #ICONS AND BUTTONS

    #Play - Drawing Cards Button
    button_text = SMALLFONT.render(DrawingCardsButton.text, True, WHITE) #text, True/False, Color
    text_rect = button_text.get_rect(center=(DrawingCardsButton.x_pos + DrawingCardsButton.length//2, DrawingCardsButton.y_pos + DrawingCardsButton.height//2))
    button_rect = pygame.rect.Rect((DrawingCardsButton.x_pos,DrawingCardsButton.y_pos),(DrawingCardsButton.length,DrawingCardsButton.height))
    
    '''
    DButtonLock is the variable that locks Drawing Cards. 
    It changes between 0 and 1.
    - When DButtonLock is 0, the player can draw cards. 
    - When DButtonLock is 1, the player cannot draw cards. 
    It always starts at 0, and goes up by 1 every time the player presses the Draw Button.
    It resets to 0 when the player has made 3 actions (SlotCounter = 3)
    For purposes of manipulating the draw button being turned on and off, we can pause the program
    that regulates the ButtonLock with 'DrawingEachTurn', allowing us to manually shut it down
    '''

    if DrawingEachTurn == True:
        if DButtonLock == 1:
            DrawingCardsButton.enabled = False
        elif DButtonLock != 1:
            DrawingCardsButton.enabled = True
        if SlotCounter == 3:
            DButtonLock = 0

    if DrawingCardsButton.enabled == True:
        bcolor = DrawingCardsButton.color
    elif DrawingCardsButton.enabled == False:
        bcolor = GRAY
    
    if button_rect.collidepoint(mouse_pos) and DrawingCardsButton.enabled == True:
        if LeftClick:
            bcolor = DARK_ORANGE
            DButtonLock = DButtonLock + 1
            SlotCounter = 0
            PotionCounter = 0
            if len(Deck) > 3:
                for i in Slots:
                    if not i:
                        i.append(Deck.pop(0))
            elif len(Deck) == 3:
                print('Deck with 3 cards') #this is a placeholder; in theory, the deck is never supposed to have 3 cards at any moment. If it does, the error will appear here
                quit()

            elif len(Deck) < 3:
                for i in Slots:
                    if not i:
                        if Deck:
                            i.append(Deck.pop(0))
                for i in Slots:
                    if i:
                        if i[0].type == 'Monster' or i[0].type == 'Weapon':
                            DiscardPileSlot.append(i.pop(0))
                        elif i[0].type == 'Potion':
                            Score = Score + i[0].value
                            DiscardPileSlot.append(i.pop(0))
                Score = Score + HealthPoints
                YouWinImage = os.path.join(image_folder,"YouWin.jpg")
                YWI = pygame.transform.scale(pygame.image.load(YouWinImage), (WIDTH*0.45, HEIGHT*0.45))
                WIN.blit(YWI, (WIDTH*0.25, HEIGHT*0.30))
                DrawingCardsButton.enabled = False
                GOMainMenuButton.enabled = True
                GOScoreboardButton.enabled = True
                GOQuitButton.enabled = True  

        else:
            bcolor = LIGHT_ORANGE
    pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
    pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
    WIN.blit(button_text, text_rect)

    #Play - Settings Button
    button_text = SMALLFONT.render(PlaySettingsButton.text, True, WHITE) #text, True/False, Color
    text_rect = button_text.get_rect(center=(PlaySettingsButton.x_pos + PlaySettingsButton.length//2, PlaySettingsButton.y_pos + PlaySettingsButton.height//2))
    button_rect = pygame.rect.Rect((PlaySettingsButton.x_pos,PlaySettingsButton.y_pos),(PlaySettingsButton.length,PlaySettingsButton.height))

    if PlaySettingsButton.enabled == True:
        bcolor = PlaySettingsButton.color
    elif PlaySettingsButton.enabled == False:
        bcolor = GRAY
    
    if button_rect.collidepoint(mouse_pos) and PlaySettingsButton.enabled == True:
        if LeftClick:
            bcolor = DARK_ORANGE
            #.
            DrawingEachTurn = False
            DrawingCardsButton.enabled = False
            PlaySettingsButton.enabled = False
            #.
            PlaySettingsBox_Enabled = True
            #.
            ReturntoGameButton.enabled = True
            SoundToggleButton.enabled = True
            HUDToggleButton.enabled = True
            TipsToggleButton.enabled = True
            MainMenuPlayButton.enabled = True
            QuitGamePlayButton.enabled = True
        else:
            bcolor = LIGHT_ORANGE

    pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
    pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
    WIN.blit(button_text, text_rect)

    #Play - See Discard Pile Button
    if DiscardPileSeeBox_Enabled == True:
        DiscardPileText = 'See Discard: ON'
    elif DiscardPileSeeBox_Enabled == False:
        DiscardPileText = 'See Discard: OFF'
    else:
        DiscardPileText = 'ERROR'
    
    button_text = SMALLFONT.render(DiscardPileText, True, WHITE) #text, True/False, Color
    text_rect = button_text.get_rect(center=(SeeDiscardPileButton.x_pos + SeeDiscardPileButton.length//2, SeeDiscardPileButton.y_pos + SeeDiscardPileButton.height//2))
    button_rect = pygame.rect.Rect((SeeDiscardPileButton.x_pos,SeeDiscardPileButton.y_pos),(SeeDiscardPileButton.length,SeeDiscardPileButton.height))
    
    if SeeDiscardPileButton.enabled == True:
        bcolor = SeeDiscardPileButton.color
    elif SeeDiscardPileButton.enabled == False:
        bcolor = GRAY
    
    if button_rect.collidepoint(mouse_pos) and SeeDiscardPileButton.enabled == True:
        if LeftClick:
            bcolor = DARK_ORANGE
            #.
            if DiscardPileSeeBox_Enabled == True: 
                DiscardPileSeeBox_Enabled = False      
            elif DiscardPileSeeBox_Enabled == False:    
                DiscardPileSeeBox_Enabled = True

            #Setting up the first Images
            if len(DiscardPileSlot) > 0:
                DiscardImage1 = DiscardPileSlot[-1].cardimage #this is fecthing the image (.png) of the first card from the back
        
            if len(DiscardPileSlot) > 1:
                DiscardImage2 = DiscardPileSlot[-2].cardimage #this is fecthing the image (.png) of the second card from the back

            if len(DiscardPileSlot) > 2:
                DiscardImage3 = DiscardPileSlot[-3].cardimage #this is fecthing the image (.png) of the third card from the back
        else:
            bcolor = LIGHT_ORANGE

    pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
    pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
    WIN.blit(button_text, text_rect)

    #   Discard Pile - See Box
    if DiscardPileSeeBox_Enabled == True:

        #PRINTING BOX
        '''
        Box is being printed at bottom-right (HEIGHT, WIDTH) - 20
        Box has: 
        WIDTH: 3 * 128 + 4 * 10 + 40 * 2 = 504 
        WIDTH: 3 * CW + 4 * 10 + 40 (3 cards, 4 spaces arrow-card1, card1-card2, card2-card3, card3-arrow + 2 arrows of 40 width)
        HEIGHT: 178 + 10 + 10 = 198 (1 card + 10 above and below)
        '''
        DiscardPileSeeBox = pygame.Rect(WIDTH-20-DiscardPileSeeBoxWIDTH, HEIGHT-20-DiscardPileSeeBoxHEIGHT, DiscardPileSeeBoxWIDTH, DiscardPileSeeBoxHEIGHT) #pygame.rect(pos.x, pos.y, width, height)
        pygame.draw.rect(WIN,ORANGE,DiscardPileSeeBox,border_top_left_radius=12,border_bottom_left_radius=12, border_top_right_radius=12,border_bottom_right_radius=12) #pygame.draw.rect(surface, color, figure, bordertopleft [optional], borderbottomleft [optional])
        pygame.draw.rect(WIN,BLACK, DiscardPileSeeBox, 1, border_top_left_radius=12,border_bottom_left_radius=12, border_top_right_radius=12,border_bottom_right_radius=12)   

        #PRINTING ARROW
        DPArrowR = os.path.join(sprites_folder, "arrow_right.png")
        DPArrowL = os.path.join(sprites_folder, "arrow_left.png")
        DPAWR = pygame.transform.scale(pygame.image.load(DPArrowR), (40, 25))
        DPAWL = pygame.transform.scale(pygame.image.load(DPArrowL), (40, 25))
        Button_Rect_AR = DPAWR.get_rect()
        Button_Rect_AL = DPAWL.get_rect()
        Button_Rect_AR.topleft = ((WIDTH-20-40, HEIGHT-20-DiscardPileSeeBoxHEIGHT/2-(25/2))) 
        Button_Rect_AL.topleft = ((WIDTH-20-DiscardPileSeeBoxWIDTH, HEIGHT-20-DiscardPileSeeBoxHEIGHT/2-(25/2))) 
        WIN.blit(DPAWR, Button_Rect_AR.topleft)
        WIN.blit(DPAWL, Button_Rect_AL.topleft)

        #PRINTING IMAGES
        if DiscardImage1:
            DiscardImageSlot1 = os.path.join(Current_Deck, DiscardImage1) 
            DIMG1 = pygame.transform.scale(pygame.image.load(DiscardImageSlot1), (CW, CH))
            WIN.blit(DIMG1, ((WIDTH-20-40*1-3*CW-3*10), (HEIGHT-20-CH-10))) 

        if DiscardImage2:
            DiscardImageSlot2 = os.path.join(Current_Deck, DiscardImage2) 
            DIMG2 = pygame.transform.scale(pygame.image.load(DiscardImageSlot2), (CW, CH))
            WIN.blit(DIMG2, ((WIDTH-20-40*1-2*CW-2*10), (HEIGHT-20-CH-10))) 

        if DiscardImage3:
            DiscardImageSlot3 = os.path.join(Current_Deck, DiscardImage3) 
            DIMG3 = pygame.transform.scale(pygame.image.load(DiscardImageSlot3), (CW, CH))
            WIN.blit(DIMG3, ((WIDTH-20-40*1-1*CW-1*10), (HEIGHT-20-CH-10))) 

        #this checks if the first image printed is NOT the last discard card on the DiscardPileSlot
        #if the condition is met, it changes the image shown by +1 (goes forward one unit)
        if Button_Rect_AL.collidepoint(mouse_pos) and LeftClick and DiscardImage1 and DiscardImage1 != DiscardPileSlot[-1].cardimage:
            DiscardImage1 = increment_first_index(DiscardImage1)
            DiscardImage2 = increment_first_index(DiscardImage2)
            DiscardImage3 = increment_first_index(DiscardImage3)

        #this checks if the last image printed is NOT the first discard card on the DiscardPileSlot
        #if the condition is met, it changes the image shown by -1 (goes backwards one unit)
        if Button_Rect_AR.collidepoint(mouse_pos) and LeftClick and DiscardImage3 and DiscardImage3 != DiscardPileSlot[0].cardimage: 
            DiscardImage1 = decrement_first_index(DiscardImage1)
            DiscardImage2 = decrement_first_index(DiscardImage2)
            DiscardImage3 = decrement_first_index(DiscardImage3)


    #   Play - Return to Game Button  
    button_text = SMALLFONT.render(ReturntoGameButton.text, True, BLACK) #text, True/False, Color
    text_rect = button_text.get_rect(center=(ReturntoGameButton.x_pos + ReturntoGameButton.length//2, ReturntoGameButton.y_pos + ReturntoGameButton.height//2))
    button_rect = pygame.rect.Rect((ReturntoGameButton.x_pos,ReturntoGameButton.y_pos),(ReturntoGameButton.length,ReturntoGameButton.height))

    if ReturntoGameButton.enabled == True:
        bcolor = ReturntoGameButton.color
    elif ReturntoGameButton.enabled == False:
        bcolor = GRAY
    if button_rect.collidepoint(mouse_pos) and ReturntoGameButton.enabled == True:
        if LeftClick:
            bcolor = DARK_ORANGE
            #.
            DrawingEachTurn = True
            DrawingCardsButton.enabled = True
            PlaySettingsButton.enabled = True
            #.
            PlaySettingsBox_Enabled = False
            MainMenuPlayButton.enabled = False
            HUDToggleButton.enabled = False
            TipsToggleButton.enabled = False
            SoundToggleButton.enabled = False
            QuitGamePlayButton.enabled = False
        else:
            bcolor = LIGHT_ORANGE
    
    if PlaySettingsBox_Enabled == True:
        pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
        pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
        WIN.blit(button_text, text_rect)

    #   Play - HUD Toggle Button
    if HUDToggle == "ON": 
        PShud_enabled = True
    elif HUDToggle == "OFF":
        PShud_enabled = False
        #There is also a bunch of variables that will set off/on when PShud_enabled is set to true/false

    if PShud_enabled == True:
        PSHUDText = 'HUD: ON'
    elif PShud_enabled == False:
        PSHUDText = 'HUD: OFF'
    else:
        PSHUDText = 'Error'
     
    button_text = SMALLFONT.render(PSHUDText, True, BLACK) #text, True/False, Color
    text_rect = button_text.get_rect(center=(HUDToggleButton.x_pos + HUDToggleButton.length//2, HUDToggleButton.y_pos + HUDToggleButton.height//2))
    button_rect = pygame.rect.Rect((HUDToggleButton.x_pos,HUDToggleButton.y_pos),(HUDToggleButton.length,HUDToggleButton.height))
    if HUDToggleButton.enabled == True:
        bcolor = HUDToggleButton.color
    elif HUDToggleButton.enabled == False:
        bcolor = GRAY
    if button_rect.collidepoint(mouse_pos) and HUDToggleButton.enabled == True:
        if LeftClick:
            bcolor = DARK_ORANGE
            #.
            ToggleHUD()
            ReadHUD()
        else:
            bcolor = LIGHT_ORANGE
    if PlaySettingsBox_Enabled == True:
        pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
        pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
        WIN.blit(button_text, text_rect)

    #   Play - Sound Toggle Button
    if PSsound_enabled == True:
        PSSoundText = 'Sound: ON'
    elif PSsound_enabled == False:
        PSSoundText = 'Sound: OFF'
    else:
        PSSoundText = 'Error'
     
    button_text = SMALLFONT.render(PSSoundText, True, BLACK) #text, True/False, Color
    text_rect = button_text.get_rect(center=(SoundToggleButton.x_pos + SoundToggleButton.length//2, SoundToggleButton.y_pos + SoundToggleButton.height//2))
    button_rect = pygame.rect.Rect((SoundToggleButton.x_pos,SoundToggleButton.y_pos),(SoundToggleButton.length,SoundToggleButton.height))

    if SoundToggleButton.enabled == True:
        bcolor = SoundToggleButton.color
    elif SoundToggleButton.enabled == False:
        bcolor = GRAY
    if button_rect.collidepoint(mouse_pos) and SoundToggleButton.enabled == True:
        if LeftClick:
            bcolor = DARK_ORANGE
            #PUT THE SOUND TOGGLE FUNCTION HERE IN THE FUTURE. FOR NOW, IT JUST TOGGLES THE VARIABLE
            if PSsound_enabled == True:
                PSsound_enabled = False
            elif PSsound_enabled == False:
                PSsound_enabled = True
        else:
            bcolor = LIGHT_ORANGE
    if PlaySettingsBox_Enabled == True:
        pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
        pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
        WIN.blit(button_text, text_rect)

    #   Play - Tips Toggle Button
    if TEXTToggle == "ON":
        PSTipsText = 'Tips: ON'
    elif TEXTToggle == "OFF":
        PSTipsText = 'Tips: OFF'
    else:
        PSTipsText = 'Error'
    button_text = SMALLFONT.render(PSTipsText, True, BLACK) #text, True/False, Color
    text_rect = button_text.get_rect(center=(TipsToggleButton.x_pos + TipsToggleButton.length//2, TipsToggleButton.y_pos + TipsToggleButton.height//2))
    button_rect = pygame.rect.Rect((TipsToggleButton.x_pos,TipsToggleButton.y_pos),(TipsToggleButton.length,TipsToggleButton.height))  

    if TipsToggleButton.enabled == True:
        bcolor = TipsToggleButton.color
    elif TipsToggleButton.enabled == False:
        bcolor = GRAY
    if button_rect.collidepoint(mouse_pos) and TipsToggleButton.enabled == True:
        if LeftClick:
            bcolor = DARK_ORANGE
            ToggleTEXT()
            ReadTEXT()
        else:
            bcolor = LIGHT_ORANGE
    if PlaySettingsBox_Enabled == True:
        pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
        pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
        WIN.blit(button_text, text_rect)

    #   Play - Main Menu Button
    button_text = SMALLFONT.render(MainMenuPlayButton.text, True, BLACK) #text, True/False, Color
    text_rect = button_text.get_rect(center=(MainMenuPlayButton.x_pos + MainMenuPlayButton.length//2, MainMenuPlayButton.y_pos + MainMenuPlayButton.height//2))
    button_rect = pygame.rect.Rect((MainMenuPlayButton.x_pos,MainMenuPlayButton.y_pos),(MainMenuPlayButton.length,MainMenuPlayButton.height))

    if MainMenuPlayButton.enabled == True:
        bcolor = MainMenuPlayButton.color
    elif MainMenuPlayButton.enabled == False:
        bcolor = GRAY
    
    if button_rect.collidepoint(mouse_pos) and MainMenuPlayButton.enabled == True:
        if LeftClick:
            bcolor = DARK_ORANGE
            PlaySettingsBox_Enabled = False
            #.
            PlayMenuConfirmationBox_Enabled = True
            PlayMenuConfirmationFlag = "Main Menu"
            PlayMenuConfirmationBox_YesButton.enabled = True
            PlayMenuConfirmationBox_NoButton.enabled = True
            #.
            DrawingCardsButton.enabled = False
            PlaySettingsButton.enabled = False
            #.
            ReturntoGameButton.enabled = False
            SoundToggleButton.enabled = False
            HUDToggleButton.enabled = False
            TipsToggleButton.enabled = False
            MainMenuPlayButton.enabled = False
            QuitGamePlayButton.enabled = False
        else:
            bcolor = LIGHT_ORANGE
    if PlaySettingsBox_Enabled == True:
        pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
        pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
        WIN.blit(button_text, text_rect)

    #       Play - Menu Confirmation Box - Yes Button
    '''
    The YES button is used for BOTH returning to the main menu and quitting the game.
    It regulates itself by a flag called either "Main Menu" or "Quit Game".
    When clicking YES, the button will change the game state to "Main Menu" or quit() the game.
    When clicking NO, the button returns the player to the SettingsMenu
    '''
    button_text = SMALLFONT.render(PlayMenuConfirmationBox_YesButton.text, True, BLACK) #text, True/False, Color
    text_rect = button_text.get_rect(center=(PlayMenuConfirmationBox_YesButton.x_pos + PlayMenuConfirmationBox_YesButton.length//2, PlayMenuConfirmationBox_YesButton.y_pos + PlayMenuConfirmationBox_YesButton.height//2))
    button_rect = pygame.rect.Rect((PlayMenuConfirmationBox_YesButton.x_pos,PlayMenuConfirmationBox_YesButton.y_pos),(PlayMenuConfirmationBox_YesButton.length,PlayMenuConfirmationBox_YesButton.height))

    if PlayMenuConfirmationBox_YesButton.enabled == True:
        bcolor = PlayMenuConfirmationBox_YesButton.color
    elif PlayMenuConfirmationBox_YesButton.enabled == False:
        bcolor = GRAY
    
    if button_rect.collidepoint(mouse_pos) and PlayMenuConfirmationBox_YesButton.enabled == True:
        if LeftClick and PlayMenuConfirmationFlag == "Main Menu":
            bcolor = DARK_ORANGE
            #.
            HUDToggleButton.enabled = False
            SoundToggleButton.enabled = False
            TipsToggleButton.enabled = False
            MainMenuPlayButton.enabled = False
            QuitGamePlayButton.enabled = False
            #.
            PlayMenuConfirmationBox_Enabled = False
            PlayMenuConfirmationBox_YesButton.enabled = False
            PlayMenuConfirmationBox_NoButton.enabled = False
            #.
            game_state = "Main_Menu"
            #.
            DrawingCardsButton.enabled = True
            PlaySettingsButton.enabled = True

        elif LeftClick and PlayMenuConfirmationFlag == "Quit Game":
            quit()
        else:
            bcolor = LIGHT_ORANGE
    
    if PlayMenuConfirmationBox_Enabled == True:
        pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
        pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
        WIN.blit(button_text, text_rect)

    #       Play - Menu Confirmation Box - No Button
    '''
    Clicking NO 
    '''
    button_text = SMALLFONT.render(PlayMenuConfirmationBox_NoButton.text, True, BLACK) #text, True/False, Color
    text_rect = button_text.get_rect(center=(PlayMenuConfirmationBox_NoButton.x_pos + PlayMenuConfirmationBox_NoButton.length//2, PlayMenuConfirmationBox_NoButton.y_pos + PlayMenuConfirmationBox_NoButton.height//2))
    button_rect = pygame.rect.Rect((PlayMenuConfirmationBox_NoButton.x_pos,PlayMenuConfirmationBox_NoButton.y_pos),(PlayMenuConfirmationBox_NoButton.length,PlayMenuConfirmationBox_NoButton.height))

    if PlayMenuConfirmationBox_NoButton.enabled == True:
        bcolor = PlayMenuConfirmationBox_NoButton.color
    elif PlayMenuConfirmationBox_NoButton.enabled == False:
        bcolor = GRAY
    
    if button_rect.collidepoint(mouse_pos) and PlayMenuConfirmationBox_NoButton.enabled == True:
        if LeftClick:
            bcolor = DARK_ORANGE
            #.
            PlaySettingsButton.enabled = False
            PlayMenuConfirmationBox_Enabled = False
            #.
            PlaySettingsBox_Enabled = True
            ReturntoGameButton.enabled = True
            SoundToggleButton.enabled = True
            HUDToggleButton.enabled = True
            TipsToggleButton.enabled = True
            MainMenuPlayButton.enabled = True
            QuitGamePlayButton.enabled = True
            #.
            PlayMenuConfirmationBox_YesButton.enabled = False
            PlayMenuConfirmationBox_NoButton.enabled = False
        else:
            bcolor = LIGHT_ORANGE
    
    if PlayMenuConfirmationBox_Enabled == True:
        pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
        pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
        WIN.blit(button_text, text_rect)

    #   Play - Quit Game Button
    button_text = SMALLFONT.render(QuitGamePlayButton.text, True, BLACK) #text, True/False, Color
    text_rect = button_text.get_rect(center=(QuitGamePlayButton.x_pos + QuitGamePlayButton.length//2, QuitGamePlayButton.y_pos + QuitGamePlayButton.height//2))
    button_rect = pygame.rect.Rect((QuitGamePlayButton.x_pos,QuitGamePlayButton.y_pos),(QuitGamePlayButton.length,QuitGamePlayButton.height))

    if QuitGamePlayButton.enabled == True:
        bcolor = QuitGamePlayButton.color
    elif QuitGamePlayButton.enabled == False:
        bcolor = GRAY
    
    if button_rect.collidepoint(mouse_pos) and QuitGamePlayButton.enabled == True:
        if LeftClick:
            bcolor = DARK_ORANGE
            PlayMenuConfirmationBox_Enabled = True
            PlayMenuConfirmationFlag = "Quit Game"
            PlayMenuConfirmationBox_YesButton.enabled = True
            PlayMenuConfirmationBox_NoButton.enabled = True
            #.
            DrawingCardsButton.enabled = False
            SoundToggleButton.enabled = False
            HUDToggleButton.enabled = False
            TipsToggleButton.enabled = False
            MainMenuPlayButton.enabled = False
            QuitGamePlayButton.enabled = False
        else:
            bcolor = LIGHT_ORANGE
    
    if PlaySettingsBox_Enabled == True:
        pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
        pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
        WIN.blit(button_text, text_rect)

    #Game Over - Main Menu Button
    if GOMainMenuButton.enabled == True:    
        button_text = SMALLFONT.render(GOMainMenuButton.text, True, BLACK)
        text_rect = button_text.get_rect(center=(GOMainMenuButton.x_pos + GOMainMenuButton.length//2, GOMainMenuButton.y_pos + GOMainMenuButton.height//2))
        button_rect = pygame.rect.Rect((GOMainMenuButton.x_pos,GOMainMenuButton.y_pos),(GOMainMenuButton.length,GOMainMenuButton.height))
        bcolor = GOMainMenuButton.color
        if button_rect.collidepoint(mouse_pos):
            if LeftClick:
                bcolor = DARK_ORANGE
                game_state = "Main_Menu"
            else:
                bcolor = LIGHT_ORANGE
        pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
        pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
        WIN.blit(button_text, text_rect)
    
    #Game Over - Score Button
    if GOScoreboardButton.enabled == True:    
        button_text = SMALLFONT.render(GOScoreboardButton.text, True, BLACK)
        text_rect = button_text.get_rect(center=(GOScoreboardButton.x_pos + GOScoreboardButton.length//2, GOScoreboardButton.y_pos + GOScoreboardButton.height//2))
        button_rect = pygame.rect.Rect((GOScoreboardButton.x_pos,GOScoreboardButton.y_pos),(GOScoreboardButton.length,GOScoreboardButton.height))
        bcolor = GOScoreboardButton.color
        if button_rect.collidepoint(mouse_pos):
            if LeftClick:
                bcolor = DARK_ORANGE
                game_state = "Scoreboard"
            else:
                bcolor = LIGHT_ORANGE
        pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
        pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
        WIN.blit(button_text, text_rect)   

    #Game Over - Quit Button
    if GOQuitButton.enabled == True:    
        button_text = SMALLFONT.render(GOQuitButton.text, True, BLACK)
        text_rect = button_text.get_rect(center=(GOQuitButton.x_pos + GOQuitButton.length//2, GOQuitButton.y_pos + GOQuitButton.height//2))
        button_rect = pygame.rect.Rect((GOQuitButton.x_pos,GOQuitButton.y_pos),(GOQuitButton.length,GOQuitButton.height))
        bcolor = GOQuitButton.color
        if button_rect.collidepoint(mouse_pos):
            if LeftClick:
                bcolor = DARK_ORANGE
                quit()
            else:
                bcolor = LIGHT_ORANGE
        pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
        pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
        WIN.blit(button_text, text_rect)

    #HEALTH CHECK
    if HealthPoints <= 0:
        DrawingEachTurn = False
        DrawingCardsButton.enabled = False
        GameOverImage = os.path.join(image_folder,"GameOver.jpg")
        GOI = pygame.transform.scale(pygame.image.load(GameOverImage), (WIDTH*0.45, HEIGHT*0.45))
        WIN.blit(GOI, (WIDTH*0.25, HEIGHT*0.30))
        GOMainMenuButton.enabled = True
        GOScoreboardButton.enabled = True
        GOQuitButton.enabled = True
        if Flag == 0:
            for i in Deck:
                if i.type == "Monster":
                    Score = Score - i.value
            Flag = Flag + 1
            for i in Slots:
                if i:
                    if i[0].type =="Monster":
                        Score = Score - i[0].value
            Flag = Flag + 1
            #Flag is just a way to prevent the score for being calculated more than once
        #game_state = "Game_Over"

    #UPDATE
    pygame.display.update()
    return game_state

#---------------------------------------------------------------------------------------------------------------------------

#SETTINGS SCREEN
def draw_settings(mouse_pos, LeftClick):

#---------------------------------------------------------------------------------------------------------------------------

    #SETTINGS - VARIABLES
    global action_pending1, action_pending2, Delay1000MS, Delay500MS, Delay300MS, Delay100MS, button_clicked_time
    global game_state, ESCAPE
    global backgrounds, get_backgrounds, BGIndex, BGName, BGNameCropped, BGNameBackground
    global DeckTitle
    global OrangeBoxSet_Enabled, WSSelectorMode
    global DIOrangeBoxSet_Enabled, DISelectorMode, DIArrowCondition, DIConfirmationBox_Enabled, DIArrowR, DIArrowL, deck_image1, deck_image2, DeckImage, DeckImageWidth, DeckImageHeight
    global BGOrangeBoxSet_Enabled, BGSelectorMode, BGArrowCondition, BGConfirmationBox_Enabled, BGArrowR, BGArrowL, BGImage, BGImage_Width, BGImage_Height, BGOKButton, BGCancelButton, BGApplyButton, BGIndex
    global Button_Rect_AR, Button_Rect_AL
    global WSOrangeBoxSet_Enabled, WSArrowCondition
    global STEscapeButton, STControlsButton, STWindowSizeButton, STBackgroundButton, STSoundButton, STDeckImageButton
    global STSoundText, sound_enabled
    global WSArrow1, WSArrow2, WSArrow3, WSArrow4, WSArrow5, WSArrow6, WSArrow7, WSArrow8, WSArrow9, WSArrow10, WSArrow11, WSArrow12
    global WSArrowSlot, WSArrowSlots
    global WSConfirmationBox_Enabled
    global WIDTH, HEIGHT, WIN
 
#---------------------------------------------------------------------------------------------------------------------------

   #SETTTINGS - BACKGROUND
    #BGImage is being set in the beginning of the program
    BG = pygame.transform.scale(pygame.image.load(BGImage).convert(), (WIDTH, HEIGHT))
    WIN.blit(BG, (0, 0)) 

    padding_x = 10
    padding_y = 10
    lines_spacing = 5

    '''
    BUTTONS:
    Escape
    Controls
    WIndowsSize
    Sound
    Background
    Deck Image
    '''

#---------------------------------------------------------------------------------------------------------------------------

    #SETTINGS - ESCAPE BUTTON
    button_text = SMALLFONT.render(STEscapeButton.text, True, BLACK)
    text_rect = button_text.get_rect(center=(STEscapeButton.x_pos + STEscapeButton.length//2, STEscapeButton.y_pos + STEscapeButton.height//2))
    button_rect = pygame.rect.Rect((STEscapeButton.x_pos,STEscapeButton.y_pos),(STEscapeButton.length,STEscapeButton.height))
    if STEscapeButton.enabled == True:
        bcolor = STEscapeButton.color
    elif STEscapeButton.enabled == False:
        bcolor = GRAY
    if button_rect.collidepoint(mouse_pos) and STEscapeButton.enabled == True:
        if LeftClick:
            bcolor = DARK_ORANGE
            game_state = "Main_Menu"            
        else:
            bcolor = LIGHT_ORANGE  
    
    pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
    pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
    WIN.blit(button_text, text_rect)

#---------------------------------------------------------------------------------------------------------------------------

    #SETTINGS - CONTROLS BUTTON
    button_text = SMALLFONT.render(STControlsButton.text, True, BLACK)
    text_rect = button_text.get_rect(center=(STControlsButton.x_pos + STControlsButton.length//2, STControlsButton.y_pos + STControlsButton.height//2))
    button_rect = pygame.rect.Rect((STControlsButton.x_pos,STControlsButton.y_pos),(STControlsButton.length,STControlsButton.height))
    if STControlsButton.enabled == True:
        bcolor = STControlsButton.color
    elif STControlsButton.enabled == False:
        bcolor = GRAY
    if button_rect.collidepoint(mouse_pos) and STControlsButton.enabled == True:
        if LeftClick:
            bcolor = DARK_ORANGE
            #.
            STEscapeButton.enabled = False
            STControlsButton.enabled = False
            STWindowSizeButton.enabled = False
            STBackgroundButton.enabled = False
            STSoundButton.enabled = False
            STDeckImageButton.enabled = False
            OrangeBoxSet_Enabled = True #OrangeBox is below in the drawing section  
            #.
            return game_state #this is here so that when you click the button the function stops, ending it and
            #only updating everything on the next frame. This causes everything to load at the same frame
        else:
            bcolor = LIGHT_ORANGE

    pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
    pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
    WIN.blit(button_text, text_rect)

    #   Orange Box
    #OrangeBox is the orange box with lines for the controls part
    OrangeBoxLines = [
        'This game is made to played primarily with the mouse.',
        '',
        'IN GAME',
        'LEFT CLICK: encounter card (Monster/Weapon/Potion);',
        'RIGHT CLICK: slay the Monster with the equipped weapon (if any exists).',
        '',
        'IN MENUS',
        'ARROW KEYS: move inside menus;',
        'ENTER: select option;',
        'ESC: return.'
    ]
    OrangeBoxReminderText = SMALLFONT.render('ESC: return to Settings.',True, WHITE)

    if OrangeBoxSet_Enabled == True:
        OrangeBoxSet = pygame.Rect(230, 0.10*HEIGHT, 0.70*WIDTH, 0.70*HEIGHT) #pygame.rect(pos.x, pos.y, width, height)
        pygame.draw.rect(WIN,ORANGE,OrangeBoxSet,border_top_left_radius=12,border_bottom_left_radius=12, border_top_right_radius=12,border_bottom_right_radius=12) #pygame.draw.rect(surface, color, figure, bordertopleft [optional], borderbottomleft [optional])
        pygame.draw.rect(WIN,BLACK, OrangeBoxSet, 1, border_top_left_radius=12,border_bottom_left_radius=12, border_top_right_radius=12,border_bottom_right_radius=12)
        WIN.blit(OrangeBoxReminderText,(240,0.06*HEIGHT))
        y_offset = OrangeBoxSet.y + padding_y

        for line in OrangeBoxLines:
            text_surface = SMALLFONT.render(line, True, BLACK)
            text_rect =text_surface.get_rect(topleft=(OrangeBoxSet.x + padding_x, y_offset))
            WIN.blit(text_surface, text_rect)
            y_offset += text_surface.get_height() + lines_spacing

    if ESCAPE and OrangeBoxSet_Enabled == True:
        OrangeBoxSet_Enabled = False
        STEscapeButton.enabled = True
        STControlsButton.enabled = True
        STWindowSizeButton.enabled = True
        STBackgroundButton.enabled = True
        STDeckImageButton.enabled = True
        STSoundButton.enabled = True
        return game_state #this is here so that when you click the button the function stops, ending it and
        #only updating everything on the next frame. This causes everything to load at the same frame

#---------------------------------------------------------------------------------------------------------------------------

    #SETTINGS - SOUND BUTTON
    if sound_enabled == True:
        STSoundText = 'Sound: ON'
    elif sound_enabled == False:
        STSoundText = 'Sound: OFF'
    else:
        STSoundText = 'Error' 

    button_text = SMALLFONT.render(STSoundText, True, BLACK)
    text_rect = button_text.get_rect(center=(STSoundButton.x_pos + STSoundButton.length//2, STSoundButton.y_pos + STSoundButton.height//2))
    button_rect = pygame.rect.Rect((STSoundButton.x_pos,STSoundButton.y_pos),(STSoundButton.length,STSoundButton.height))
    if STSoundButton.enabled == True:
        bcolor = STSoundButton.color
    elif STSoundButton.enabled == False:
        bcolor = GRAY
    if button_rect.collidepoint(mouse_pos) and STSoundButton.enabled == True:
        if LeftClick:
            bcolor = DARK_ORANGE
            toggle_sound()          
        else:
            bcolor = LIGHT_ORANGE
    
    pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
    pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
    WIN.blit(button_text, text_rect)

#---------------------------------------------------------------------------------------------------------------------------

    #SETTINGS - BACKGROUND BUTTON
    
    #Background Button
    button_text = SMALLFONT.render(STBackgroundButton.text, True, BLACK)
    text_rect = button_text.get_rect(center=(STBackgroundButton.x_pos + STBackgroundButton.length//2, STBackgroundButton.y_pos + STBackgroundButton.height//2))
    button_rect = pygame.rect.Rect((STBackgroundButton.x_pos,STBackgroundButton.y_pos),(STBackgroundButton.length,STBackgroundButton.height))
    if STBackgroundButton.enabled == True:
        bcolor = STBackgroundButton.color
    elif STBackgroundButton.enabled == False:
        bcolor = GRAY
    if button_rect.collidepoint(mouse_pos) and STBackgroundButton.enabled == True:
        if LeftClick:
            bcolor = DARK_ORANGE
            BGOrangeBoxSet_Enabled = True 
            BGSelectorMode = True 
            BGArrowCondition = True
            BGApplyButton.enabled = True
            BGCancelButton.enabled = True
            BGNameBackground = BGNameCropped #this sets the first name to appear in the file selection as the current background
            #.
            STEscapeButton.enabled = False
            STControlsButton.enabled = False
            STWindowSizeButton.enabled = False
            STBackgroundButton.enabled = False
            STSoundButton.enabled = False
            STDeckImageButton.enabled = False  
            #.
            return game_state #this skips the rest of the def() function, so we can load properly on 1 frame
        else:
            bcolor = LIGHT_ORANGE
    
    pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
    pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
    WIN.blit(button_text, text_rect)

    #   Orange Box
    BGOrangeBoxLines = ['Select your Background:']
    BGOrangeBoxReminderText = SMALLFONT.render('ESC: return to Settings.',True, WHITE)

    if BGOrangeBoxSet_Enabled == True:
        BGOrangeBoxSet = pygame.Rect(0.25*WIDTH, 0.25*HEIGHT, 0.50*WIDTH, 0.50*HEIGHT) #pygame.rect(pos.x, pos.y, width, height)
        pygame.draw.rect(WIN,ORANGE,BGOrangeBoxSet,border_top_left_radius=12,border_bottom_left_radius=12, border_top_right_radius=12,border_bottom_right_radius=12) #pygame.draw.rect(surface, color, figure, bordertopleft [optional], borderbottomleft [optional])
        pygame.draw.rect(WIN,BLACK, BGOrangeBoxSet, 1, border_top_left_radius=12,border_bottom_left_radius=12, border_top_right_radius=12,border_bottom_right_radius=12)
        WIN.blit(BGOrangeBoxReminderText,(240,0.06*HEIGHT)) #Width,Height
        y_offset = BGOrangeBoxSet.y + padding_y #y its the y_pos, padding_y = padding_x = 10

        for line in BGOrangeBoxLines:
            text_surface = SMALLFONT.render(line, True, BLACK)
            text_rect =text_surface.get_rect(topleft=(BGOrangeBoxSet.x + padding_x, y_offset))
            #print(f"Text: '{line.strip()}', y_position: {y_offset}, height: {text_surface.get_height()}")
            WIN.blit(text_surface, text_rect)
            y_offset += text_surface.get_height() + lines_spacing #lines_spacing = 5

    #   Escape
    '''This ESC button is only for the Deck Image 'Orange Box'''
    if ESCAPE and BGOrangeBoxSet_Enabled == True: 
        BGArrowCondition = False
        BGSelectorMode = False
        BGOrangeBoxSet_Enabled = False
        BGApplyButton.enabled = False
        BGCancelButton.enabled = False
        #.
        STEscapeButton.enabled = True
        STControlsButton.enabled = True
        STWindowSizeButton.enabled = True
        STBackgroundButton.enabled = True
        STSoundButton.enabled = True
        STDeckImageButton.enabled = True
        #.
        return game_state #this skips the rest of the def() function, so we can load properly on 1 frame

    #   Selector Mode
    if BGSelectorMode == True: 
        #BGImage = os.path.join(background_folder, BGName) #this is the default BG
        #BGName it's the variable that saves the name of the current deck in the config (EX: BGName = '1-Dice.png')
        #BGNameCropped = BGName.split("-")[1].split(".")[0] #this is just the name of the image file (EX: Dice)
        #BGSpacing = 24
        #BGImage_Width = 0.125*WIDTH
        #BGImage_Height = BGImage_Width*(7/5) The image have a 9:16 ratio
        
        '''
        #This is an old asset I was using for background image. I'm not deleting it, just leaving it here in case I want to use it again.
        #The True BI is in fact just below in 'Arrows and Images' as BGP
        BI = pygame.transform.scale(pygame.image.load(BGImage), (BGImage_Width, BGImage_Height))
        WIN.blit(BI, (0,0))
        '''
        for i in backgrounds:
            if backgrounds.index(i) != BGIndex:
                continue
            elif backgrounds.index(i) == BGIndex:
                BGNameBackground = os.path.join(i["path"])
                dot_index = BGNameBackground.rfind('.')
                extension = BGNameBackground[dot_index:]  # ".jpg" or ".png"
                if extension in ('.jpg', '.png'):
                    # Find the dash before the name, searching backwards from the dot
                    dash_index = BGNameBackground.rfind('-', 0, dot_index)
                    IndexedBackgroundName = BGNameBackground[dash_index + 1 : dot_index]  # "Dice"
                BG_Writing = SMALLFONT.render(IndexedBackgroundName,True, BLACK)
                BG_WritingWidth = BG_Writing.get_width()
                WIN.blit(BG_Writing,(0.50*WIDTH - BG_WritingWidth/2, 0.75*HEIGHT-BGImage_Height-20-DISpacing-20-DISpacing - 25)) #Name of the current Deck 

    #Arrows and Images
    if BGArrowCondition == True:
        BGArrowR = os.path.join(sprites_folder, "arrow_right.png")
        BGArrowL = os.path.join(sprites_folder, "arrow_left.png")
        BGAWR = pygame.transform.scale(pygame.image.load(BGArrowR), (50, 35))
        BGAWL = pygame.transform.scale(pygame.image.load(BGArrowL), (50, 35))
        Button_Rect_AR = BGAWR.get_rect()
        Button_Rect_AL = BGAWL.get_rect()
        Button_Rect_AR.topleft = ((0.75*WIDTH - 70, 0.50*HEIGHT)) 
        Button_Rect_AL.topleft = (0.25*WIDTH + 20, 0.50*HEIGHT) 
        WIN.blit(BGAWR, Button_Rect_AR.topleft)
        WIN.blit(BGAWL, Button_Rect_AL.topleft)

        IndexLength = len(backgrounds) #this is the quantity of images in the backgrounds. 
        #Remember that a 3 items-lenght-list has 0, 1 and 2 indexes.
        #Example: in the default 4 images folder, the list has:
        #lenght: 4 
        #positions 0 - 3
        #Index = Position (or len -1)
        
        '''
        This is a function that looks for the current Background (saved by the function) capturing_index that executed in the
        beginning of the Game when the game first opens, printing it in the orange box.
        Afterwards, everytime we change the BGIndex the game should use this function to re-print it correctly by changing the
        BGPreview.
        '''
        for i in backgrounds:
            if backgrounds.index(i) != BGIndex:
                continue
            elif backgrounds.index(i) == BGIndex:
                BGPreview = os.path.join(i["path"])
                BGP = pygame.transform.scale(pygame.image.load(BGPreview), (BGImage_Width, BGImage_Height))
                WIN.blit(BGP, (0.50*WIDTH - BGImage_Width/2, 0.75*HEIGHT-BGImage_Height-20-DISpacing-20-DISpacing))
            else:
                print("Error. BGIndex not found")

        #Right Arrow
        #This is the arrow that appears on the right, and it changes the deck to the next one on the right, which is the next one on the list'''
        if Button_Rect_AR.collidepoint(mouse_pos) and LeftClick:
            #blink arrow and sound
            if BGIndex == IndexLength - 1: #this checks if the image is the last one; if it's, it changes to the first image (image 0)
                BGIndex = 0
            elif BGIndex != IndexLength - 1: #if BGIndex is a number AND it's not the last one, increases the integer in 1.
                BGIndex += 1

        #Left Arrow 
        #This is the arrow that appears on the left, and it changes the deck to the last one on the list'
        if Button_Rect_AL.collidepoint(mouse_pos) and LeftClick:
           #blink arrow and sound
            if BGIndex == 0:
                BGIndex = IndexLength-1
            elif BGIndex >= 1:
                BGIndex -= 1
    
    #Pressing ESC
        if ESCAPE:
            BGArrowCondition = False
            BGSelectorMode = False
            BGOrangeBoxSet_Enabled = False
            BGApplyButton.enabled = False
            BGCancelButton.enabled = False
            #.
            STEscapeButton.enabled = True
            STControlsButton.enabled = True  
            STWindowSizeButton.enabled = True
            STSoundButton.enabled = True
            STBackgroundButton.enabled = True
            STDeckImageButton.enabled = True    
            #.
            return game_state #this skips the rest of the def() function, so we can load properly on 1 frame  

    #Apply Button 
    if BGOrangeBoxSet_Enabled == True:
        button_text = SMALLFONT.render(BGApplyButton.text, True, BLACK)
        text_rect = button_text.get_rect(center=(BGApplyButton.x_pos + BGApplyButton.length//2, BGApplyButton.y_pos + BGApplyButton.height//2))
        button_rect = pygame.rect.Rect((BGApplyButton.x_pos,BGApplyButton.y_pos),(BGApplyButton.length,BGApplyButton.height))     
        
        if BGApplyButton.enabled == True:
            bcolor = BGApplyButton.color
        elif BGApplyButton.enabled == False:
            bcolor = GRAY

        if button_rect.collidepoint(mouse_pos) and BGApplyButton.enabled == True:
            if LeftClick:
                #.blink button and sound
                path = backgrounds[BGIndex]["path"]
                reversed_path = path[::-1]
                filename_reversed = ''
                for char in reversed_path:
                    if char == "\\":
                        break
                    filename_reversed += char
                
                filename = filename_reversed[::-1]
                #.
                BGArrowCondition = False
                BGSelectorMode = False
                BGOrangeBoxSet_Enabled = False
                BGApplyButton.enabled = False
                BGCancelButton.enabled = False
                #.
                BGConfirmationBox_Enabled = True
                BGOKButton.enabled = True
                #.
                with open(ConfigFile, 'r', encoding='utf-8') as file:
                    lines = file.readlines()

                for i, line in enumerate(lines):
                    if line.startswith('BACKGROUND'):
                        lines[i] = f"BACKGROUND = {filename}\n" 

                with open(ConfigFile, 'w', encoding='utf-8') as file:
                    file.writelines(lines)
                
                DrawBackground()
                return game_state #this skips the rest of the def() function, so we can load properly on 1 frame

        pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
        pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
        WIN.blit(button_text, text_rect) #text and position 

    #Cancel Button
    if BGOrangeBoxSet_Enabled == True:
        button_text = SMALLFONT.render(BGCancelButton.text, True, BLACK)
        text_rect = button_text.get_rect(center=(BGCancelButton.x_pos + BGCancelButton.length//2, BGCancelButton.y_pos + BGCancelButton.height//2))
        button_rect = pygame.rect.Rect((BGCancelButton.x_pos,BGCancelButton.y_pos),(BGCancelButton.length,BGCancelButton.height))

        if BGCancelButton.enabled == True:
            bcolor = BGCancelButton.color
        elif BGCancelButton.enabled == False:
                bcolor = GRAY
            
        if button_rect.collidepoint(mouse_pos) and BGCancelButton.enabled == True:
            if LeftClick:
                bcolor = DARK_ORANGE
                #.
                BGConfirmationBox_Enabled = False
                BGOrangeBoxSet_Enabled = False
                BGOKButton.enabled = False
                BGArrowCondition = False
                BGSelectorMode = False
                #.
                STEscapeButton.enabled = True
                STControlsButton.enabled = True  
                STWindowSizeButton.enabled = True
                STSoundButton.enabled = True
                STBackgroundButton.enabled = True
                STDeckImageButton.enabled = True
                #.
                return game_state #this skips the rest of the def() function, so we can load properly on 1 frame
            else:
                bcolor = LIGHT_ORANGE
                
        pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
        pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
        WIN.blit(button_text, text_rect)

    #   Confirmation Box 
    '''BGConfirmationBox_Width = 328 
    BGConfirmationBox_Height = 220''' '''this is just used for the confirmation to apply the changes, after pressing the button APPLY'''

    if BGConfirmationBox_Enabled == True:
        BGConfirmationRect = pygame.Rect(0.5*WIDTH-BGConfirmationBox_Width/2, 0.5*HEIGHT-BGConfirmationBox_Height/2,BGConfirmationBox_Width, BGConfirmationBox_Height) #left, top, width, height
        pygame.draw.rect(WIN, ORANGE, BGConfirmationRect, border_radius=12)
        pygame.draw.rect(WIN, BLACK, BGConfirmationRect, 1, border_radius=12)
        ConfirmationText = FONT.render('Changes applied.', True, BLACK)
        ConfirmationText_rect = ConfirmationText.get_rect(center=(WIDTH//2, HEIGHT//2 - 30))
        WIN.blit(ConfirmationText, ConfirmationText_rect)

    #   Ok Button 
        if BGConfirmationBox_Enabled == True and BGOKButton.enabled == True:
            button_text = SMALLFONT.render(BGOKButton.text, True, BLACK)
            text_rect = button_text.get_rect(center=(BGOKButton.x_pos + BGOKButton.length//2, BGOKButton.y_pos + BGOKButton.height//2))
            button_rect = pygame.rect.Rect((BGOKButton.x_pos,BGOKButton.y_pos),(BGOKButton.length,BGOKButton.height)) 

            if BGOKButton.enabled == True:
                bcolor = BGOKButton.color
            elif BGOKButton.enabled == False:
                bcolor = GRAY

            if button_rect.collidepoint(mouse_pos) and BGOKButton.enabled == True:
                if LeftClick:
                    bcolor = DARK_ORANGE
                    #.
                    BGConfirmationBox_Enabled = False 
                    BGArrowCondition = False
                    BGSelectorMode = False
                    BGOrangeBoxSet_Enabled = False               
                    BGSelectorMode = False
                    BGArrowCondition = False
                    BGApplyButton.enabled = False
                    BGCancelButton.enabled = False
                    #.
                    STEscapeButton.enabled = True
                    STControlsButton.enabled = True 
                    STWindowSizeButton.enabled = True 
                    STBackgroundButton.enabled = True 
                    STSoundButton.enabled = True 
                    STDeckImageButton.enabled = True
                    #.
                    return game_state #this skips the rest of the def() function, so we can load properly on 1 frame   
                else:
                    bcolor = LIGHT_ORANGE
           
        pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
        pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
        WIN.blit(button_text, text_rect) #text and position       

#---------------------------------------------------------------------------------------------------------------------------

    #SETTINGS - DECK IMAGE BUTTON

    #Deck ImageButton
    button_text = SMALLFONT.render(STDeckImageButton.text, True, BLACK)
    text_rect = button_text.get_rect(center=(STDeckImageButton.x_pos + STDeckImageButton.length//2, STDeckImageButton.y_pos + STDeckImageButton.height//2))
    button_rect = pygame.rect.Rect((STDeckImageButton.x_pos,STDeckImageButton.y_pos),(STDeckImageButton.length,STDeckImageButton.height))
    if STDeckImageButton.enabled == True:
        bcolor = STDeckImageButton.color
    elif STDeckImageButton.enabled == False:
        bcolor = GRAY
    if button_rect.collidepoint(mouse_pos) and STDeckImageButton.enabled == True:
        if LeftClick:
            bcolor = DARK_ORANGE
            DIOrangeBoxSet_Enabled = True 
            DISelectorMode = True 
            DIArrowCondition = True
            STEscapeButton.enabled = False
            STControlsButton.enabled = False
            STWindowSizeButton.enabled = False
            STBackgroundButton.enabled = False
            STSoundButton.enabled = False
            STDeckImageButton.enabled = False
            #.
            return game_state #this skips the rest of the def() function, so we can load properly on 1 frame   
        else:
            bcolor = LIGHT_ORANGE
    
    pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
    pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
    WIN.blit(button_text, text_rect)

    #   Orange Box
    DIOrangeBoxLines = ['Select the Deck you want to play with:']
    DIOrangeBoxReminderText = SMALLFONT.render('ESC: return to Settings.',True, WHITE)

    if DIOrangeBoxSet_Enabled == True:
        DIOrangeBoxSet = pygame.Rect(0.25*WIDTH, 0.25*HEIGHT, 0.50*WIDTH, 0.50*HEIGHT) #pygame.rect(pos.x, pos.y, width, height)
        pygame.draw.rect(WIN,ORANGE,DIOrangeBoxSet,border_top_left_radius=12,border_bottom_left_radius=12, border_top_right_radius=12,border_bottom_right_radius=12) #pygame.draw.rect(surface, color, figure, bordertopleft [optional], borderbottomleft [optional])
        pygame.draw.rect(WIN,BLACK, DIOrangeBoxSet, 1, border_top_left_radius=12,border_bottom_left_radius=12, border_top_right_radius=12,border_bottom_right_radius=12)
        WIN.blit(DIOrangeBoxReminderText,(240,0.06*HEIGHT)) #Width,Height
        y_offset = DIOrangeBoxSet.y + padding_y #y its the y_pos, padding_y = padding_x = 10

        for line in DIOrangeBoxLines:
            text_surface = SMALLFONT.render(line, True, BLACK)
            text_rect =text_surface.get_rect(topleft=(DIOrangeBoxSet.x + padding_x, y_offset))
            #print(f"Text: '{line.strip()}', y_position: {y_offset}, height: {text_surface.get_height()}")
            WIN.blit(text_surface, text_rect)
            y_offset += text_surface.get_height() + lines_spacing #lines_spacing = 5

    #   Escape
    '''This ESC button is only for the Deck Image 'Orange Box'''
    if ESCAPE and DIOrangeBoxSet_Enabled == True: 
        DIArrowCondition = False
        DISelectorMode = False
        DIOrangeBoxSet_Enabled = False
        STEscapeButton.enabled = True
        STControlsButton.enabled = True
        STWindowSizeButton.enabled = True
        STBackgroundButton.enabled = True
        STSoundButton.enabled = True
        STDeckImageButton.enabled = True
        #.
        return game_state #this skips the rest of the def() function, so we can load properly on 1 frame

    #   Selector Mode
    if DISelectorMode == True: 
        #deck_image1 = os.path.join(Current_Deck,'cardback.png')
        #deck_image2 = os.path.join(Current_Deck,'ace_of_spades.png')
        #DISpacing = 24
        #DeckImageWidth = 0.125*WIDTH
        #DeckImageHeight = DeckImageWidth*(7/5) The cards have a 5:7 ratio
        
        DI1 = pygame.transform.scale(pygame.image.load(deck_image1), (DeckImageWidth, DeckImageHeight))
        DI2 = pygame.transform.scale(pygame.image.load(deck_image2), (DeckImageWidth, DeckImageHeight))
        WIN.blit(DI1, (0.50*WIDTH-DeckImageWidth-DISpacing, 0.75*HEIGHT-DeckImageHeight-20-DISpacing))
        WIN.blit(DI2, (0.50*WIDTH+DISpacing, 0.75*HEIGHT-DeckImageHeight-20-DISpacing))
        Deck_Writing = SMALLFONT.render(DeckTitle,True, BLACK)
        WIN.blit(Deck_Writing,(0.50*WIDTH - 50,0.75*HEIGHT-DeckImageHeight-20-DISpacing-20-DISpacing)) #Name of the current Deck

    #   Arrows and Images
        if DIArrowCondition == True:
            DIArrowR = os.path.join(sprites_folder, "arrow_right.png")
            DIArrowL = os.path.join(sprites_folder, "arrow_left.png")
            DIAWR = pygame.transform.scale(pygame.image.load(DIArrowR), (50, 35))
            DIAWL = pygame.transform.scale(pygame.image.load(DIArrowL), (50, 35))
            Button_Rect_AR = DIAWR.get_rect()
            Button_Rect_AL = DIAWL.get_rect()
            Button_Rect_AR.topleft = ((0.75*WIDTH - 70, 0.50*HEIGHT)) 
            Button_Rect_AL.topleft = (0.25*WIDTH + 20, 0.50*HEIGHT) 
            WIN.blit(DIAWR, Button_Rect_AR.topleft)
            WIN.blit(DIAWL, Button_Rect_AL.topleft)

    #   Right Arrow
    #This is the arrow that appears on the right, and it changes the deck to the next one on the right, which is the next one on the list'''
        if Button_Rect_AR.collidepoint(mouse_pos) and LeftClick:
            #blink arrow and sound
            for i in Image_Folders:
                if i == DeckTitle:
                    current_index = Image_Folders.index(i)
                    if current_index < len(Image_Folders) - 1:
                        next_index = current_index + 1
                    else:
                        next_index = 0
                    DeckTitle = Image_Folders[next_index] #DeckTitle its the name of the Folder that we are changing into
                    for i in os.listdir(image_folder):
                        if os.path.isdir(os.path.join(image_folder, i)) and i == DeckTitle:
                            NewDeckName = i
                            NewDeckPath = os.path.join(image_folder, NewDeckName)
                    deck_image1 = os.path.join(NewDeckPath, 'cardback.png')
                    deck_image2 = os.path.join(NewDeckPath, 'ace_of_spades.png')
                    break

    #   Left Arrow
    #This is the arrow that appears on the left, and it changes the deck to the last one on the list'
        if Button_Rect_AL.collidepoint(mouse_pos) and LeftClick:
           #blink arrow and sound
            for i in Image_Folders:
                if i == DeckTitle:
                    current_index = Image_Folders.index(i)
                    if current_index != 0:
                        next_index = current_index - 1
                    else:
                        next_index = len(Image_Folders) - 1
                    DeckTitle = Image_Folders[next_index]
                    for i in os.listdir(image_folder):
                        if os.path.isdir(os.path.join(image_folder, i)) and i == DeckTitle:
                            NewDeckName = i
                            NewDeckPath = os.path.join(image_folder, NewDeckName)
                    deck_image1 = os.path.join(NewDeckPath, 'cardback.png')
                    deck_image2 = os.path.join(NewDeckPath, 'ace_of_spades.png')
                    break

    #   Apply Button
    if DIOrangeBoxSet_Enabled == True:
        button_text = SMALLFONT.render(DIApplyButton.text, True, BLACK)
        text_rect = button_text.get_rect(center=(DIApplyButton.x_pos + DIApplyButton.length//2, DIApplyButton.y_pos + DIApplyButton.height//2))
        button_rect = pygame.rect.Rect((DIApplyButton.x_pos,DIApplyButton.y_pos),(DIApplyButton.length,DIApplyButton.height))     
        
        if DIApplyButton.enabled == True:
            bcolor = DIApplyButton.color
        elif DIApplyButton.enabled == False:
            bcolor = GRAY

        if button_rect.collidepoint(mouse_pos) and DIApplyButton.enabled == True:
            if LeftClick:
                button_clicked_time = pygame.time.get_ticks()  # Get the current time in milliseconds
                action_pending2 = True
                bcolor = DARK_ORANGE 
            else:
                bcolor = LIGHT_ORANGE

        if action_pending2:
            DIArrowCondition = False
            DISelectorMode = False
            DIOrangeBoxSet_Enabled = False
            DIApplyButton.enabled = False
            DICancelButton.enabled = False
            DIConfirmationBox_Enabled = True
            DIOKButton.enabled = True
            with open(ConfigFile, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            for i, line in enumerate(lines):
                if line.startswith('DECK IMAGE'):
                    lines[i] = f"DECK IMAGE = {DeckTitle}\n" 

            with open(ConfigFile, 'w', encoding='utf-8') as file:
                file.writelines(lines)
            BuildDeckImage()
            action_pending2 = False
            return game_state #this skips the rest of the def() function, so we can load properly on 1 frame

        pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
        pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
        WIN.blit(button_text, text_rect) #text and position 

    #   Cancel Button 
    if DIOrangeBoxSet_Enabled == True:
        button_text = SMALLFONT.render(DICancelButton.text, True, BLACK)
        text_rect = button_text.get_rect(center=(DICancelButton.x_pos + DICancelButton.length//2, DICancelButton.y_pos + DICancelButton.height//2))
        button_rect = pygame.rect.Rect((DICancelButton.x_pos,DICancelButton.y_pos),(DICancelButton.length,DICancelButton.height))

        if DICancelButton.enabled == True:
            bcolor = DICancelButton.color
        elif DICancelButton.enabled == False:
                bcolor = GRAY
            
        if button_rect.collidepoint(mouse_pos) and DICancelButton.enabled == True:
            if LeftClick:
                bcolor = DARK_ORANGE
                DIConfirmationBox_Enabled = False
                DIOrangeBoxSet_Enabled = False
                DIOKButton.enabled = False
                DIArrowCondition = False
                DISelectorMode = False
                STEscapeButton.enabled = True
                STControlsButton.enabled = True  
                STWindowSizeButton.enabled = True
                STSoundButton.enabled = True
                STBackgroundButton.enabled = True
                STDeckImageButton.enabled = True   
                #.
                return game_state #this skips the rest of the def() function, so we can load properly on 1 frame
            else:
                bcolor = LIGHT_ORANGE
                
        pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
        pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
        WIN.blit(button_text, text_rect)

    #   Confirmation Box
    '''DIConfirmationBox_Width = 328
    DIConfirmationBox_Height = 220''' '''this is just used for the confirmation to apply the changes, after pressing the button APPLY'''

    if DIConfirmationBox_Enabled == True:
        DIConfirmationRect = pygame.Rect(0.5*WIDTH-DIConfirmationBox_Width/2, 0.5*HEIGHT-DIConfirmationBox_Height/2,WSConfirmationBox_Width, DIConfirmationBox_Height) #left, top, width, height
        pygame.draw.rect(WIN, ORANGE, DIConfirmationRect, border_radius=12)
        pygame.draw.rect(WIN, BLACK, DIConfirmationRect, 1, border_radius=12)
        ConfirmationText = FONT.render('Changes applied.', True, BLACK)
        ConfirmationText_rect = ConfirmationText.get_rect(center=(WIDTH//2, HEIGHT//2 - 30))
        WIN.blit(ConfirmationText, ConfirmationText_rect)

    #   Ok Button
        if DIConfirmationBox_Enabled == True and DIOKButton.enabled == True:
            button_text = SMALLFONT.render(DIOKButton.text, True, BLACK)
            text_rect = button_text.get_rect(center=(DIOKButton.x_pos + DIOKButton.length//2, DIOKButton.y_pos + DIOKButton.height//2))
            button_rect = pygame.rect.Rect((DIOKButton.x_pos,DIOKButton.y_pos),(DIOKButton.length,DIOKButton.height)) 

            if DIOKButton.enabled == True:
                bcolor = DIOKButton.color
            elif DIOKButton.enabled == False:
                bcolor = GRAY

            if button_rect.collidepoint(mouse_pos) and DIOKButton.enabled == True:
                if LeftClick:
                    button_clicked_time = pygame.time.get_ticks()  # Get the current time in milliseconds
                    action_pending1 = True
                    bcolor = DARK_ORANGE
                else:
                    bcolor = LIGHT_ORANGE

    #   Resolving the OK Button and the Confirmation Box
        'This is separated from the OK Button cause I was experimenting with'
        'the idea of delay, as we can see the the action pending1 if statement that checks for a'
        'delayed time of 0 ms. As of the final product, Im not using this feature, but left it'
        'here in case I find it necessary for the future '           
        if action_pending1:
            current_time = pygame.time.get_ticks()
            if current_time - button_clicked_time >= 0:  # Check if Delayed time has passed. As I don't want to use any yet, it's set to 0.
                action_pending1 = False 
                DIConfirmationBox_Enabled = False 
                #.
                DIArrowCondition = False
                DISelectorMode = False
                DIOrangeBoxSet_Enabled = False               
                DISelectorMode = False
                DIArrowCondition = False
                DIApplyButton.enabled = False
                DICancelButton.enabled = False
                #.
                STEscapeButton.enabled = True
                STControlsButton.enabled = True 
                STWindowSizeButton.enabled = True 
                STBackgroundButton.enabled = True 
                STSoundButton.enabled = True 
                STDeckImageButton.enabled = True  
                #.
                return game_state #this skips the rest of the def() function, so we can load properly on 1 frame

        pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
        pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
        WIN.blit(button_text, text_rect) #text and position       

#---------------------------------------------------------------------------------------------------------------------------

    #SETTINGS - WINDOW SIZE BUTTON

    #Settings Button
    button_text = SMALLFONT.render(STWindowSizeButton.text, True, BLACK)
    text_rect = button_text.get_rect(center=(STWindowSizeButton.x_pos + STWindowSizeButton.length//2, STWindowSizeButton.y_pos + STWindowSizeButton.height//2))
    button_rect = pygame.rect.Rect((STWindowSizeButton.x_pos,STWindowSizeButton.y_pos),(STWindowSizeButton.length,STWindowSizeButton.height))
    if STWindowSizeButton.enabled == True:
        bcolor = STWindowSizeButton.color
    elif STWindowSizeButton.enabled == False:
        bcolor = GRAY
    if button_rect.collidepoint(mouse_pos) and STWindowSizeButton.enabled == True:
        if LeftClick:
            bcolor = DARK_ORANGE
            WSSelectorMode = True
            WSArrowCondition = True
            WSOrangeBoxSet_Enabled = True
            WSArrowSlot = WSArrowSlots[0]
            #.
            STEscapeButton.enabled = False
            STControlsButton.enabled = False  
            STWindowSizeButton.enabled = False
            STSoundButton.enabled = False
            STBackgroundButton.enabled = False
            STDeckImageButton.enabled = False
            #.
            return game_state #this skips the rest of the def() function, so we can load properly on 1 frame        
        else:
            bcolor = LIGHT_ORANGE
    
    pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
    pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
    WIN.blit(button_text, text_rect)

    #Orange Box
    WSOrangeBoxLines = [
        'Choose your Window Size:',
        '               800 x 600', 
        '               1024 x 768', 
        '               1152 x 864', 
        '               1280 x 600',
        '               1280 x 800',
        '               1280 x 960',
        '               1280 x 1024',
        '               1360 x 768',
        '               1400 x 1050',
        '               1600 x 900', 
        '               1680 x 1050', 
        '               1920 x 1080'
    ]
    WSOrangeBoxReminderText = SMALLFONT.render('ESC: return to Settings.',True, WHITE)

    if WSOrangeBoxSet_Enabled == True:
        WSOrangeBoxSet = pygame.Rect(230, 0.10*HEIGHT, 0.70*WIDTH, 0.70*HEIGHT) #pygame.rect(pos.x, pos.y, width, height)
        pygame.draw.rect(WIN,ORANGE,WSOrangeBoxSet,border_top_left_radius=12,border_bottom_left_radius=12, border_top_right_radius=12,border_bottom_right_radius=12) #pygame.draw.rect(surface, color, figure, bordertopleft [optional], borderbottomleft [optional])
        pygame.draw.rect(WIN,BLACK, WSOrangeBoxSet, 1, border_top_left_radius=12,border_bottom_left_radius=12, border_top_right_radius=12,border_bottom_right_radius=12)
        WIN.blit(WSOrangeBoxReminderText,(240,0.06*HEIGHT))
        y_offset = WSOrangeBoxSet.y + padding_y #y its the y_pos, padding_y = padding_x = 10

        for line in WSOrangeBoxLines:
            text_surface = SMALLFONT.render(line, True, BLACK)
            text_rect =text_surface.get_rect(topleft=(WSOrangeBoxSet.x + padding_x, y_offset))
            #print(f"Text: '{line.strip()}', y_position: {y_offset}, height: {text_surface.get_height()}")
            WIN.blit(text_surface, text_rect)
            y_offset += text_surface.get_height() + lines_spacing #lines_spacing = 5

        STEscapeButton.enabled = False
        STControlsButton.enabled = False
        STWindowSizeButton.enabled = False
        STBackgroundButton.enabled = False
        STSoundButton.enabled = False
        STDeckImageButton.enabled = False

    if ESCAPE and WSOrangeBoxSet_Enabled == True:
        WSArrowCondition = False
        WSOrangeBoxSet_Enabled = False
        #.
        STEscapeButton.enabled = True
        STControlsButton.enabled = True
        STWindowSizeButton.enabled = True
        STBackgroundButton.enabled = True
        STDeckImageButton.enabled = True
        STSoundButton.enabled = True
        return game_state #this skips the rest of the def() function, so we can load properly on 1 frame

    #Selector Mode
    if WSSelectorMode == True: 
        
    #   Arrow blit
        if WSArrowCondition == True:
            WSArrow = os.path.join(sprites_folder, "arrow_right.png")
            AW = pygame.transform.scale(pygame.image.load(WSArrow).convert_alpha(), (50, 35))
            WSArrowX = WSArrowSlot[1] #this fetches the arrow's X position (from the Arrow Slot) to blit later on
            WSArrowY = WSArrowSlot[2] #this fetches the arrow's Y position (from the Arrow Slot) to blit later on
            WIN.blit(AW, (WSArrowX, WSArrowY))

            if DOWNARROW:
                if WSArrowSlot[0] != 12: #this checks if the arrow is not in the last row
                        #sound
                        WSArrowSlot = WSArrowSlots[WSArrowSlot[0]] #this is incrementing in 1 position
            elif UPARROW:
                if WSArrowSlot[0] != 1: #this checks if the arrow is not in the first row
                        #sound
                        WSArrowSlot = WSArrowSlots[WSArrowSlot[0]-2]

    #   Pressing ENTER
        if ENTER:
            WSConfirmationBox_Enabled = True
            WSCancelButton.enabled = True
            WSOKButton.enabled = True
            WSArrowCondition = False
            WSSelectorMode = False  
        
    #   Pressing ESC
        if ESCAPE:
            WSArrowCondition = False
            WSSelectorMode = False
            STEscapeButton.enabled = True
            STControlsButton.enabled = True  
            STWindowSizeButton.enabled = True
            STSoundButton.enabled = True
            STBackgroundButton.enabled = True
            STDeckImageButton.enabled = True      
            WSArrowSlot = WSArrowSlots[0]

    #Confirmation Box
    '''WSConfirmationBox_Width = 328
       WSConfirmationBox_Height = 220'''

    if WSConfirmationBox_Enabled == True:
        WSConfirmationRect = pygame.Rect(0.5*WIDTH-WSConfirmationBox_Width/2, 0.5*HEIGHT-WSConfirmationBox_Height/2,WSConfirmationBox_Width, WSConfirmationBox_Height) #left, top, width, height
        pygame.draw.rect(WIN, ORANGE, WSConfirmationRect, border_radius=12)
        pygame.draw.rect(WIN, BLACK, WSConfirmationRect, 1, border_radius=12)
        ConfirmationText = FONT.render('Apply changes?', True, BLACK)
        ConfirmationText_rect = ConfirmationText.get_rect(center=(WIDTH//2, HEIGHT//2 - 30))
        WIN.blit(ConfirmationText, ConfirmationText_rect)

    #   Ok Button
        button_text = SMALLFONT.render(WSOKButton.text, True, BLACK)
        text_rect = button_text.get_rect(center=(WSOKButton.x_pos + WSOKButton.length//2, WSOKButton.y_pos + WSOKButton.height//2))
        button_rect = pygame.rect.Rect((WSOKButton.x_pos,WSOKButton.y_pos),(WSOKButton.length,WSOKButton.height))     
        
        if WSOKButton.enabled == True:
            bcolor = WSOKButton.color
        elif WSOKButton.enabled == False:
            bcolor = GRAY

        if button_rect.collidepoint(mouse_pos) and WSOKButton.enabled == True:
            if LeftClick:
                bcolor = DARK_ORANGE 
                WIDTH = WSArrowSlot[3]
                HEIGHT = WSArrowSlot[4]
                with open (ConfigFile,'r') as file:
                    lines = file.readlines()
                
                #modifying
                for i in range(len(lines)):
                    if lines[i].startswith('WIDTH'):
                        lines[i] = f'WIDTH = {WIDTH}\n'
                    elif lines[i].startswith('HEIGHT'):
                        lines[i] = f'HEIGHT = {HEIGHT}\n'
           
                WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #this changes the window

                #writing
                with open(ConfigFile, 'w') as file:
                    file.writelines(lines)

                #fixing modes
                WSArrowCondition = True
                WSSelectorMode = True
                WSConfirmationBox_Enabled = False

                #fixing arrows
                Build_WS_Arrows()

                #.
                return game_state #this skips the rest of the def() function, so we can load properly on 1 frame
            else:
                bcolor = LIGHT_ORANGE

        pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
        pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
        WIN.blit(button_text, text_rect) #text and position 

    #   Cancel Button
        button_text = SMALLFONT.render(WSCancelButton.text, True, BLACK)
        text_rect = button_text.get_rect(center=(WSCancelButton.x_pos + WSCancelButton.length//2, WSCancelButton.y_pos + WSCancelButton.height//2))
        button_rect = pygame.rect.Rect((WSCancelButton.x_pos,WSCancelButton.y_pos),(WSCancelButton.length,WSCancelButton.height))

        if WSCancelButton.enabled == True:
            bcolor = WSCancelButton.color
        elif WSCancelButton.enabled == False:
            bcolor = GRAY
        
        if button_rect.collidepoint(mouse_pos) and WSCancelButton.enabled == True:
            if LeftClick:
                bcolor = DARK_ORANGE
                WSConfirmationBox_Enabled = False
                WSArrowCondition = True
                WSSelectorMode = True
                WSOKButton.enabled = False
                WSCancelButton.enabled = False
                #.
                return game_state #this skips the rest of the def() function, so we can load properly on 1 frame
            else:
                bcolor = LIGHT_ORANGE
        
        pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
        pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
        WIN.blit(button_text, text_rect)

#---------------------------------------------------------------------------------------------------------------------------

    #SETTINGS - UPDATE
    pygame.display.update()
    return game_state

#---------------------------------------------------------------------------------------------------------------------------

#TUTORIAL SCREEN
def draw_tutorial(mouse_pos, LeftClick):
    global game_state, UPARROW, DOWNARROW, RIGHTARROW, LEFTARROW, ESCAPE, ENTER
    global TutorialPage, drawlink

    '''
    This is the screen we get when we click the "Tutorial" in the main menu. It's purpose is
    showing how to play the game
    '''

    #BACKGROUND
    #BGImage is being set in the beginning of the program
    BG = pygame.transform.scale(pygame.image.load(BGImage).convert(), (WIDTH, HEIGHT))
    WIN.blit(BG, (0, 0))

    #MAIN SCREEN
    CRColor = ORANGE
    CRtext = BLACK
    padding_y = 10
    padding_x = 5
    lines_spacing = 5

    '''
    In all screens, the main orange box in the middle has the following dimensions:
    Width = WIDTH - 100
    Height = HEIGHT - 150
    Distance from Top = 100
    Distance from Bottom = 50
    Distance from Left = 50
    Distance from Right = 50
    '''

    if TutorialPage == 1:
        tutorial1text = [
            'HOW TO PLAY THE GAME',
            '',
            'Scoundrel is a dungeon-crawler one-person game, in which your objective is to clear all cards from the deck, or as it’s called in-game: your dungeon.',
            'Every turn, you are going to draw new cards and face them. Cards can be one of 3 types:',
            '',
            '- Monsters (Spades and Clubs): Need to be slain, either un-armed or with a weapon;',
            '- Weapons (Diamonds): Can be equipped, making you take less damage from monsters;',
            '- Potions (Hearts): Recover your Health Points.',
        ]
        
        OrangeBoxSet = pygame.Rect(50, 100, WIDTH-100, HEIGHT-150) 
        pygame.draw.rect(WIN,CRColor,OrangeBoxSet,border_top_left_radius=12,border_bottom_left_radius=12, border_top_right_radius=12,border_bottom_right_radius=12) #pygame.draw.rect(surface, color, figure, bordertopleft [optional], borderbottomleft [optional])
        pygame.draw.rect(WIN,BLACK, OrangeBoxSet, 1, border_top_left_radius=12,border_bottom_left_radius=12, border_top_right_radius=12,border_bottom_right_radius=12)
        y_offset = OrangeBoxSet.y + padding_y
        max_text_width = OrangeBoxSet.width - (padding_x * 2)

        #this is just some splitting of the OrangeBoxSet into spaces for plotting images, the division follows:
        #space 1 + CW + space 2 + CW + space 3 + CW + space 4
        SPACE = (WIDTH-100)-3*CW
        SPACES = SPACE/6
        SPACE1 = SPACES
        SPACE2 = 2*SPACES
        SPACE3 = 2*SPACES
        SPACE4 = SPACES

        def draw_wrapped_text(surface, text, font, color, x, y, max_width):
            words = text.split(' ')
            line = ''
            lines = []
            for word in words:
                test_line = line + word + ' '
                if font.size(test_line)[0] <= max_width:
                    line = test_line
                else:
                    lines.append(line)
                    line = word + ' '
            lines.append(line)
            return lines

        for line in tutorial1text:
            if line == '':
                y_offset += SMALLFONT.get_height() + lines_spacing
                continue
            wrapped_lines = draw_wrapped_text(WIN, line, SMALLFONT, CRtext, 
                                            OrangeBoxSet.x + padding_x, y_offset, max_text_width)
            for wrapped_line in wrapped_lines:
                text_surface = SMALLFONT.render(wrapped_line, True, CRtext)
                WIN.blit(text_surface, (OrangeBoxSet.x + padding_x, y_offset))
                y_offset += text_surface.get_height() + lines_spacing

        #these are the images shown below the text

        TextImage1 = "MONSTER"
        TextImage2 = "WEAPON"
        TextImage3 = "POTION"

        Text1 = SMALLFONT.render(TextImage1 ,True, BLACK)
        Text2 = SMALLFONT.render(TextImage2 ,True, BLACK)
        Text3 = SMALLFONT.render(TextImage3 ,True, BLACK)

        WIN.blit(Text1,((WIDTH/2- SPACE2 - CW - CW/4),(HEIGHT-150-20-CH-30)))
        WIN.blit(Text2,((WIDTH/2 - CW/4), (HEIGHT-150-20-CH-30)))
        WIN.blit(Text3,((WIDTH/2+ CW/2 + SPACE3 + CW/2 - CW/4), (HEIGHT-150-20-CH-30)))

        #IMAGES
        Image1 = os.path.join(Current_Deck, "6_of_clubs.png") 
        IMG1 = pygame.transform.scale(pygame.image.load(Image1), (CW, CH))
        WIN.blit(IMG1, ((WIDTH/2-CW/2 - SPACE2 - CW), (HEIGHT-150-20-CH)))   

        Image2 = os.path.join(Current_Deck, "3_of_diamonds.png") 
        IMG2 = pygame.transform.scale(pygame.image.load(Image2), (CW, CH))
        WIN.blit(IMG2, ((WIDTH/2-CW/2), (HEIGHT-150-20-CH))) 

        Image3 = os.path.join(Current_Deck, "8_of_hearts.png") 
        IMG3 = pygame.transform.scale(pygame.image.load(Image3), (CW, CH))
        WIN.blit(IMG3, ((WIDTH/2+ CW/2 + SPACE3), (HEIGHT-150-20-CH)))

    if TutorialPage == 2:
        tutorial2text = [
            'STARTING THE GAME',
            '',
            'The deck is a traditional 52 cards deck, in which one remove all red face cards (Q, J, K) and aces (A), as well as the possible jokers, ending up with a 44 cards deck.',
            '',
            'You start the game by drawing 4 cards and placing them face-up. This is your current room. You clear the room once you encounter 3 of the 4 cards revealed. ',
            'Once that happens, you draw 3 new cards, and face them again. This repeats until you either lose the game by deplenishing your health or facing all cards in the game.',
            '',
            'Hence, you start the game with 44 cards to encounter and with 20 Health Points (HP). Should your HP get to 0 or below at any time, you die, and your run is over.',
        ]
        
        OrangeBoxSet = pygame.Rect(50, 100, WIDTH-100, HEIGHT-150) 
        pygame.draw.rect(WIN,CRColor,OrangeBoxSet,border_top_left_radius=12,border_bottom_left_radius=12, border_top_right_radius=12,border_bottom_right_radius=12) #pygame.draw.rect(surface, color, figure, bordertopleft [optional], borderbottomleft [optional])
        pygame.draw.rect(WIN,BLACK, OrangeBoxSet, 1, border_top_left_radius=12,border_bottom_left_radius=12, border_top_right_radius=12,border_bottom_right_radius=12)
        y_offset = OrangeBoxSet.y + padding_y
        max_text_width = OrangeBoxSet.width - (padding_x * 2)

        def draw_wrapped_text(surface, text, font, color, x, y, max_width):
            words = text.split(' ')
            line = ''
            lines = []
            for word in words:
                test_line = line + word + ' '
                if font.size(test_line)[0] <= max_width:
                    line = test_line
                else:
                    lines.append(line)
                    line = word + ' '
            lines.append(line)
            return lines

        for line in tutorial2text:
            if line == '':
                y_offset += SMALLFONT.get_height() + lines_spacing
                continue
            wrapped_lines = draw_wrapped_text(WIN, line, SMALLFONT, CRtext, 
                                            OrangeBoxSet.x + padding_x, y_offset, max_text_width)
            for wrapped_line in wrapped_lines:
                text_surface = SMALLFONT.render(wrapped_line, True, CRtext)
                WIN.blit(text_surface, (OrangeBoxSet.x + padding_x, y_offset))
                y_offset += text_surface.get_height() + lines_spacing
            
        SPACE = (WIDTH-150)
        DEDUCTION_SPACE = SPACE - 5*CW
        SPACES = DEDUCTION_SPACE/12
        BIG_SPACE = 3*SPACES
        SMALL_SPACE = 1*SPACES
        '''
        This is dividing the orange screen in 12 parts. The division uses "big spaces" as 3 parts and "small spaces as 1 part"
        It follows as: 
        BIG SPACE - DECK - BIG SPACE - SLOT 1 - SMALL SPACE - SLOT 2 - SMALL SPACE - SLOT 3 - SMALL SPACE - SLOT 4 - BIG SPACE
        '''
        #these are the X positions for the spacial coordinates of the deck and the 4 slots.
        DeckX = int(50 + 1*BIG_SPACE)
        Slot1X = int(50 + 2*BIG_SPACE + 1*CW)
        Slot2X = int(50 + 2*BIG_SPACE + 2*CW + 1*SMALL_SPACE)
        Slot3X = int(50 + 2*BIG_SPACE + 3*CW + 2*SMALL_SPACE)
        Slot4X = int(50 + 2*BIG_SPACE + 4*CW + 3*SMALL_SPACE)
        SPACING = int(80)
        YPos = int(HEIGHT-50-SPACING-CH)

        TextImage1 = "DECK"
        TextImage2 = "EXAMPLE OF ROOM"

        Text1 = SMALLFONT.render(TextImage1, True, BLACK)
        Text2 = SMALLFONT.render(TextImage2, True, BLACK)

        WIN.blit(Text1,((50+1*BIG_SPACE + CW/2 - 10),(YPos - 30))) #this X POS is in the middle of the deck slots
        WIN.blit(Text2,((50+2*BIG_SPACE+1.5*SMALL_SPACE+3*CW - 40), (YPos - 30))) #this X POS is in the middle of the 4 slots

        #IMAGES
        Image1 = os.path.join(Current_Deck, "cardback.png") 
        IMG1 = pygame.transform.scale(pygame.image.load(Image1), (CW, CH))
        WIN.blit(IMG1, ((DeckX), (YPos)))   

        Image2 = os.path.join(Current_Deck, "5_of_clubs.png") 
        IMG2 = pygame.transform.scale(pygame.image.load(Image2), (CW, CH))
        WIN.blit(IMG2, ((Slot1X), (YPos))) 

        Image3 = os.path.join(Current_Deck, "6_of_diamonds.png") 
        IMG3 = pygame.transform.scale(pygame.image.load(Image3), (CW, CH))
        WIN.blit(IMG3, ((Slot2X), (YPos)))

        Image4 = os.path.join(Current_Deck, "2_of_hearts.png") 
        IMG4 = pygame.transform.scale(pygame.image.load(Image4), (CW, CH))
        WIN.blit(IMG4, ((Slot3X), (YPos)))

        Image5 = os.path.join(Current_Deck, "jack_of_clubs.png") 
        IMG5 = pygame.transform.scale(pygame.image.load(Image5), (CW, CH))
        WIN.blit(IMG5, ((Slot4X), (YPos)))

    if TutorialPage == 3:
        tutorial3text = ['ENCOUNTERING CARDS',
            '',
            'Encountering cards is how you resolve the game. Basically, click the card with the LEFT CLICK to face it. If you have a weapon, you can use RIGHT CLICK to use the weapon. The 3 types of cards are:',
            '',
            '- Monsters: you can slain the monster, killing it and taking damage equal to the monsters’ score. Numbers have a score equal to its value, and J, Q, K, A have a value of 11, 12, 13 and 14, respectively.',
            '- Weapon: you can equip the weapon. You can only use 1 weapon at a time. Weapons reduce the damage you take by the weapons’ value. Once a monster is slain, it becomes a trophy with that weapon. You cannot slain monsters of equal score or stronger than your trophies’ score.',
            '- Potion: you can recover your health points equal the value of the potion. Only 1 potion per turn will have effect, meaning if you use 2 or more potions in one turn, all the potions but the second will yield no effect.'
        ]

        OrangeBoxSet = pygame.Rect(50, 100, WIDTH-100, HEIGHT-150) 
        pygame.draw.rect(WIN,CRColor,OrangeBoxSet,border_top_left_radius=12,border_bottom_left_radius=12, border_top_right_radius=12,border_bottom_right_radius=12) #pygame.draw.rect(surface, color, figure, bordertopleft [optional], borderbottomleft [optional])
        pygame.draw.rect(WIN,BLACK, OrangeBoxSet, 1, border_top_left_radius=12,border_bottom_left_radius=12, border_top_right_radius=12,border_bottom_right_radius=12)
        y_offset = OrangeBoxSet.y + padding_y
        max_text_width = OrangeBoxSet.width - (padding_x * 2)

        def draw_wrapped_text(surface, text, font, color, x, y, max_width):
            words = text.split(' ')
            line = ''
            lines = []
            for word in words:
                test_line = line + word + ' '
                if font.size(test_line)[0] <= max_width:
                    line = test_line
                else:
                    lines.append(line)
                    line = word + ' '
            lines.append(line)
            return lines

        for line in tutorial3text:
            if line == '':
                y_offset += SMALLFONT.get_height() + lines_spacing
                continue
            wrapped_lines = draw_wrapped_text(WIN, line, SMALLFONT, CRtext, 
                                            OrangeBoxSet.x + padding_x, y_offset, max_text_width)
            for wrapped_line in wrapped_lines:
                text_surface = SMALLFONT.render(wrapped_line, True, CRtext)
                WIN.blit(text_surface, (OrangeBoxSet.x + padding_x, y_offset))
                y_offset += text_surface.get_height() + lines_spacing

        SPACE = (WIDTH-150)
        DEDUCTION_SPACE = SPACE - 5*CW
        SPACES = DEDUCTION_SPACE/12
        BIG_SPACE = 3*SPACES
        SMALL_SPACE = 1*SPACES
        '''
        This is dividing the orange screen in 12 parts. The division uses "big spaces" as 3 parts and "small spaces as 1 part"
        It follows as: 
        BIG SPACE - DECK - BIG SPACE - SLOT 1 - SMALL SPACE - SLOT 2 - SMALL SPACE - SLOT 3 - SMALL SPACE - SLOT 4 - BIG SPACE
        '''
        #these are the X positions for the spacial coordinates of the deck and the 4 slots.
        DeckX = int(50 + 1*BIG_SPACE)
        Slot1X = int(50 + 2*BIG_SPACE + 1*CW)
        Slot2X = int(50 + 2*BIG_SPACE + 2*CW + 1*SMALL_SPACE)
        Slot3X = int(50 + 2*BIG_SPACE + 3*CW + 2*SMALL_SPACE)
        Slot4X = int(50 + 2*BIG_SPACE + 4*CW + 3*SMALL_SPACE)
        SPACING = int(80)
        YPos = int(HEIGHT-50-SPACING-CH)

        TextImage1 = "DECK"
        TextImage2 = "EXAMPLE OF ROOM"

        Text1 = SMALLFONT.render(TextImage1, True, BLACK)
        Text2 = SMALLFONT.render(TextImage2, True, BLACK)

        WIN.blit(Text1,((50+1*BIG_SPACE + CW/2 - 10),(YPos - 30))) #this X POS is in the middle of the deck slots
        WIN.blit(Text2,((50+2*BIG_SPACE+1.5*SMALL_SPACE+3*CW - 40), (YPos - 30))) #this X POS is in the middle of the 4 slots

        Explanation1 = "5 Damage"
        Explanation2 = "Absorbs 6 Damage"
        Explanation3 = "Recovers 2 HP"
        Explanation4 = "11 Damage"
    
        EXP1 = SMALLFONT.render(Explanation1, True, BLACK)
        EXP2 = SMALLFONT.render(Explanation2, True, BLACK)       
        EXP3 = SMALLFONT.render(Explanation3, True, BLACK)
        EXP4 = SMALLFONT.render(Explanation4, True, BLACK)

        WIN.blit(EXP1,((Slot1X + 25),(YPos + CH + 10)))
        WIN.blit(EXP2,((Slot2X + 0),(YPos + CH + 10)))
        WIN.blit(EXP3,((Slot3X + 15),(YPos + CH + 10)))
        WIN.blit(EXP4,((Slot4X + 25),(YPos + CH + 10)))

        #IMAGES
        Image1 = os.path.join(Current_Deck, "cardback.png") 
        IMG1 = pygame.transform.scale(pygame.image.load(Image1), (CW, CH))
        WIN.blit(IMG1, ((DeckX), (YPos)))   

        Image2 = os.path.join(Current_Deck, "5_of_clubs.png") 
        IMG2 = pygame.transform.scale(pygame.image.load(Image2), (CW, CH))
        WIN.blit(IMG2, ((Slot1X), (YPos))) 

        Image3 = os.path.join(Current_Deck, "6_of_diamonds.png") 
        IMG3 = pygame.transform.scale(pygame.image.load(Image3), (CW, CH))
        WIN.blit(IMG3, ((Slot2X), (YPos)))

        Image4 = os.path.join(Current_Deck, "2_of_hearts.png") 
        IMG4 = pygame.transform.scale(pygame.image.load(Image4), (CW, CH))
        WIN.blit(IMG4, ((Slot3X), (YPos)))

        Image5 = os.path.join(Current_Deck, "jack_of_clubs.png") 
        IMG5 = pygame.transform.scale(pygame.image.load(Image5), (CW, CH))
        WIN.blit(IMG5, ((Slot4X), (YPos)))

    if TutorialPage == 4:
        tutorial4text = [
            'FINISHING THE GAME',
            '',
            'When you finish the game, either by clearing all cards from the dungeon or dying, the game calculates your score by the following rules:',
            '',
            '1 - Monsters that weren’t slain, either in the dungeon deck or the room, counts as negative values;',
            '2 - Remaining potions count as positive values;',
            '3 - Remaining health points count as positive values.',
            '',
            'Therefore, the lowest score possible is -208, while the maximum score possible is 30, although anything above 0 is already beating the game and anything from 20 or more is beating the game without a scratch. Try to get to 30!',
            '',
            "OBS: If you're still unsure how to play and want a video explanation, Rulies has an amazing video on how to play Scoundrel on Youtube:",
        ]

        OrangeBoxSet = pygame.Rect(50, 100, WIDTH-100, HEIGHT-150) 
        pygame.draw.rect(WIN,CRColor,OrangeBoxSet,border_top_left_radius=12,border_bottom_left_radius=12, border_top_right_radius=12,border_bottom_right_radius=12) #pygame.draw.rect(surface, color, figure, bordertopleft [optional], borderbottomleft [optional])
        pygame.draw.rect(WIN,BLACK, OrangeBoxSet, 1, border_top_left_radius=12,border_bottom_left_radius=12, border_top_right_radius=12,border_bottom_right_radius=12)
        y_offset = OrangeBoxSet.y + padding_y
        max_text_width = OrangeBoxSet.width - (padding_x * 2)

        def draw_wrapped_text(surface, text, font, color, x, y, max_width):
            words = text.split(' ')
            line = ''
            lines = []
            for word in words:
                test_line = line + word + ' '
                if font.size(test_line)[0] <= max_width:
                    line = test_line
                else:
                    lines.append(line)
                    line = word + ' '
            lines.append(line)
            return lines

        for line in tutorial4text:
            if line == '':
                y_offset += SMALLFONT.get_height() + lines_spacing
                continue
            wrapped_lines = draw_wrapped_text(WIN, line, SMALLFONT, CRtext, 
                                            OrangeBoxSet.x + padding_x, y_offset, max_text_width)
            for wrapped_line in wrapped_lines:
                text_surface = SMALLFONT.render(wrapped_line, True, CRtext)
                WIN.blit(text_surface, (OrangeBoxSet.x + padding_x, y_offset))
                y_offset += text_surface.get_height() + lines_spacing

        #IMAGE
        ImageWidth = 620/2
        ImageHeight = 356/2
        FinalImage = os.path.join(image_folder, "Scoundrel_by_Rulies.png") 
        FIMG = pygame.transform.scale(pygame.image.load(FinalImage), (ImageWidth, ImageHeight))
        WIN.blit(FIMG, ((WIDTH/2)-ImageWidth/2, (HEIGHT-50-25-ImageHeight)))    

        #LINK
        temp_surface = SMALLFONT.render("How to Play Scoundrel", True, BLACK)
        link_rect = temp_surface.get_rect(topleft=((WIDTH/2-ImageWidth/4), (HEIGHT-50-25-ImageHeight - 25)))
        hovered = link_rect.collidepoint(mouse_pos)

        link = drawlink(WIN, "How to Play Scoundrel", "https://www.youtube.com/watch?v=Gt2tYzM93h4&t=251s", ((WIDTH/2-ImageWidth/4), (HEIGHT-50-25-ImageHeight - 25)), hovered)
        
        if link.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        if LeftClick and link.collidepoint(mouse_pos):
            webbrowser.open("https://www.youtube.com/watch?v=Gt2tYzM93h4&t=251s")

            
    #BUTTONS
    #   Go Back Button
    EscapeButton = Button("Go Back",50,50,True,20,CW,ORANGE)

    button_text = SMALLFONT.render(EscapeButton.text, True, BLACK)
    text_rect = button_text.get_rect(center=(EscapeButton.x_pos + EscapeButton.length//2, EscapeButton.y_pos + EscapeButton.height//2))
    button_rect = pygame.rect.Rect((EscapeButton.x_pos,EscapeButton.y_pos),(EscapeButton.length,EscapeButton.height))
    bcolor = EscapeButton.color
    if button_rect.collidepoint(mouse_pos):
        if LeftClick:
            bcolor = DARK_ORANGE
            game_state = "Main_Menu"            
        else:
            bcolor = LIGHT_ORANGE
    pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
    pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
    WIN.blit(button_text, text_rect)
    
    #   Arrows
    ArrowR = os.path.join(sprites_folder, "arrow_right.png")
    ArrowL = os.path.join(sprites_folder, "arrow_left.png")
    AWR = pygame.transform.scale(pygame.image.load(ArrowR), (40, 25))
    AWL = pygame.transform.scale(pygame.image.load(ArrowL), (40, 25))
    Button_Rect_AR = AWR.get_rect()
    Button_Rect_AL = AWL.get_rect()
    Button_Rect_AR.topleft = ((50+WIDTH-100-40,(HEIGHT - 50) - 25 - 50)) 
    Button_Rect_AL.topleft = ((50,(HEIGHT - 50) - 25 - 50))
    WIN.blit(AWR, Button_Rect_AR.topleft)
    WIN.blit(AWL, Button_Rect_AL.topleft)

    if Button_Rect_AL.collidepoint(mouse_pos) and LeftClick:
        if TutorialPage == 1:
            pass
        elif TutorialPage == 2 or TutorialPage== 3 or TutorialPage == 4:
            TutorialPage = TutorialPage-1

    if Button_Rect_AR.collidepoint(mouse_pos) and LeftClick:
        if TutorialPage == 4:
            pass
        elif TutorialPage == 1 or TutorialPage== 2 or TutorialPage == 3:
            TutorialPage = TutorialPage+1

    #PAGES
    PagesText1 = str(TutorialPage)
    PagesText2 = "/4"
    PagesText = SMALLFONT.render(PagesText1+PagesText2 ,True, BLACK)
    WIN.blit(PagesText, ((50+WIDTH-100-35), (100+HEIGHT-150-35)))

    #UPDATE
    pygame.display.update()
    return game_state

#---------------------------------------------------------------------------------------------------------------------------

#SCOREBOARD SCREEN
def draw_STscoreboard(mouse_pos, LeftClick):
    global game_state, UPARROW, DOWNARROW, RIGHTARROW, LEFTARROW, ESCAPE, ENTER

    '''
    This is the screen we get when we click the "scoreboard" in the main menu. It's only purpose is
    showing the score and save files.
    '''

    #BACKGROUND
    #BGImage is being set in the beginning of the program
    BG = pygame.transform.scale(pygame.image.load(BGImage).convert(), (WIDTH, HEIGHT))
    WIN.blit(BG, (0, 0))

    #BUTTONS
    #   Go Back Button
    button_text = SMALLFONT.render(STSC_MainMenuButton.text, True, BLACK)
    text_rect = button_text.get_rect(center=(STSC_MainMenuButton.x_pos + STSC_MainMenuButton.length//2, STSC_MainMenuButton.y_pos + STSC_MainMenuButton.height//2))
    button_rect = pygame.rect.Rect((STSC_MainMenuButton.x_pos,STSC_MainMenuButton.y_pos),(STSC_MainMenuButton.length,STSC_MainMenuButton.height))
    if STSC_MainMenuButton.enabled == True:
        bcolor = STSC_MainMenuButton.color
    elif STSC_MainMenuButton.enabled == False:
        bcolor = GRAY
    if button_rect.collidepoint(mouse_pos) and STSC_MainMenuButton.enabled == True:
        if LeftClick:
            bcolor = DARK_ORANGE
            game_state = "Main_Menu"
        else:
            bcolor = LIGHT_ORANGE
    pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
    pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
    WIN.blit(button_text, text_rect)

    #SCOREBOARD SCREEN
    SCColor = ORANGE
    SCText = BLACK

    #   LeftRectangle (Called Surf1)
    SC_surf1 = BIGFONT.render ('',True,SCText)
    rect1 = pygame.Rect(0.15*WIDTH, 0.15*HEIGHT, 0.35*WIDTH, 0.70*HEIGHT)  #pygame.rect(pos.x, pos.y, width, height)
    pygame.draw.rect(WIN,SCColor,rect1, border_top_left_radius=12,border_bottom_left_radius=12) #pygame.draw.rect(surface, color, figure, bordertopleft [optional], borderbottomleft [optional])
    
    text_rect = SC_surf1.get_rect(center=rect1.center)
    WIN.blit(SC_surf1, text_rect)

    #   RightRectangle (Called Surf2)
    SC_surf2 = BIGFONT.render ('',True,SCText)
    rect2 = pygame.Rect(0.50*WIDTH, 0.15*HEIGHT, 0.35*WIDTH, 0.70*HEIGHT) #pygame.rect(pos.x, pos.y, width, height)
    pygame.draw.rect(WIN,SCColor,rect2, border_top_right_radius=12,border_bottom_right_radius=12) #pygame.draw.rect(surface, color, figure, bordertopleft [optional], borderbottomleft [optional])
    
    text_rect = SC_surf2.get_rect(center=rect2.center)
    WIN.blit(SC_surf2, text_rect)

    #   Black Border
    rect3 = pygame.Rect(0.15*WIDTH, 0.15*HEIGHT, 0.70*WIDTH, 0.70*HEIGHT)  #pygame.rect(pos.x, pos.y, width, height)
    pygame.draw.rect(WIN, BLACK, rect3, width = 1, border_top_left_radius=12,border_bottom_left_radius=12, border_top_right_radius=12,border_bottom_right_radius=12)

    #   Plotting Saves 1 - 5 in Left Rectangle
    i = -1 #increment to print slots
    for Save in Saves:
        if Save[0] == 'Save6':
            break
        i = i + 1
        if Save[1] == 'Empty':
            SaveText = '_ _ _'
        else:
            if str(Save[2]) == '-inf':
                ScoreValue = ''
            else:
                ScoreValue = str(Save[2])
            SaveText = Save[1] + ' ' + ScoreValue
        text = BIGFONT.render(SaveText,True, BLACK)
        WIN.blit(text,((rect1.x + 0.15*(rect1.width)),((rect1.y + 0.10*(rect1.height)+(i*0.15*(rect1.height)))))) #(surface, pos.x, pos.y)
    i = 0

    #   Plotting Saves 6 - 10 in Right Rectangle
    i = -1 #increment to print slots
    for Save in Saves:
        if Save[0] == 'Save1' or Save[0] == 'Save2' or Save[0] == 'Save3' or Save[0] == 'Save4' or Save[0] == 'Save5':
            continue
        i = i + 1
        if Save[1] == 'Empty':
            SaveText = '_ _ _'
        else:
            if str(Save[2]) == '-inf':
                ScoreValue = ''
            else:
                ScoreValue = str(Save[2])
            SaveText = Save[1] + ' ' + ScoreValue
        text = BIGFONT.render(SaveText,True, BLACK)
        #WIN.blit(Source,(x,y))
        WIN.blit(text,((rect2.x + 0.15*(rect2.width)),((rect2.y + 0.10*(rect2.height)+(i*0.15*(rect2.height))))))
    i = 0

    #UPDATE
    pygame.display.update()
    return game_state

#---------------------------------------------------------------------------------------------------------------------------

#GAME SCOREBOARD SCREEN
def draw_scoreboard(mouse_pos, LeftClick):
    global game_state, UPARROW, DOWNARROW, RIGHTARROW, LEFTARROW, ESCAPE, ENTER
    global Saves
    global ArrowCondition, ArrowSlots, ArrowSlot, Arrow1, Arrow2, Arrow3, Arrow4, Arrow5, Arrow6, Arrow7, Arrow8, Arrow9, Arrow10
    global SaveSelectorMode, WritingMode, SaveDeleteMode, DeleteMode, DeleteConfirmationBoxEnabled, DeleteYesButton, DeleteNoButton
    global PlayerName, rows 
    global BGImage
    global y_offset

    #BACKGROUND
    #BGImage is being set in the beginning of the program
    BG = pygame.transform.scale(pygame.image.load(BGImage).convert(), (WIDTH, HEIGHT))
    WIN.blit(BG, (0, 0))

    #ICONS
    #Arrows Scoreboard
    #ArrowZ = [No, Row, Column, PosX, PosY] Remember that the arrows are 40, 20
    Arrow1  = [1, 1, 1,(0.15*WIDTH) ,(0.15*HEIGHT + 0.10*(0.70*HEIGHT)+(1*0.15*(0.70*HEIGHT))-(50))]
    Arrow2  = [2, 2, 1,(0.15*WIDTH) ,(0.15*HEIGHT + 0.10*(0.70*HEIGHT)+(2*0.15*(0.70*HEIGHT))-(50))]
    Arrow3  = [3, 3, 1,(0.15*WIDTH) ,(0.15*HEIGHT + 0.10*(0.70*HEIGHT)+(3*0.15*(0.70*HEIGHT))-(50))]
    Arrow4  = [4, 4, 1,(0.15*WIDTH) ,(0.15*HEIGHT + 0.10*(0.70*HEIGHT)+(4*0.15*(0.70*HEIGHT))-(50))]
    Arrow5  = [5, 5, 1,(0.15*WIDTH) ,(0.15*HEIGHT + 0.10*(0.70*HEIGHT)+(5*0.15*(0.70*HEIGHT))-(50))]
    Arrow6  = [6, 1, 2,(0.50*WIDTH) ,(0.15*HEIGHT + 0.10*(0.70*HEIGHT)+(1*0.15*(0.70*HEIGHT))-(50))]
    Arrow7  = [7, 2, 2,(0.50*WIDTH) ,(0.15*HEIGHT + 0.10*(0.70*HEIGHT)+(2*0.15*(0.70*HEIGHT))-(50))]
    Arrow8  = [8, 3, 2,(0.50*WIDTH) ,(0.15*HEIGHT + 0.10*(0.70*HEIGHT)+(3*0.15*(0.70*HEIGHT))-(50))]
    Arrow9  = [9, 4, 2,(0.50*WIDTH) ,(0.15*HEIGHT + 0.10*(0.70*HEIGHT)+(4*0.15*(0.70*HEIGHT))-(50))]
    Arrow10 = [10, 5, 2,(0.50*WIDTH) ,(0.15*HEIGHT + 0.10*(0.70*HEIGHT)+(5*0.15*(0.70*HEIGHT))-(50))]
    
    #there is also the variable 'ArrowSlot', that saves one of the arrow from the ArrowSlots on it, the current we are in.
    ArrowSlots = [Arrow1, Arrow2, Arrow3, Arrow4, Arrow5, Arrow6, Arrow7, Arrow8, Arrow9, Arrow10]

    '''
    Just rememebering, the ArrowSlots has a 1:1 correspondency with the List of Saves. The List of Saves is something like:
    Save1 = ["Slot1", "Name", "Score"]
    Save2 = ["Slot2", "Name", "Score"]
    Save3 = ["Slot3", "Name", "Score"]
    Save4 = ["Slot4", "Name", "Score"]
    Save5 = ["Slot5", "Name", "Score"]
    Save6 = ["Slot6", "Name", "Score"]
    Save7 = ["Slot7", "Name", "Score"]
    Save8 = ["Slot8", "Name", "Score"]
    Save9 = ["Slot9", "Name", "Score"]
    Save10 = ["Slot10", "Name", "Score"]

    Saves =[Save1, Save2, Save3, Save4, Save5, Save6, Save7, Save8, Save9, Save10]
    '''

    #BUTTONS
    #Text, Xpos, Ypos, Enabled, FontSize, Length, Color
    #SC_MainMenuButton  
    #SC_SaveGameButton
    #SC_DeleteGameButton 
    #SC_QuitButton 

    #   Main Menu Button
    button_text = SMALLFONT.render(SC_MainMenuButton.text, True, BLACK)
    text_rect = button_text.get_rect(center=(SC_MainMenuButton.x_pos + SC_MainMenuButton.length//2, SC_MainMenuButton.y_pos + SC_MainMenuButton.height//2))
    button_rect = pygame.rect.Rect((SC_MainMenuButton.x_pos,SC_MainMenuButton.y_pos),(SC_MainMenuButton.length,SC_MainMenuButton.height))
    if SC_MainMenuButton.enabled == True:
        bcolor = SC_MainMenuButton.color
    elif SC_MainMenuButton.enabled == False:
        bcolor = GRAY
    if button_rect.collidepoint(mouse_pos) and SC_MainMenuButton.enabled == True:
        if LeftClick:
            bcolor = DARK_ORANGE
            game_state = "Main_Menu"
        else:
            bcolor = LIGHT_ORANGE
    pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
    pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
    WIN.blit(button_text, text_rect)

    #   Save Game Button
    button_text = SMALLFONT.render(SC_SaveGameButton.text, True, BLACK)
    text_rect = button_text.get_rect(center=(SC_SaveGameButton.x_pos + SC_SaveGameButton.length//2, SC_SaveGameButton.y_pos + SC_SaveGameButton.height//2))
    button_rect = pygame.rect.Rect((SC_SaveGameButton.x_pos,SC_SaveGameButton.y_pos),(SC_SaveGameButton.length,SC_SaveGameButton.height))
    if SC_SaveGameButton.enabled == True:
        bcolor = SC_SaveGameButton.color
    elif SC_SaveGameButton.enabled == False:
        bcolor = GRAY
    if button_rect.collidepoint(mouse_pos) and SC_SaveGameButton.enabled == True:
        if LeftClick: 
            SC_MainMenuButton.enabled = False
            SC_SaveGameButton.enabled = False
            SC_DeleteGameButton.enabled = False
            SC_QuitButton.enabled = False
            SaveSelectorMode = True
            ArrowCondition = True
            #.
            #finding the first empty slot
            ArrowSlot = None
            for i in range(0, 10): 
                    if Saves[i][1] == 'Empty':
                        ArrowSlot = ArrowSlots[i]
                        break
                    elif Saves[i][1] != 'Empty' and i == 9:
                        #put a warning, something here when all slots are full
                        break
                    else:
                        continue
        else:
            bcolor = LIGHT_ORANGE

    pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
    pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
    WIN.blit(button_text, text_rect)

    #   Delete Game Button
    button_text = SMALLFONT.render(SC_DeleteGameButton.text, True, BLACK)
    text_rect = button_text.get_rect(center=(SC_DeleteGameButton.x_pos + SC_DeleteGameButton.length//2, SC_DeleteGameButton.y_pos + SC_DeleteGameButton.height//2))
    button_rect = pygame.rect.Rect((SC_DeleteGameButton.x_pos,SC_DeleteGameButton.y_pos),(SC_DeleteGameButton.length,SC_DeleteGameButton.height))
    if SC_DeleteGameButton.enabled == True:
        bcolor = SC_DeleteGameButton.color
    elif SC_DeleteGameButton.enabled == False:
        bcolor = GRAY
    if button_rect.collidepoint(mouse_pos) and SC_DeleteGameButton.enabled == True:
        if LeftClick:
            SC_MainMenuButton.enabled = False
            SC_SaveGameButton.enabled = False
            SC_DeleteGameButton.enabled = False
            SC_QuitButton.enabled = False
            SaveDeleteMode = True
            ArrowCondition = True
            ArrowSlot = None
            #.
            #finding the first non-empty slot
            for i in range(0, 10): 
                if Saves[i][1] != 'Empty':
                    ArrowSlot = ArrowSlots[i]
                    break
                elif i == 9 and Saves[i][1] != 'Empty':
                    #put a warning, something here when all slots are full
                    break
                else:
                    continue
        else:
            bcolor = LIGHT_ORANGE
    
    pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
    pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
    WIN.blit(button_text, text_rect)

    #   Quit Game Button
    button_text = SMALLFONT.render(SC_QuitButton.text, True, BLACK)
    text_rect = button_text.get_rect(center=(SC_QuitButton.x_pos + SC_QuitButton.length//2, SC_QuitButton.y_pos + SC_QuitButton.height//2))
    button_rect = pygame.rect.Rect((SC_QuitButton.x_pos,SC_QuitButton.y_pos),(SC_QuitButton.length,SC_QuitButton.height))
    if SC_QuitButton.enabled == True:
        bcolor = SC_QuitButton.color
    elif SC_QuitButton.enabled == False:
        bcolor = GRAY
    if button_rect.collidepoint(mouse_pos) and SC_QuitButton.enabled == True:
        if LeftClick:
            quit()
        else:
            bcolor = LIGHT_ORANGE
    
    pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
    pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
    WIN.blit(button_text, text_rect)

    #SCOREBOARD
    SCColor = ORANGE
    SCText = BLACK
    TipsColor = WHITE

    #   Button Tips
    ButtonTip1 = SMALLFONT.render ('Arrow Keys = Change save slot',True, TipsColor)
    WIN.blit(ButtonTip1, (0.15*WIDTH+20, 0.03*HEIGHT))

    ButtonTip2 = SMALLFONT.render ('ENTER = Select Save to write',True, TipsColor)
    WIN.blit(ButtonTip2, (0.15*WIDTH+20, 0.07*HEIGHT))   

    ButtonTip3 = SMALLFONT.render ('Esc = Go back',True, TipsColor)
    WIN.blit(ButtonTip3, (0.15*WIDTH+20, 0.11*HEIGHT))

    #   LeftRectangle (Called Surf1)
    SC_surf1 = BIGFONT.render ('',True,SCText)
    rect1 = pygame.Rect(0.15*WIDTH, 0.15*HEIGHT, 0.35*WIDTH, 0.70*HEIGHT)  #pygame.rect(pos.x, pos.y, width, height)
    pygame.draw.rect(WIN,SCColor,rect1, border_top_left_radius=12,border_bottom_left_radius=12) #pygame.draw.rect(surface, color, figure, bordertopleft [optional], borderbottomleft [optional])
    
    text_rect = SC_surf1.get_rect(center=rect1.center)
    WIN.blit(SC_surf1, text_rect)

    #   RightRectangle (Called Surf2)
    SC_surf2 = BIGFONT.render ('',True,SCText)
    rect2 = pygame.Rect(0.50*WIDTH, 0.15*HEIGHT, 0.35*WIDTH, 0.70*HEIGHT) #pygame.rect(pos.x, pos.y, width, height)
    pygame.draw.rect(WIN,SCColor,rect2, border_top_right_radius=12,border_bottom_right_radius=12) #pygame.draw.rect(surface, color, figure, bordertopleft [optional], borderbottomleft [optional])
    
    text_rect = SC_surf2.get_rect(center=rect2.center)
    WIN.blit(SC_surf2, text_rect)

    #   Black Border
    rect3 = pygame.Rect(0.15*WIDTH, 0.15*HEIGHT, 0.70*WIDTH, 0.70*HEIGHT)  #pygame.rect(pos.x, pos.y, width, height)
    pygame.draw.rect(WIN, BLACK, rect3, width = 1, border_top_left_radius=12,border_bottom_left_radius=12, border_top_right_radius=12,border_bottom_right_radius=12)

    #   Plotting Saves 1 - 5 in Left Rectangle
    i = -1 #increment to print slots
    for Save in Saves:
        if Save[0] == 'Save6':
            break
        i = i + 1
        if Save[1] == 'Empty':
            SaveText = '_ _ _'
        else:
            if str(Save[2]) == '-inf':
                ScoreValue = ''
            else:
                ScoreValue = str(Save[2])
            SaveText = Save[1] + ' ' + ScoreValue
        text = BIGFONT.render(SaveText,True, BLACK)
        WIN.blit(text,((rect1.x + 0.15*(rect1.width)),((rect1.y + 0.10*(rect1.height)+(i*0.15*(rect1.height)))))) #(surface, pos.x, pos.y)
    i = 0

    #   Plotting Saves 6 - 10 in Right Rectangle
    i = -1 #increment to print slots
    for Save in Saves:
        if Save[0] == 'Save1' or Save[0] == 'Save2' or Save[0] == 'Save3' or Save[0] == 'Save4' or Save[0] == 'Save5':
            continue
        i = i + 1
        if Save[1] == 'Empty':
            SaveText = '_ _ _'
        else:
            if str(Save[2]) == '-inf':
                ScoreValue = ''
            else:
                ScoreValue = str(Save[2])
            SaveText = Save[1] + ' ' + ScoreValue
        text = BIGFONT.render(SaveText,True, BLACK)
        #WIN.blit(Source,(x,y))
        WIN.blit(text,((rect2.x + 0.15*(rect2.width)),((rect2.y + 0.10*(rect2.height)+(i*0.15*(rect2.height))))))
    i = 0

    #SAVE SELECTOR
    if SaveSelectorMode == True:
        #Arrow blit
        if ArrowCondition == True:
            Arrow = os.path.join(sprites_folder, "arrow_right.png")
            AW = pygame.transform.scale(pygame.image.load(Arrow).convert_alpha(), (50, 35))
            ArrowX = ArrowSlot[3] #this fetches the arrow's X position (from the Arrow Slot) to blit later on
            ArrowY = ArrowSlot[4] #this fetches the arrow's Y position (from the Arrow Slot) to blit later on
            WIN.blit(AW, (ArrowX, ArrowY)) 

        #Pressing Arrow Keys
        if LEFTARROW:
            if ArrowSlot[0] not in range(1, 6): #this checks if the arrow slot is not on the left panel (Is between number 1 and 5)
                if Saves[(ArrowSlot[0]-6)][1] != 'Empty':
                    pass 
                else:
                    #sound
                    ArrowSlot = ArrowSlots[ArrowSlot[0] - 6]
        elif RIGHTARROW:
            if ArrowSlot[0] not in range(6, 11): #this checks if the arrow slot is not on the right panel (Is between number 6 and 10)
                if Saves[(ArrowSlot[0] + 4)][1] != 'Empty':
                    pass
                else:
                    #sound
                    ArrowSlot = ArrowSlots[ArrowSlot[0] + 4]
        elif DOWNARROW:
            if ArrowSlot[0] != 10: #this checks if the arrow is not in the last row
                if Saves[(ArrowSlot[0])][1] != 'Empty':
                    pass
                else:
                    #sound
                    ArrowSlot = ArrowSlots[ArrowSlot[0]]
        elif UPARROW:
            if ArrowSlot[0] != 1: #this checks if the arrow is not in the first row
                if Saves[(ArrowSlot[0]-2)][1] != 'Empty':
                    pass 
                else:
                    #sound
                    ArrowSlot = ArrowSlots[ArrowSlot[0]-2]

        #Pressing ENTER
        if ENTER:
            #Constants
            WritingMode = True
            #travar outros botões (especilamente setas)

            #Animation
            #print a animation (maybe blink the arrow?) to show it was selected

            #Capturing Buttons
        if TYPED_CHAR and WritingMode == True:
                Max_Length = 3
                SavePosition = ArrowSlot[0]-1  
                char = BUTTON_PRESSED
                if char and char.isalnum() and len(PlayerName) < Max_Length:
                    PlayerName += char.upper()
                    Saves[SavePosition][1] = PlayerName #saving PlayerName into 'Saves' Lists

                    with open(SaveFile, 'r', newline='') as read_file:
                        reader = csv.reader(read_file)

                        with open(SaveFile, 'w', newline='') as write_file:
                            writer = csv.writer(write_file)
                            
                            writer.writerow(['Slot','Name','Score'])
                            writer.writerows(Saves)
                                    
                    if len(PlayerName) == 3:
                        Saves[SavePosition][2] = str(Score)
                        with open(SaveFile, 'r', newline='') as read_file:
                            reader = csv.reader(read_file)

                            with open(SaveFile, 'w', newline='') as write_file:
                                writer = csv.writer(write_file)
                            
                                writer.writerow(['Slot','Name','Score'])
                                writer.writerows(Saves)

                        WritingMode = False
                        #colocar alguma coisa aqui para falar quando atinge as 3 palavras

        #Pressing ESC
        if ESCAPE:
            SC_MainMenuButton.enabled = True
            SC_SaveGameButton.enabled = True
            SC_DeleteGameButton.enabled = True
            SC_QuitButton.enabled = True
            SaveSelectorMode = False
            ArrowCondition = False
            ArrowSlot = ArrowSlots[0]

    elif SaveSelectorMode == False:
        pass

    #DELETE MODE
    if SaveDeleteMode == True:
        #Arrow blit
        if ArrowCondition == True:
            Arrow = os.path.join(sprites_folder, "arrow_right.png")
            AW = pygame.transform.scale(pygame.image.load(Arrow).convert_alpha(), (50, 35))
            ArrowX = ArrowSlot[3] #this fetches the arrow's X position (from the Arrow Slot) to blit later on
            ArrowY = ArrowSlot[4] #this fetches the arrow's Y position (from the Arrow Slot) to blit later on
            WIN.blit(AW, (ArrowX, ArrowY)) 

        #Pressing Arrow Keys
        if LEFTARROW:
            if ArrowSlot[0] not in range(1, 6): #this checks if the arrow slot is not on the left panel (Is between number 1 and 5)
                if Saves[(ArrowSlot[0]-6)][1] == 'Empty':
                    pass 
                else:
                    #sound
                    ArrowSlot = ArrowSlots[ArrowSlot[0] - 6]
        elif RIGHTARROW:
            if ArrowSlot[0] not in range(6, 11): #this checks if the arrow slot is not on the right panel (Is between number 6 and 10)
                if Saves[(ArrowSlot[0] + 4)][1] == 'Empty':
                    pass
                else:
                    #sound
                    ArrowSlot = ArrowSlots[ArrowSlot[0] + 4]
        elif DOWNARROW:
            if ArrowSlot[0] != 10: #this checks if the arrow is not in the last row
                if Saves[(ArrowSlot[0])][1] == 'Empty':
                    pass
                else:
                    #sound
                    ArrowSlot = ArrowSlots[ArrowSlot[0]]
        elif UPARROW:
            if ArrowSlot[0] != 1: #this checks if the arrow is not in the first row
                if Saves[(ArrowSlot[0]-2)][1] == 'Empty':
                    pass 
                else:
                    #sound
                    ArrowSlot = ArrowSlots[ArrowSlot[0]-2]

        #Pressing ENTER
        if ENTER:
            DeleteConfirmationBoxEnabled = True
            DeleteYesButton.enabled = True
            DeleteNoButton.enabled = True
            #.
            CurrentSave = Saves[ArrowSlot[0]-1]
            CurrentSlot = Saves[ArrowSlot[0]-1][0] #SlotPosition
            CurrentName = Saves[ArrowSlot[0]-1][1] #Name
            CurrentScore = Saves[ArrowSlot[0]-1][2] #Score
                
        #Pressing ESC
        if ESCAPE:
            SC_MainMenuButton.enabled = True
            SC_SaveGameButton.enabled = True
            SC_DeleteGameButton.enabled = True
            SC_QuitButton.enabled = True
            SaveDeleteMode = False
            ArrowCondition = False
            ArrowSlot = ArrowSlots[0]

    if DeleteConfirmationBoxEnabled == True:
        DeleteConfirmationText = "Delete Save File?" 
        #.
        DeleteConfirmationBox = pygame.Rect(0.50*WIDTH-DeleteConfirmationBox_Width/2,0.50*HEIGHT-DeleteConfirmationBox_Height/2,DeleteConfirmationBox_Width, DeleteConfirmationBox_Height) #pygame.rect(pos.x, pos.y, width, height)
        pygame.draw.rect(WIN,ORANGE,DeleteConfirmationBox,border_top_left_radius=12,border_bottom_left_radius=12, border_top_right_radius=12,border_bottom_right_radius=12) #pygame.draw.rect(surface, color, figure, bordertopleft [optional], borderbottomleft [optional])
        pygame.draw.rect(WIN,BLACK, DeleteConfirmationBox, 1, border_top_left_radius=12,border_bottom_left_radius=12, border_top_right_radius=12,border_bottom_right_radius=12)
        #.
        padding_y = padding_x = 10
        y_offset = padding_y
        text_surface = SMALLFONT.render(DeleteConfirmationText, True, BLACK)
        text_rect = text_surface.get_rect(topleft=(DeleteConfirmationBox.x + padding_x, DeleteConfirmationBox.y + padding_y))
        WIN.blit(text_surface,text_rect)

        #   Delete Confirmation - Button Yes
        button_text = SMALLFONT.render(DeleteYesButton.text, True, BLACK)
        text_rect = button_text.get_rect(center=(DeleteYesButton.x_pos + DeleteYesButton.length//2, DeleteYesButton.y_pos + DeleteYesButton.height//2))
        button_rect = pygame.rect.Rect((DeleteYesButton.x_pos,DeleteYesButton.y_pos),(DeleteYesButton.length,DeleteYesButton.height))

        if DeleteYesButton.enabled == True:
            bcolor = DeleteYesButton.color
        elif DeleteYesButton.enabled == False:
                bcolor = GRAY
            
        if button_rect.collidepoint(mouse_pos) and DeleteYesButton.enabled == True:
            if LeftClick:
                bcolor = DARK_ORANGE
                #.
                Saves[ArrowSlot[0]-1][1] = "Empty" #this is writing "Empty" instead of the original name
                Saves[ArrowSlot[0]-1][2] = float("-inf") #this is writing "-inf" instead of the score

                #writing back
                with open(SaveFile, 'w', newline='') as file:
                    writer= csv.writer(file)
                    writer.writerow(["Slot","Name","Score"])

                    for row in Saves:
                        if row[2] == float('-inf'):
                            savescore = 'inf'
                        else:
                            savescore = str(row[2])
                        writer.writerow([row[0],row[1],savescore])
                #.
                DeleteConfirmationBoxEnabled = False
                DeleteYesButton.enabled = False
                DeleteNoButton.enabled = False
                SaveDeleteMode = True
                ArrowCondition = True 
            else:
                bcolor = LIGHT_ORANGE
                
        pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
        pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
        WIN.blit(button_text, text_rect) 

        #   Delete Confirmation - Button No
        button_text = SMALLFONT.render(DeleteNoButton.text, True, BLACK)
        text_rect = button_text.get_rect(center=(DeleteNoButton.x_pos + DeleteNoButton.length//2, DeleteNoButton.y_pos + DeleteNoButton.height//2))
        button_rect = pygame.rect.Rect((DeleteNoButton.x_pos,DeleteNoButton.y_pos),(DeleteNoButton.length,DeleteNoButton.height))

        if DeleteNoButton.enabled == True:
            bcolor = DeleteNoButton.color
        elif DeleteNoButton.enabled == False:
                bcolor = GRAY
            
        if button_rect.collidepoint(mouse_pos) and DeleteNoButton.enabled == True:
            if LeftClick:
                bcolor = DARK_ORANGE
                #.
                DeleteConfirmationBoxEnabled = False
                DeleteYesButton = False
                DeleteNoButton = False
                #.
                SaveDeleteMode = True
                ArrowCondition = True
            else:
                bcolor = LIGHT_ORANGE
                
        pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
        pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
        WIN.blit(button_text, text_rect) 

    #UPDATE
    pygame.display.update()
    return game_state

#---------------------------------------------------------------------------------------------------------------------------

#CREDITS SCREEN
def draw_credits(mouse_pos, LeftClick):
    global game_state, BGImage, Image_Folders, drawlink

    #BACKGROUND
    #BGImage is being set in the beginning of the program
    BG = pygame.transform.scale(pygame.image.load(BGImage).convert(), (WIDTH, HEIGHT))
    WIN.blit(BG, (0, 0)) 

    #MESSAGE
    padding_y = 10
    padding_x = 5
    lines_spacing = 5

    CRColor = ORANGE
    CRTextColor= BLACK
    CRText = ['CREDITS',
        '',
        'Hi! This is the creator. Thanks for playing the game!',
        'Everything here is open-source, as it is a Pygame, and made by me, using just Python. With some exceptions – cited in the files – all images and sound were also self-made (everything that wasn’t made by me is copyright free).',
        'Most of the art used some sort of AI as I’m no artist myself and can’t make awesome art, as some of you surely do.',
        'You are free to use the game, tweak it or distribute it, but always cite the source (me!). ',
        '',
        'If you want to contact me, have any questions or feedback, you can find me on the socials below.',
        'Have a great game!',
        '',
        'Bruno Syllos'
        ]
 
    OrangeBoxSet = pygame.Rect(50, 100, WIDTH-100, HEIGHT-150) #this is 100 from the top, 50 from below
    pygame.draw.rect(WIN,CRColor,OrangeBoxSet,border_top_left_radius=12,border_bottom_left_radius=12, border_top_right_radius=12,border_bottom_right_radius=12) #pygame.draw.rect(surface, color, figure, bordertopleft [optional], borderbottomleft [optional])
    pygame.draw.rect(WIN,BLACK, OrangeBoxSet, 1, border_top_left_radius=12,border_bottom_left_radius=12, border_top_right_radius=12,border_bottom_right_radius=12)
    y_offset = OrangeBoxSet.y + padding_y
    max_text_width = OrangeBoxSet.width - (padding_x * 2)

    def draw_wrapped_text(surface, text, font, color, x, y, max_width):
        words = text.split(' ')
        line = ''
        lines = []
        for word in words:
            test_line = line + word + ' '
            if font.size(test_line)[0] <= max_width:
                line = test_line
            else:
                lines.append(line)
                line = word + ' '
        lines.append(line)
        return lines

    for line in CRText:
        if line == '':
            y_offset += SMALLFONT.get_height() + lines_spacing
            continue
        wrapped_lines = draw_wrapped_text(WIN, line, SMALLFONT, CRTextColor, 
                                        OrangeBoxSet.x + padding_x, y_offset, max_text_width)
        for wrapped_line in wrapped_lines:
            text_surface = SMALLFONT.render(wrapped_line, True, CRTextColor)
            WIN.blit(text_surface, (OrangeBoxSet.x + padding_x, y_offset))
            y_offset += text_surface.get_height() + lines_spacing

    #IMAGES
    ChihuahuaWidth = 240
    ChihuahuaHeight = 160
    #.
    ExtraTitleW = 400
    ExtraTitleH = 200

    Image1 = os.path.join(image_folder, "Chihuahua.png") 
    IMG1 = pygame.transform.scale(pygame.image.load(Image1), (ChihuahuaWidth, ChihuahuaHeight))
    WIN.blit(IMG1, ((WIDTH - 100 - ExtraTitleW + ExtraTitleW/2 - ChihuahuaWidth/2 + 25), (HEIGHT - 50 - ChihuahuaHeight)))

    ExtraTitle = os.path.join(image_folder, "Thanks_for_Playing.png")
    ET = pygame.transform.scale(pygame.image.load(ExtraTitle), (ExtraTitleW, ExtraTitleH))
    WIN.blit(ET, ((WIDTH - 100 - ExtraTitleW), (HEIGHT - ChihuahuaHeight - 20 - ExtraTitleH)))

    ContactsWidth = 125
    ContactsHeight = 150
    Image2 = os.path.join(image_folder, "Contacts_Icon.png") 
    IMG2 = pygame.transform.scale(pygame.image.load(Image2), (ContactsWidth, ContactsHeight))
    WIN.blit(IMG2, ((50 + 15), (HEIGHT-50-ContactsHeight-15)))
    IMG2REC = IMG2.get_rect(topleft=((ContactsWidth), (ContactsHeight)))

    if LeftClick and IMG2REC.collidepoint(mouse_pos):
        pass #if in the future I add something that clicks on the personal info, I'll change this part

    #TEXT
    Text1 = "GitHub:"
    Text2 = "Email = bruno.syllos@gmail.com"
    Text3 = "LinkedIn = www.linkedin.com/in/bruno-syllos"
    TxtColor = BLACK

    text_surface1 = SMALLFONT.render(Text1, True, TxtColor)
    WIN.blit(text_surface1, (50+15+ContactsWidth+15,HEIGHT-50-ContactsHeight-15 + 10))
    text_surface2 = SMALLFONT.render(Text2, True, TxtColor)
    WIN.blit(text_surface2, (50+15+ContactsWidth+15,HEIGHT-50-ContactsHeight-15 + 10 + 50))
    text_surface3 = SMALLFONT.render(Text3, True, TxtColor)
    WIN.blit(text_surface3, (50+15+ContactsWidth+15,HEIGHT-50-ContactsHeight-15 + 10 + 100))

    #BUTTONS
    EscapeButton = Button("Go Back",50,50,True,20,CW,ORANGE)

    button_text = SMALLFONT.render(EscapeButton.text, True, BLACK)
    text_rect = button_text.get_rect(center=(EscapeButton.x_pos + EscapeButton.length//2, EscapeButton.y_pos + EscapeButton.height//2))
    button_rect = pygame.rect.Rect((EscapeButton.x_pos,EscapeButton.y_pos),(EscapeButton.length,EscapeButton.height))
    bcolor = EscapeButton.color
    if button_rect.collidepoint(mouse_pos):
        if LeftClick:
            bcolor = DARK_ORANGE
            game_state = "Main_Menu"            
        else:
            bcolor = LIGHT_ORANGE
    pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
    pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
    WIN.blit(button_text, text_rect)

    #UPDATE
    pygame.display.update()
    return game_state

#---------------------------------------------------------------------------------------------------------------------------

#GAME OVER SCREEN
def draw_gameover(mouse_pos, LeftClick):
    global game_state, BGImage, PlayGameTexts_Enabled

    #BACKGROUND
    #BGImage is being set in the beginning of the program
    BG = pygame.transform.scale(pygame.image.load(BGImage).convert(), (WIDTH, HEIGHT))
    WIN.blit(BG, (0, 0)) 

    #MESSAGE
    MessageColor = BLACK
    MessageText = BIGFONT.render("GAME OVER", True, MessageColor)
    WIN.blit(MessageText, ((WIDTH/2)-150, (HEIGHT/2)-50))   

    #BUTTONS
    MenuButton = Button("Main Menu",(WIDTH/2)-(CW/2),(HEIGHT/2)+40,True,20,CW,ORANGE)

    button_text = SMALLFONT.render(MenuButton.text, True, BLACK)
    text_rect = button_text.get_rect(center=(MenuButton.x_pos + MenuButton.length//2, MenuButton.y_pos + MenuButton.height//2))
    button_rect = pygame.rect.Rect((MenuButton.x_pos,MenuButton.y_pos),(MenuButton.length,MenuButton.height))
    bcolor = MenuButton.color
    if button_rect.collidepoint(mouse_pos):
        if LeftClick:
            bcolor = DARK_ORANGE
            game_state = "Main_Menu"
            PlayGameTexts_Enabled = False           
        else:
            bcolor = LIGHT_ORANGE
    
    pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
    pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
    WIN.blit(button_text, text_rect)

    SaveScoreboardButton = Button("Save Scoreboard",(WIDTH/2)-(CW/2),(HEIGHT/2)+70,True,20,CW,ORANGE)

    button_text = SMALLFONT.render(SaveScoreboardButton.text, True, BLACK)
    text_rect = button_text.get_rect(center=(SaveScoreboardButton.x_pos + SaveScoreboardButton.length//2, SaveScoreboardButton.y_pos + SaveScoreboardButton.height//2))
    button_rect = pygame.rect.Rect((SaveScoreboardButton.x_pos,SaveScoreboardButton.y_pos),(SaveScoreboardButton.length,SaveScoreboardButton.height))
    bcolor = SaveScoreboardButton.color
    if button_rect.collidepoint(mouse_pos):
        if LeftClick:
            bcolor = DARK_ORANGE
            game_state = "Scoreboard" 
            PlayGameTexts_Enabled = False          
        else:
            bcolor = LIGHT_ORANGE
    
    pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
    pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
    WIN.blit(button_text, text_rect)


    QuitButton = Button("Quit",(WIDTH/2)-(CW/2),(HEIGHT/2)+100,True,20,CW,ORANGE)

    button_text = SMALLFONT.render(QuitButton.text, True, BLACK)
    text_rect = button_text.get_rect(center=(QuitButton.x_pos + QuitButton.length//2, QuitButton.y_pos + QuitButton.height//2))
    button_rect = pygame.rect.Rect((QuitButton.x_pos,QuitButton.y_pos),(QuitButton.length,QuitButton.height))
    bcolor = QuitButton.color
    if button_rect.collidepoint(mouse_pos):
        if LeftClick:
            bcolor = DARK_ORANGE
            quit()        
        else:
            bcolor = LIGHT_ORANGE
    
    pygame.draw.rect(WIN, bcolor, button_rect, 0, border_radius=12)
    pygame.draw.rect(WIN, BLACK, button_rect, 1, border_radius=12)
    WIN.blit(button_text, text_rect)

    #UPDATE
    pygame.display.update()
    return game_state

#---------------------------------------------------------------------------------------------------------------------------

#MAIN LOOP
def game():
    global elapsed_time, start_time, game_state, UPARROW, DOWNARROW, RIGHTARROW, LEFTARROW, ESCAPE, ENTER, TYPED_CHAR, BUTTON_PRESSED, B_PRESSED
    running = True
    
    #CLOCK
    clock = pygame.time.Clock() #This is to control the frame rate of the game
    start_time = time.time()
    elapsed_time = 0

    #ACTIVE LOOP
    '''
    mouse_pos = (0,0)
    LeftClick = False
    RightClick = False
    '''

    while running:
        clock.tick(60) #Sets the framerate to 60 FPS
        elapsed_time = time.time() - start_time

        #Resets buttons
        LeftClick = RightClick = False
        UPARROW = DOWNARROW = RIGHTARROW = LEFTARROW = ESCAPE = ENTER = TYPED_CHAR = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #this is checking if we press "X" in window
                running = False
                break
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    LeftClick = event.button #Left click
                if event.button == 3:
                    RightClick = event.button #Right click

            if event.type == pygame.KEYDOWN:
                if event.key == K_UP:
                    UPARROW = event.key #Up Arrow Button
                elif event.key == K_DOWN:
                    DOWNARROW = event.key #Down Arrow Button
                elif event.key == K_RIGHT:
                    RIGHTARROW = event.key #Right Arrow Button
                elif event.key == K_LEFT:
                    LEFTARROW = event.key #Left Arrow Button
                elif event.key == K_ESCAPE:
                    ESCAPE = event.key #ESC Button
                elif event.key == K_RETURN:
                    ENTER = event.key #Enter Button
                else:
                    TYPED_CHAR = event.unicode
                    if TYPED_CHAR.isalnum():
                        B_PRESSED = True
                        BUTTON_PRESSED = TYPED_CHAR.upper()
                    else:
                        B_PRESSED = False
                        BUTTON_PRESSED = None

        #TRACKS THE MOUSE   
        mouse_pos = pygame.mouse.get_pos()

        #DRAW FUNCTION
        if game_state == "Main_Menu":
            draw_menu(mouse_pos, LeftClick)
        elif game_state == "Settings":
            draw_settings(mouse_pos, LeftClick)
        elif game_state == "Tutorial":
            draw_tutorial(mouse_pos, LeftClick)
        elif game_state == "Scoreboard":
            draw_scoreboard(mouse_pos, LeftClick)
        elif game_state == "Settings Scoreboard":
            draw_STscoreboard(mouse_pos, LeftClick)
        elif game_state =="Credits":
            draw_credits(mouse_pos, LeftClick)
        elif game_state == "Play":
            draw_play(None,elapsed_time,mouse_pos,LeftClick,RightClick) 
        elif game_state == "Game_Over":
            draw_gameover(mouse_pos, LeftClick)

    pygame.quit()

game()

