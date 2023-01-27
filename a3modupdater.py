import os
import sys
from subprocess import Popen, PIPE, CalledProcessError, DEVNULL, STDOUT, check_call
import glob

armaServerAppId = "233780"
armaClientAppId = "107410"

modsDirectory = "C:\\A3Master\\mods\\"
keysDirectory = "C:\\A3Master\\keys\\"
armaDirectory = "C:\\A3Master\\"
steamCMD = "C:\\steamcmd\\steamcmd.exe"
steamContentDirectory = "C:\\steamCMD\\a3server\\steamapps\\workshop\\content\\" + armaClientAppId + "\\"
steamTempScript = "C:\\SteamCMD\\tempUpdateScript.txt"
steamAuth = "C:\\steamcmd\\auth.txt"
workshopItems = "C:\\A3Master\\Steam Workshop IDs.txt"

userLogin = "you_dream_ru"
userPass = "XGm8QGu5fO8j"

def updateServer():
    print("Updating Server...")
    # Get the users login
    checkUserLogin()
    os.system(steamCMD + ' +login ' + userLogin + ' ' + userPass + ' +force_install_dir ' + armaDirectory + ' "+app_update ' + armaServerAppId + '" validate +quit')

def checkUserLogin():
    global userLogin
    global userPass
    
    if userLogin == "":
        userLogin = input("Steam> Username: ")
    if userPass == "":
        userPass = input("Steam> Password: ")
        
def copyKeys():
    for filename in glob.iglob(modsDirectory+'**\\*.bikey', recursive=True):
        os.system("xcopy " + filename + " " + keysDirectory + " /s /y")
        
error = ""

def main():
    os.system('cls')
    global userLogin
    global userPass

    try:
        with open(steamAuth) as f:
            for line in f:
                info = line.split(" ")
                if len(info) == 2:
                    userLogin = info[0]
                    userPass = info[1]
    except:
        pass

    global error 

    while True:
        userInput = input("Main Menu \n1. Update Server\n2. Update Mods\n3. Update Keys\n4. Exit\n" + error + ">> ")

        error = ""
        
        if userInput == "1":
            updateServer()
            input("Press any key to continue...")
            os.system('cls')
            
        elif userInput == "2":
            # Get the users login
            checkUserLogin()

            # Clear the temp script
            file = open(steamTempScript, 'w')

            script = "@ShutdownOnFailedCommand 1\n"
            script += "@NoPromptForPassword 1\n"
            script += "login " + userLogin + " " + userPass + "\n"
            script += "force_install_dir " + armaDirectory + "\n"

            mods = {}

            # Loop through each item in the workshop file
            with open(workshopItems) as f:
                for line in f:
                    modInfo = line.split(" ", 1)
                    steamWorkshopId = modInfo[0].strip()
                    modName = modInfo[1].strip()
                    modFolder = "@"+modName.replace(" ", "_").lower()

                    mods[steamWorkshopId] = {"name": modName, "folder": modFolder}
                    
                    script += 'workshop_download_item ' + armaClientAppId + ' ' + steamWorkshopId + ' validate\n'

                    # Make a link to the downloaded content (way better than moving...)
                    symLink = modsDirectory + modFolder
                    if not os.path.exists(symLink):
                        os.system('mklink /J ' + symLink + ' ' + steamContentDirectory + steamWorkshopId + '\n')

            script += "quit"
             
            file.write(script)
            file.close()

            # Run the script
            print("\n=====================================\nLogging into Steam...\n=====================================")
            
            with Popen(steamCMD + " +runscript " + steamTempScript, stdout=PIPE, bufsize=1, universal_newlines=True) as p:
                for line in p.stdout:
                    line = line.strip()
                    if line != "":
                        if line.find("Downloading item") != -1:
                            downloadingLine = line.split("Downloading item")
                            if downloadingLine[0]:  
                                print(downloadingLine[0])

                            try:
                                modIdLine = downloadingLine[1].strip().split(" ")
                                steamWorkshopId = modIdLine[0]
                                print("\n=====================================\nDownloading "+mods[steamWorkshopId]["name"] + " ["+str(steamWorkshopId)+"]...\n=====================================")
                            except:
                                pass
                                
                        else:
                            print(line)
            
            # Automatically copy bikeys over
            print("\n=====================================\nCopying addon keys...\n=====================================")
            copyKeys()
            
            input("\nPress any key to continue...")
            os.system('cls')
     
        elif userInput == "3":
            # Search for any bikeys and copy them into keys folder
            copyKeys()
            input("Press any key to continue...")
            os.system('cls')
        elif userInput == "4":
            sys.exit(0)
        elif userInput == "":
            os.system('cls')
        else:
            error = "[ERROR] Unknown choice. Try again\n"
		
		
def update_mods():
		# Get the users login
        checkUserLogin()

        # Clear the temp script
        file = open(steamTempScript, 'w')

        script = "@ShutdownOnFailedCommand 1\n"
        script += "@NoPromptForPassword 1\n"
        script += "login " + userLogin + " " + userPass + "\n"
        script += "force_install_dir " + armaDirectory + "\n"

        mods = {}

        # Loop through each item in the workshop file
        with open(workshopItems) as f:
            for line in f:
                modInfo = line.split(" ", 1)
                steamWorkshopId = modInfo[0].strip()
                modName = modInfo[1].strip()
                modFolder = "@"+modName.replace(" ", "_").lower()

                mods[steamWorkshopId] = {"name": modName, "folder": modFolder}
                
                script += 'workshop_download_item ' + armaClientAppId + ' ' + steamWorkshopId + ' validate\n'

                # Make a link to the downloaded content (way better than moving...)
                symLink = modsDirectory + modFolder
                if not os.path.exists(symLink):
                    os.system('mklink /J ' + symLink + ' ' + steamContentDirectory + steamWorkshopId + '\n')

        script += "quit"
         
        file.write(script)
        file.close()

        # Run the script
        print("\n=====================================\nLogging into Steam...\n=====================================")
        
        with Popen(steamCMD + " +runscript " + steamTempScript, stdout=PIPE, bufsize=1, universal_newlines=True) as p:
            for line in p.stdout:
                line = line.strip()
                if line != "":
                    if line.find("Downloading item") != -1:
                        downloadingLine = line.split("Downloading item")
                        if downloadingLine[0]:  
                            print(downloadingLine[0])

                        try:
                            modIdLine = downloadingLine[1].strip().split(" ")
                            steamWorkshopId = modIdLine[0]
                            print("\n=====================================\nDownloading "+mods[steamWorkshopId]["name"] + " ["+str(steamWorkshopId)+"]...\n=====================================")
                        except:
                            pass
                            
                    else:
                        print(line)
        
        # Automatically copy bikeys over
        print("\n=====================================\nCopying addon keys...\n=====================================")
        copyKeys()
        os.system('cls')
        logo()
        print("Bot ready")
if __name__ == "__main__":
    main ()
    
    
def logo():
    names = str("KENPATISERLERBAN"*200)
    print(names[0:60])
    print(names[0:14]+" "*30+names[0:16])
    print(names[0:10]+" "*8+r"//"+f"{names[0:20]}"+r"\\"+" "*8+names[0:10])
    print(names[0:10]+" "*7+r"//"+f"{names[0:22]}"+r"\\"+" "*7+names[0:10])
    print(names[0:10]+" "*7+r"||"+f"{names[0:4]}"+r"//"+" "*16+"---"+" "*6+names[0:10])
    print(names[0:10]+" "*7+r"||"+f"{names[0:4]}"+r"||"+" "*25+names[0:10])
    print(names[0:10]+" "*7+r"||"+f"{names[0:4]}"+r"||"+" "*25+names[0:10])
    print(names[0:10]+" "*7+r"\\"+f"{names[0:4]}"+r"\\"+" "*25+names[0:10])
    print(names[0:10]+" "*8+r"\\"+f"{names[0:4]}"+r"\\"+" "*24+names[0:10])
    print(names[0:10]+" "*9+r"\\"+f"{names[0:21]}"+r"\\"+" "*6+names[0:10])
    print(names[0:10]+" "*10+r"\\"+f"{names[0:21]}"+r"\\"+" "*5+names[0:10])
    print(names[0:10]+" "*27+r"\\"+f"{names[0:4]}"+r"||"+" "*5+names[0:10])
    print(names[0:10]+" "*27+r"||"+f"{names[0:4]}"+r"||"+" "*5+names[0:10])
    print(names[0:10]+" "*27+r"||"+f"{names[0:4]}"+r"||"+" "*5+names[0:10])
    print(names[0:10]+" "*27+r"//"+f"{names[0:4]}"+r"//"+" "*5+names[0:10])
    print(names[0:10]+" "*6+"---"+" "*17+r"//"+f"{names[0:4]}"+r"//"+" "*6+names[0:10])
    print(names[0:10]+" "*7+r"\\"+f"{names[0:22]}"+r"//"+" "*7+names[0:10])
    print(names[0:10]+" "*8+r"\\"+f"{names[0:20]}"+r"//"+" "*8+names[0:10])
    print(names[0:14]+" "*30+names[0:16])
    print(names[0:60]+"\n")
