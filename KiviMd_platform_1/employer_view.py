

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.splitter import Splitter
from kivy.utils import get_color_from_hex

from kivymd.app import MDApp
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatIconButton, MDRectangleFlatButton, MDFloatingActionButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp, sp
from kivy.uix.recycleview import RecycleView
from kivymd.uix.button import MDIconButton, MDFlatButton, MDRaisedButton, MDRoundFlatIconButton


class CardItem(MDCard, RoundedRectangularElevationBehavior):
    pass


class Screen_review(Screen):
    dialog = None

    def create_table(self):

        # Initialization of datatable
        self.table = MDDataTable(
            pos_hint={"center_y": 0.5, "center_x": 0.5},
            size_hint=(0.95, 0.75),
            check=False,
            rows_num=10,
            use_pagination=True,
            column_data=[
                ("Job", dp(110)),
                ("Status", dp(20)),
            ],
            row_data=[["Jørgen", ("checkbox-marked-circle",
                                 [0, 100, 0, 1],
                                "Accepted")],
                      ["Kent", ("close-circle",
                               [50, 0, 0, 1],
                               "Denied")],
                      ["Bo", ("close-circle",
                               [50, 0, 0, 1],
                                 "Denied")],
                      ["Børge", ("close-circle",
                                 [50, 0, 0, 1],
                                 "Denied")],
                      ["Jens", ("close-circle",
                                  [50, 0, 0, 1],
                                  "Denied")],
                      ["Eskild", ("close-circle",
                                [50, 0, 0, 1],
                                "Denied")],
                      ["Charlotte", ("close-circle",
                                [50, 0, 0, 1],
                                "Denied")],
                      ["Jeanette", ("checkbox-marked-circle",
                                 [0, 100, 0, 1],
                                "Accepted")],
                      ["Troels", ("checkbox-marked-circle",
                                 [0, 100, 0, 1],
                                "Accepted")],
                      ["Kenneth", ("close-circle",
                                     [50, 0, 0, 1],
                                     "Denied")],
                      ["Ester", ("close-circle",
                                     [50, 0, 0, 1],
                                     "Denied")],
                      ]
        )

        self.add_widget(self.table)

    # Creates datatable when the screen is active
    def on_enter(self):
        self.create_table()


class Screen_jobs(Screen):
    pass

class Example(MDApp):

    def build(self):
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_palette = "Orange"
        Builder.load_file("layouts/jobs_layout.kv")
        Builder.load_file("layouts/rewied_layout.kv")
        return Builder.load_file("layouts/template_layout.kv")

    def switch_screen(
        self, instance_navigation_rail, instance_navigation_rail_item
    ):
        '''
        Called when tapping on rail menu items. Switches application screens.
        '''

        self.root.ids.screen_manager.current = (
            "review"
        )

    def on_start(self):
        '''Creates application screens.'''
        self.root.ids.screen_manager.add_widget(Screen_jobs(name="job"))
        self.root.ids.screen_manager.add_widget(Screen_review(name="review"))
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

