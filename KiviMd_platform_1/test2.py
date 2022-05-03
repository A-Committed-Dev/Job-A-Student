
from tkinter import *   # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.utils import get_color_from_hex

from kivymd.app import MDApp
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.fitimage import FitImage
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivy.animation import Animation
from custom_classes import *
from template_generator import *






class CardItem(MDCard, RoundedRectangularElevationBehavior):
    def test(self, idd, screen_name):
        app.main_Screen.test(idd, screen_name)



class Screen_jobs(Screen):
    pass
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
            list = [self.ids.name.text, self.ids.desc.text, self.ids.img.source]
            print(list)

        # checks the length of a string

    def password_length(self, password):
        # using a list comprehension we can split
        # string at all chars
        char_lsit = [char for char in password]
        # returns length of list
        return len(char_lsit)

class Screen_student_account(Screen):
    pass
class Screen_waiting_employer(Screen):
    pass
class Screen_reviewed(Screen):
    pass

class Screen_main(Screen):
    Builder.load_file("layouts/joblist_employer.kv")
    Builder.load_file("layouts/account_layout.kv")
    Builder.load_file("layouts/waiting_employer_layout.kv")

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
                        padding: 10
                        MDTextField:
                                text: {}
                                text_color_normal: 0,0,0
                                text_color_focus: 0,0,0
                                multiline: True
                                disabled: True
                                size: 0.5,1 
               """.format(user_name_string, user_job_string, user_img_string, user_desc_string))
        try:
            new_screen = Screen(name=idd_string)
            new_screen.add_widget(button)
        except:
            pass
        self.ids.screen_manager.get_screen(screen_name).ids.content_view.add_widget(new_screen)



    def test(self, idd, screen_name):
        idd_string = "'" + str(idd) + "'"
        self.ids.screen_manager.get_screen(screen_name).ids.content_view.current = idd_string

    def render_cards(self, idd, screen_name, value, user_name, user_subtitle, user_img):
        screen_name_string = "'" + str(screen_name) + "'"

        if value == 1:
            x = Builder.load_string(create_card_student(
                user_name,  user_subtitle, user_img, "root.test({}, {})".format(idd, screen_name_string)),
                                filename="myrule.kv")
        if value == 2:
            x = Builder.load_string(create_card_employer_jobs(
                user_name, user_subtitle, user_img, "root.test({}, {})".format(idd, screen_name_string)),
                filename="myrule.kv")
        if value == 3:
            x = Builder.load_string(create_card_employer_awaiting(
                user_name, user_subtitle, user_img, "root.test({}, {})".format(idd, screen_name_string)),
                filename="myrule.kv")

        self.ids.screen_manager.get_screen(screen_name).ids.content.add_widget(CardItem())
        x = Builder.unload_file("myrule.kv")

    def on_enter(self):
        '''Creates application screens.'''
        self.ids.screen_manager.add_widget(Screen_jobs(name="joblist"))
        self.ids.screen_manager.add_widget(Screen_waiting_employer(name="awaiting"))
        self.ids.screen_manager.add_widget(Screen_reviewed(name="reviewed"))
        self.ids.screen_manager.add_widget(Screen_account(name="account"))

        list = [1,2,3,4,5,6,7,8,9,10]
        for x in list:
            self.create_content_screens(x, "joblist", "claus", "1.png", "robot", "ouihgehgueuoihjfouieuiojfoiadwijojioawjdoijawoidjoijawdijiojawiodjoijawo")
            self.render_cards(x, "joblist", 2, "Claus"+str(x), "kage er gud", "1.png")


class Example(MDApp):
    sm = ScreenManager()
    main_Screen = None
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Orange"
        Builder.load_file("layouts/main_layout.kv")
        self.main_Screen = Screen_main(name="main")
        self.sm.add_widget(self.main_Screen)
        self.sm.current = "main"
        return self.sm



app = Example()
app.run()
