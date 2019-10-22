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
                ORDER BY year DESC,field(semester,'Winter','Fall','Summer','Spring')", (ID,))
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
            #only calculate gpa if credit and gpa is not null
            if (course[3] != None and course[4] != None):
                sum = sum + convertToGP(course[3]) * float(course[4])
                creditSum = creditSum + float(course[4])
                gpa = sum / creditSum
                isGPAnull = False
    
        #print semester info
        if (isGPAnull == False):
            print("\n%s %s GPA : %f" % (group[0], group[1], gpa))
        else:
            #when gpa is null, don't print gpa
            print("\n%s %s GPA : " % (group[0], group[1]))

        #print each course info    
        print("course_id\ttitle\tdept_name\tcredits\tgrade")
        for course in courses:
            title = ""
            dept_name = ""
            grade = ""
            tot_cred = ""
            #check for null
            if (course[1] != None):
                title = course[1]
            if (course[2] != None):
                dept_name = course[2]
            if (course[3] != None):
                grade = course[3]
            #set to null if grade or credit is None
            if (course[4] != None and course[3] != None):
                tot_cred = str(course[4])

            print("%s\t%s\t%s\t%s\t%s" % (course[0], title, dept_name, tot_cred, grade))
    c.close()
    return

def print_time_table():
    ID = user_acc.ID
    c = user_acc.conn.cursor()
    
    c.execute("SELECT distinct year, semester\
    FROM student natural join takes\
    WHERE ID = '%s'\
    ORDER BY year desc, field(semester,'Winter','Fall','Summer','Spring');" % (ID,))
        # 최근 순으로 정렬
    semes = c.fetchall()
    
    print("Please select semester to view")
    i=0
    for each in semes:
       i=i+1
       print("%d) %s %s" % (i,each[0],each[1])) 
    try:
        j = int(input())
        if(j<1 or j>i):
            raise Exception("range is not correct!")
    except Exception as e:
        c.close()
        print(e)
        return
    # if range isn't correct or invalid input comes, print Exception and return
    
    print("\nTime Table\n")
    
    c.execute("SELECT course_id,title,day,start_hr,start_min,end_hr,end_min\
            FROM course natural join \
                (SELECT * from time_slot natural join \
                    (SELECT course_id, time_slot_id \
		            from takes natural join section \
		            where ID = '%s' and year='%s' and semester='%s')as T)as TT;" % (ID,semes[j-1][0],semes[j-1][1]))
    
    # ID, year, semester에 맞는 time_slot을 가져오고, Title 알기 위해 course와 조인 후, 출력
    
    tt = c.fetchall()
    
    print("%10s\t%40s\t%15s\t%10s\t%10s" %("course_id","title","day","start_time","end_time"))
    for i in tt:
        print("%10s\t%40s\t%15s\t%10s : %s\t%10s : %s" % i )
    
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

