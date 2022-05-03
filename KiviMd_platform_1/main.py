from kivy.core.window import Window
from tkinter import *  # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import partial
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog

from custom_classes import *
from database import *
from template_generator import *

# makes kivy use mouse input and disables multitouch
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

class CardItem(MDCard, RoundedRectangularElevationBehavior):
    def test(self, idd, screen_name):
        app.main_Screen.test(idd, screen_name)

    def remove(self, idd):
        # opens database connection
        val = establish_connection()
        # save gets username
        delete_from_job(val[1], idd)
        # closes connection
        close_connection(val[0])
        app.main_Screen.ids.screen_manager.get_screen("joblist").ids.content.clear_widgets()
        app.main_Screen.ids.screen_manager.get_screen("joblist").ids.content_view.clear_widgets()
        app.main_Screen.populate_joblist()

    def add(self, idd):
        try:
            val = establish_connection()
            # save gets username
            database = get_from_jobs_by_jobid(val[1], idd)
            database_userinfo = get_from_user_info(val[1], app.current_account)
            insert_into_awaiting(val[1], database_userinfo[0][0], database_userinfo[0][1], database_userinfo[0][2], database[0][3], idd, app.current_account)
            # closes connection
            close_connection(val[0])
            Mainapp.show_alert_box(Mainapp(), "Succesfully applied for job")
        except:
            Mainapp.show_alert_box(Mainapp(), "No Acount info")

    def move(self, idd, status):
        val = establish_connection()
        # save gets username
        database = get_from_awaiting_by_jobid(val[1], idd)
        insert_into_reviewed(val[1], database[0][0], database[0][3], status, database[0][5])
        insert_into_reviewed(val[1], database[0][0], database[0][3], status, app.current_account)
        delete_from_awaiting(val[1], idd)
        if status == 1:
            delete_from_job(val[1], idd)
            Mainapp.show_alert_box(Mainapp(), "Accepted application")
            
        if status == 0:
            Mainapp.show_alert_box(Mainapp(), "Denied application")
        # closes connection
        close_connection(val[0])
        app.main_Screen.ids.screen_manager.get_screen("awaiting").ids.content.clear_widgets()
        app.main_Screen.populate_awaiting()


class Screen_jobs(Screen):
    def on_enter(self, *args):
        app.main_Screen.ids.screen_manager.get_screen("joblist").ids.content_view.clear_widgets()
        app.main_Screen.ids.screen_manager.get_screen("joblist").ids.content.clear_widgets()
        app.main_Screen.populate_joblist()






class Screen_account(Screen):
    def pick_file(self):
        Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
        filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
        self.ids.img.source = filename

    def save_account(self):
        if self.password_length(self.ids.desc.text) > 600:
            print("sur")
            #TODO bliv sur
        else:
            # opens database connection
            val = establish_connection()
            # save gets username
            database = insert_to_user_info(val[1], self.ids.name.text, self.ids.desc.text, self.ids.img.source, app.current_account)
            # closes connection
            close_connection(val[0])


    def on_enter(self, *args):
        try:
            #reads the database for account info and displays on gui
            # opens database connection
            val = establish_connection()
            # save gets username
            database = get_from_user_info(val[1], app.current_account)
            # closes connection
            close_connection(val[0])

            self.ids.name.text = database[0][0]
            self.ids.desc.text = database[0][1]
            self.ids.img.source = database[0][2]
        except:
            pass


    def password_length(self, password):
        # using a list comprehension we can split
        # string at all chars
        char_lsit = [char for char in password]
        # returns length of list
        return len(char_lsit)

class Screen_waiting_student(Screen):
    pass
class Screen_waiting_employer(Screen):
    def on_enter(self, *args):
        app.main_Screen.ids.screen_manager.get_screen("awaiting").ids.content_view.clear_widgets()
        app.main_Screen.ids.screen_manager.get_screen("awaiting").ids.content.clear_widgets()
        app.main_Screen.populate_awaiting()
class Screen_reviewed(Screen):
    pass

class Screen_main(Screen):


    def rail_switch_screen(self, instance_navigation_rail, instance_navigation_rail_item):

        self.ids.screen_manager.current = (
            instance_navigation_rail_item.text.lower()
        )

    def create_content_screens(self, idd, screen_name, user_name, user_img, user_job, user_desc):
        idd_string = "'" + str(idd) + "'"
        user_name_string = "'" + user_name + "'"
        user_img_string = "'" + user_img + "'"
        user_job_string = "'" + user_job + "'"
        user_desc_string = "'" + user_desc + "'"

        button = Builder.load_string("""Screen:
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
               """.format(user_name_string, user_job_string, user_img_string, user_desc_string))

        #checks if screen already exists
        try:
            if self.ids.screen_manager.get_screen(screen_name).ids.content_view.get_screen(idd_string):
                self.ids.screen_manager.get_screen(screen_name).ids.content_view.get_screen(idd_string).add_widget(button)
                return
        except:
            pass
        try:
            new_screen = Screen(name=idd_string)
            new_screen.add_widget(button)
        except:
            pass
        self.ids.screen_manager.get_screen(screen_name).ids.content_view.add_widget(new_screen)



    def test(self, idd, screen_name):
        idd_string = "'" + str(idd) + "'"
        self.ids.screen_manager.get_screen(screen_name).ids.content_view.current = idd_string

    def render_cards(self, idd, screen_name, value, user_name, user_subtitle, user_img, jobid):
        screen_name_string = "'" + str(screen_name) + "'"

        if value == 0:
            x = Builder.load_string(create_card_student(
                user_name,  user_subtitle, user_img, "root.test({}, {})".format(idd, screen_name_string),  "root.add({})".format(jobid)),
                                filename="myrule.kv")
        if value == 1:
            x = Builder.load_string(create_card_employer_jobs(
                user_name, user_subtitle, user_img, "root.test({}, {})".format(idd, screen_name_string), "root.remove({})".format(jobid)),
                filename="myrule.kv")
        if value == 2:
            x = Builder.load_string(create_card_employer_awaiting(
                user_name, user_subtitle, user_img, "root.test({}, {})".format(idd, screen_name_string), "root.move({},{})".format(jobid, 1), "root.move({},{})".format(jobid, 0)),
                filename="myrule.kv")

        self.ids.screen_manager.get_screen(screen_name).ids.content.add_widget(CardItem())
        x = Builder.unload_file("myrule.kv")


    def create_job(self):
        #gets the description from textfield
        jobname = app.main_Screen.ids.screen_manager.get_screen("joblist").ids.Textfield.text
        if jobname == "":
            Mainapp.show_alert_box(Mainapp(), "Need a job title")
            return

        # reads the database for account info and displays on gui
        # opens database connection
        val = establish_connection()
        # save gets username
        database = get_from_user_info(val[1], app.current_account)
        if len(database) != 0:
            insert_into_jobs(val[1],database[0][0], database[0][1], database[0][2], jobname, app.current_account)
        else:
            Mainapp.show_alert_box(Mainapp(), "No account info")
            close_connection(val[0])
            return
        # closes connection
        close_connection(val[0])



        Mainapp.show_alert_box(Mainapp(), "succesfully created a job")

        app.main_Screen.ids.screen_manager.get_screen("joblist").ids.Textfield.text = ""
        app.main_Screen.ids.screen_manager.get_screen("joblist").ids.content.clear_widgets()

        app.main_Screen.ids.screen_manager.get_screen("joblist").ids.content_view.clear_widgets()
        self.populate_joblist()

    def populate_joblist(self):
        try:
            database = None
            if app.acoount_type == 0:
                # reads the database for account info and displays on gui
                # opens database connection
                val = establish_connection()
                # save gets username
                database = get_allfrom_jobs(val[1])
                # closes connection
                close_connection(val[0])
                print(database)

            if app.acoount_type == 1:
                # reads the database for account info and displays on gui
                # opens database connection
                val = establish_connection()
                # save gets username
                database = get_from_jobs(val[1], app.current_account)
                # closes connection
                close_connection(val[0])
                print(database)

            z = 0
            for x in database:
                print(x[1])
                app.main_Screen.create_content_screens(z, "joblist", x[0], x[2], x[3], x[1])
                app.main_Screen.render_cards(z, "joblist", app.acoount_type, x[0], x[3], x[2], x[4])
                z +=1
        except:
            pass



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

            z = 0
            for x in database:
                print(x[1])
                app.main_Screen.create_content_screens(z, "awaiting", x[0], x[2], x[3], x[1])
                app.main_Screen.render_cards(z, "awaiting", 2, x[0], x[3], x[2], x[4])
                z += 1
        except:
            pass

    def on_enter(self):
        #Creates screens for the toolbar.
        app.main_Screen.ids.screen_manager.clear_widgets()
        app.main_Screen.ids.screen_manager.add_widget(Screen_jobs(name="joblist"))
        app.main_Screen.ids.screen_manager.add_widget(Screen_reviewed(name="reviewed"))
        app.main_Screen.ids.screen_manager.add_widget(Screen_account(name="account"))


        if app.acoount_type == 0:
            # disables the add job button
            app.main_Screen.ids.screen_manager.get_screen("joblist").ids.button.disabled = True
            app.main_Screen.ids.screen_manager.get_screen("joblist").ids.Textfield.disabled = True

            #loads student layout
            Builder.load_file("layouts/waiting_student_layout.kv")
            app.main_Screen.ids.screen_manager.add_widget(Screen_waiting_student(name="awaiting"))



        if app.acoount_type == 1:
            # enable the add job button
            app.main_Screen.ids.screen_manager.get_screen("joblist").ids.button.disabled = False
            app.main_Screen.ids.screen_manager.get_screen("joblist").ids.Textfield.disabled = False

            # loads employer layout
            Builder.load_file("layouts/waiting_employer_layout.kv")
            app.main_Screen.ids.screen_manager.add_widget(Screen_waiting_employer(name="awaiting"))

            self.populate_awaiting()
        pass




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
    # TO DO: ADD DATABASE FOR LOGIN MANGEMENT.
    def request_login(self, username, password, type):
        # this imtates a sql database at the moment

        # opens database connection
        val = establish_connection()
        # save gets username
        database = get_from_login(val[1], username)
        # closes connection
        close_connection(val[0])


        if username == "" or password == "":
            sound = SoundLoader.load("sfx/Error.mp3")
            sound.play()
            Mainapp.show_alert_box(Mainapp(), "Fields cant be empty")
            self.clear_fields()
            return False

        # checks if all credentials match database and returns true
        if len(database) != 0:
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
    def request_signup(self, username, password,rpassword,  type):
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


class Screen_student(Screen):
    type = "student"








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
        self.sm.add_widget(Screen_student(name="student_main"))



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
        # creates a list from the windows.size which returns tuple.
        newlist = [x for x in Window.size]

        # checks if either width or height of window
        # is larger than the parameters
        if width > newlist[0] or height > newlist[1]:
            # if forces window size to paramters
            Window.size = (width, height)
            # shows alertbox
            self.show_alert_box("Cant resize beyond this point.")

    # this method runs after build
    def on_start(self):


        # this runs a schedueld task, to force the windows size.
        # all the time
        Clock.schedule_interval(partial(self.force_window, 800, 600), 0)



# runs the program
if __name__ == "__main__":
    app = Mainapp()
    app.run()
