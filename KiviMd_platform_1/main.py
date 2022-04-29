from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.behaviors import HoverBehavior
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFillRoundFlatIconButton, MDRectangleFlatIconButton, MDFlatButton, MDRectangleFlatButton
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.config import Config
from kivy.utils import get_color_from_hex
from functools import partial

# makes kivy use mouse input and disables multitouch
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')






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
        database = ["1", "1", "student"]

        # checks if all credentials match database and returns true
        if username == database[0] and password == database[1] and type == database[2]:
            if type == "student":
                Mainapp().change_screen(name="student_main")
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

        # if none of the conditions are met an account is successfully
        # uploaded to the data base, shows messages to user to confirm
        # that an account was created.
        # last returns account to the data base.
        # TO DO: added user to sql database instead of returning list.
        else:
            print("success")
            newlist = [username, password, type]
            Mainapp.show_alert_box(Mainapp(), "Successfully signed up")
            return newlist

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

    # this method is run first, here we put stuff like our theme and color choice.
    # we also put our screens and load the .kv files.
    def build(self):
        # sets the color themes for the whole app.
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Orange"

        # loads the .kv files
        Builder.load_file("layouts/login_layout.kv")
        Builder.load_file("layouts/signup_layout.kv")
        Builder.load_file("layouts/student_main.kv")

        # adds screens to the screen manager.
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
    Mainapp().run()
