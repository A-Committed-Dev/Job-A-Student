import sqlite3

#this function establish a connection to database
def establish_connection():
    # Connecting to sqlite
    # connection object
    connection_obj = sqlite3.connect('users.db')
    # cursor object
    cursor_obj = connection_obj.cursor()
    return connection_obj, cursor_obj

#this function creates tables
def create_tables(cursor_obj):
    # Drop the GEEK table if already exists.
    cursor_obj.execute("DROP TABLE IF EXISTS LOGIN")

    # Creating table
    table = """ CREATE TABLE LOGINS (
                user_name TEXT PRIMARY KEY,
                password TEXT,
                type INTEGER
            ); """
    table1 = """ CREATE TABLE USER_INFO (
                name TEXT,
                desc TEXT,
                img TEXT,
                userid TEXT PRIMARY KEY
            ); """
    table2 = """ CREATE TABLE JOBS (
                employer_name TEXT,
                employer_desc TEXT,
                employer_image TEXT,
                jobname TEXT,
                jobid INTEGER PRIMARY KEY AUTOINCREMENT,
                userid TEXT,
                FOREIGN KEY(userid)REFERENCES LOGIN(user_name)
            ); """

    table3 = """ CREATE TABLE USER_REVIEWED(
                name TEXT,
                jobname TEXT,
                Status INTEGER,
                userid TEXT,
                FOREIGN KEY(userid)REFERENCES LOGIN(user_name)
            ); """
    table4 = """ CREATE TABLE AWAITING(
                student_name TEXT,
                student_desc TEXT,
                student_image TEXT,
                jobname TEXT,
                jobid INTEGER,
                userid TEXT,
                FOREIGN KEY(jobid) REFERENCES JOBS(jobid),
                FOREIGN KEY(userid)REFERENCES LOGIN(user_name)
            ); """
    # list of tables to create
    newlist = [table,table1, table2, table3, table4]
    #itterates list to create tables
    for x in newlist:
        cursor_obj.execute(x)

    print("Table is Ready")

#this function closes conneciton to database
def close_connection(connection_obj):
    # Close the connection
    connection_obj.commit()
    connection_obj.close()

#this function inserts into login table
def insert_to_login(cursor_obj, user_name, password, type):
    cursor_obj.execute('''INSERT INTO LOGINS(
   user_name, password, type) VALUES 
   (?,?,?)''', (user_name, password, type))

#this function gets from login talbe
def get_from_login(cursor_obj, user_name):
    cursor_obj.execute("""SELECT * FROM LOGINS WHERE user_name = ?""", (user_name,))
    return cursor_obj.fetchall()


#this function inserts into user info
def insert_to_user_info(cursor_obj, name, desc, img, user_name):

    #checks if there alerady are information in user info
    if len(get_from_user_info(cursor_obj, user_name)) != 0:
        #updates userinfo
        if get_from_user_info(cursor_obj, user_name)[0][3] == user_name:
            cursor_obj.execute('''UPDATE USER_INFO 
            SET name = ?, desc = ?, img = ? 
            WHERE userid = ?''', (name, desc, img, user_name))
    else:
        #insert info
        cursor_obj.execute('''INSERT INTO USER_INFO(
       name, desc, img, userid) VALUES 
       (?,?,?,?)''', (name, desc, img, user_name))

#this function gets from user info
def get_from_user_info(cursor_obj, user_name):
    cursor_obj.execute("""SELECT * FROM USER_INFO WHERE userid = ?""", (user_name,))
    return cursor_obj.fetchall()

#this function insert into jobs table
def insert_into_jobs(cursor_obj, name, desc, img, jobname, user_name):
    cursor_obj.execute('''INSERT INTO JOBS(
      employer_name, employer_desc, employer_image, jobname, userid) VALUES 
      (?,?,?,?,?)''', (name, desc, img, jobname, user_name))

#this function gets from jobs table
def get_from_jobs(cursor_obj, user_name):
    cursor_obj.execute("""SELECT * FROM JOBS WHERE userid = ?""", (user_name,))
    return cursor_obj.fetchall()

#this function gets from jobs table by job id
def get_from_jobs_by_jobid(cursor_obj, jobid):
    cursor_obj.execute("""SELECT * FROM JOBS WHERE jobid = ?""", (jobid,))
    return cursor_obj.fetchall()

#this function gets everythin from jobs
def get_allfrom_jobs(cursor_obj):
    cursor_obj.execute("""SELECT * FROM JOBS""")
    return cursor_obj.fetchall()

#this function delete from job table
def delete_from_job(cursor_obj, jobid):
    cursor_obj.execute("""DELETE FROM JOBS WHERE jobid = ?""", (jobid,))

#this function insterts into awaiting table
def insert_into_awaiting(cursor_obj, name, desc, img, jobname, jobid, user_name):

    #checks if there is already a value
    if len(get_from_awaiting_by_jobid(cursor_obj, jobid)) != 0:
        # if application already exists do nothing
        if get_from_awaiting_by_jobid(cursor_obj, jobid)[0][4] == jobid:
            print("already applied")
            pass
    else:
        #insert
        cursor_obj.execute('''INSERT INTO AWAITING(
              student_name, student_desc, student_image, jobname, jobid, userid) VALUES 
              (?,?,?,?,?,?)''', (name, desc, img, jobname, jobid, user_name))

#this function gets from awaiting by jobid
def get_from_awaiting_by_jobid(cursor_obj, jobid):
    cursor_obj.execute("""SELECT * FROM AWAITING WHERE jobid = ?""", (jobid,))
    return cursor_obj.fetchall()

#this function gets from awaiting
def get_from_awaiting(cursor_obj, user_name):
    #stores data
    database = []
    #checks for jobid matching username
    for x in get_from_jobs(cursor_obj, user_name):
        #gets users job from awaiting
        cursor_obj.execute("""SELECT * FROM AWAITING WHERE jobid = ?""", (x[4],))
        #add to container
        database.append(cursor_obj.fetchall())

    return database

#this function gets from awaiting by user id
def get_from_awaiting_by_userid(cursor_obj, user_name):
    cursor_obj.execute("""SELECT * FROM AWAITING WHERE userid = ?""", (user_name,))
    return cursor_obj.fetchall()

#this function deletes from awaiting
def delete_from_awaiting(cursor_obj, jobid):
    cursor_obj.execute("""DELETE FROM AWAITING WHERE jobid = ?""", (jobid,))

#this function inserts into reviewed
def insert_into_reviewed(cursor_obj, name ,jobname, status, user_name):
    cursor_obj.execute('''INSERT INTO USER_REVIEWED(
                  name, jobname, status, userid) VALUES 
                  (?,?,?,?)''', (name, jobname, status, user_name))

#this funtion gets everything from reviewed
def get_allfrom_reviewed(cursor_obj):
    cursor_obj.execute("""SELECT * FROM USER_REVIEWED""")
    return cursor_obj.fetchall()

#this function gets from reviewed
def get_from_reviewed(cursor_obj, user_name):
    cursor_obj.execute("""SELECT * FROM USER_REVIEWED WHERE userid = ?""", (user_name,))
    return cursor_obj.fetchall()

