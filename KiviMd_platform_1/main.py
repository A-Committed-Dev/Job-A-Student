from kivy.animation import Animation
from kivy.clock import Clock
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
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')












class HoverButton(MDFillRoundFlatIconButton, HoverBehavior):

    #stores the default icon to save for change back.
    defaulticon = None
    def on_enter(self, *args):
        #when mouse hover overbutton switch bg color, and stores the default icon.
        self.md_bg_color = get_color_from_hex('#ff9800')
        #animates the button, by sizing up the x value
        Animation(size_hint=(0.6, self.height), duration=1).start(self)
        #saves default icon
        self.defaulticon = self.icon
    def on_leave(self, *args):
        # when mouse hover overbutton switch bg color, and changes to the default icon.
        self.md_bg_color = get_color_from_hex('#ececec')
        # animates the button, by sizing down the x value
        Animation(size_hint=(0.5, self.height), duration=1).start(self)
        #changes to the default icon.
        self.icon = self.defaulticon
    def on_release(self):
        #kills all animations on press
        Animation.cancel_all(self)
        #on press shrinks the button and change icon
        Animation(size_hint=(0.4, self.height), duration=0.2).start(self)
        self.icon = "check-decagram"
        #sets color to green
        self.md_bg_color = get_color_from_hex('#3fb55d')


class Screen_login(Screen):
    type = None
    def get_credentials(self):
        return self.ids.Username.text, self.ids.Upassword.text

    def set_type(self, type):
        self.type = type

    def get_type(self):
        return self.type

    def request_login(self, username, password, type):
        database = ["monkey", "word", "student"]
        if username == database[0] and password == database[1] and type == database[2]:
            return True
        else:
            self.theme_cls.primary_palette = "Orange"
            Mainapp.show_alert_box(Mainapp().root, "You did something wrong...")
            return False




class Screen_signup(Screen):
    type = None
    def get_credentials(self):
        print(self.ids.Username.text)
        print(self.ids.Upassword.text)
        return self.ids.Username.text, self.ids.Upassword.text

    def set_type(self, type):
        self.type = type

    def get_type(self):
        return self.type

    def request_login(Self, username, password, type):
        database = ["monkey", "word", "student"]
        if username == database[0] and password == database[1] and type == database[2]:
            return True
        else:
            Mainapp.show_alert_box(Mainapp(), "You did something wrong...")
            return False


class Mainapp(MDApp):
    dialog = None
    sm = ScreenManager()
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Orange"

        Builder.load_file("layouts/login_layout.kv")
        Builder.load_file("layouts/signup_layout.kv")


        self.sm.add_widget(Screen_login(name="screen_one"))
        self.sm.add_widget(Screen_signup(name="screen_two"))
        self.sm.current = "screen_two"
        # self.theme_cls.primary_light = get_color_from_hex('#ececec')


        return self.sm


    def change_screen(self, name):
        self.sm.current = name



    def show_alert_box(self, message):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Orange"
        if not self.dialog:
            self.dialog = MDDialog(
                text=message,
                buttons=[
                    MDFlatButton(
                        text="Close", text_color=self.theme_cls.primary_color, on_press = self.hide_arlarm_box
                    ),
                    MDRectangleFlatButton(
                        text="OK", text_color=self.theme_cls.primary_color, on_press = self.hide_arlarm_box
                    )
                ]
            )
        self.dialog.open()


    def hide_arlarm_box(self, obj):
        self.dialog.dismiss()


    def force_window(self, width, height, *largs):
        newlist = [x for x in Window.size]
        if width > newlist[0] or height > newlist[1]:
            Window.size = (width, height)
            self.show_alert_box("Cant resize beyond this point.")

    def on_start(self):
        Clock.schedule_interval(partial(self.force_window, 800, 600), 0)



if __name__ == "__main__":
    Mainapp().run()
