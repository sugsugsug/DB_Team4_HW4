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

    ID = user_acc.ID
    name = user_acc.name
    c = user_acc.conn.cursor()

    #get all advisees of the instructor
    c.execute("SELECT DISTINCT S.ID, S.name, S.dept_name, S.tot_cred\
                FROM advisor as A, student as S\
                WHERE A.i_ID = %s and A.s_ID = S.ID", (ID,))
    
    adviseelist = c.fetchall()

    #print each advisee info    
    print("ID\tname\tdept_name\ttot_cred")
    for advisee in adviseelist:
        advisee_id = ""
        advisee_name = ""
        advisee_dept_name = ""
        advisee_tot_cred = ""

        #check for null
        if (advisee[0] != None):
            advisee_id = advisee[0]
        if (advisee[1] != None):
            advisee_name = advisee[1]
        if (advisee[2] != None):
            advisee_dept_name = advisee[2]
        if (advisee[3] != None):
            advisee_tot_cred = str(advisee[3])

        print("%s\t%s\t%s\t%s" % (advisee_id, advisee_name, advisee_dept_name, advisee_tot_cred))
        
    c.close()
    return 

def quit_menu():
    global user_acc #global 변수를 write할때는 명시를 해야한다
    return_connect(user_acc.conn)
    del user_acc
    return

def print_wrong():
    print("\nWrong menu number!")
    return