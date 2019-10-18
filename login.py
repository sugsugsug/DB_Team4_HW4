from userAcc import *
from DBconnection import *
from studentMenu import *
from instructorMenu import *

def login():
    print ("Welcome to School Database System!")
    #if the user is not connected to the database
    while (user_acc.conn is None):
        print("Please sign in")
        ID = input("%s:"%"ID")
        name = input("%s:"%"Name")
        auth(ID, name)
    switcher = {
        0 : student_menu,
        1 : instructor_menu
    }

    #call menu based on the role of the user
    role_menu = switcher.get(user_acc.role)
    role_menu()

#check if there is a record in student with ID, name
def isStudent(ID, name, cursor):
    cursor.execute("SELECT ID, name\
                FROM student\
                WHERE ID = %s and name = %s", (ID, name))
    data = cursor.fetchone()
    if data != None:
        return True
    else:
        return False

#check if there is a record in instructor with ID, name
def isInstructor(ID, name, cursor):
    cursor.execute("SELECT ID, name\
                FROM instructor\
                WHERE ID = %s and name = %s", (ID, name))
    data = cursor.fetchone()
    if data != None:
        return True
    else:
        return False

#check if the user is one of the member in the university
def auth(ID, name):
    #connect to the database
    user_connect = get_connect()
    #get the cursor
    c = user_connect.cursor()
    if (isStudent(ID, name, c)):
         #if the user is student, set user account role, conn
         user_acc.set_attrs(ID, name, 0, user_connect)
         return

    elif (isInstructor(ID, name, c)):
        #if the user is instructor, set user account role, conn
        user_acc.set_attrs(ID, name, 1, user_connect)
        return
    else:
        print("\nWrong authentication!")
        return_connect(user_connect)
        return

   


   
   
