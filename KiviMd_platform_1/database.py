import sqlite3

def establish_connection():
    # Connecting to sqlite
    # connection object
    connection_obj = sqlite3.connect('users.db')
    # cursor object
    cursor_obj = connection_obj.cursor()
    return connection_obj, cursor_obj

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
    newlist = [table,table1, table2, table3, table4]
    for x in newlist:
        cursor_obj.execute(x)

    print("Table is Ready")

def close_connection(connection_obj):
    # Close the connection
    connection_obj.commit()
    connection_obj.close()

def insert_to_login(cursor_obj, user_name, password, type):
    cursor_obj.execute('''INSERT INTO LOGINS(
   user_name, password, type) VALUES 
   (?,?,?)''', (user_name, password, type))

def get_from_login(cursor_obj, user_name):
    cursor_obj.execute("""SELECT * FROM LOGINS WHERE user_name = ?""", (user_name,))
    return cursor_obj.fetchall()



def insert_to_user_info(cursor_obj, name, desc, img, user_name):

    if len(get_from_user_info(cursor_obj, user_name)) != 0:
        if get_from_user_info(cursor_obj, user_name)[0][3] == user_name:
            cursor_obj.execute('''UPDATE USER_INFO 
            SET name = ?, desc = ?, img = ? 
            WHERE userid = ?''', (name, desc, img, user_name))
    else:
        cursor_obj.execute('''INSERT INTO USER_INFO(
       name, desc, img, userid) VALUES 
       (?,?,?,?)''', (name, desc, img, user_name))

def get_from_user_info(cursor_obj, user_name):
    cursor_obj.execute("""SELECT * FROM USER_INFO WHERE userid = ?""", (user_name,))
    return cursor_obj.fetchall()


def insert_into_jobs(cursor_obj, name, desc, img, jobname, user_name):
    cursor_obj.execute('''INSERT INTO JOBS(
      employer_name, employer_desc, employer_image, jobname, userid) VALUES 
      (?,?,?,?,?)''', (name, desc, img, jobname, user_name))

def get_from_jobs(cursor_obj, user_name):
    cursor_obj.execute("""SELECT * FROM JOBS WHERE userid = ?""", (user_name,))
    return cursor_obj.fetchall()

def get_from_jobs_by_jobid(cursor_obj, jobid):
    cursor_obj.execute("""SELECT * FROM JOBS WHERE jobid = ?""", (jobid,))
    return cursor_obj.fetchall()

def get_allfrom_jobs(cursor_obj):
    cursor_obj.execute("""SELECT * FROM JOBS""")
    return cursor_obj.fetchall()

def delete_from_job(cursor_obj, jobid):
    cursor_obj.execute("""DELETE FROM JOBS WHERE jobid = ?""", (jobid,))


def insert_into_awaiting(cursor_obj, name, desc, img, jobname, jobid, user_name):

    if len(get_from_awaiting_by_jobid(cursor_obj, jobid)) != 0:
        if get_from_awaiting_by_jobid(cursor_obj, jobid)[0][4] == jobid:
            print("monkey")
            pass
    else:
        cursor_obj.execute('''INSERT INTO AWAITING(
              student_name, student_desc, student_image, jobname, jobid, userid) VALUES 
              (?,?,?,?,?,?)''', (name, desc, img, jobname, jobid, user_name))

def get_from_awaiting_by_jobid(cursor_obj, jobid):
    cursor_obj.execute("""SELECT * FROM AWAITING WHERE jobid = ?""", (jobid,))
    return cursor_obj.fetchall()

def get_from_awaiting(cursor_obj, user_name):
    for x in get_from_jobs(cursor_obj, user_name):
        cursor_obj.execute("""SELECT * FROM AWAITING WHERE jobid = ?""", (x[4],))
        return cursor_obj.fetchall()

def get_from_awaiting_by_userid(cursor_obj, user_name):
    cursor_obj.execute("""SELECT * FROM AWAITING WHERE userid = ?""", (user_name,))
    return cursor_obj.fetchall()

def delete_from_awaiting(cursor_obj, jobid):
    cursor_obj.execute("""DELETE FROM AWAITING WHERE jobid = ?""", (jobid,))


def insert_into_reviewed(cursor_obj, name ,jobname, status, user_name):
    cursor_obj.execute('''INSERT INTO USER_REVIEWED(
                  name, jobname, status, userid) VALUES 
                  (?,?,?,?)''', (name, jobname, status, user_name))

def get_allfrom_reviewed(cursor_obj):
    cursor_obj.execute("""SELECT * FROM USER_REVIEWED""")
    return cursor_obj.fetchall()

def get_from_reviewed(cursor_obj, user_name):
    cursor_obj.execute("""SELECT * FROM USER_REVIEWED WHERE userid = ?""", (user_name,))
    return cursor_obj.fetchall()

# v = establish_connection()
# delete_from_awaiting(v[1], 1)
# close_connection(v[0])