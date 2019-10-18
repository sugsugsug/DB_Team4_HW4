from userAcc import *
from DBconnection import *

def instructor_menu():
    menu_num = -1

    while (menu_num != '0'):
        print("\n\nWelcome %s"%user_acc.name)
        print("Please select instructor menu")
        print("1) Course Report")
        print("2) Advisee Report")
        print("0) Quit")
        menu_num = input("Enter : ")

        switcher = {
            '0' : quit_menu,
            '1' : print_course_report,
            '2' : print_advisee_report
        }

        selected_func = switcher.get(menu_num, print_wrong)
        selected_func()
    return

def print_course_report():
    #구현
    return

def print_advisee_report():
    #구현
    return 

def quit_menu():
    global user_acc #global 변수를 write할때는 명시를 해야한다
    return_connect(user_acc.conn)
    del user_acc
    return

def print_wrong():
    print("\nWrong menu number!")
    return