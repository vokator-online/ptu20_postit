import PySimpleGUI as sg
import backend

sg.theme("dark")
sg.set_options(font="sans-serif 20")

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
            values=backend.get_post_list(), 
            headings=['ID', 'Title', 'User', 'Created/Updated', 'Likes', 'Comments'],
            col_widths=[5, 30, 10, 15, 5, 5],
            justification='center', auto_size_columns=False,
        ),
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
        else:
            auth_token = ''
            main_window["-USERNAME-"].update(disabled=False)
            main_window["-PASSWORD-"].update(disabled=False)
            main_window["-LOGINOUT-"].update("LOGIN")
        main_window["-DEBUG-"].update(auth_token)
