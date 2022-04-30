

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.utils import get_color_from_hex

from kivymd.app import MDApp
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

class CardItem(MDCard, RoundedRectangularElevationBehavior):
    pass

class Screen_jobs(Screen):
    pass

class Example(MDApp):
    def build(self):
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_palette = "Orange"
        Builder.load_file("layouts/jobs_layout.kv")
        return Builder.load_file("layouts/template_layout.kv")

    def switch_screen(
        self, instance_navigation_rail, instance_navigation_rail_item
    ):
        '''
        Called when tapping on rail menu items. Switches application screens.
        '''

        self.root.ids.screen_manager.current = (
            "job"
        )

    def on_start(self):
        '''Creates application screens.'''
        self.root.ids.screen_manager.add_widget(Screen_jobs(name="job"))
        for x in range(10):
            self.root.ids.screen_manager.get_screen("job").ids.content.add_widget(CardItem())


        navigation_rail_items = self.root.ids.navigation_rail.get_items()[:]
        navigation_rail_items.reverse()

        for widget in navigation_rail_items:
            name_screen = widget.icon.split("-")[1].lower()
            screen = MDScreen(
                name=name_screen,
                md_bg_color=get_color_from_hex("#edd769"),
                radius=[18, 0, 0, 0],
            )
            box = MDBoxLayout(padding="12dp")
            label = MDLabel(
                text=name_screen.capitalize(),
                font_style="H1",
                halign="right",
                adaptive_height=True,
                shorten=True,
            )
            box.add_widget(label)
            screen.add_widget(box)
            self.root.ids.screen_manager.add_widget(screen)


Example().run()

