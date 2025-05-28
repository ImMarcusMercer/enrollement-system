#Imports
from Logic import *
from Menus import *
from Programs import *
from SharedPreferences import *

choice="0"
def setOption():
    newChoice = input("Enter choice: ")
    global choice 
    choice = newChoice

def getOption():
    global choice
    return choice




def Main():
    data = load_data()
    # main()
    # Proposed Project Logic

    #shared preferneces logic here
    isLoggedIn=get_pref("is_logged_in")
    lastuseremail=get_pref("email")
    lastuserpass=get_pref("password")

    if isLoggedIn:
        # print(lastuseremail)
        loading("Signing in")
        signIn(data,lastuseremail,lastuserpass)

    

    while True:
        header("Main Menu")
        showMenu(MAINMENU)
        setOption()

        #Enroll
        if getOption() =="1":
            Enroll(data)
            

        #Sign-in
        elif getOption() == "2":
            header("Sign In")
            email = input("Enter email: ").strip()
            password = input("Enter password: ").strip()
            signIn(data,email,password)
            

            

        #Apply
        elif getOption()=="3":
            pass

        elif getOption() == "4":
            loading("Exiting Program")
            break
        else:
            print("Invalid Input!")
            continue


if __name__ == "__main__":
    Main()