
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.splitter import Splitter
from kivy.utils import get_color_from_hex

from kivymd.app import MDApp
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatIconButton, MDRectangleFlatButton
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


class Screen_wait(Screen):
    index = 0
    dialog = None

    def create_table(self):

        # Initialization of datatable
        self.table = MDDataTable(
            pos_hint={"center_y": 0.5, "center_x": 0.5},
            size_hint=(0.95, 0.75),
            check = False,
            rows_num = 1000,
            use_pagination = False,
            column_data = [
                ("Job", dp(110)),
                ("Status", sp(20)),
            ],
            row_data=[["Bager", "Pending"],
                      ["Kok", "Pending"],
                      ["Murer", "Pending"],
                      ["Maler", "Pending"],
                      ["Politi", "Pending"],
                      ["Bubu", "Pending"],
                      ["Sulu", "Pending"],
                      ["Kulu", "Pending"],
                      ["Hulu", "Pending"],

                      ]
        )

        # Binds the method on_row_press to the datatable
        self.table.bind(on_row_press=self.row_presses)

        self.add_widget(self.table)

    # Creates datatable when the screen is active
    def on_enter(self):
        self.create_table()

    # Method that gets the instance of the row pressed
    def row_presses(self, instance_table, instance_row):

        selected_row = instance_row.index
        selected_row_name = instance_row.text

        # Deletes the previous label that showed selected row
        if len(self.children) > 2:
            self.remove_widget(self.children[0])
        else:
            pass

        # BoxLayout to house buttons and label
        buttons = MDBoxLayout(
            pos_hint={"center_x": 0.537, "center_y": 0.55},
        )

        # Delete button
        buttons.add_widget(
            MDIconButton(
                icon="trash-can-outline",
                on_release=lambda x :self.show_alert_box(selected_row)
            )
        )

        # View button
        buttons.add_widget(
            MDIconButton(
                icon="view-column",
                on_release=lambda x :self.view(selected_row_name)
            )
        )

        # "Selected: " label
        buttons.add_widget(
            MDLabel(
                text=f"Selected: {selected_row_name}",
                pos_hint={"center_y": 0.04}
            )
        )
        self.add_widget(buttons)

    # Method called when view button is clicked
    def view(self, selected_row_name):
        self.index += 1
        # Removes delete, view and "Select :" label
        self.remove_widget(self.children[0])

        # BoxLayout to house view popup screen elements
        lay = MDBoxLayout(
            size_hint=(.95, 1),
            pos_hint={"center_x": 1, "center_y": 0.5},
            md_bg_color=get_color_from_hex("#FFFFFF")
        )

        # Button to close popup screem
        lay.add_widget(
            MDIconButton(
                icon="arrow-collapse-right",
                on_release = lambda x: self.remove_widget(self.children[0]),
                pos_hint={"center_x": 0.1, "center_y": 0.5},
            )
        )

        # This should be where we insert data from database
        lay.add_widget(
            MDLabel(
                text=str(selected_row_name),
                text_color = [0, 0, 0, 1]
            )
        )
        self.add_widget(lay)

    def show_alert_box(self, selected_row):

        # checks if there is no box already
        if not self.dialog:
            # creates an alertbox with the message
            self.dialog = MDDialog(
                text="Do you wish to delete?",
                # adds buttons to the alertbox
                buttons=[
                    # button when clicked calls the hide_arlarm_box method
                    MDFlatButton(
                        text="Close", on_press = self.hide_arlarm_box
                    ),
                    # button when clicked calls the hide_arlarm_box method
                    MDRectangleFlatButton(
                        text="OK", on_press = lambda x: self.remove(selected_row)
                    )
                ]
            )
        # shows alertbox
        self.dialog.open()

    # removes the alert box
    def hide_arlarm_box(self, *args):
        self.dialog.dismiss()

    # Method called when delete button is clicked
    def remove(self, selected_row):
        self.hide_arlarm_box()
        # Using the selected row instance to determine which row to delete.
        if selected_row == 0:
            self.table.remove_row(self.table.row_data[int(selected_row)])
        else:
            # Divide selected_row by 2, because selected_row's index is double row_data's index
            self.table.remove_row(self.table.row_data[int(selected_row/2)])
        self.remove_widget(self.children[0])


class Screen_review(Screen):

    def create_table(self):

        # Initialization of datatable
        self.table = MDDataTable(
            pos_hint={"center_y": 0.5, "center_x": 0.5},
            size_hint=(0.95, 0.75),
            check=False,
            rows_num=1000,
            use_pagination=False,
            column_data=[
                ("Job", dp(110)),
                ("Status", dp(20)),
            ],
            row_data=[["Bager", ("checkbox-marked-circle",
                                 [0, 100, 0, 1],
                                "Accepted")],
                      ["Kok", ("close-circle",
                               [50, 0, 0, 1],
                               "Denied")],
                      ["Murer", ("close-circle",
                               [50, 0, 0, 1],
                                 "Denied")],
                      ["Maler", ("close-circle",
                                 [50, 0, 0, 1],
                                 "Denied")],
                      ["Politi", ("close-circle",
                                  [50, 0, 0, 1],
                                  "Denied")],
                      ["Bubu", ("close-circle",
                                [50, 0, 0, 1],
                                "Denied")],
                      ["Sulu", ("close-circle",
                                [50, 0, 0, 1],
                                "Denied")],
                      ["Kulu", ("checkbox-marked-circle",
                                 [0, 100, 0, 1],
                                "Accepted")],
                      ["Hulu", ("checkbox-marked-circle",
                                 [0, 100, 0, 1],
                                "Accepted")],

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
        Builder.load_file("layouts/waiting_student_layout.kv")
        Builder.load_file("layouts/review_layout.kv")
        return Builder.load_file("layouts/main_layout.kv")

    def switch_screen(
        self, instance_navigation_rail, instance_navigation_rail_item
    ):
        '''
        Called when tapping on rail menu items. Switches application screens.
        '''

        self.root.ids.screen_manager.current = (
            "wait"
        )

    def on_start(self):
        '''Creates application screens.'''
        self.root.ids.screen_manager.add_widget(Screen_jobs(name="job"))
        self.root.ids.screen_manager.add_widget(Screen_wait(name="wait"))
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
