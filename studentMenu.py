from userAcc import *
from DBconnection import *

def student_menu():
    menu_num = -1

    while (menu_num != '0'):
        print("\n\nPlease select student menu")
        print("1) Student Report")
        print("2) View Time Table")
        print("0) Quit")
        menu_num = input("Enter : ")

        #call method based on the menu number
        switcher = {
            '0' : quit_menu,
            '1' : print_student_report,
            '2' : print_time_table
        }

        selected_func = switcher.get(menu_num, print_wrong)
        selected_func()
    return

def convertToGP(grade):
    if (grade == "A+"): return 4.3
    elif (grade == 'A '): return 4.0
    elif (grade == "A-"): return 3.7
    elif (grade == "B+"): return 3.3
    elif (grade == 'B '): return 3.0
    elif (grade == "B-"): return 2.7
    elif (grade == "C+"): return 2.3
    elif (grade == 'C '): return 2.0
    elif (grade == "C-"): return 1.7
    elif (grade == "D+"): return 1.3
    elif (grade == 'D '): return 1.0
    elif (grade == "D-"): return 0.7
    else: return 0

def print_student_report():
    ID = user_acc.ID
    name = user_acc.name
    c = user_acc.conn.cursor()
    dept_name = ""
    tot_cred = ""

    #get department name and total credit
    c.execute("SELECT dept_name, tot_cred\
                FROM student\
                WHERE ID = %s and name = %s", (ID, name))
    data = c.fetchone()
    if (data[0] != None):
        dept_name = data[0]
    if (data[1] != None):
        tot_cred = str(data[1])
    print("\nWelcome %s!\nYou are a member of %s\nYou have taken total of %s credits" % (name, dept_name, tot_cred))
    print("\nSemester report")

    #get distinct year and semester in descending order
    c.execute("SELECT distinct year, semester\
                FROM takes\
                WHERE id = %s\
                ORDER BY year DESC, semester", (ID,))
    groups = c.fetchall()

    #for each year and semester, get all courses information
    for group in groups:
        c.execute("SELECT takes.course_id, title, dept_name, grade, credits\
                FROM takes, course\
                WHERE ID = %s and takes.course_id = course.course_id and year = %s and semester = %s", (ID, group[0], group[1]))
        courses = c.fetchall()

        #calculate GPA
        sum = 0.0
        creditSum = 0.0
        isGPAnull = True
        for course in courses:
            if (course[3] != None and course[4] != None):
                sum = sum + convertToGP(course[3]) * float(course[4])
                creditSum = creditSum + float(course[4])
                gpa = sum / creditSum
                isGPAnull = False
    
        #print semester info
        if (isGPAnull == False):
            print("\n%s %s GPA : %f" % (group[0], group[1], gpa))
        else:
            print("\n%s %s GPA : " % (group[0], group[1]))

        #print each course info    
        print("course_id\ttitle\tdept_name\tcredits\tgrade")
        for course in courses:
            title = ""
            dept_name = ""
            grade = ""
            tot_cred = ""
            if (course[1] != None):
                title = course[1]
            if (course[2] != None):
                dept_name = course[2]
            if (course[3] != None):
                grade = course[3]
            if (course[4] != None and isGPAnull == False):
                tot_cred = str(course[4])

            print("%s\t%s\t%s\t%s\t%s" % (course[0], title, dept_name, tot_cred, grade))
    c.close()
    return

def print_time_table():
    c = user_acc.conn.cursor()
    #구현
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
