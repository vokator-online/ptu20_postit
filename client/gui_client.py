import PySimpleGUI as sg
import backend
from gui_post_detail import post_detail
from gui_post_create import post_create

sg.theme("dark")
sg.set_options(font="sans-serif 20")

try:
    posts = backend.get_post_list()
except ConnectionError as error:
    posts = []
    sg.PopupOK(error, title="Oops")

def main(posts: dict[str, str]):
    main_layout = [
        [
            sg.Input("", key="-USERNAME-", size=15),
            sg.Input("", key="-PASSWORD-", size=15, password_char="x"),
            sg.Button("Login", key="-LOGINOUT-"),
        ],
        [
            sg.Text("PostIt"),
        ],
        [
            sg.Table(
                values=posts, 
                headings=['ID', 'Title', 'User', 'Created/Updated', 'Likes', 'Comments'],
                col_widths=[5, 30, 10, 15, 5, 5],
                justification='c', auto_size_columns=False,
                key="-LIST-",
            ),
        ],
        [
            sg.Button("SHOW", key="-DETAIL-"),
            sg.Button("+ NEW POST", key="-NEW-", disabled=True),
        ],
        [
            sg.Text("", key="-DEBUG-"),
        ],
    ]

    main_window = sg.Window(
        "PostIt", 
        main_layout, 
        element_justification="center", 
        element_padding=10,
        finalize=True
    )

    auth_token = ''
    while True:
        event, values = main_window.read()
        if event in [sg.WINDOW_CLOSED, "-EXIT-"]:
            break
        if event == "-DETAIL-" and values["-LIST-"]:
            for selected in values["-LIST-"]:
                post_detail(posts[selected][0], main_window, auth_token)
        if event == "-NEW-":
            new_post = post_create(main_window, auth_token)
            if new_post:
                posts = backend.get_post_list()
                main_window["-LIST-"].update(posts)
        if event == "-LOGINOUT-":
            if auth_token == '':
                try:
                    auth_token = backend.login(values["-USERNAME-"], values["-PASSWORD-"])
                except ConnectionError as error:
                    sg.PopupOK(error, title="Oops")
                    auth_token = ''
                else:
                    main_window["-LOGINOUT-"].update("LOGOUT")
                    main_window["-USERNAME-"].update(disabled=True)
                    main_window["-PASSWORD-"].update(disabled=True)
                    main_window["-NEW-"].update(disabled=False)
            else:
                auth_token = ''
                main_window["-USERNAME-"].update(disabled=False)
                main_window["-PASSWORD-"].update(disabled=False)
                main_window["-LOGINOUT-"].update("LOGIN")
                main_window["-NEW-"].update(disabled=True)
            main_window["-DEBUG-"].update(auth_token)

if __name__ == "__main__" and posts:
    main(posts)
