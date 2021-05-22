# Co-Win Notifier v2

![BD](https://github.com/ashvnv/Co-Win-Notifier/blob/master/Pics/Screenshot%20from%202021-05-21%2020-51-55.png)

### Read Before Using This Software!

This utitlity is not signed with any certificates, so Windows may flag this file as virus. The file is totally safe and only checks for slots availablity along with Telegram alerts. The program source code is available in this repository.


Read more on why windows considers non-signed programs virus:
https://posts.specterops.io/what-is-it-that-makes-a-microsoft-executable-a-microsoft-executable-b43ac612195e
This is an open source program, which does not collect any user data. The app only accesses the CoWIN API for getting the slots information and Telegram API for sending alerts. 



### Changelog:
- Added Telegram alert 
    - Does auth process between user and bot and bot and user
    - chatid is saved in the telcofig.txt file so that after rebooting the program, configuring the telegram is not required
    - telcongif.txt saved in current program directory  
- Added Vaccine search filer:<br>
    - Search based on Age filer [18+ and 45+]
    - Search slots based on first or second dose
    - Search for paid or free vaccine slots          
- tkinter main frame is moved inside mainf(), this was necessary because easygui could not render images so tkinter root is destroyed while easygui is called during configuring telegram alert
- pin wise and district wise slots find functions were updated, some redundant codes were removed
- some variables had to be declared global as tkinter is declared inside the mainf() and scope in python won't modifiy the global value of the variable
- Added update feature. When the app is launched, it checks for update from github repository. If update is available, a prompt is shown for updating the app to the latest version

### For security concerns, the telegram api configuration is blanked in the repository codes, so building the code from source would require adding these configurations unless telegram alert feature is not needed
### Co-Win Notifier.exe is already bundled with necessary telegram api and tokens. So telegram alert feature will run without additional configurations


  

