from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivymd.uix.behaviors import HoverBehavior, MagicBehavior
from kivymd.uix.button import MDFillRoundFlatIconButton, MDRectangleFlatIconButton, MDFlatButton, MDRectangleFlatButton
from kivy.utils import get_color_from_hex





class HoverButton(MDFillRoundFlatIconButton, HoverBehavior,):

    #stores the default icon to save for change back.
    defaulticon = None

    #this method checks if mouse is over button.
    def on_enter(self, *args):
        #when mouse hover overbutton switch bg color, and stores the default icon.
        self.md_bg_color = get_color_from_hex('#ff9800')
        #animates the button, by sizing up the x value
        Animation(size_hint=(0.6, self.height), duration=1).start(self)
        #saves default icon
        self.defaulticon = self.icon

    # this method checks if mouse is no longer over the button.
    def on_leave(self, *args):
        # when mouse hover over button switch bg color, and changes to the default icon.
        self.md_bg_color = get_color_from_hex('#ececec')
        # animates the button, by sizing down the x value
        Animation(size_hint=(0.5, self.height), duration=1).start(self)
        #changes to the default icon.
        self.icon = self.defaulticon





# custom class for button, specfically for the purpose of login
# inherits from Hoverbutton an magicbehavior.
class LoginButton(HoverButton, MagicBehavior):
    # this method animates the login button.
    def login_animation(self, boolean):
        # kills all animations on press
        Animation.cancel_all(self)
        # on press shrinks the button and change icon
        Animation(size_hint=(0.4, self.height), duration=0.2).start(self)
        if boolean:
            # sets icon
            self.icon = "check-decagram"
            # sets color to green
            self.md_bg_color = get_color_from_hex('#3bff8c')
        else:
            # uses wobble from magicbehavior
            self.wobble()
            # sets icon
            self.icon = "alert-decagram"
            # sets color to green
            self.md_bg_color = get_color_from_hex('#ff583b')