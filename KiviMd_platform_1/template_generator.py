def create_card_employer_jobs(title, subtitle, img, function, delete_function):
    image_string = "'"+img+"'"
    title_string = "'"+title+"'"
    subtitle_string = "'"+subtitle+"'"

    card = """<CardItem>
    size_hint_y: None
    height: "86dp"
    padding: "4dp"
    radius: 12
    elevation: 4
    on_release: {}

    FitImage:
        source: {}
        radius: root.radius
        size_hint_x: None
        width: root.height

    MDBoxLayout:
        orientation: "vertical"
        adaptive_height: True
        spacing: "6dp"
        padding: "12dp", 0, 0, 0
        pos_hint: {{"center_y": .5}}


        MDLabel:
            text: {}
            font_style: "H5"
            bold: True
            adaptive_height: True

        MDLabel:
            text: {}
            theme_text_color: "Hint"
            adaptive_height: True
    MDIconButton:
        id: button
        icon: "delete-circle"
        on_release: {}
    """.format(function, image_string, title_string, subtitle_string, delete_function)
    return card

def create_card_employer_awaiting(title, subtitle, img, function):
    image_string = "'"+img+"'"
    title_string = "'"+title+"'"
    subtitle_string = "'"+subtitle+"'"

    card = """<CardItem>
    size_hint_y: None
    height: "86dp"
    padding: "4dp"
    radius: 12
    elevation: 4
    on_release: {}

    FitImage:
        source: {}
        radius: root.radius
        size_hint_x: None
        width: root.height

    MDBoxLayout:
        orientation: "vertical"
        adaptive_height: True
        spacing: "6dp"
        padding: "12dp", 0, 0, 0
        pos_hint: {{"center_y": .5}}


        MDLabel:
            text: {}
            font_style: "H5"
            bold: True
            adaptive_height: True

        MDLabel:
            text: {}
            theme_text_color: "Hint"
            adaptive_height: True
    MDIconButton:
        id: button
        icon: "check-circle"
    MDIconButton:
        id: button
        icon: "close-circle"
    """.format(function, image_string, title_string, subtitle_string)
    return card

def create_card_student(title, subtitle, img, function):
    image_string = "'"+img+"'"
    title_string = "'"+title+"'"
    subtitle_string = "'"+subtitle+"'"

    card = """<CardItem>
    size_hint_y: None
    height: "86dp"
    padding: "4dp"
    radius: 12
    elevation: 4
    on_release: {}

    FitImage:
        source: {}
        radius: root.radius
        size_hint_x: None
        width: root.height

    MDBoxLayout:
        orientation: "vertical"
        adaptive_height: True
        spacing: "6dp"
        padding: "12dp", 0, 0, 0
        pos_hint: {{"center_y": .5}}


        MDLabel:
            text: {}
            font_style: "H5"
            bold: True
            adaptive_height: True

        MDLabel:
            text: {}
            theme_text_color: "Hint"
            adaptive_height: True
    MDIconButton:
        id: button
        icon: "check-circle"
    """.format(function, image_string, title_string, subtitle_string)
    return card