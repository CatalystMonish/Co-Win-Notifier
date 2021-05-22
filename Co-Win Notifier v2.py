#------------------------------------------
#Co-Win Notifier v2
#
#Original Co-Win Notifier can be found here: https://github.com/CatalystMonish/Co-Win-Notifier by Monish Meher

#Modified by Ashwin V [github.com/ashvnv] 21 May 2021
#https://github.com/ashvnv/Co-Win-Notifier
#Changelog:
#            Added Telegram alert
#                     Does auth process between user and bot and bot and user
#                     chatid is saved in the telcofig.txt file so that after rebooting the program, configuring the telegram is not required
#                    telcongif.txt saved in current program directory 
#            Vaccine search filer:
#                     Search based on Age filer [18+ and 45+]
#                     Search slots based on first or second dose
#                     Search for paid or free vaccine slots
#            tkinter main frame is made inside mainf(), this was necessary because easygui could not render images so tkinter root is destroyed while easygui is called during configuring telegram alert
#
#            pin wise and district wise slots find functions were updated, some redundant codes were removed
#
#            some variables had to be declared global as tkinter is declared inside the mainf() and scope in python won't modifiy the global value of the variable
#
#            Added update feature. When the app is launched, it checks for update from github repository. If update is available, a prompt is shown for updating the app to the latest version         
#
#Data files:
#----------image------------
#these files are stored in data folder
#data/qr-code.png
#data/bot.png
#data/github.png
#data/happybot.png
#data/icon.ico
#data/instagram.png
#data/qr-code.png
#data/sadbot.png
#data/splash.png
#data/update.png
#data/nonet.png

#----------doc------------
#stored in website folder
#website/slot.html
#

#------------App version-----------------
current_ver = 2
#----------------------------------------

from tkinter import *
import os
import webbrowser
import datetime
from datetime import timedelta
import time
from threading import Timer
import requests
from urllib.request import urlopen, Request
import json
from threading import Thread

import sys #add

#-------------------
import platform
import getpass
#------------------

#-------------easygui--------------
from easygui import *
import sys

#-----------telegram---------------
import urllib.request

#used while checking updates
import re



def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def raise_issue():
    webbrowser.open('https://github.com/ashvnv/miscellaneous')


### --------------------Check internet-------------------------
def check_conn():
    PING_URL = 'http://google.com'
    try:
        urllib.request.urlopen(PING_URL)
        return 0
    except:
        return 1

while(check_conn() == 1):
    easytitle = "No Internet"
    easymsg = "You are not connected to the Internet!"
    easybutton_list = ['Try again', 'Raise an issue', 'Exit']

    easyclk = buttonbox(easymsg, easytitle, image = resource_path("data/nonet.png"), choices = easybutton_list)

    if easyclk == 'Raise an issue':
        raise_issue()
        sys.exit("No internet, exit")

    elif easyclk == 'Exit':
        sys.exit("No internet, exit")

   


####################################### Update check ######################################
update_chk = requests.get('https://raw.githubusercontent.com/ashvnv/miscellaneous/main/updates/cowinnotifier.txt').content

update_ver=re.findall(r'\d+', str(update_chk))[0]
print ('Version found: ' + update_ver)

if (current_ver < int(update_ver)): #update found
    #-----------------Update available frame-------------------------------
    
    easytitle = "Update available"
    easymsg = "An update is available for the app!\n\nDownload the latest version before continuing!\n\n\
Current version: 2\nNew version available: " + update_ver

    #image acts as a button in easygui. clicking on the image gives invalid value, so loop makes sure image button not clicked
    easybutton_list = ['Update','Raise an issue', 'Exit']
    easyclknull = True
    while(easyclknull):
        easyclk = buttonbox(easymsg, easytitle, image = resource_path("data/update.png"), choices = easybutton_list)
        if easyclk in easybutton_list:
            easyclknull = False #found button

    if easyclk == 'Raise an issue':
        raise_issue()

    elif easyclk == 'Update':
         webbrowser.open('https:bit.ly/CoWinNotifier')

    sys.exit("Update available")



#-----------------Telegram configure------------------------------------------------------------------------------
global telegram_alert
telegram_alert = False

global telchatid
#---------------------------
#url not disclosed due to privacy concerns
telurl = 'https://api.telegram.org/' + 'bot'  ### Token removed

#func returns true is send successful

def send_telegram_message(msg):
#    """Sends message via Telegram"""
    global telchatid

    data = {
        "chat_id": telchatid,
        "text": msg + '\n\nCo-WIN site\nhttps://selfregistration.cowin.gov.in/\n-----------------------------------\n\
This message was sent from Co-Win Notifier software running on ' + platform.system() + ' ' + platform.release() + '\nUsername: ' + getpass.getuser() + '\n\n\
Bot will never send messages automatically. If you received this message without running the Co-Win Notifier immediatety block the bot' 
    }
    try:
        response = requests.request(
            "POST",
            telurl + '/sendMessage',
            params=data
        )
        
        print("This is the Telegram response")
        print(response.text)
        telegram_data = json.loads(response.text)
        return True
    
    except Exception as e:
        print("An error occurred in sending the alert message via Telegram")
        print(e)
        return False

#---------------------------find auth code------------------------------------


#updates telchatid variable if authcode text found

def tel_find_chat_id(authcode):
    tel_temp = urllib.request.urlopen(telurl + '/getUpdates')
    tel_string = tel_temp.read().decode('utf-8')
    tel_json_obj = json.loads(tel_string)
    print(tel_json_obj)

    for temp_tel in tel_json_obj['result']:
        if temp_tel['message']['text'] == authcode:
            print('found, chat id: ' + str(temp_tel['message']['chat']['id']))
            global telchatid
            telchatid = str(temp_tel['message']['chat']['id'])
            print(str(tel_config_file(telchatid)) + ': chat id written to telconfig.txt')
            return True

#------------------------send auth code---------------------------------------
        #if auth code received! auth successful
    
def auth_code_gen():
    #return 6 digit random int
    return str(time.time_ns())[11:]
    
#---------------------------------------------------------------------------------



#----------------------------telegram configure read------------------------
#configuration saved as a txt file with chat id.

def tel_config_file(wrt):
    # if wrt = 0: file read mode
    if wrt == 0:
        if os.path.exists('telconfig.txt'):
            tel_readconfig = open('telconfig.txt',"r+")
            temp = tel_readconfig.readline()
            if temp.isdigit():
                global telchatid
                telchatid = temp # update the id
                tel_readconfig.close()
                return True
            else:
                return False
            
            
        else:
            return False
    else:
        telconfigw = open('telconfig.txt', 'w')
        telconfigw.write(wrt)
        telconfigw.close()
        return True

#----------------------------------easygui--------------------------------------------------------------------------------------------
#using easygui for configuring telegram alert
easytitle = "Co-Win Notifier v2 Telegram alert"

def tel_easygui1():
    #-----------------easygui first frame-------------------------------

    easymsg = "Welcome! The bot will send you alerts when slots are found along with the slots info and link to registration site\n\nOpen the chatbot in Telegram:\
\n\n*Search for the bot in Telegram search bar using the username\n@co_win_notifier_bot\n\nor\n\n*Open this link:\nt.me/co_win_notifier_bot \n\nor \n\n\
*Scan the below QR code from your phone"

#image acts as a button in easygui. clicking on the image gives invalid value, so loop makes sure image button not clicked
    easybutton_list = ['Next','Raise an issue', 'Cancel']
    easyclknull = True
    while(easyclknull):
        easyclk = buttonbox(easymsg, easytitle, image = resource_path("data/qr-code.png"), choices = easybutton_list)
        if easyclk in easybutton_list:
            easyclknull = False #found button
    return easyclk



def tel_easygui2(auth_code):
    #-----------------easygui second frame------------------------------ user to bot auth
    #get unique number from telegram func and display

    easymsg = "Now lets authenticate! Send this unique number to the bot: \n\n" + auth_code + "\n\n\
Once you click on 'Next', the window may not be visible for some seconds. The program is trying to search your message from the server and may take some time to load!!!!\n\n\
Meantime you can check your telegram to see if the bot has sent you received message"

    easybutton_list = ['Next','Raise an issue', 'Cancel']
    easyclknull = True
    while(easyclknull):
        easyclk = buttonbox(easymsg, easytitle, image = resource_path("data/bot.png"), choices = easybutton_list)
        if easyclk in easybutton_list:
            easyclknull = False #found button
    return easyclk

        
    #--------------------could not auth------------------------------------
def tel_easygui3(auth_code):
    
    easymsg = "Heyyy I did not get your message! Sure you sent the correct code?\n\n" + auth_code

    easybutton_list = ['Try again','Raise an issue', 'Cancel']
    easyclknull = True
    while(easyclknull):
        easyclk = buttonbox(easymsg, easytitle, image = resource_path("data/sadbot.png"), choices = easybutton_list)
        if easyclk in easybutton_list:
            easyclknull = False #found button
    return easyclk


    
def tel_easygui4():
    #-----------------easygui second frame------------------------------ bot to user auth
    easymsg = "Woohoo! I got your code! Let me make sure it was you only.\n\nI have sent another code to you. Enter that in the box\n\nIf code not received, keep the box blank and click OK"

    easytxt = enterbox(easymsg, easytitle)
    return easytxt

        
    #---------------cound not auth-----------------------------------------------------------
def tel_easygui5():
    easymsg = "Hey thats not what I sent! Try again\n\nGo back if you did not receive the code"

    easybutton_list = ['Try again','Go back','Raise an issue', 'Cancel']
    easyclknull = True
    while(easyclknull):
        easyclk = buttonbox(easymsg, easytitle, image = resource_path("data/sadbot.png"), choices = easybutton_list)
        if easyclk in easybutton_list:
            easyclknull = False #found button
    return easyclk


#---------------------final confirm----------------------------------
def tel_easygui6():
    easytitle = "Co-Win-Notifier Telegram alert"
    easymsg = "Amazing! You have been authenticated. I will send you alerts as soon as slots are available!\n\nYou can send a message to me from the textbox below and I will forward the same message \
to you on Telegram. Write anything your want or you can exit the telegram configure"

    easybutton_list = ['Exit','Send message','Raise an issue']
    easyclknull = True
    while(easyclknull):
        easyclk = buttonbox(easymsg, easytitle, image = resource_path("data/happybot.png"), choices = easybutton_list)
        if easyclk in easybutton_list:
            easyclknull = False #found button
    return easyclk
    

#simple msg send from user
def tel_easygui7():
    easymsg = "Try sending a message. If you are not receiving the message, try configuring the the telegram alert again from the start"
    easytxt = textbox(easymsg, easytitle, 'Type here')
    return easytxt
    


#--------------------main easygui func----------------------------------------------------------

def tel_easygui_configure():
    root.destroy() #tkinter throws exception when easygui renders images
    
    tel_para = tel_easygui1() #call first frame
    if (tel_para == 'Cancel'):
        mainf(0) #recreate main frame
        return
    elif (tel_para == 'Raise an issue'):
        raise_issue()
        mainf(0) #recreate main frame
        return 
#---------------------------------------------------------------------
    #auth between bot and user
    
    tel_guiloop2 = True
    
    while(tel_guiloop2):
        auth_code = auth_code_gen()
        tel_guiloop = True
        while(tel_guiloop):
            tel_para = tel_easygui2(auth_code) #user to bot auth
            if (tel_para == 'Cancel'):
                tel_config_file('NA') #clear found chat id
                mainf(0) #recreate main frame
                return
            elif (tel_para == 'Raise an issue'):
                raise_issue()
                tel_config_file('NA') #clear found chat id
                mainf(0) #recreate main frame
                return 
            elif tel_find_chat_id(auth_code): #if func returned True authcode verified
                tel_guiloop = False #Authcode verified
            else:
                tel_para = tel_easygui3(auth_code)
                if (tel_para == 'Cancel'):
                    tel_config_file('NA') #clear found chat id
                    mainf(0) #recreate main frame
                    return
                elif (tel_para == 'Raise an issue'):
                    raise_issue()
                    tel_config_file('NA') #clear found chat id
                    mainf(0) #recreate main frame
                    return 
            


        auth_code = auth_code_gen()
        tel_guiloop = True
        while(tel_guiloop):
            send_telegram_message('Auth code: ' + auth_code + '\nEnter this code in the Co-Win Notifier software') #send the code to user
            tel_para = tel_easygui4() #bot to user auth
            if tel_para == auth_code:
                tel_guiloop = False #auth complete
                tel_guiloop2 = False #break auth loop and go to next section

            else:
                tel_para = tel_easygui5()
                if tel_para == 'Go back':
                    tel_guiloop = False #repeat user to bot auth
                
                elif tel_para == 'Cancel':
                    tel_config_file('NA') #clear found chat id
                    mainf(0) #recreate main frame
                    return
                elif (tel_para == 'Raise an issue'):
                    raise_issue()
                    tel_config_file('NA') #clear found chat id
                    mainf(0) #recreate main frame
                    return
#---------------------------------------------------------------------------

    tel_guiloop = True
    while(tel_guiloop):
        tel_para = tel_easygui6() #final frame
        if (tel_para == 'Raise an issue'):
            raise_issue()
            tel_config_file('NA') #clear found chat id
            mainf(0) #recreate main frame
            return
        elif (tel_para == 'Send message'):
            tel_para = tel_easygui7()
            if tel_para == None:
                print('None')
            else:
                send_telegram_message(tel_para)
                
        else:
            tel_guiloop = False

    global telegram_alert
    #telegram_alert = True # turn on the telegram alerts | set in mainf()
    mainf(0) #recreate main frame

#---------------------------------------------------------------------------------



global data_dir
data_dir = resource_path("data")


global website_dir
website_dir = resource_path("website")


def open_link_github():
  webbrowser.open('www.github.com/CatalystMonish')
def open_link_instagram():
  webbrowser.open('www.instagram.com/meher._.catalyst')
def splashWin():
  canvas.destroy()

def checkModePin():
    mainf(2)
    seletedModePin()

def checkModeDistrict():
    mainf(2)
    seletedModeDistrict()



def firstPin():

  #welcome text
  welcomeText = Label(root, text ="Welcome to Co-win Notifier", fg="black", bg='#dbdbdb', font="Ubuntu 20 bold")
  welcomeText.place(x=200, y=30, anchor="center")

  choiceText = Label(root, text="Select Checking Mode",fg="black", font="Ubuntu 18")
  choiceText.place(x=200, y=180, anchor="center")

  buttonPin = Button(root, text="By PinCode", font="Ubuntu 10", command=checkModePin)
  buttonPin.place(x=150, y=220, anchor="center")

  buttonDistrict = Button(root, text="By District", font="Ubuntu 10", command=checkModeDistrict)
  buttonDistrict.place(x=250, y=220, anchor="center") 



#--------------------------------------------------------------------------------------------------------------
#---------------------------------------------------Main Frame--------------------------------------------------

# data_dir = os.path.join(os.path.dirname(__file__), "data")
# website_dir = os.path.join(os.path.dirname(__file__), "website")

print("This is an Console Window, errors if any will be printed here!")

global root


def mainf(func):
    global welcomeText2,welcomeText,choiceText,buttonDistrict,buttonPin,internetText,tel_choiceText,tel_buttonPin,doseR1,doseR2, ageR1, ageR2, payR1, payR2
    global enteredPin, date, variable, variableDis,indexDistrict, selectedStateId, statesArray, idArray, districtArray, districtIdAray, dateRadio, availableDosesArray
    
    if (func == 2): #destroy
        welcomeText2.destroy()
        welcomeText.destroy()
        choiceText.destroy()
        buttonDistrict.destroy()
        buttonPin.destroy()
        internetText.destroy()

        tel_choiceText.destroy()
        tel_buttonPin.destroy()
        doseR1.destroy()
        doseR2.destroy()
        ageR1.destroy()
        ageR2.destroy()
        payR1.destroy()
        payR2.destroy()

        return
    
    #Due to garbage collection, declare image variables as global
    
    #0: no canvas
    #1: show canvas
    #2: destroy created objects

    global website_dir
    global website_dir
    global root

    root = Tk()
    root.title("Co-Win Notifier v2")
    root.geometry('400x400')
    root.resizable(width=False, height=False)
    root.iconbitmap(resource_path("data/icon.ico"))    

    enteredPin = StringVar() 
    date = StringVar()
    variable = StringVar()
    variableDis = StringVar()
    indexDistrict = StringVar()
    selectedStateId = StringVar()
    statesArray = []
    idArray = []
    districtArray = []
    districtIdAray = []
    dateRadio = IntVar()
    availableDosesArray = [] 

    
    #welcome text
    welcomeText = Label(root, text ="Welcome to Co-Win Notifier v2", fg="black", bg='#dbdbdb', font="Ubuntu 17")
    welcomeText.place(x=200, y=30, anchor="center")

    welcomeText2 = Label(root, text ="This Utility checks for\nboth dose 1 and dose 2 slots!", fg="red", font="Ubuntu 10")
    welcomeText2.place(x=200, y=80, anchor="center")

    creditText = Label(root, text ="Made by Catalyst", fg="gray", font="Ubuntu 8 bold")
    creditText.place(x=300, y=380, anchor="center")
    global github_btn, instagram_btn #### global
    github_btn= PhotoImage(file=resource_path('data/github.png'))
    buttonGit= Button(root, image=github_btn,command= open_link_github, borderwidth=0)
    buttonGit.place(x=360, y=380, anchor="center")
    instagram_btn= PhotoImage(file=resource_path('data/instagram.png'))
    buttonInsta= Button(root, image=instagram_btn, command=open_link_instagram, borderwidth=0)
    buttonInsta.place(x=380, y=380, anchor="center")

    def opensite():
        webbrowser.open('www.github.com/ashvnv')
    creditText2 = Label(root, text ="Modified by ashvnv", fg="gray", font="Ubuntu 8 bold")  
    creditText2.place(x=60, y=380, anchor="center")
    global github_btn2 ### global
    github_btn2= PhotoImage(file=resource_path('data/github.png'))
    buttonGit2= Button(root, image=github_btn,command=opensite, borderwidth=0)
    buttonGit2.place(x=125, y=380, anchor="center")

#---------------------------------------------------------------------------------
#Telegram alert
    global telegram_alert
    
    if tel_config_file(0): #read the config file and get the id
        telegram_alert = True
    else:
        telegram_alert = False
        
    if telegram_alert == True:
        tel_choiceTextSet = 'Telegram alert already configured'
        tel_choicebtntext = 'configure again'
        tel_xlen = 325
    else:
        tel_choiceTextSet = "Set-up Telegram alert"
        tel_choicebtntext = 'configure'
        tel_xlen = 270
        
    tel_choiceText = Label(root, text=tel_choiceTextSet,fg="black", font="Ubuntu 11")
    tel_choiceText.place(x=150, y=120, anchor="center")

    tel_buttonPin = Button(root, text=tel_choicebtntext, font="Ubuntu 8", command=tel_easygui_configure)
    tel_buttonPin.place(x=tel_xlen, y=120, anchor="center")
#---------------------------------------------------------------------------------

#----------------------dose option----------------------
    global chkdoseop
    chkdoseop = StringVar()

    doseR1 = Radiobutton(root,text='Dose 1',variable=chkdoseop, value='available_capacity_dose1')
    doseR1.place(x=70, y=160, anchor="center")
    doseR1.select()

    doseR2 = Radiobutton(root,text='Dose 2',variable=chkdoseop, value='available_capacity_dose2')
    doseR2.place(x=70, y=180, anchor="center")
#-------------------------------------------------------


#---------------------------age option--------------------
    global chkageop
    chkageop = IntVar()

    ageR1 = Radiobutton(root,text='Age 18+',variable=chkageop, value=18)
    ageR1.place(x=180, y=160, anchor="center")
    ageR1.select()

    ageR2 = Radiobutton(root,text='Age 45+',variable=chkageop, value=45)
    ageR2.place(x=180, y=180, anchor="center")

#-----------------------------------------------------------

    
#---------------------------paid or free--------------------
    global chkpayop
    chkpayop = StringVar()

    payR1 = Radiobutton(root,text='Free',variable=chkpayop, value='Free')
    payR1.place(x=290, y=160, anchor="center")
    payR1.select()

    payR2 = Radiobutton(root,text='Paid',variable=chkpayop, value='Paid')
    payR2.place(x=290, y=180, anchor="center")

#-----------------------------------------------------------



    choiceText = Label(root, text="Select Checking Mode",fg="black", font="Ubuntu 18")
    choiceText.place(x=200, y=220, anchor="center")

    buttonPin = Button(root, text="By PinCode", font="Ubuntu 10", command=checkModePin)
    buttonPin.place(x=145, y=260, anchor="center")

    buttonDistrict = Button(root, text="By District", font="Ubuntu 10", command=checkModeDistrict)
    buttonDistrict.place(x=245, y=260, anchor="center")

    internetText = Label(root, text="Ensure your internet is\nworking before clicking",fg="green", font="Ubuntu 12")
    internetText.place(x=200, y=320, anchor="center")

    
    if (func == 1): #calling for the first time
        global canvas, splashImage
        canvas = Canvas(root, width = 400, height = 400) 
        canvas.place(x=200, y=200, anchor="center") 
        splashImage = PhotoImage(file= resource_path('data/splash.png'))
        canvas.create_image(200,200, anchor="center", image=splashImage) 
        t = Timer(2.0, splashWin)
        t.start()


mainf(1) ## call mainf first time with canvas

def seletedModePin():
  #picode text
  testText = Label(root, text="Enter Pincode",fg="black", font="Ubuntu 18")
  testText.place(x=200, y=40, anchor="center")

  #pincode input
  pinInput = Entry(root, font="Ubuntu 10", width=10, textvariable = enteredPin)
  pinInput.place(x=200, y=80, anchor="center")

    #picode text
  testText = Label(root, text="Select Day \n(Ideally Select Tommorow or Day After)",fg="black", font="Ubuntu 12")
  testText.place(x=200, y=120, anchor="center")
  
  #radio
  dateSelectToday = Radiobutton(root, text="Today", variable=dateRadio, value= 0)
  dateSelectToday.place(x=133, y=170, anchor=E)

  dateSelectTommorow = Radiobutton(root, text="Tommorow", variable=dateRadio, value= 1)
  dateSelectTommorow.place(x=246, y=170, anchor=E)

  dateSelectNext = Radiobutton(root, text="Day After", variable=dateRadio, value= 2)
  dateSelectNext.place(x=350, y=170, anchor=E)

  #start button
  startPinCheck = Button(root,text="START" ,font="Ubuntu 10", command= checkPinBox)
  startPinCheck.place(x=200, y=210, anchor="center")

#---------------------------------------------------------------------------------------------------------------
global counter
counter=0

def checkPinBox():
  if len(str(enteredPin.get())) == 6:
    startCheckingPin()

  else:
    warning = Label(root, text="Enter Valid PinCode",fg="red", font="Ubuntu 10")
    warning.place(x=310, y=80, anchor="center")
    root.after(1000, warning.destroy)
    

def startCheckingPin():
  print("Checking ...")
  now = datetime.datetime.now()
  diff = datetime.timedelta(days=(dateRadio.get()))
  dateSelected = now + diff
  finalDate = dateSelected.strftime('%d-%m-%Y')
  pin = str(enteredPin.get())
  print(f"Selected pin is {pin}")
  finalUrl = (f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={pin}&date={finalDate}")
  print(finalUrl)
  checkLoop(finalUrl)


def checkLoop(finalUrl):
    global counter
    counter+=1
    
    req = Request(finalUrl, headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(req)
    data_json = json.loads(response.read())
    dataRaw = "{'sessions': []}"
    print(f"The data recieved from the server is \n\n {data_json} \n")

    if str(data_json) == dataRaw:
        output = Label(root, text="No Slots Available \n Will Automatically Check Again in 5s ecs... \n\n\n This will launch your browser once\n\
when slot is Available! \n\n\n Do not close this window!!\n\nNumber of retries: " + str(counter),width=200, height=50, fg="white", bg="black",  font="Ubuntu 13") 
        output.place(x=200, y=160, anchor="center")   
        root.after(5000, output.destroy)  
        root.after(5000, startCheckingPin)
    else:
        for center in data_json['sessions']:
            outputText =  str(center[chkdoseop.get()]) # edit here
            print(outputText)
            if int(outputText) > 0:
                if chkageop.get() == int(center['min_age_limit']) and chkpayop.get() == str(center['fee_type']):
                    fnd_info = str(json.dumps(center))
                    temp = fnd_info.translate(str.maketrans(
                        {',': '\n',
                         '"': '',
                         '[': '\n',
                         ']': '',
                         '{': '',
                         '{': ''})) # remove JSON characters
                    print(temp)
                    webbrowser.open(resource_path("website/slot.html"))
                    if telegram_alert == True:
                        send_telegram_message('Slot found!\n\n' + temp)
                    # easy gui slots info
                    msgbox(temp, 'Slot info', 'Ok')
                    counter = 0
                    return
        output = Label(root, text= "No Slots Available \n Will Automatically Check Again in 5 secs... \n\n\n This will launch your browser once\n\
when slot is Available! \n\n\n Do not close this window!!\n\nNumber of retries: " + str(counter),width=200, height=50, fg="white", bg="black",  font="Ubuntu 13")
        output.place(x=200, y=160, anchor="center")
        root.after(5000, output.destroy)
        root.after(5000, startCheckingPin)

#------------------------------------------------------------------------


def seletedModeDistrict():
    global  statesArray, idArray, variable
    #Get State Data from API
    urlStates = 'https://cdn-api.co-vin.in/api/v2/admin/location/states'
    req = Request(urlStates, headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(req)
    data_json = json.loads(response.read())

    for states in data_json['states']:
        statesArray.append(states.get('state_name'))
    for id in data_json['states']:
        idArray.append(id.get('state_id'))

    warnText2 = Label(root, text ="Loading of States and Districts can take a few secs....", fg="red", font="Ubuntu 10")
    warnText2.place(x=200, y=20, anchor="center")

    stateText = Label(root, text="State", fg="black", font="Ubuntu 10")
    stateText.place(x=200, y=45, anchor='center')

    variable.set('Select your state')
    stateDrop = OptionMenu(root, variable, *statesArray, command=districtSelect)
    stateDrop.config(width=38)
    stateDrop.place(x=45, y=70, anchor='w')

  
def districtSelect(self):
    global  statesArray, idArray, variableDis,districtArray,districtIdAray,dateRadio
    districtArray.clear() ## clear list if user selects another state
    districtIdAray.clear()

    districtText = Label(root, text="District", fg="black", font="Ubuntu 10")
    districtText.place(x=200, y=120, anchor='center')

    
    indexDistrict = statesArray.index(variable.get())
    selectedStateId = idArray[indexDistrict]
    urlDistricts = (f"https://cdn-api.co-vin.in/api/v2/admin/location/districts/{selectedStateId}")
    print(urlDistricts)
    req = Request(urlDistricts, headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(req)
    data_json = json.loads(response.read())
    for districts in data_json['districts']:
        districtArray.append(districts.get('district_name'))
    for district_id in data_json['districts']:
        districtIdAray.append(district_id.get('district_id'))  

 
    variableDis.set('Select your district')
    districtDrop = OptionMenu(root, variableDis, *districtArray)
    districtDrop.config(width=38)
    districtDrop.place(x=45, y=150, anchor='w')

    testText = Label(root, text="Select Day \n(Ideally Select Tommorow or Day After)",fg="black", font="Ubuntu 12")
    testText.place(x=200, y=220, anchor="center")

  #radio
    dateSelectToday = Radiobutton(root, text="Today", variable=dateRadio, value= 0)
    dateSelectToday.place(x=133, y=260, anchor=E)

    dateSelectTommorow = Radiobutton(root, text="Tommorow", variable=dateRadio, value= 1)
    dateSelectTommorow.place(x=246, y=260, anchor=E)
 
    dateSelectNext = Radiobutton(root, text="Day After", variable=dateRadio, value= 2)
    dateSelectNext.place(x=350, y=260, anchor=E)

    startDistrictCheck = Button(root, text="START" ,font="Ubuntu 10", command=startCheckingDistrict)
    startDistrictCheck.place(x=200, y=300, anchor="center")


def startCheckingDistrict():
    global finalUrl #changes made here to global variable
    
    print("Checking ...")
    now = datetime.datetime.now()
    diff = datetime.timedelta(days=(dateRadio.get()))
    dateSelected = now + diff
    finalDate = dateSelected.strftime('%d-%m-%Y') #date final
    print('Final date' +str(finalDate))
    districtID = str(variableDis.get())  #district id
    print(f"Selected district is {districtID}")  
    selectedDistrictId = districtArray.index(variableDis.get())
    realDistrictId = districtIdAray[selectedDistrictId]  

    finalUrl = (f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={realDistrictId}&date={finalDate}")
    print(finalUrl)
    checkLoopDis(finalUrl)

def checkLoopDis(finalUrl):
    global counter
    counter+=1
    
    req = Request(finalUrl, headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(req)
    data_json = json.loads(response.read())
    dataRaw = "{'sessions': []}"
    print(f"The data recieved from the server is \n\n {data_json} \n")

    if str(data_json) == dataRaw:
        output = Label(root, text="No Slots Available \n Will Automatically Check Again in 5s ecs... \n\n\n This will launch your browser once\n\
when slot is Available! \n\n\n Do not close this window!!\n\nNumber of retries: " + str(counter),width=200, height=50, fg="white", bg="black",  font="Ubuntu 13") 
        output.place(x=200, y=160, anchor="center")   
        root.after(5000, output.destroy)  
        root.after(5000, startCheckingDistrict)
    else:
        for center in data_json['sessions']:
            outputText =  str(center[chkdoseop.get()]) # edit here
            print(outputText)
            if int(outputText) > 0:
                if chkageop.get() == int(center['min_age_limit']) and chkpayop.get() == str(center['fee_type']):
                    fnd_info = str(json.dumps(center))
                    temp = fnd_info.translate(str.maketrans(
                        {',': '\n',
                         '"': '',
                         '[': '\n',
                         ']': '',
                         '{': '',
                         '{': ''})) # remove JSON characters
                    print(temp)
                    webbrowser.open(resource_path("website/slot.html"))
                    if telegram_alert == True:
                        send_telegram_message('Slot found!\n\n' + temp)
                    # easy gui slots info
                    msgbox(temp, 'Slot info', 'Ok')
                    counter = 0 #reset counter
                    return
        output = Label(root, text= "No Slots Available \n Will Automatically Check Again in 5 secs... \n\n\n This will launch your browser once\n\
when slot is Available! \n\n\n Do not close this window!!\n\nNumber of retries: " + str(counter),width=200, height=50, fg="white", bg="black",  font="Ubuntu 13")
        output.place(x=200, y=160, anchor="center")
        root.after(5000, output.destroy)
        root.after(5000, startCheckingDistrict)

root.mainloop()


