
def showMenu(listofMenu:list):
    count =1
    for items in listofMenu:
        print(f"[{count}] {items}")
        count +=1

MAINMENU=["Enroll", "Sign-in", "Faculty Login","Exit Program"]

STUDENTDASHBOARD=["Show C.O.R", "Show Subjects","Account","Logout"]

# showMenu(MAINMENU)