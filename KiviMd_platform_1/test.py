from kivy.lang import Builder
from kivymd.uix.list import IconRightWidget


from kivymd.app import MDApp
from kivymd.uix.behaviors import MagicBehavior
from kivymd.uix.button import MDRaisedButton, MDFillRoundFlatButton, MDRoundFlatButton, MDRectangleFlatButton, \
    MDFlatButton

kv = """
#:import utils kivy.utils
#:import md_icons kivymd.icon_definitions.md_icons
#:import fonts kivymd.font_definitions.fonts
<Roundbutton@MDFlatButton>
    background_color: (0,0,0,0)
    background_normal: ""
    canvas.before:
        Color:
            rgb: utils.get_color_from_hex('#ff9800')
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [58]
                
<MagicButton@MagicBehavior+Roundbutton>


MDFloatLayout:
    MagicButton:
        text: f"[size=30][font={fonts[-1]['fn_regular']}]{md_icons['login-variant']}[/size][/font] Login"
        pos_hint: {"center_x": .5, "center_y": .5}
        size_hint: 0.3, 0.3
        font_size: 20
        on_release: self.twist()
        
"""

# class MagicButton(MagicBehavior, MDFlatButton):
#     pass


class Exam(MDApp):
    def build(self):

        return Builder.load_string(kv)

Exam().run()