from kivy.core.window import Window
from tkinter import *  # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp, sp
from kivy.properties import partial
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField

from custom_classes import *
from database import *
from template_generator import *

# makes kivy use mouse input and disables multitouch
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

#this class is the custom cards that contains jobs.
class CardItem(MDCard, RoundedRectangularElevationBehavior):
    #this method calls the card change screen method from the main screen.
    def card_change_screen(self, idd, screen_name):
        app.main_Screen.card_change_screen(idd, screen_name)

    #this method removes a card from the joblist
    def remove(self, idd):
        try:
            # opens database connection
            val = establish_connection()
            # removes job by jobidd from jobs table
            delete_from_job(val[1], idd)
            # closes connection
            close_connection(val[0])

            # removes cards, and content screens.
            app.main_Screen.ids.screen_manager.get_screen("joblist").ids.content_view.clear_widgets()
            app.main_Screen.ids.screen_manager.get_screen("joblist").ids.content.clear_widgets()
            # recreates cards and content screens.
            app.main_Screen.populate_joblist()
        except:
            pass

    #this method lets students apply to a job
    def add(self, idd):
        try:
            val = establish_connection()
            # gets the jobname from id
            database = get_from_jobs_by_jobid(val[1], idd)
            #gets the students information
            database_userinfo = get_from_user_info(val[1], app.current_account)
            #inserts the job name from jobdatbase,
            # and the students information from user info into the awawiting database.
            insert_into_awaiting(val[1],
                                 database_userinfo[0][0],
                                 database_userinfo[0][1],
                                 database_userinfo[0][2],
                                 database[0][3],
                                 idd, app.current_account)
            # closes connection
            close_connection(val[0])
            Mainapp.show_alert_box(Mainapp(), "Succesfully applied for job")
        except:
            Mainapp.show_alert_box(Mainapp(), "No Acount info")

    # this method moves data from awaiting into reviewd
    def move(self, idd, status):
        try:
            val = establish_connection()
            # gets data from awating by jobid
            database = get_from_awaiting_by_jobid(val[1], idd)
            database_userinfo = get_from_user_info(val[1], app.current_account)

            # inserts into employer rewviewed, student name,jobname, and stutus
            insert_into_reviewed(val[1], database_userinfo[0][0], database[0][3], status, database[0][5])
            # inserts into student rewviewed, employername,jobname, and stutus
            insert_into_reviewed(val[1], database[0][0], database[0][3], status, app.current_account)
            #removes the student from awaiting
            delete_from_awaiting(val[1], idd)
            #checks if student have been accepted
            if status == 1:
                #removes the job if accepted
                delete_from_job(val[1], idd)
                Mainapp.show_alert_box(Mainapp(), "Accepted application")

            #checks if student have been denied
            if status == 0:
                Mainapp.show_alert_box(Mainapp(), "Denied application")
            # closes connection
            close_connection(val[0])
            #removes cards, and content screens.
            app.main_Screen.ids.screen_manager.get_screen("awaiting").ids.content.clear_widgets()
            app.main_Screen.ids.screen_manager.get_screen("awaiting").ids.content_view.clear_widgets()
            # recreates cards and content screens.
            app.main_Screen.populate_awaiting()
        except:
            pass

#this class is for the jobs screen.
class Screen_jobs(Screen):
    #this runs when job screen is entered
    def on_enter(self, *args):
        #removes cards, and content screens.
        app.main_Screen.ids.screen_manager.get_screen("joblist").ids.content_view.clear_widgets()
        app.main_Screen.ids.screen_manager.get_screen("joblist").ids.content.clear_widgets()
        #recreates cards and content screens.
        app.main_Screen.populate_joblist()





#this class stores methods relevant to the account screen.
class Screen_account(Screen):
    #this method borrows tkinter file picker dialog to get file path
    def pick_file(self):
        Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
        filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
        #sets image on screen to file path
        self.ids.img.source = filename

    #this method save account details.
    def save_account(self):
        try:
            #checks the length of the desc
            if self.password_length(self.ids.desc.text) > 600:
                #plays sound
                sound = SoundLoader.load("sfx/Error.mp3")
                sound.play()
                Mainapp.show_alert_box(Mainapp(), "desc too long")
            else:
                # opens database connection
                val = establish_connection()
                # inserts values into user info table
                database = insert_to_user_info(val[1], self.ids.name.text, self.ids.desc.text, self.ids.img.source, app.current_account)
                # closes connection
                close_connection(val[0])
        except:
            pass

    #this method is run when the screen is entered
    def on_enter(self, *args):
        try:
            #reads the database for account info and displays on gui
            # opens database connection
            val = establish_connection()
            # gets user information from database
            database = get_from_user_info(val[1], app.current_account)
            # closes connection
            close_connection(val[0])

            #sets the fields on the screen to the values from the database
            self.ids.name.text = database[0][0]
            self.ids.desc.text = database[0][1]
            self.ids.img.source = database[0][2]
        except:
            pass

    #this method gets the char length of a string
    def password_length(self, password):
        # using a list comprehension we can split
        # string at all chars
        char_lsit = [char for char in password]
        # returns length of list
        return len(char_lsit)

#this calss is the student awiaiting screen, this is where the user can see the applied jobs.
#and delete them
class Screen_waiting_student(Screen):
    index = 0

    #this method creates table with values from awaiting database
    def create_table(self):

        # reads the database for account info and displays on gui
        # opens database connection
        val = establish_connection()
        # jobs from awaiting by user id
        database = get_from_awaiting_by_userid(val[1], app.current_account)

        #database for changed values
        new_database = []
        for z in database:
            #get job information from, jobid we got from the awaiting database
            database_jobs = get_from_jobs_by_jobid(val[1], z[4])

            for x in database_jobs:
                new_list = []#container for values
                new_list.append(x[0])
                new_list.append(x[3])
                new_list.append("Pending...")
                new_list.append(x[4])
                #delet icon to the end of the table, this is the button we need to hit.
                new_list.append(("delete-circle", [0, 0, 0, 1], ""))
                #adds container to list
                new_database.append(new_list)




        # closes connection
        close_connection(val[0])


        # Initialization of datatable
        self.table = MDDataTable(
            pos_hint={"center_y": 0.5, "center_x": 0.5},
            size_hint=(0.95, 0.75),
            check=False,
            rows_num=1000,
            use_pagination=False,
            column_data=[
                ("Employer", self.width / 25),
                ("Job", self.width/25),
                ("Status", self.width/25),
                ("ID", self.width / 25),
                ("Delete", self.width / 25),
            ],
            row_data= new_database)

        # Binds the method on_row_press to the datatable
        self.table.bind(on_row_press=self.row_presses)

        self.add_widget(self.table)

    # Creates datatable when the screen is active
    def on_enter(self):
        self.create_table()

    # Method that gets the instance of the row pressed
    def row_presses(self, instance_table, instance_row):
        try:
            #checks if table is not empty
            if len(self.table.row_data) != 0:
                z = 4 # start index of first button
                new_list = [] #container for values
                #creates index for buttons depinding on the amount of rows
                for x in range(0, len(self.table.row_data)):
                    #adds index to list
                    new_list.append(z)
                    #gets next index
                    z += 5
                #checks if pressed row is in the list
                if instance_row.index in new_list:
                    #removes row from table by getting the button from the index list
                    # and fetches the id from the table at index 3
                    self.remove(self.table.row_data[new_list.index(instance_row.index)][3])
        except:
            pass



    #method to remove element from table
    def remove(self, idd):
        try:
            # reads the database for account info and displays on gui
            # opens database connection
            val = establish_connection()
            # removes id from database
            database = delete_from_awaiting(val[1], idd)
            # closes connection
            close_connection(val[0])
            #all data from table
            self.clear_widgets()
            #creates new table
            self.create_table()
        except:
            pass


#screen for employer to sort applied students
class Screen_waiting_employer(Screen):
    #when screen is entered loads cards
    def on_enter(self, *args):
        #clears card content view
        app.main_Screen.ids.screen_manager.get_screen("awaiting").ids.content_view.clear_widgets()
        # clears card from screen
        app.main_Screen.ids.screen_manager.get_screen("awaiting").ids.content.clear_widgets()
        #recreates cards
        app.main_Screen.populate_awaiting()

#screen that stores the reviewed table.
#houses function to create table from database
class Screen_reviewed(Screen):
    def create_table(self):
        try:
            # reads the database for account info and displays on gui
            # opens database connection
            val = establish_connection()
            # gets from the reviewed table by username
            database = get_from_reviewed(val[1], app.current_account)
            # closes connection
            close_connection(val[0])

            #creates empty list to store a new database
            new_database = []
            for x in database:
                #container for data from the database
                new_list = []

                #gets student or employer name
                new_list.append(x[0])

                #gets jobname
                new_list.append(x[1])
                #checks status if 1 accepted if 0 denied
                if x[2] == 1:
                    new_list.append(("checkbox-marked-circle", [0, 100, 0, 1], "Accepted"))
                # checks status if 1 accepted if 0 denied
                if x[2] == 0:
                    new_list.append(("close-circle", [50, 0, 0, 1], "Denied"))

                #adds container to database
                new_database.append(new_list)
        except:
            pass

        # Initialization of datatable
        self.table = MDDataTable(
            pos_hint={"center_y": 0.5, "center_x": 0.5},
            size_hint=(0.95, 0.75),
            check=False,
            rows_num=1000,
            use_pagination=False,
            column_data=[
                ("name", self.width / 14),
                ("Job", self.width/14),
                ("Status", self.width/25),
            ],
            row_data=new_database
        )
        self.add_widget(self.table)

    # Creates datatable when the screen is active
    def on_enter(self):
        self.create_table()


#this class is the main screen which is accesed after loggin in.
#this i the hub for the methods for controlling the creation of cards
class Screen_main(Screen):

    #gets the active button in the toolbar
    #changes screen to match name
    def rail_switch_screen(self, instance_navigation_rail, instance_navigation_rail_item):
        self.ids.screen_manager.current = (
            instance_navigation_rail_item.text.lower()
        )

    def create_content_screens(self, idd, screen_name, user_name, user_img, user_job, user_desc):
        #incases values as string
        idd_string = "'" + str(idd) + "'"
        user_name_string = "'" + user_name + "'"
        user_img_string = "'" + user_img + "'"
        user_job_string = "'" + user_job + "'"
        user_desc_string = "'" + user_desc + "'"

        #loads formatted template to builder
        content = Builder.load_string("""Screen:
        MDBoxLayout:
                line_color: utils.get_color_from_hex('#ff9800')
                line_width: 1.4
                size_hint: 1, 1
                orientation: "vertical"
                MDBoxLayout:
                        line_color: utils.get_color_from_hex('#ff9800')
                        line_width: 1.4
                        size: self.width, self.height
                        MDBoxLayout:
                                padding: 10
                                line_color: utils.get_color_from_hex('#ff9800')
                                line_width: 1.4
                                size: self.width, self.height
                                orientation: "vertical"
                                MDBoxLayout:

                                        Label:  
                                                text: "Name:"
                                                color: 0,0,0
                                                size: self.width,self.height
                                        Label:  
                                                text: {}
                                                color: 0,0,0
                                                size: self.width,self.height

                                MDBoxLayout:

                                        Label:
                                                text: "Job:"
                                                color: 0,0,0
                                                size: self.width,self.height
                                        Label:
                                                text: {}
                                                color: 0,0,0
                                                size: self.width,self.height
                        MDBoxLayout:
                                padding: 10
                                line_color: utils.get_color_from_hex('#ff9800')
                                line_width: 1.4
                                size: self.width, self.height
                                FitImage:
                                        source: {}
                MDBoxLayout:
                        line_color: utils.get_color_from_hex('#ff9800')
                        line_width: 1.4
                        size: self.width, self.height
                        padding: 40
                        MDTextField:
                                text: {}
                                text_color_normal: 0,0,0
                                text_color_focus: 0,0,0
                                multiline: True
                                disabled: True
                                size: 0.5,1 
               """.format(user_name_string,
                          user_job_string,
                          user_img_string,
                          user_desc_string)) #formats the template with paramters

        try:
            # checks if screen already exists
            if self.ids.screen_manager.get_screen(screen_name)\
                    .ids.content_view.get_screen(idd_string):
                #adds content to exsisting screen
                self.ids.screen_manager.get_screen(screen_name)\
                    .ids.content_view.get_screen(idd_string).add_widget(content)
                return
        except:
            pass
        try:
            #creates a screen with id from args
            new_screen = Screen(name=idd_string)
            # adds content to new screen
            new_screen.add_widget(content)
        except:
            pass
        #adds the new screen to the card content view
        self.ids.screen_manager.get_screen(screen_name)\
            .ids.content_view.add_widget(new_screen)


    #this method changes the card content screen
    def card_change_screen(self, idd, screen_name):
        idd_string = "'" + str(idd) + "'"
        #sets the contentscreen by card
        self.ids.screen_manager.get_screen(screen_name).ids.content_view.current = idd_string

    #this method renders cards and adds them to the screen
    def render_cards(self, idd, screen_name, value, user_name, user_subtitle, user_img, jobid):
        screen_name_string = "'" + str(screen_name) + "'"
        try:
            #cecks for the wanted type of card by the type paramter
            if value == 0:
                # loads card to builder from paramters
                x = Builder.load_string(create_card_student(
                    user_name,
                    user_subtitle,
                    user_img,
                    # function need to be passed as a string so we use format to change args
                    "root.card_change_screen({}, {})".format(idd, screen_name_string),
                    "root.add({})".format(jobid)),
                    filename="cards.kv")
            # cecks for the wanted type of card by the type paramter
            if value == 1:
                # loads card to builder from paramters
                x = Builder.load_string(create_card_employer_jobs(
                    user_name,
                    user_subtitle,
                    user_img,
                    #function need to be passed as a string so we use format to change args
                    "root.card_change_screen({}, {})".format(idd, screen_name_string),
                    "root.remove({})".format(jobid)),
                    filename="cards.kv")
            # cecks for the wanted type of card by the type paramter
            if value == 2:
                #loads card to builder from paramters
                x = Builder.load_string(create_card_employer_awaiting(
                    user_name,
                    user_subtitle,
                    user_img,
                    # function need to be passed as a string so we use format to change args
                    "root.card_change_screen({}, {})".format(idd, screen_name_string),
                    "root.move({},{})".format(jobid, 1),
                    "root.move({},{})".format(jobid, 0)),
                    filename="cards.kv")

            #add card to screen
            self.ids.screen_manager.get_screen(screen_name)\
                .ids.content.add_widget(CardItem())
            #unload card from the builder
            x = Builder.unload_file("cards.kv")
        except:
            pass

    # this method creates, a new job. and adds it to the database
    # and updates the screen
    def create_job(self):
        #gets the job description from textfield
        jobname = app.main_Screen.ids.screen_manager.get_screen("joblist").ids.Textfield.text

        #checks if the textfield is empty
        if jobname == "":
            Mainapp.show_alert_box(Mainapp(), "Need a job title")
            return

        try:
            # reads the database for account info and displays on gui
            # opens database connection
            val = establish_connection()
            # gets user information
            database = get_from_user_info(val[1], app.current_account)
            #checcks if database is not empty
            #if empty ask to create info for database.
            if len(database) != 0:
                insert_into_jobs(val[1],database[0][0], database[0][1], database[0][2], jobname, app.current_account)
            else:
                Mainapp.show_alert_box(Mainapp(), "No account info")
                close_connection(val[0])
                return
            # closes connection
            close_connection(val[0])
        except:
            pass

        #shows pop up with messeage
        Mainapp.show_alert_box(Mainapp(), "succesfully created a job")
        #clears the text field and screen and cards
        app.main_Screen.ids.screen_manager.get_screen("joblist").ids.Textfield.text = ""
        app.main_Screen.ids.screen_manager.get_screen("joblist").ids.content.clear_widgets()
        #clears content views
        app.main_Screen.ids.screen_manager.get_screen("joblist").ids.content_view.clear_widgets()
        #recreate the cards
        self.populate_joblist()


    # this function loads data from the job database.
    # and create cards on the job screen.
    def populate_joblist(self):
        try:

            if app.acoount_type == 0:
                # reads the database for account info and displays on gui
                # opens database connection
                val = establish_connection()
                # save gets username
                database = get_allfrom_jobs(val[1])
                # closes connection
                close_connection(val[0])


            if app.acoount_type == 1:
                # reads the database for account info and displays on gui
                # opens database connection
                val = establish_connection()
                # save gets username
                database = get_from_jobs(val[1], app.current_account)
                # closes connection
                close_connection(val[0])
            print(database)

            z = 0 # id for screens
            # iterates everything from database
            for x in database:
                app.main_Screen.create_content_screens(z, "joblist", x[0], x[2], x[3], x[1])
                app.main_Screen.render_cards(z, "joblist", app.acoount_type, x[0], x[3], x[2], x[4])
                z +=1
        except:
            pass


    #this function loads data from the awaiting database for the employer.
    #and create cards on the awaiting screen.
    def populate_awaiting(self):
        try:
            # reads the database for account info and displays on gui
            # opens database connection
            val = establish_connection()
            # save gets username
            database = get_from_awaiting(val[1], app.current_account)
            print(database)
            # closes connection
            close_connection(val[0])

            z = 0 # id for screens
            #iterates everything from database
            for x in database:
                print(x[0])
                app.main_Screen.create_content_screens(z, "awaiting", x[0][0], x[0][2], x[0][3], x[0][1])
                app.main_Screen.render_cards(z, "awaiting", 2, x[0][0], x[0][3], x[0][2], x[0][4])
                z += 1
        except:
            pass


    #this method is loaded when you enter the main screen after login
    def on_enter(self):
        #Creates screens for the toolbar.
        app.main_Screen.ids.screen_manager.clear_widgets()
        app.main_Screen.ids.screen_manager.add_widget(Screen_jobs(name="joblist"))
        app.main_Screen.ids.screen_manager.add_widget(Screen_reviewed(name="reviewed"))
        app.main_Screen.ids.screen_manager.add_widget(Screen_account(name="account"))

        # checks if you are a student
        if app.acoount_type == 0:
            # disables the add job button
            app.main_Screen.ids.screen_manager.get_screen("joblist").ids.button.disabled = True
            app.main_Screen.ids.screen_manager.get_screen("joblist").ids.Textfield.disabled = True

            #loads student layout
            Builder.load_file("layouts/waiting_student_layout.kv")
            app.main_Screen.ids.screen_manager.add_widget(Screen_waiting_student(name="awaiting"))


        # checks if you are an employer
        if app.acoount_type == 1:
            # enable the add job button
            app.main_Screen.ids.screen_manager.get_screen("joblist").ids.button.disabled = False
            app.main_Screen.ids.screen_manager.get_screen("joblist").ids.Textfield.disabled = False

            # loads employer layout
            Builder.load_file("layouts/waiting_employer_layout.kv")
            app.main_Screen.ids.screen_manager.add_widget(Screen_waiting_employer(name="awaiting"))

            #renders cards for employer
            self.populate_awaiting()





# this is the login screen class. which provides the code
# for the login_layout.kv file.
class Screen_login(Screen):
    # this varible is for the account type.
    type = None

    # this method gets the users credentials from the fields
    def get_credentials(self):
        # returns texts from fields by searching for fields ids
        return self.ids.Username.text, self.ids.Upassword.text

    # this method sets the varible type to the account type
    # from the check boxes
    def set_type(self, type):
        self.type = type

    # this method returns the account type
    def get_type(self):
        return self.type

    # this method reqeust a login to the app.
    def request_login(self, username, password, type):

        try:
            # opens database connection
            val = establish_connection()
            # save gets username
            database = get_from_login(val[1], username)
            # closes connection
            close_connection(val[0])
        except:
            pass

        #checks if textfields is empty
        if username == "" or password == "":
            sound = SoundLoader.load("sfx/Error.mp3")
            sound.play()
            Mainapp.show_alert_box(Mainapp(), "Fields cant be empty")
            self.clear_fields()
            return False

        try:
            #makes sure that database isnt empty
            if len(database) != 0:
                # checks if all credentials match database and returns true
                if username == database[0][0] and password == database[0][1] and type == database[0][2]:
                    app.change_screen("main")
                    self.clear_fields()

                    #sets account varibles
                    app.current_account = username
                    app.acoount_type = type

                    return True

                else:
                    # if not
                    # clears fields. plays angry sound, and shows an alert box, last function returns false
                    self.clear_fields()
                    sound = SoundLoader.load("sfx/Error.mp3")
                    sound.play()
                    Mainapp.show_alert_box(Mainapp(), "You did something wrong...")
                    return False
        except:
            pass

    # this method clears all text fields by setting
    # the value to an empty string
    def clear_fields(self):
        self.ids.Username.text = ""
        self.ids.Upassword.text = ""







# this is the signup screen class. which provides the code
# for the signup_layout.kv file.
class Screen_signup(Screen):
    # this varible is for the account type.
    type = None

    # this method gets the users credentials from the fields
    def get_credentials(self):
        # returns texts from fields by searching for fields ids
        return self.ids.Username.text, self.ids.Upassword.text, self.ids.Urepeat.text

    # this method sets the varible type to the account type
    # from the check boxes
    def set_type(self, type):
        self.type = type

    # this method returns the account type
    def get_type(self):
        return self.type

    # this method request a signup to the app.
    # TO DO: make a sql database for users.
    def request_signup(self, username, password, rpassword,  type):
        # loads the sound error.mp3 as variable sound
        sound = SoundLoader.load("sfx/Error.mp3")

        #opens database connection
        val = establish_connection()
        #save gets username
        database = get_from_login(val[1], username)
        #closes connection
        close_connection(val[0])





        # checks that an account type was chosen.
        # if  plays angry sound. and shows alert
        # last returns false
        if type is None:
            sound.play()
            Mainapp.show_alert_box(Mainapp(), "You need to pick either employee or student")
            self.clear_fields()
            return False

        # checks if fields are empty.
        # if  plays angry sound. and shows alert
        # last returns false
        elif username == "" or password == "" or rpassword == "":
            sound.play()
            Mainapp.show_alert_box(Mainapp(), "Fields cant be empty")
            self.clear_fields()
            return False

        # checks if password is longer than 12.
        # if  plays angry sound. and shows alert
        # last returns false
        elif self.password_length(password) > 12:
            sound.play()
            self.clear_password_fields()
            Mainapp.show_alert_box(Mainapp(), "Password's are longer than 12 characters")
            return False



        # checks if passwords are not the same.
        # if plays angry sound. and shows alert
        # last returns false
        elif password != rpassword:
            sound.play()
            self.clear_password_fields()
            Mainapp.show_alert_box(Mainapp(), "Password's are not the same")
            return False

        # if database is empty, allows to proceed
        elif len(database) != 0:
            if username == database[0][0]:
                sound.play()
                self.clear_password_fields()
                Mainapp.show_alert_box(Mainapp(), "User already exists")

        # if none of the conditions are met an account is successfully
        # uploaded to the data base, shows messages to user to confirm
        # that an account was created.
        # last returns account to the data base.
        # TO DO: added user to sql database instead of returning list.
        else:
            print("success")
            newlist = [username, password, type]
            Mainapp.show_alert_box(Mainapp(), "Successfully signed up")
            #opens database connection
            val = establish_connection()
            #saves account details to LOGINS table
            insert_to_login(val[1], username, password, type)
            #closes connenction
            close_connection(val[0])

            return True

    # checks the length of a string
    def password_length(self, password):
        # using a list comprehension we can split
        # string at all chars
        char_lsit = [char for char in password]
        # returns length of list
        return len(char_lsit)

    # clears only the password fields.
    def clear_password_fields(self):
        # sets fields to empty string by their ids
        self.ids.Upassword.text = ""
        self.ids.Urepeat.text = ""

    # this method clears all text fields by setting
    # the value to an empty string
    def clear_fields(self):
        # sets fields to empty string by their ids
        self.ids.Username.text = ""
        self.ids.Upassword.text = ""
        self.ids.Urepeat.text = ""











# this is the main class for the gui
# this is where we build the gui, sets
# themes and more.
class Mainapp(MDApp):
    # stores the kivydialog / alertbox
    dialog = None
    # stores the screenManager class
    sm = ScreenManager()

    #stores the mainscreen
    main_Screen = None

    # stores the logged in user
    current_account = None
    # stores wether account is student or employer
    acoount_type = None

    # this method is run first, here we put stuff like our theme and color choice.
    # we also put our screens and load the .kv files.
    def build(self):
        # try creating database
        try:
            # opens database connection
            val = establish_connection()
            # creates database
            create_tables(val[1])
            # closes connection
            close_connection(val[0])
        except:
            print("database already exists")


        # sets the color themes for the whole app.
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Orange"

        # loads the .kv files
        Builder.load_file("layouts/login_layout.kv")
        Builder.load_file("layouts/signup_layout.kv")
        Builder.load_file("layouts/main_layout.kv")
        Builder.load_file("layouts/joblist_employer.kv")
        Builder.load_file("layouts/account_layout.kv")
        Builder.load_file("layouts/waiting_employer_layout.kv")

        # adds screens to the screen manager.
        self.main_Screen = Screen_main(name="main")
        self.sm.add_widget(self.main_Screen)
        self.sm.add_widget(Screen_login(name="login_screen"))
        self.sm.add_widget(Screen_signup(name="signup_screen"))



        # sets the start up screen
        self.sm.current = "login_screen"

        # returns screenmanager which is what is displayed
        return self.sm

    # this method is used to change the screens
    def change_screen(self, name):
        self.sm.current = name
        self.main_Screen.ids.screen_manager.get_screen("joblist").ids.content.clear_widgets()



    # when this method is called it shows an alert box
    # with the message added as a parameter.
    def show_alert_box(self, message):
        # sets color theme for the alert.
        # for some reseon they are not affected by
        # the global theme
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Orange"

        # checks if there is no box already
        if not self.dialog:
            # creates an alertbox with the message
            self.dialog = MDDialog(
                text=message,
                # adds buttons to the alertbox
                buttons=[
                    # button when clicked calls the hide_arlarm_box method
                    MDFlatButton(
                        text="Close", text_color=self.theme_cls.primary_color, on_press = self.hide_arlarm_box
                    ),
                    # button when clicked calls the hide_arlarm_box method
                    MDRectangleFlatButton(
                        text="OK", text_color=self.theme_cls.primary_color, on_press = self.hide_arlarm_box
                    )
                ]
            )
        # shows alertbox
        self.dialog.open()

    # removes the alert box
    def hide_arlarm_box(self, obj):
        self.dialog.dismiss()

    # this method forces the window size to be the size of,
    # width and height parameter.
    def force_window(self, width, height, *largs):

        # checks if either width or height of window
        # is larger than the parameters
        if width > Window.size[0] or height > Window.size[1]:
            # if forces window size to paramters
            Window.size = (width, height)
            # shows alertbox
            self.show_alert_box("Cant resize beyond this point.")

    # this method runs after build
    def on_start(self):
        #maximizes the window
        Window.maximize()
        # this runs a schedueld task, to force the windows size.
        # all the time
        Clock.schedule_interval(partial(self.force_window, 800, 600), 0)



# runs the program
if __name__ == "__main__":
    app = Mainapp()
    app.run()
