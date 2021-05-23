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

# data_dir = os.path.join(os.path.dirname(__file__), "data")
# website_dir = os.path.join(os.path.dirname(__file__), "website")

print("This is an Console Window, errors if any will be printed here!")

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

data_dir = resource_path("data")
website_dir = resource_path("website")    

def open_link_github():
  webbrowser.open('www.github.com/CatalystMonish')
def open_link_instagram():
  webbrowser.open('www.instagram.com/meher._.catalyst')
def splashWin():
  canvas.destroy()

def checkModePin():
  welcomeText2.destroy()
  welcomeText.destroy()
  choiceText.destroy()
  buttonDistrict.destroy()
  buttonPin.destroy()
  internetText.destroy()
  seletedModePin()

def checkModeDistrict():
  welcomeText2.destroy()
  welcomeText.destroy()
  choiceText.destroy()
  buttonDistrict.destroy()
  buttonPin.destroy()
  internetText.destroy()
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


  
  
root = Tk()

 
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

root.title("Cowin Notifier")
root.geometry('400x400')
root.resizable(width=False, height=False)
root.iconbitmap(resource_path("data/icon.ico"))

#welcome text
welcomeText = Label(root, text ="Welcome to Co-win Notifier", fg="black", bg='#dbdbdb', font="Ubuntu 20")
welcomeText.place(x=200, y=30, anchor="center")

welcomeText2 = Label(root, text ="Note: This only Utility checks for\nonly Vaccine 1 Slots!", fg="red", font="Ubuntu 10")
welcomeText2.place(x=200, y=80, anchor="center")

#credits
creditText = Label(root, text ="Made by Catalyst", fg="gray", font="Ubuntu 8 bold")
creditText.place(x=300, y=380, anchor="center")
github_btn= PhotoImage(file=resource_path('data/github.png'))
buttonGit= Button(root, image=github_btn,command= open_link_github, borderwidth=0)
buttonGit.place(x=360, y=380, anchor="center")
instagram_btn= PhotoImage(file=resource_path('data/instagram.png'))
buttonInsta= Button(root, image=instagram_btn, command=open_link_instagram, borderwidth=0)
buttonInsta.place(x=380, y=380, anchor="center")

choiceText = Label(root, text="Select Checking Mode",fg="black", font="Ubuntu 18")
choiceText.place(x=200, y=180, anchor="center")

buttonPin = Button(root, text="By PinCode", font="Ubuntu 10", command=checkModePin)
buttonPin.place(x=150, y=220, anchor="center")

buttonDistrict = Button(root, text="By District", font="Ubuntu 10", command=checkModeDistrict)
buttonDistrict.place(x=250, y=220, anchor="center")

internetText = Label(root, text="Ensure your internet is\nWorking before clicking",fg="green", font="Ubuntu 12")
internetText.place(x=200, y=280, anchor="center")

canvas = Canvas(root, width = 400, height = 400) 
canvas.place(x=200, y=200, anchor="center") 
splashImage = PhotoImage(file= resource_path('data/splash.png'))
canvas.create_image(200,200, anchor="center", image=splashImage) 
t = Timer(2.0, splashWin)
t.start()


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
  req = Request(finalUrl, headers={'User-Agent': 'Mozilla/5.0'})
  response = urlopen(req)
  data_json = json.loads(response.read())
  dataRaw = "{'sessions': []}"
  print(f"The data recieved from the server is \n\n {data_json} \n")
  for center in data_json['sessions']:
    outputText =  str(center['available_capacity_dose1']) 
  if str(data_json) == dataRaw:
    output = Label(root, text="No Slots Available \n Will Automatically Check Again in 10secs... \n\n\n This will launch your browser once\nwhen slot is Available! \n\n\n Do not close this window!!",width=200, height=50, fg="white", bg="black",  font="Ubuntu 13") 
    output.place(x=200, y=160, anchor="center")   
    root.after(10000, output.destroy)  
    root.after(10000, startCheckingPin)
      
  else:  
    if int(outputText) == 0:
      output = Label(root, text=f"{outputText} Slots Available \n Will Automatically Check Again in 10secs... \n\n\n This will launch your browser once\nwhen slot is Available! \n\n\n Do not close this window!!",width=200, height=50, fg="white", bg="black",  font="Ubuntu 13") 
      output.place(x=200, y=160, anchor="center")   
      root.after(10000, output.destroy) 
      root.after(10000, startCheckingPin)
    else :  
      output = Label(root, text="Found", fg="white", bg="black",  font="Ubuntu 13")   
      output.place(x=200, y=160, anchor="center")
      webbrowser.open(resource_path("website/slot.html"))

def seletedModeDistrict():
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

  stateText = Label(root, text="Select Your State", fg="black", font="Ubuntu 10")
  stateText.place(x=150, y=50, anchor='center')
  districtText = Label(root, text="Select Your District", fg="black", font="Ubuntu 10")
  districtText.place(x=150, y=80, anchor='center')
  
  stateDrop = OptionMenu(root, variable, *statesArray, command=districtSelect)
  stateDrop.place(x=240, y=50, anchor='w')
 

def districtSelect(self):
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

 

  districtDrop = OptionMenu(root, variableDis, *districtArray)
  districtDrop.place(x=240, y=80, anchor='w')

  testText = Label(root, text="Select Day \n(Ideally Select Tommorow or Day After)",fg="black", font="Ubuntu 12")
  testText.place(x=200, y=130, anchor="center")

  #radio
  dateSelectToday = Radiobutton(root, text="Today", variable=dateRadio, value= 0)
  dateSelectToday.place(x=133, y=180, anchor=E)

  dateSelectTommorow = Radiobutton(root, text="Tommorow", variable=dateRadio, value= 1)
  dateSelectTommorow.place(x=246, y=180, anchor=E)

  dateSelectNext = Radiobutton(root, text="Day After", variable=dateRadio, value= 2)
  dateSelectNext.place(x=350, y=180, anchor=E)

  startDistrictCheck = Button(root, text="START" ,font="Ubuntu 10", command=startCheckingDistrict)
  startDistrictCheck.place(x=200, y=210, anchor="center")

def startCheckingDistrict():
  print("Checking ...")
  now = datetime.datetime.now()
  diff = datetime.timedelta(days=(dateRadio.get()))
  dateSelected = now + diff
  finalDate = dateSelected.strftime('%d-%m-%Y')
  districtID = str(variableDis.get())  
  print(f"Selected district is {districtID}")  
  selectedDistrictId = districtArray.index(variableDis.get())
  realDistrictId = districtIdAray[selectedDistrictId]  

  finalUrl = (f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={realDistrictId}&date={finalDate}")
  print(finalUrl)
  checkLoopDis(finalUrl)

def checkLoopDis(finalUrl):  
  req = Request(finalUrl, headers={'User-Agent': 'Mozilla/5.0'})
  response = urlopen(req)
  data_json = json.loads(response.read())
  dataRaw = "{'sessions': []}"
  for center in data_json['sessions']:
    if(center != dataRaw):
     availableDosesArray.append(center.get('available_capacity_dose1'))
  totalDoses = sum(availableDosesArray)
  print(f"The total number of doses available {totalDoses}")   
  if str(data_json) == dataRaw:
    output = Label(root, text="No Slots Available \n Will Automatically Check Again in 10secs... \n\n\n This will launch your browser once\nwhen slot is Available! \n\n\n Do not close this window!!",width=200, height=50, fg="white", bg="black",  font="Ubuntu 13") 
    output.place(x=200, y=160, anchor="center")   
    root.after(10000, output.destroy)  
    root.after(10000, startCheckingDistrict)   
  elif int(totalDoses) > 0:
    output = Label(root, text="Found", fg="white", bg="black",  font="Ubuntu 13")   
    output.place(x=200, y=160, anchor="center")
    webbrowser.open(resource_path("website/slot.html"))
  elif int(totalDoses) == 0:
    output = Label(root, text="No Slots Available \n Will Automatically Check Again in 10secs... \n\n\n This will launch your browser once\nwhen slot is Available! \n\n\n Do not close this window!!",width=200, height=50, fg="white", bg="black",  font="Ubuntu 13") 
    output.place(x=200, y=160, anchor="center")   
    root.after(10000, output.destroy)  
    root.after(10000, startCheckingDistrict) 
  else :  
    output = Label(root, text="Found", fg="white", bg="black",  font="Ubuntu 13")   
    output.place(x=200, y=160, anchor="center")
    webbrowser.open(resource_path("website/slot.html"))

root.mainloop()
