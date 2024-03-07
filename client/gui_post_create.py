import PySimpleGUI as sg
import backend


def post_create(root_window:sg.Window, auth_token: str) -> dict[str, str]:
    root_window.hide()

    layout = [
        [
            sg.Text("Title:"),
            sg.Input("", key="-TITLE-", size=60),
        ],
        [
            sg.Multiline("", key="-BODY-", expand_x=True, expand_y=True, size=(80, 10)),
        ],
        [
            sg.Button("POST", key="-POST-"),
            sg.Button("CLOSE", key="-CLOSE-"),
        ]
    ]

    window = sg.Window(
        f"Writing a post", 
        layout, 
        element_justification='center', 
        element_padding=10, 
        finalize=True
    )

    created_post = None
    while True:
        event, values = window.read()
        if event in [sg.WINDOW_CLOSED, "-CLOSE-"]:
            break
        if event == "-POST-":
            try:
                created_post = backend.post_create(values["-TITLE-"], values["-BODY-"], auth_token)
            except ConnectionError as error:
                sg.PopupOK(error, title="Oops")
            else:
                break

    window.close()
    root_window.un_hide()

    if created_post:
        return created_post
