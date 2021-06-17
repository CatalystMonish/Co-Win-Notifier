#------------------------------------------
#Co-Win Notifier v3.1
#
#6 June 2021
#https://github.com/ashvnv/Co-Win-Notifier
#Monish Meher
#Ashwin Vallaban

#Changelog v3.1:
#            Added Azure ttk theme [v1.3] # Copyright (c) 2021 rdbende <rdbende@gmail.com> | https://github.com/rdbende/Azure-ttk-theme
#            Slot retry time reduced to 3.1 Seconds
#            UI improvements
#            Added start window which shows the startup operations performed by the app (checking network[1], checking for updates[2], getting vaccine data[3]). Start window operations are threaded
#            App now reads the vaccine data (vaccine name, API JSON search name) from github repository [https://raw.githubusercontent.com/ashvnv/miscellaneous/main/updates/vaccinedatab.txt]
#            and accordingly enables or disables the vaccine checkbox
#            Added try-except block wherever the program performs networking operation and accordingly gives indication to the user if error occurs


#Changelog v3:
#            [\d.]+ <- Regex updated for getting app latest version | now supports app version number in decimal
#            Radio buttons changed to checkboxes (for free, paid slots options)
#            Added vaccine name filter (Sputnik V, Covishield, Covaxin)
#            Added back button in pinmode, district and slots retry window
#            Changed slot retry time to 3.5 Seconds from 5 seconds (Now making approx. 85 calls are made in 5 minutes [100 calls limit in 5 minutes])
#            Auth code digits reduced to 6 from 8
#            Lot of bug fixes and UI improvements



#Changelog v2:
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

#-------Azure-dark------
#All files added

#------------App version-----------------
current_ver = 3.1
base_ver = int(current_ver) #remove fractional part
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
import sys
import threading

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

#
from tkinter import ttk #For theme


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def raise_issue():
    webbrowser.open('https://github.com/ashvnv/miscellaneous')


#----------------------------------------App init checks---------------------------------------------------------
global INIT_DONE
INIT_DONE = False # when init done completely it is made True


def updateAppLink():
    webbrowser.open('http://bit.ly/cowinnotifierIO')

def quitinit():
    startroot.destroy()
    sys.exit("Terminated init by user")


################################# Update App Vaccine database #############################

def vacData_file(wrt):
    # if wrt = 0: file read mode
    if wrt == 0:
        return open('vacData.txt',"r+").readline()
    else:
        telconfigw = open('vacData.txt', 'w')
        telconfigw.write(str(wrt))
        telconfigw.close()
        return True

global VacData
VacData = [] # Buttons read this list

def VaccDat(): # Update app vaccine database
    print('VaccDat()')

    statmsg['text'] = 'Updating vaccine data...'
    statmsg['fg'] = 'gray'

    #-----------------------------GitHub vac database-------------------------------
    try:
        update_chk = requests.get('https://raw.githubusercontent.com/ashvnv/miscellaneous/main/updates/vaccinedatab.txt').content
        
        print('response:' + str(update_chk))

        dat_temp = re.findall(r'[#][\w -]+[#]', str(update_chk))

        dat_size = len(dat_temp)

        print('Database size: ' + str(dat_size))

        if (dat_size == 27):
            vacData_file(dat_temp) # write to local file
            print('Written to local database')
            for dat in dat_temp:
                VacData.append(re.findall(r'[\w -]+', dat)[0])
            return
    except:
        print('Exception raised')

#-------------------------Local vac database----------------------------------
    print('Error reading the vaccine database.')
    if (os.path.exists('vacData.txt')):
        print('Local database exits.. Reading....')
        #print(vacData_file(0)) #read
        
        dat_temp = re.findall(r'[#][\w -]+[#]', vacData_file(0))

        print('Local database read')

        dat_size = len(dat_temp)

        print('Database size: ' + str(dat_size))

        if (dat_size == 27):
            for dat in dat_temp:
                VacData.append(re.findall(r'[\w -]+', dat)[0])
            return

    print('local database... Error')
    raise Exception("Vaccine database read error")


####################################### Update check ######################################

def AppUpdate():
    print('AppUpdate()')
    
    statmsg['text'] = 'Searching for updates...'
    statmsg['fg'] = 'gray'
    
    update_chk = requests.get('https://raw.githubusercontent.com/ashvnv/miscellaneous/main/updates/cowinnotifier.txt').content
    print('response:' + str(update_chk))
    
    update_ver=re.findall(r'[\d].[\d]', re.findall(r'#[\d].[\d]#', str(update_chk))[0])[0]
    #update_ver=re.findall(r'[\d].[\d]', re.findall(r'#[\d].[\d]#', '5.0 #3.9# 4.0 5.6')[0])[0] #<version num>#
    print('Regex: ' + str(update_ver))
        
    print ('Latest Version: ' + update_ver)

    if (current_ver < float(update_ver)): #update found
    #-----------------Update available frame-------------------------------
        
        print('Update available')

        pb.place_forget()
        statmsg['text'] = 'Update available | Current: v' + str(current_ver)
        statmsg['fg'] = '#87CEEB'

        func_button['text']='Update to v' + update_ver
        func_button['command']=updateAppLink
        func_button.place(x=150,y=30, anchor='center')

        return True
    return False
        
####################################### Check network ###################################
global PING_URL
google_ping = 'http://google.com'
bing_ping = 'http://bing.com' # backup ping addres

def check_conn(link):
    print('check_conn()')
    
    global PING_URL
    PING_URL = link
    print(PING_URL)
    try:
        urllib.request.urlopen(PING_URL)
        return 0
    except:
        print('ping failed')
        if PING_URL == bing_ping:
            return 1
        return check_conn(bing_ping)

def connection():
    print('connection()')
    
    #place progress bar
    pb.place(x=150,y=30, anchor='center')

    #remove func button
    func_button.place_forget()

    statmsg['text'] = 'Checking network...'
    statmsg['fg'] = 'gray'
    
    if check_conn(google_ping) == 1:
        print('No internet')

        statmsg['text'] = 'No internet!'
        statmsg['fg'] = '#F7347A'
    
        pb.place_forget()
        func_button['text']='Try Again'
        func_button['command']=createThreadinit # add button command, create new thread 
        func_button.place(x=150,y=30, anchor='center')
    else:
        print('Ping successful')

        try:
            if (AppUpdate()): #check for app updates
                return
        except:
            print('Update check failed. skipped..')
            
        try:
            VaccDat() # update vaccine database
            
        except:
            print('Exception raised inside VaccDat()')
            statmsg['text'] = 'Error occurred!'
            statmsg['fg'] = '#F7347A'
    
            pb.place_forget()
            func_button['text']='Try Again'
            func_button['command']=createThreadinit # add button command, create new thread 
            func_button.place(x=150,y=30, anchor='center')

            return

        #------Start app-----------
        global INIT_DONE
        INIT_DONE = True # make flag true

        #---------------launch app------------------------
        statmsg['text'] = 'launching app...'
        statmsg['fg'] = 'gray'
            
        startroot.after(1000, startroot.destroy) #init done
    return



##################################### Init window #######################################

global pb, func_button, issue_button, exit_button, statmsg, startroot


def createThreadinit():
    # Create a Thread with a function without any arguments
    th = threading.Thread(target=connection) # check internet connectivity
    # Start the thread  
    th.start()

def disable_event(): # close button removed
    pass

def initWindow():
    global pb, func_button, issue_button, exit_button, statmsg, startroot
    
    startroot = Tk()
    startroot.geometry('300x160')
    startroot.title('Starting Co-Win Notifier')
    startroot.resizable(width=False, height=False)
    startroot.protocol("WM_DELETE_WINDOW", disable_event)


    #---------------------Theme------------------------------
    ### Here are the three lines by which we set the theme ###
    # Create a style
    global style
    style = ttk.Style(startroot)
    # Import the tcl file
    startroot.tk.call('source', 'azure-dark.tcl')
    # Set the theme with the theme_use method
    style.theme_use('azure-dark')
    #---------------------------------------------------------
    
    # progress bar
    pb = ttk.Progressbar(
        startroot,
        orient='horizontal',
        mode='indeterminate',
        length=280
        )
    #progress bar placed inside connection()
    pb.start([5])


    # func button displayed in place of progress bar
    func_button = ttk.Button(
        startroot,
        text='NA',
        style='AccentButton',
        )


    # raise an issue button ##add command
    issue_button = ttk.Button(
        startroot,
        text='Raise an issue',
        command=raise_issue
        )
    issue_button.place(x=80, y=85, anchor='center')


    # exit button
    exit_button = ttk.Button(
        startroot,
        text='Quit',
        command=quitinit
        )
    exit_button.place(x=220, y=85, anchor='center')


    # stat message
    statmsg = Label(startroot, text = "Initializing...", fg="gray")
    statmsg.place(x=150, y=135, anchor="center")

    createThreadinit()
    
    startroot.mainloop()

initWindow()

#-------------------------------------------------
# check if init process completed successfully
if (INIT_DONE == False):
    sys.exit("Init failed")

print('Init done')

################################ Init done ####################################




#-----------------Telegram configure------------------------------------------------------------------------------
global telegram_alert
telegram_alert = False

global telchatid
#---------------------------
#url not disclosed due to privacy concerns
telurl = 'https://api.telegram.org/' + 'bot<>' #Bot link removed

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

        if 'message' in temp_tel: ### if no 'message key' skip!
            print(temp_tel['message']['text'] + ' text found')
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
    return str(time.time_ns())[13:]
    
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
easytitle = "Co-Win Notifier v" + str(base_ver) + " Telegram alert"

def tel_easygui1():
    #-----------------easygui first frame-------------------------------

    easymsg = "Welcome! The bot will send you alerts when slots are found\n\nOpen the chatbot in Telegram:\
\n*Search for the bot in Telegram search bar: Co-Win Notifier v" + str(base_ver) + "\nor\n*Open this link:\nt.me/co_win_notifier_bot \nor \n\
*Scan the QR code below using any QR code scanner\n------------------------------------------\n\
Make sure the bot profile photo matches with the one given in the QR code below\nOnce your found the bot click on 'Next' below the QR code"

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
Once you sent the code click on 'Next' below. This window may not be visible for some seconds. The program is trying to search your message from the server and may take some time to load!!!!\n\n\
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

#------------
global vaccOP
def vaccinechkboxveri(): # verify checkboxes | returns false if no checkbox selected else updates vaccOP list and returns True
    global vaccOP
    if (vacc1.get() + vacc2.get() + vacc3.get() + vacc4.get() + vacc5.get() + vacc6.get() + vacc7.get() + vacc8.get() + vacc9.get() == '000000000'):
        return False

    vaccOP = f'{vacc1.get()} {vacc2.get()} {vacc3.get()} {vacc4.get()} {vacc5.get()} {vacc6.get()} {vacc7.get()} {vacc8.get()} {vacc9.get()}'.split(' ')
    print(vaccOP) # updated vaccOP
    return True
    


#---------------Back button------------------------
def backmain():
    root.destroy()
    mainf(0) #recreate main frame

def backbtn():
    global backbtnimg
    backbtnimg= PhotoImage(file=resource_path('data/back.png'))
    back_btn= ttk.Button(root, text='Back', image=backbtnimg, command=backmain, compound=LEFT)
    back_btn.place(x=80, y=460, anchor="center")
#---------------------------------------------------

def checkboxwarning(txt):
    warning = Label(root, text=txt,fg="#F7347A", font="Ubuntu 10")
    warning.place(x=190, y=375, anchor="center")
    root.after(5000, warning.destroy)


def checkModePin():
    global chkmode #which mode usr selected | 0: Pin, 1: District

#----------------------Checkbox verify-----------------------------------------------
    global chkvac_sputnik, chkvac_covi, chkvac_cova #vaccine name buttons
    global chk_free, chk_paid #free paid buttons

#-----vaccine names----------------
    if (vaccinechkboxveri() == False):
        checkboxwarning("Select atleast one vaccine")
        return
#----Free paid---------------------
    if (chk_free.get() + chk_paid.get() == '00'):
        checkboxwarning("Free, Paid slots?")
        return
#------------------------------------------------------------------------------------
    
    chkmode = 0
    mainf(2)
    backbtn() ##add  back button
    seletedModePin()



def checkModeDistrict():
    global chkmode #which mode usr selected | 0: Pin, 1: District


#----------------------Checkbox verify-----------------------------------------------
    global vacc1,vacc2,vacc3,vacc4,vacc5,vacc6,vacc7,vacc8,vacc9 #vaccine name buttons
    global chk_free, chk_paid #free paid buttons

#-----vaccine names----------------
    if (vaccinechkboxveri() == False):
        checkboxwarning("Select atleast one vaccine")
        return
#----Free paid---------------------
    if (chk_free.get() + chk_paid.get() == '00'):
        checkboxwarning("Free, Paid slots?")
        return
#------------------------------------------------------------------------------------
    
    chkmode = 1
    mainf(2)
    backbtn() ##add  back button
    seletedModeDistrict()


#--------------------------------------------------------------------------------------------------------------
#---------------------------------------------------Main Frame--------------------------------------------------

print("This is an Console Window, errors if any will be printed here!")

global root


def mainf(func):
    global welcomeText2,welcomeText,choiceText,buttonDistrict,buttonPin,tel_choiceText,tel_buttonPin,doseR1,doseR2, ageR1, ageR2, payR1, payR2, updatetext  #elements which will be destroyed later
    global enteredPin, date, variableState, variableDis,indexDistrict, selectedStateId, statesArray, idArray, districtArray, districtIdAray, dateRadio, availableDosesArray #variables

    #checkbox
    global vacc1,vacc2,vacc3,vacc4,vacc5,vacc6,vacc7,vacc8,vacc9
    global vacc1_btn, vacc2_btn, vacc3_btn, vacc4_btn, vacc5_btn, vacc6_btn, vacc7_btn, vacc8_btn, vacc9_btn #checkbox button #destroyed
    global vaccnalb #label #destroyed
    
    if (func == 2): #destroy
        welcomeText2.destroy()
        welcomeText.destroy()
        choiceText.destroy()
        buttonDistrict.destroy()
        buttonPin.destroy()

        tel_choiceText.destroy()
        tel_buttonPin.destroy()
        doseR1.destroy()
        doseR2.destroy()
        ageR1.destroy()
        ageR2.destroy()
        payR1.destroy()
        payR2.destroy()
        updatetext.destroy()

        vaccnalb.destroy()
        vacc1_btn.destroy()
        vacc2_btn.destroy()
        vacc3_btn.destroy()
        vacc4_btn.destroy()
        vacc5_btn.destroy()
        vacc6_btn.destroy()
        vacc7_btn.destroy()
        vacc8_btn.destroy()
        vacc9_btn.destroy()
        
        return
    
    #Due to garbage collection, declare image variables as global
    
    #0: no canvas
    #1: show canvas
    #2: destroy created objects

    global website_dir
    global website_dir
    global root

    root = Tk()
    root.title("Co-Win Notifier v" + str(base_ver))
    root.geometry('400x500')
    root.resizable(width=False, height=False)
    root.iconbitmap(resource_path("data/icon.ico"))

    #---------------------Theme------------------------------
    ### Here are the three lines by which we set the theme ###
    # Create a style
    global style
    style = ttk.Style(root)
    # Import the tcl file
    root.tk.call('source', 'azure-dark.tcl')
    # Set the theme with the theme_use method
    style.theme_use('azure-dark')
    #---------------------------------------------------------

    enteredPin = StringVar() 
    date = StringVar()
    variableState = StringVar()
    variableDis = StringVar()
    indexDistrict = StringVar()
    selectedStateId = StringVar()
    statesArray = []
    idArray = []
    districtArray = []
    districtIdAray = []
    dateRadio = IntVar(value=1)
    availableDosesArray = [] 

    
    #welcome text
    welcomeText = Label(root, text ="Welcome to Co-Win Notifier v" + str(base_ver), fg="white", font="Ubuntu 17")
    welcomeText.place(x=200, y=30, anchor="center")

    welcomeText2 = Label(root, text ="This Utility only checks for slot availability", fg="#F7347A", font="Ubuntu 10")
    welcomeText2.place(x=200, y=60, anchor="center")

    global github_btn, instagram_btn #### global
    github_btn= PhotoImage(file=resource_path('data/github.png'))
    
    def opensite():
        webbrowser.open('https://github.com/ashvnv/Co-Win-Notifier')
    creditText2 = Label(root, text ="GitHub", fg="gray", font="Ubuntu 10 bold")  
    creditText2.place(x=330, y=480, anchor="center")
    global github_btn2 ### global
    github_btn2= PhotoImage(file=resource_path('data/github.png'))
    buttonGit2= Button(root, image=github_btn,command=opensite, borderwidth=0)
    buttonGit2.place(x=370, y=480, anchor="center")

    updatetext = Label(root, text ="No updates available | Current version " + str(current_ver), fg="gray", font="Ubuntu 8 bold")
    updatetext.place(x=120, y=480, anchor='center')

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
        
    tel_choiceText = Label(root, text=tel_choiceTextSet,fg="#E0DCDB", font="Ubuntu 11")
    tel_choiceText.place(x=140, y=100, anchor="center")

    tel_buttonPin = ttk.Button(root, text=tel_choicebtntext, style='AccentButton', command=tel_easygui_configure)
    tel_buttonPin.place(x=tel_xlen, y=100, anchor="center")
#---------------------------------------------------------------------------------

#----------------------dose option----------------------
    global chkdoseop
    chkdoseop = StringVar(value='available_capacity_dose1')

    doseR1 = ttk.Radiobutton(root,text='Dose 1',variable=chkdoseop, value='available_capacity_dose1')
    doseR1.place(x=80, y=160, anchor="center")

    doseR2 = ttk.Radiobutton(root,text='Dose 2',variable=chkdoseop, value='available_capacity_dose2')
    doseR2.place(x=80, y=190, anchor="center")
#-------------------------------------------------------


#---------------------------age option--------------------
    global chkageop
    chkageop = IntVar(value=18)

    ageR1 = ttk.Radiobutton(root,text='Age 18+',variable=chkageop, value=18)
    ageR1.place(x=195, y=160, anchor="center")

    ageR2 = ttk.Radiobutton(root,text='Age 45+',variable=chkageop, value=45)
    ageR2.place(x=195, y=190, anchor="center")

#-----------------------------------------------------------

    
#---------------------------paid or free--------------------
    #global chkpayop
    #chkpayop = StringVar()

    #payR1 = Radiobutton(root,text='Free',variable=chkpayop, value='Free')
    #payR1.place(x=290, y=160, anchor="center")
    #payR1.select()

    #payR2 = Radiobutton(root,text='Paid',variable=chkpayop, value='Paid')
    #payR2.place(x=290, y=180, anchor="center")


    # added checkbuttons
    global chk_free
    global chk_paid
    
    chk_free = StringVar(value='Free')
    payR1 = ttk.Checkbutton(root, text = "Free", variable = chk_free, onvalue = 'Free', offvalue = '0')
    payR1.place(x=300, y=160, anchor="center")

    chk_paid = StringVar(value='Paid')
    payR2 = ttk.Checkbutton(root, text = "Paid", variable = chk_paid, onvalue = 'Paid', offvalue = '0')
    payR2.place(x=300, y=190, anchor="center")

#-----------------------------------------------------------

#-----------------------Vaccine names-------------------------
    
    global chkvac_sputnik
    global chkvac_covi
    global chkvac_cova
    
    #chkvac_sputnik = StringVar(value='SPUTNIKV')
    #vacnmbtn1 = ttk.Checkbutton(root, text = "Sputnik V", variable = chkvac_sputnik, onvalue = 'SPUTNIKV', offvalue = '0')
    #vacnmbtn1.place(x=70, y=240, anchor="center")

    #chkvac_covi = StringVar(value='COVISHIELD')
    #vacnmbtn2 = ttk.Checkbutton(root, text = 'Covishield', variable = chkvac_covi, onvalue = 'COVISHIELD', offvalue = '0')
    #vacnmbtn2.place(x=195, y=240, anchor="center")

    #chkvac_cova = StringVar(value='COVAXIN')
    #vacnmbtn3 = ttk.Checkbutton(root, text = "Covaxin", variable = chkvac_cova, onvalue = 'COVAXIN', offvalue = '0')
    #vacnmbtn3.place(x=320, y=240, anchor="center")

    #---------------------- vaccines ---------------------------
    # accessing VacData list updated during init
    # VacData format: <Vaccine name> <API search name> <Approved or not (Y/N)>
    #                   Covishield       COVISHIELD              Y
    # data stored in a list VacData


    vaccnalb = Label(root, text ="Some vaccine options may be disabled\nCheckbox will be enabled once the vaccine is approved", fg="#76D7C4", font="Ubuntu 10")
    vaccnalb.place(x=200, y=230, anchor="center")

    #-----Buttons initialize----------
    vacc1_btn = ttk.Checkbutton(root, text=VacData[0], onvalue=VacData[1], offvalue = '0', state=DISABLED)
    vacc1_btn.place(x=70, y=275, anchor="center")
    
    vacc2_btn = ttk.Checkbutton(root, text=VacData[3], onvalue=VacData[4], offvalue = '0', state=DISABLED)
    vacc2_btn.place(x=195, y=275, anchor="center")
    
    vacc3_btn = ttk.Checkbutton(root,text=VacData[6], onvalue=VacData[7], offvalue = '0', state=DISABLED)
    vacc3_btn.place(x=320, y=275, anchor="center")
    
    vacc4_btn = ttk.Checkbutton(root,text=VacData[9], onvalue=VacData[10], offvalue = '0', state=DISABLED)
    vacc4_btn.place(x=70, y=310, anchor="center")
    
    vacc5_btn = ttk.Checkbutton(root,text=VacData[12], onvalue=VacData[13], offvalue = '0', state=DISABLED)
    vacc5_btn.place(x=195, y=310, anchor="center")
    
    vacc6_btn = ttk.Checkbutton(root,text=VacData[15], onvalue=VacData[16], offvalue = '0', state=DISABLED)
    vacc6_btn.place(x=320, y=310, anchor="center")
    
    vacc7_btn = ttk.Checkbutton(root,text=VacData[18], onvalue=VacData[19], offvalue = '0', state=DISABLED)
    vacc7_btn.place(x=70, y=345, anchor="center")
    
    vacc8_btn = ttk.Checkbutton(root,text=VacData[21], onvalue=VacData[22], offvalue = '0', state=DISABLED)
    vacc8_btn.place(x=195, y=345, anchor="center")

    vacc9_btn = ttk.Checkbutton(root,text=VacData[24], onvalue=VacData[25], offvalue = '0', state=DISABLED)
    vacc9_btn.place(x=320, y=345, anchor="center")

    #-----Initialize variable
    if VacData[2] == 'Y': #Vaccine approved
        vacc1 = StringVar(value=VacData[1])
        vacc1_btn['state']=NORMAL
    else:
        vacc1 = StringVar(value='0')
    vacc1_btn['variable']=vacc1


    if VacData[5] == 'Y': #Vaccine approved
        vacc2 = StringVar(value=VacData[4])
        vacc2_btn['state']=NORMAL
    else:
        vacc2 = StringVar(value='0')
    vacc2_btn['variable']=vacc2

    if VacData[8] == 'Y': #Vaccine approved
        vacc3 = StringVar(value=VacData[7])
        vacc3_btn['state']=NORMAL
    else:
        vacc3 = StringVar(value='0')
    vacc3_btn['variable']=vacc3

    if VacData[11] == 'Y': #Vaccine approved
        vacc4 = StringVar(value=VacData[10])
        vacc4_btn['state']=NORMAL
    else:
        vacc4 = StringVar(value='0')
    vacc4_btn['variable']=vacc4

    if VacData[14] == 'Y': #Vaccine approved
        vacc5 = StringVar(value=VacData[13])
        vacc5_btn['state']=NORMAL
    else:
        vacc5 = StringVar(value='0')
    vacc5_btn['variable']=vacc5

    if VacData[17] == 'Y': #Vaccine approved
        vacc6 = StringVar(value=VacData[16])
        vacc6_btn['state']=NORMAL
    else:
        vacc6 = StringVar(value='0')
    vacc6_btn['variable']=vacc6

    if VacData[20] == 'Y': #Vaccine approved
        vacc7 = StringVar(value=VacData[19])
        vacc7_btn['state']=NORMAL
    else:
        vacc7 = StringVar(value='0')
    vacc7_btn['variable']=vacc7

    if VacData[23] == 'Y': #Vaccine approved
        vacc8 = StringVar(value=VacData[22])
        vacc8_btn['state']=NORMAL
    else:
        vacc8 = StringVar(value='0')
    vacc8_btn['variable']=vacc8

    if VacData[26] == 'Y': #Vaccine approved
        vacc9 = StringVar(value=VacData[25])
        vacc9_btn['state']=NORMAL
    else:
        vacc9 = StringVar(value='0')
    vacc9_btn['variable']=vacc9
        
#--------------------------------------------------------------

#--------------------------------------------------------------



    choiceText = Label(root, text="Select Checking Mode",fg="#C6E2FF", font="Ubuntu 18")
    choiceText.place(x=200, y=400, anchor="center")

    buttonPin = ttk.Button(root, text="By PinCode", command=checkModePin)
    buttonPin.place(x=140, y=440, anchor="center")

    buttonDistrict = ttk.Button(root, text="By District", command=checkModeDistrict)
    buttonDistrict.place(x=250, y=440, anchor="center")

    
    if (func == 1): #calling for the first time
        global canvas, splashImage
        canvas = Canvas(root, width = 400, height = 500) 
        canvas.place(x=200, y=250, anchor="center") 
        splashImage = PhotoImage(file= resource_path('data/splash.png'))
        canvas.create_image(200,250, anchor="center", image=splashImage) 
        t = Timer(2.0, splashWin)
        t.start()


mainf(1) ## call mainf first time with canvas


#-------------------------------------------------------------------------------------------------------------------------

def warningtxt():
    warning = Label(root, text="Error occurred! Check your network\nIf error still persists raise an issue on GitHub",fg="#F7347A", font="Ubuntu 10")
    warning.place(x=200, y=355, anchor="center")
    root.after(10000, warning.destroy)
    global counter
    counter = 0 #reset counter

#-------------------------------------------------------------------------------------------------------------------------
#create and destroy the checking window functions

global counter
counter=0 #initialize counter

global DESTROYCHK
DESTROYCHK = False


def chkagain():
    global chkmode #which mode usr selected | 0: Pin, 1: District
    global output, chkstopbtn
    global DESTROYCHK
    global counter

    output.destroy() #destroy current label
    chkstopbtn.destroy() #destroy 
    
    if (DESTROYCHK == False):
        if chkmode == 0:
            startCheckingPin()
        else:
            startCheckingDistrict()
    else:
        DESTROYCHK = False
        print('Window destroyed')
        counter = 0

        if chkmode == 1: #district button enable
            global startDistrictCheck
            startDistrictCheck['text'] = 'START'
            startDistrictCheck['state'] = 'normal'
        else: # pin button enable
            global startPinCheck
            startPinCheck['text'] = 'START'
            startPinCheck['state'] = 'normal'
            


def chkwin():
    print('no pref slots found')
    global output
    output = Label(root, text="No Slots Available \n Will Automatically Check Again in 3 secs... \n\n\n This will launch your browser once\n\
when slot is Available! \n\n\n Do not close this window!!\n\nNumber of retries: " + str(counter),width=200, height=50, fg="white", bg="black",  font="Ubuntu 13") 
    output.place(x=200, y=160, anchor="center")

    global chkstopbtn
    chkstopbtn = ttk.Button(root, text="Stop", style='AccentButton', command=chkwindest)
    chkstopbtn.place(x=200, y=330, anchor="center")

    root.after(3100, chkagain) #call chkagain() every 3.1 seconds | making 96 API calls ~ 90
    
def chkwindest():
    global DESTROYCHK, chkstopbtn
    DESTROYCHK = True
    chkstopbtn['text'] = 'Stopping'
    chkstopbtn['state'] = 'disabled'

#------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------

def seletedModePin():
  #picode text
  testText = Label(root, text="Enter Pincode",fg="#E6E6FA", font="Ubuntu 18")
  testText.place(x=200, y=40, anchor="center")

  #pincode input
  pinInput = ttk.Entry(root, font="Ubuntu 10", width=10, textvariable = enteredPin)
  pinInput.place(x=200, y=80, anchor="center")

    #pincode text
  testText = Label(root, text="Select Day \n(Ideally Select Tomorrow or Day After)",fg="#E6E6FA", font="Ubuntu 12")
  testText.place(x=200, y=120, anchor="center")
  
  #radio
  global dateRadio
  dateSelectToday = ttk.Radiobutton(root, text="Today", variable=dateRadio, value= 0)
  dateSelectToday.place(x=133, y=170, anchor=E)

  dateSelectTommorow = ttk.Radiobutton(root, text="Tomorrow", variable=dateRadio, value= 1)
  dateSelectTommorow.place(x=246, y=170, anchor=E)

  dateSelectNext = ttk.Radiobutton(root, text="Day After", variable=dateRadio, value= 2)
  dateSelectNext.place(x=350, y=170, anchor=E)

  #start button
  global startPinCheck
  startPinCheck = ttk.Button(root,text="START",style='AccentButton', command= checkPinBox)
  startPinCheck.place(x=200, y=220, anchor="center")

#---------------------------------------------------------------------------------------------------------------

def checkPinBox():    
    if len(str(enteredPin.get())) == 6:
        pin_temp_()
    else:
        warning = Label(root, text="Enter Valid Pincode",fg="#F7347A", font="Ubuntu 10")
        warning.place(x=200, y=255, anchor="center")
        root.after(1000, warning.destroy)

def pin_temp_(): #disable button and call next func
    global startPinCheck
    startPinCheck['text'] = 'Searching!'
    startPinCheck['state'] = 'disabled'
    root.after(10, startCheckingPin)

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
    try:
        checkLoop(finalUrl)
    except:
        print('Error occurred in PinMode check')
        warningtxt()
        global startPinCheck
        startPinCheck['text'] = 'Error occurred! Try again'
        startPinCheck['state'] = 'normal'
        return
        


#----------------------------------

def checkLoop(finalUrl):
    global counter
    counter+=1
    
    req = Request(finalUrl, headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(req)
    data_json = json.loads(response.read())
    dataRaw = "{'sessions': []}"
    print(f"The data received from the server is \n\n {data_json} \n")

    if str(data_json) == dataRaw:
        chkwin()
    else:
        for center in data_json['sessions']:
            outputText =  str(center[chkdoseop.get()]) # dose count check
            print(outputText)
            if int(outputText) > 0:

                #level 1: age and slot fee check
                if chkageop.get() == int(center['min_age_limit']) and (chk_free.get() == str(center['fee_type']) or chk_paid.get() == str(center['fee_type'])):
                    print('level 1 passed: age & fee')

                    #level 2: vaccine name check
                    #if (str(center['vaccine']) == chkvac_sputnik.get() or str(center['vaccine']) == chkvac_covi.get() or str(center['vaccine']) == chkvac_cova.get()):
                    if str(center['vaccine']) in vaccOP:
                        print('level 2 passed: vaccine name')
                        
                        fnd_info = str(json.dumps(center))
                        temp = fnd_info.translate(str.maketrans(
                            {',': '\n',
                             '"': '',
                             '[': '\n',
                             ']': '',
                             '{': '',
                             '{': ''})) # remove JSON characters
                        print(temp)
                        counter = 0 #reset counter
                        webbrowser.open(resource_path("website/slot.html"))
                        if telegram_alert == True:
                            send_telegram_message('Slot found!\n\n' + temp)

                        # enable pin mode button
                        global startPinCheck
                        startPinCheck['text'] = 'close SLOT-INFO window'

                        # easy gui slots info
                        msgbox(temp, 'SLOT-INFO', 'Close')

                        startPinCheck['text'] = 'START'
                        startPinCheck['state'] = 'normal'
                        
                        return
        chkwin()

        

#------------------------------------------------------------------------
        #District
#------------------------------------------------------------------------

def seletedModeDistrict():
    global  statesArray, idArray, variableState
    #Get State Data from API
    urlStates = 'https://cdn-api.co-vin.in/api/v2/admin/location/states'
    req = Request(urlStates, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urlopen(req)
    except:
        warningtxt()
        return
        
    data_json = json.loads(response.read())

    statesArray.append('Select your state') #for ttk OptionMenu
    
    for states in data_json['states']:
        statesArray.append(states.get('state_name'))
    for id in data_json['states']:
        idArray.append(id.get('state_id'))

    warnText2 = Label(root, text ="Loading of States and Districts can take a few secs....", fg="#F7347A", font="Ubuntu 10")
    warnText2.place(x=200, y=20, anchor="center")
    
    stateText = Label(root, text="State", fg="#E6E6FA", font="Ubuntu 10")
    stateText.place(x=200, y=45, anchor='center')

    stateDrop = ttk.OptionMenu(root, variableState, *statesArray, command=districtSelect)
    stateDrop.config(width=38)
    stateDrop.place(x=45, y=75, anchor='w')

  
def districtSelect(self):
    global  statesArray, idArray, variableDis,districtArray,districtIdAray,dateRadio
    districtArray.clear() ## clear list if user selects another state
    districtIdAray.clear()

    districtText = Label(root, text="District", fg="#E6E6FA", font="Ubuntu 10")
    districtText.place(x=200, y=120, anchor='center')

    
    indexDistrict = statesArray.index(variableState.get())-1 # added 'Select your state' to statesArray inside selectedModeDistrict()
    selectedStateId = idArray[indexDistrict]
    urlDistricts = (f"https://cdn-api.co-vin.in/api/v2/admin/location/districts/{selectedStateId}")
    print(urlDistricts)
    req = Request(urlDistricts, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urlopen(req)
    except:
        warningtxt()
        return
        
    data_json = json.loads(response.read())

    districtArray.append('Select your district') #string is checked inside district_temp_() to confirm if user has selected any option
    
    for districts in data_json['districts']:
        districtArray.append(districts.get('district_name'))
    for district_id in data_json['districts']:
        districtIdAray.append(district_id.get('district_id'))  


    districtDrop = ttk.OptionMenu(root, variableDis, *districtArray)
    districtDrop.config(width=38)
    districtDrop.place(x=45, y=150, anchor='w')

    testText = Label(root, text="Select Day \n(Ideally Select Tomorrow or Day After)",fg="#E6E6FA", font="Ubuntu 12")
    testText.place(x=200, y=210, anchor="center")

  #radio
    global dateRadio
    dateSelectToday = ttk.Radiobutton(root, text="Today", variable=dateRadio, value= 0)
    dateSelectToday.place(x=133, y=260, anchor=E)

    dateSelectTommorow = ttk.Radiobutton(root, text="Tomorrow", variable=dateRadio, value= 1)
    dateSelectTommorow.place(x=246, y=260, anchor=E)
 
    dateSelectNext = ttk.Radiobutton(root, text="Day After", variable=dateRadio, value= 2)
    dateSelectNext.place(x=350, y=260, anchor=E)

    global startDistrictCheck
    startDistrictCheck = ttk.Button(root, text="START",style='AccentButton',command=district_temp_)
    startDistrictCheck.place(x=200, y=300, anchor="center")
    
#--------------------------------------------
def district_temp_(): #disable button and call next func
    global startDistrictCheck

    if variableDis.get() == 'Select your district': #district not selected
        print('District null')
        warning = Label(root, text='Select district',fg="#F7347A", font="Ubuntu 10")
        warning.place(x=200, y=330, anchor="center")
        root.after(3000, warning.destroy)
        return
        
    startDistrictCheck['text'] = 'Searching!'
    startDistrictCheck['state'] = 'disabled'
    
    root.after(10, startCheckingDistrict)


def startCheckingDistrict():
    global finalUrl #changes made here to global variable
    
    print("Checking ...")
    now = datetime.datetime.now()
    diff = datetime.timedelta(days=(dateRadio.get()))
    dateSelected = now + diff
    finalDate = dateSelected.strftime('%d-%m-%Y') #date final
    print('Final date ' +str(finalDate))
    districtID = str(variableDis.get())  #district id
    print(f"Selected district is {districtID}")  
    selectedDistrictId = districtArray.index(variableDis.get())-1 # added 'Select your district' to districtArray inside districtSelect()
    realDistrictId = districtIdAray[selectedDistrictId]  

    finalUrl = (f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={realDistrictId}&date={finalDate}")
    print(finalUrl)
    
    try:
        checkLoopDis(finalUrl)
    except:
        print('Error occurred in DistrictMode check')
        warningtxt()
        global startPinCheck
        startDistrictCheck['text'] = 'Error occurred! Try again'
        startDistrictCheck['state'] = 'normal'
        return

def checkLoopDis(finalUrl):
    global counter
    counter+=1
    
    req = Request(finalUrl, headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(req)
    data_json = json.loads(response.read())
    dataRaw = "{'sessions': []}"
    print(f"The data recieved from the server is \n\n {data_json} \n")

    if str(data_json) == dataRaw:
        chkwin()
    else:
        for center in data_json['sessions']:
            outputText =  str(center[chkdoseop.get()]) # dose count check
            print(outputText)
            if int(outputText) > 0:

                #level 1: age and slot fee check
                if chkageop.get() == int(center['min_age_limit']) and (chk_free.get() == str(center['fee_type']) or chk_paid.get() == str(center['fee_type'])):
                    print('level 1 passed: age & fee')

                    #level 2: vaccine name check
                    if str(center['vaccine']) in vaccOP:
                        print('level 2 passed: vaccine name')
                        
                        fnd_info = str(json.dumps(center))
                        temp = fnd_info.translate(str.maketrans(
                            {',': '\n',
                             '"': '',
                             '[': '\n',
                             ']': '',
                             '{': '',
                             '{': ''})) # remove JSON characters
                        print(temp)
                        counter = 0 #reset counter
                        webbrowser.open(resource_path("website/slot.html"))
                        if telegram_alert == True:
                            send_telegram_message('Slot found!\n\n' + temp)

                        global startDistrictCheck
                        startDistrictCheck['text'] = 'close SLOT-INFO window'
                        
                        # easy gui slots info
                        msgbox(temp, 'SLOT-INFO', 'Close')

                        # enable buttons
                        startDistrictCheck['text'] = 'START'
                        startDistrictCheck['state'] = 'normal'
                        
                        return
        chkwin()

        

root.mainloop()


